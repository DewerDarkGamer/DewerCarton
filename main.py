import tkinter as tk
from datetime import datetime
import os
from tkinter import messagebox, ttk
from print_config import (
    format_label_text,
    get_print_command,
    get_paper_settings
)
from data_manager import DataManager, open_data_manager

def get_part_rev_from_lot(lot_number):
    """Get part and revision data based on lot number from data manager"""
    try:
        data_manager = DataManager()
        return data_manager.get_part_rev(lot_number)
    except Exception as e:
        messagebox.showerror("Error", f"Error processing lot number: {str(e)}")
        return None, None

def scan_and_print():
    lot = entry_lot.get().strip()

    if not lot:
        messagebox.showwarning("Warning", "Please enter lot number")
        return

    # Get part and revision data from database
    part, rev = get_part_rev_from_lot(lot)

    if part is None or rev is None:
        messagebox.showwarning("Warning", "No data found for this lot in the system")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ใช้รูปแบบ macarton_label
    result = format_label_text(lot, part, rev, now, "macarton_label")

    # Display result on screen
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, result)

    # Save file for printing
    try:
        filename = f"macarton_label_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)

        # Try different print methods based on OS
        import platform
        if platform.system() == "Windows":
            import subprocess
            try:
                # ใช้ notepad /p เพื่อพิมพ์ทันที
                subprocess.run(["notepad", "/p", filename], check=True)
                # ลบไฟล์หลังพิมพ์เสร็จ
                try:
                    os.remove(filename)
                except:
                    pass
                messagebox.showinfo("Success", "Printed MACarton Label (9x4 cm)")
            except:
                os.startfile(filename, "print")
        else:
            # For Linux/Unix systems
            import subprocess
            try:
                # ใช้คำสั่งพิมพ์สำหรับ MACarton
                print_cmd = get_print_command(filename, "normal", "Label").split()
                subprocess.run(print_cmd, check=True)
                # ลบไฟล์หลังพิมพ์เสร็จ
                try:
                    os.remove(filename)
                except:
                    pass
                messagebox.showinfo("Success", "Printed MACarton Label (9x4 cm)")

            except (subprocess.CalledProcessError, FileNotFoundError):
                messagebox.showinfo("File Saved", f"File saved as: {filename}\nConnect to MACarton printer and print manually")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot process file: {str(e)}")

def check_printer_status():
    """Check if MACarton printer is available"""
    try:
        import subprocess
        import platform

        if platform.system() == "Windows":
            try:
                result = subprocess.run(["wmic", "printer", "get", "name"], 
                                      capture_output=True, text=True)
                printers = result.stdout

                if result.returncode == 0:
                    if 'macarton' in printers.lower():
                        messagebox.showinfo("Printer Status", "MACarton printer is connected and ready")
                    else:
                        messagebox.showinfo("Printer Status", f"Available printers:\n{printers}")
                else:
                    result = subprocess.run(["powershell", "-Command", "Get-Printer | Select-Object Name"], 
                                          capture_output=True, text=True)
                    printers = result.stdout
                    if 'macarton' in printers.lower():
                        messagebox.showinfo("Printer Status", "MACarton printer is connected and ready")
                    else:
                        messagebox.showinfo("Printer Status", f"Available printers:\n{printers}")
            except:
                messagebox.showinfo("Printer Status", "Cannot check printer status on Windows.\nPlease check MACarton printer manually.")
        else:
            result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
            printers = result.stdout

            if 'macarton' in printers.lower():
                messagebox.showinfo("Printer Status", "MACarton printer is connected and ready")
            else:
                messagebox.showwarning("Printer Status", "MACarton not found. Available printers:\n" + printers)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot check printer status: {str(e)}")

# Create GUI
root = tk.Tk()
root.title("MACarton Lot Scanner")
root.geometry("500x450")

# Define fonts
try:
    default_font = ("DejaVu Sans", 12)
    small_font = ("DejaVu Sans", 10)
    large_font = ("DejaVu Sans", 14)
    title_font = ("DejaVu Sans", 16, "bold")
except:
    default_font = ("TkDefaultFont", 12)
    small_font = ("TkDefaultFont", 10)
    large_font = ("TkDefaultFont", 14)
    title_font = ("TkDefaultFont", 16, "bold")

# App title
title_label = tk.Label(root, text="MACarton Lot Scanner", font=title_font)
title_label.pack(pady=10)

# Lot number input field
tk.Label(root, text="Scan Lot Number:", font=default_font).pack()
entry_lot = tk.Entry(root, font=large_font, width=20)
entry_lot.pack(pady=5)

# Function to convert input to uppercase
def on_key_release_lot(event):
    current_text = entry_lot.get()
    if current_text != current_text.upper():
        cursor_pos = entry_lot.index(tk.INSERT)
        entry_lot.delete(0, tk.END)
        entry_lot.insert(0, current_text.upper())
        entry_lot.icursor(cursor_pos)

entry_lot.bind('<KeyRelease>', on_key_release_lot)

# Scan and print button
btn_scan = tk.Button(root, text="Scan and Print", command=scan_and_print,
                     font=default_font, bg="#4CAF50", fg="white", pady=5)
btn_scan.pack(pady=10)

# Check printer button
btn_printer = tk.Button(root, text="Check MACarton", command=check_printer_status,
                       font=small_font, bg="#FF9800", fg="white")
btn_printer.pack(pady=5)

# Data management button
btn_data_manager = tk.Button(root, text="Manage Data", command=lambda: open_data_manager(root),
                           font=small_font, bg="#607D8B", fg="white")
btn_data_manager.pack(pady=5)

# Output area
tk.Label(root, text="Label Preview:", font=default_font).pack(pady=(20,0))
text_output = tk.Text(root, height=8, width=50, font=("Courier", 9))
text_output.pack(pady=5)

# Instructions
info_text = """Instructions:
1. System checks digits 2-3 and digit 6 of lot number
2. Example: QSTZ8B2206 → Digits 2-3: ST, Digit 6: B
3. Lot number must be at least 6 digits long
4. Label size: 9x4 cm (MACarton format)
5. Font: Times New Roman"""

info_label = tk.Label(root, text=info_text, font=small_font,
                     justify=tk.LEFT, fg="gray")
info_label.pack(pady=10)

# Set focus to lot entry field on start
entry_lot.focus()

# Allow Enter key to scan and print immediately
def on_enter_key(event):
    scan_and_print()
    # Clear the lot entry field after printing for next scan
    entry_lot.delete(0, tk.END)

entry_lot.bind('<Return>', on_enter_key)

root.mainloop()

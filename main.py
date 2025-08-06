import tkinter as tk
from datetime import datetime
import os
from tkinter import messagebox, ttk
from print_config import (
    format_label_text, 
    get_print_command, 
    get_paper_settings,
    LabelFormat,
    PaperConfig,
    PrinterConfig
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

    # ใช้รูปแบบ compact_label ที่เหมาะกับกระดาษขนาดเล็ก
    result = format_label_text(lot, part, rev, now, "compact_label")

    # Display result on screen
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, result)

    # Save file and attempt to print
    try:
        filename = f"lot_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)

        # Try different print methods based on OS
        import platform
        if platform.system() == "Windows":
            os.startfile(filename, "print")
        else:
            # For Linux/Unix systems (like Replit) with printer
            import subprocess
            try:
                # Check if MACanton or any printer is available
                result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                printers = result.stdout

                # Try to find MACanton or use default printer
                macanton_printer = None
                for line in printers.split('\n'):
                    if 'macanton' in line.lower() or 'default' in line.lower():
                        macanton_printer = line.split()[1]  # Get printer name
                        break

                if macanton_printer:
                    # ใช้คำสั่งพิมพ์จากไฟล์ตั้งค่าสำหรับกระดาษขนาด 95x46 มม.
                    print_cmd = get_print_command(filename, "normal", "Label").split()
                    subprocess.run(print_cmd, check=True)
                    messagebox.showinfo("Success", f"File sent to MACanton (Label 95x46mm): {filename}")
                else:
                    # Try default printer with small font settings
                    subprocess.run(["lp", "-o", "cpi=20", "-o", "lpi=10", filename], check=True)
                    messagebox.showinfo("Success", f"File sent to default printer: {filename}")

            except (subprocess.CalledProcessError, FileNotFoundError):
                # If lp is not available, save file with printer-ready format
                messagebox.showinfo("File Saved", f"File saved as: {filename}\nConnect to printer and use: lp -o cpi=20 -o lpi=10 {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot process file: {str(e)}")

def check_printer_status():
    """Check if MACanton printer is available"""
    try:
        import subprocess
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        printers = result.stdout

        if 'macanton' in printers.lower():
            messagebox.showinfo("Printer Status", "MACanton printer is connected and ready")
        else:
            messagebox.showwarning("Printer Status", "MACanton not found. Available printers:\n" + printers)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot check printer status: {str(e)}")

# Create GUI
root = tk.Tk()
root.title("Lot Scanner")
root.geometry("400x350")

# Define fonts
try:
    # Try to use Unicode-supporting fonts
    default_font = ("DejaVu Sans", 12)
    small_font = ("DejaVu Sans", 10)
    large_font = ("DejaVu Sans", 14)
    title_font = ("DejaVu Sans", 16, "bold")
except:
    # If not available, use default fonts
    default_font = ("TkDefaultFont", 12)
    small_font = ("TkDefaultFont", 10)
    large_font = ("TkDefaultFont", 14)
    title_font = ("TkDefaultFont", 16, "bold")

# App title
title_label = tk.Label(root, text="Lot Scanner", font=title_font)
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
btn_printer = tk.Button(root, text="Check MACanton", command=check_printer_status, 
                       font=small_font, bg="#FF9800", fg="white")
btn_printer.pack(pady=5)

# Data management button
btn_data_manager = tk.Button(root, text="Manage Data", command=lambda: open_data_manager(root), 
                           font=small_font, bg="#607D8B", fg="white")
btn_data_manager.pack(pady=5)

# Output area
tk.Label(root, text="Result:", font=default_font).pack(pady=(20,0))
text_output = tk.Text(root, height=6, width=40, font=small_font)
text_output.pack(pady=5)

# Instructions
info_text = """Instructions:
1. System checks digits 2-3 and digit 6 of lot number
2. Example: QSTZ8B2206 → Digits 2-3: ST, Digit 6: B
3. Lot number must be at least 6 digits long
4. Paper size: 95x46 mm (Label)"""

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

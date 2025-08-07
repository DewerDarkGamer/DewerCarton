import tkinter as tk
from datetime import datetime
import os
import platform
from tkinter import messagebox
from print_config import (
    format_label_text,
    get_print_command
)

# ตรวจสอบว่าเป็น Windows และ Raw Printing พร้อมใช้งาน
RAW_PRINT_AVAILABLE = False
IS_WINDOWS = platform.system().lower() == 'windows'

if IS_WINDOWS:
    try:
        import win32print
        import win32api
        RAW_PRINT_AVAILABLE = True
        from print_raw import print_raw_text, get_available_printers
    except ImportError:
        RAW_PRINT_AVAILABLE = False

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

    # พิมพ์สำหรับ Windows
    if IS_WINDOWS and RAW_PRINT_AVAILABLE:
        try:
            # ลองพิมพ์ Raw Text โดยตรงไปยัง MACarton printer
            if print_raw_text("MACarton", result, "MACarton Label"):
                messagebox.showinfo("Success", "Printed MACarton Label (9x4 cm)")
                return
        except Exception as e:
            print(f"Raw printing failed: {e}")
    
    # ถ้าพิมพ์ Raw ไม่ได้ หรือไม่ใช่ Windows ให้สร้างไฟล์
    try:
        filename = f"macarton_label_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)

        if IS_WINDOWS:
            # ใช้ Windows Print Spooler สำหรับการพิมพ์
            import subprocess
            print_success = False
            
            # Method 1: ใช้คำสั่ง print กับชื่อ printer ที่ชัดเจน
            try:
                result = subprocess.run(['print', f'/D:MACarton', filename], 
                                      capture_output=True, text=True, check=True)
                messagebox.showinfo("Success", f"Sent to MACarton printer via Print Spooler\nFile: {filename}")
                print_success = True
            except subprocess.CalledProcessError as e:
                print(f"Print command failed: {e}")
                print(f"Output: {e.stdout}")
                print(f"Error: {e.stderr}")
                
            # Method 2: ลองใช้คำสั่ง copy ไปยัง default printer
            if not print_success:
                try:
                    result = subprocess.run(['copy', f'/B', filename, 'PRN'], 
                                          shell=True, capture_output=True, text=True, check=True)
                    messagebox.showinfo("Success", "Printed to default printer")
                    print_success = True
                except subprocess.CalledProcessError as e:
                    print(f"Copy to PRN failed: {e}")
                    
            # Method 3: ลองใช้ PowerShell สำหรับพิมพ์
            if not print_success:
                try:
                    ps_command = f'Get-Content "{filename}" | Out-Printer -Name "MACarton"'
                    result = subprocess.run(['powershell', '-Command', ps_command], 
                                          capture_output=True, text=True, check=True)
                    messagebox.showinfo("Success", "Printed via PowerShell")
                    print_success = True
                except subprocess.CalledProcessError as e:
                    print(f"PowerShell print failed: {e}")
                    
            # Method 4: ลองใช้ notepad /p เพื่อเปิด print dialog
            if not print_success:
                try:
                    subprocess.run(['notepad', '/p', filename], check=True)
                    messagebox.showinfo("Print Dialog", f"Print dialog opened\nFile: {filename}\nPlease select MACarton printer and click Print")
                    print_success = True
                except:
                    pass
                    
            # ถ้าทุกวิธีไม่ได้ผล
            if not print_success:
                messagebox.showinfo("File Saved", 
                    f"File saved as: {filename}\n"
                    f"Please:\n"
                    f"1. Check if MACarton printer is connected\n"
                    f"2. Right-click the file and select 'Print'\n"
                    f"3. Or drag the file to MACarton printer icon")
        else:
            # คำสั่งสำหรับ Linux/Unix
            import subprocess
            try:
                print_cmd = get_print_command(filename, "normal", "Label").split()
                subprocess.run(print_cmd, check=True)
                os.remove(filename)
                messagebox.showinfo("Success", "Printed MACarton Label (9x4 cm)")
            except:
                messagebox.showinfo("File Saved", f"File saved as: {filename}\nConnect to MACarton printer and print manually")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot process file: {str(e)}")

def check_printer_status():
    """Check if MACarton printer is available"""
    try:
        if IS_WINDOWS and RAW_PRINT_AVAILABLE:
            # ใช้ win32print สำหรับ Windows
            printers = get_available_printers()
            if not printers:
                messagebox.showinfo("Printer Status", "No printers found")
                return
                
            printer_list = "\n".join([f"- {printer}" for printer in printers])
            
            if any('macarton' in printer.lower() for printer in printers):
                messagebox.showinfo("Printer Status", f"MACarton printer found!\n\nAvailable printers:\n{printer_list}")
            else:
                messagebox.showinfo("Printer Status", f"MACarton printer not found\n\nAvailable printers:\n{printer_list}")
        else:
            # สำหรับ Windows ที่ไม่มี win32print หรือ Linux
            import subprocess
            
            if IS_WINDOWS:
                # ใช้คำสั่ง wmic สำหรับ Windows
                result = subprocess.run(["wmic", "printer", "get", "name"], 
                                      capture_output=True, text=True)
                printers = result.stdout
            else:
                # ใช้คำสั่ง lpstat สำหรับ Linux
                result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                printers = result.stdout

            if result.returncode == 0:
                if 'macarton' in printers.lower():
                    messagebox.showinfo("Printer Status", "MACarton printer is connected and ready")
                else:
                    messagebox.showinfo("Printer Status", f"Available printers:\n{printers}")
            else:
                messagebox.showinfo("Printer Status", "No printers found or command not available")
    except Exception as e:
        messagebox.showinfo("Printer Status", f"Cannot check printer status: {str(e)}")

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

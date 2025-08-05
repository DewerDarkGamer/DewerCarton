
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
    
    # ใช้รูปแบบจากไฟล์ตั้งค่า
    selected_template = template_var.get()
    result = format_label_text(lot, part, rev, now, selected_template)
    
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
            # For Linux/Unix systems (like Replit) with Epson L210
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
                    # ใช้คำสั่งพิมพ์จากไฟล์ตั้งค่า
                    selected_quality = quality_var.get()
                    print_cmd = get_print_command(filename, selected_quality).split()
                    subprocess.run(print_cmd, check=True)
                    messagebox.showinfo("Success", f"File sent to MACanton ({selected_quality} quality): {filename}")
                else:
                    # Try default printer
                    subprocess.run(["lp", filename], check=True)
                    messagebox.showinfo("Success", f"File sent to default printer: {filename}")
                    
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If lp is not available, try lpr with Epson settings
                try:
                    subprocess.run(["lpr", "-P", "Epson_L210", filename], check=True)
                    messagebox.showinfo("Success", f"File sent to Epson L210: {filename}")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # If no printer available, save file with printer-ready format
                    messagebox.showinfo("File Saved", f"File saved as: {filename}\nConnect to Epson L210 and use: lp -d Epson_L210 {filename}")
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

def show_conditions():
    """Show current conditions configured in the system"""
    conditions_text = """Current Conditions:
    
If digits 2-3 = "TB" and digit 6 = "Q"
→ Part: J3011, Revision: Rev.04

To add more conditions, modify the get_part_rev_from_lot() function in the code."""
    
    messagebox.showinfo("System Conditions", conditions_text)

def show_print_settings():
    """แสดงการตั้งค่าการพิมพ์ปัจจุบัน"""
    current_template = template_var.get()
    current_quality = quality_var.get()
    current_paper = paper_var.get()
    
    template_info = LabelFormat.LAYOUT_TEMPLATES[current_template]
    paper_info = get_paper_settings(current_paper)
    
    settings_text = f"""Current Print Settings:

Template: {template_info['name']}
Description: {template_info['description']}

Print Quality: {current_quality}
Paper Size: {current_paper}
Printer: {PrinterConfig.PRINTER_NAME}

Sample Output:
{format_label_text(
    lot='TB123Q789',
    part='J3011', 
    rev='Rev.04',
    time='2024-01-15 14:30:25',
    template=current_template
)}"""
    
    messagebox.showinfo("Print Settings", settings_text)

# Create GUI
root = tk.Tk()
root.title("Lot Scanner")
root.geometry("500x400")

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

# ส่วนการตั้งค่าการพิมพ์
settings_frame = tk.LabelFrame(root, text="Print Settings", font=default_font)
settings_frame.pack(pady=10, padx=20, fill="x")

# เลือกรูปแบบเอกสาร
tk.Label(settings_frame, text="Template:", font=small_font).grid(row=0, column=0, sticky="w", padx=5, pady=2)
template_var = tk.StringVar(value="label_with_barcode")
template_combo = ttk.Combobox(settings_frame, textvariable=template_var, font=small_font, width=15)
template_combo['values'] = list(LabelFormat.LAYOUT_TEMPLATES.keys())
template_combo.grid(row=0, column=1, padx=5, pady=2)

# เลือกคุณภาพการพิมพ์
tk.Label(settings_frame, text="Quality:", font=small_font).grid(row=0, column=2, sticky="w", padx=5, pady=2)
quality_var = tk.StringVar(value="normal")
quality_combo = ttk.Combobox(settings_frame, textvariable=quality_var, font=small_font, width=10)
quality_combo['values'] = list(PrinterConfig.PRINT_QUALITY.keys())
quality_combo.grid(row=0, column=3, padx=5, pady=2)

# เลือกขนาดกระดาษ  
tk.Label(settings_frame, text="Paper:", font=small_font).grid(row=1, column=0, sticky="w", padx=5, pady=2)
paper_var = tk.StringVar(value="Label")
paper_combo = ttk.Combobox(settings_frame, textvariable=paper_var, font=small_font, width=15)
paper_combo['values'] = list(PaperConfig.PAPER_SIZES.keys())
paper_combo.grid(row=1, column=1, padx=5, pady=2)

# Scan and print button
btn_scan = tk.Button(root, text="Scan and Print", command=scan_and_print, 
                     font=default_font, bg="#4CAF50", fg="white", pady=5)
btn_scan.pack(pady=10)

# Show conditions button
btn_conditions = tk.Button(root, text="Show Conditions", command=show_conditions, 
                          font=small_font, bg="#2196F3", fg="white")
btn_conditions.pack(pady=5)

# Check printer button
btn_printer = tk.Button(root, text="Check MACanton", command=check_printer_status, 
                       font=small_font, bg="#FF9800", fg="white")
btn_printer.pack(pady=5)

# Print settings button
btn_settings = tk.Button(root, text="View Print Settings", command=show_print_settings, 
                        font=small_font, bg="#9C27B0", fg="white")
btn_settings.pack(pady=5)

# Data management button
btn_data_manager = tk.Button(root, text="Manage Data", command=lambda: open_data_manager(root), 
                           font=small_font, bg="#607D8B", fg="white")
btn_data_manager.pack(pady=5)

# Output area
tk.Label(root, text="Result:", font=default_font).pack(pady=(20,0))
text_output = tk.Text(root, height=8, width=50, font=default_font)
text_output.pack(pady=5)

# Instructions
info_text = """Instructions:
1. System checks digits 2-3 and digit 6 of lot number
2. Example: QSTZ8B2206 → Digits 2-3: ST, Digit 6: B
3. Lot number must be at least 6 digits long
4. Click 'Manage Data' to add/edit/delete conditions"""

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

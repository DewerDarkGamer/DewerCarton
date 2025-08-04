
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

def get_part_rev_from_lot(lot_number):
    """Get part and revision data based on lot number conditions"""
    try:
        # Check if lot number has sufficient length
        if len(lot_number) < 6:
            return None, None
        
        # Extract digits at positions 2, 3, and 6 (index 1, 2, and 5)
        digit_2_3 = lot_number[1:3]  # digits 2 and 3
        digit_6 = lot_number[5]      # digit 6
        
        # Apply conditions
        if digit_2_3 == "TB" and digit_6 == "Q":
            return "J3011", "Rev.04"
        
        # Add more conditions here as needed
        # Example:
        # elif digit_2_3 == "AB" and digit_6 == "X":
        #     return "J2022", "Rev.03"
        
        # If no conditions match
        return None, None
            
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
                # Check if Epson L210 is available
                result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                printers = result.stdout
                
                # Try to find Epson L210 or similar printer
                epson_printer = None
                for line in printers.split('\n'):
                    if 'epson' in line.lower() or 'l210' in line.lower():
                        epson_printer = line.split()[1]  # Get printer name
                        break
                
                if epson_printer:
                    # ใช้คำสั่งพิมพ์จากไฟล์ตั้งค่า
                    selected_quality = quality_var.get()
                    print_cmd = get_print_command(filename, selected_quality).split()
                    subprocess.run(print_cmd, check=True)
                    messagebox.showinfo("Success", f"File sent to Epson L210 ({selected_quality} quality): {filename}")
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
    """Check if Epson L210 printer is available"""
    try:
        import subprocess
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        printers = result.stdout
        
        if 'epson' in printers.lower() or 'l210' in printers.lower():
            messagebox.showinfo("Printer Status", "Epson L210 printer is connected and ready")
        else:
            messagebox.showwarning("Printer Status", "Epson L210 not found. Available printers:\n" + printers)
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
{template_info['format'].format(
    lot='TB123Q789',
    part='J3011', 
    rev='Rev.04',
    time='2024-01-15 14:30:25'
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

# ส่วนการตั้งค่าการพิมพ์
settings_frame = tk.LabelFrame(root, text="Print Settings", font=default_font)
settings_frame.pack(pady=10, padx=20, fill="x")

# เลือกรูปแบบเอกสาร
tk.Label(settings_frame, text="Template:", font=small_font).grid(row=0, column=0, sticky="w", padx=5, pady=2)
template_var = tk.StringVar(value="standard")
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
paper_var = tk.StringVar(value="A4")
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
btn_printer = tk.Button(root, text="Check Epson L210", command=check_printer_status, 
                       font=small_font, bg="#FF9800", fg="white")
btn_printer.pack(pady=5)

# Print settings button
btn_settings = tk.Button(root, text="View Print Settings", command=show_print_settings, 
                        font=small_font, bg="#9C27B0", fg="white")
btn_settings.pack(pady=5)

# Output area
tk.Label(root, text="Result:", font=default_font).pack(pady=(20,0))
text_output = tk.Text(root, height=8, width=50, font=default_font)
text_output.pack(pady=5)

# Instructions
info_text = """Instructions:
1. System checks digits 2-3 and digit 6 of lot number
2. If digits 2-3 = "TB" and digit 6 = "Q" → Part: J3011, Rev: Rev.04
3. Lot number must be at least 6 digits long
4. Click 'Show Conditions' to see all configured conditions"""

info_label = tk.Label(root, text=info_text, font=small_font, 
                     justify=tk.LEFT, fg="gray")
info_label.pack(pady=10)

# Set focus to lot entry field on start
entry_lot.focus()

# Allow Enter key to scan
entry_lot.bind('<Return>', lambda event: scan_and_print())

root.mainloop()

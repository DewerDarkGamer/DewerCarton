import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys

class DataManager:
    """คลาสสำหรับจัดการข้อมูล Part และ Revision"""

    @staticmethod
    def get_data_file_path():
        # ใช้ path เดิมของ .exe
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, 'part_data.json')

    def __init__(self, data_file=None):
        self.data_file = data_file or self.get_data_file_path()
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_data(self, digits_2_3, digit_6, part, revision, description=""):
        key = f"{digits_2_3}_{digit_6}"
        self.data[key] = {
            "part": part,
            "revision": revision,
            "description": description or f"Digits 2-3: {digits_2_3}, Digit 6: {digit_6}"
        }
        self.save_data()
        return True

    def update_data(self, key, part, revision, description=""):
        if key in self.data:
            self.data[key]["part"] = part
            self.data[key]["revision"] = revision
            if description:
                self.data[key]["description"] = description
            self.save_data()
            return True
        return False

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()
            return True
        return False

    def get_part_rev(self, lot_number):
        try:
            if len(lot_number) < 6:
                return None, None
            digit_2_3 = lot_number[1:3]
            digit_6 = lot_number[5]
            key = f"{digit_2_3}_{digit_6}"
            if key in self.data:
                return self.data[key]["part"], self.data[key]["revision"]
            return None, None
        except Exception:
            return None, None


class DataManagerGUI:
    """หน้าจัดการข้อมูล GUI"""
    
    def __init__(self, parent=None):
        self.data_manager = DataManager()
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Data Manager - Part and Revision Management")
        self.window.geometry("800x600")
        self.setup_gui()
        self.refresh_table()
    
    def setup_gui(self):
        """สร้าง GUI"""
        # หัวข้อ
        title_label = tk.Label(self.window, text="Data Manager", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # ส่วนเพิ่มข้อมูลใหม่
        add_frame = tk.LabelFrame(self.window, text="Add New Data", 
                                 font=("Arial", 12))
        add_frame.pack(pady=10, padx=20, fill="x")
        
        # Input fields
        tk.Label(add_frame, text="Digits 2-3:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.digits_23_entry = tk.Entry(add_frame, font=("Arial", 10), width=10)
        self.digits_23_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Digit 6:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.digit_6_entry = tk.Entry(add_frame, font=("Arial", 10), width=5)
        self.digit_6_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_frame, text="Part Number:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.part_entry = tk.Entry(add_frame, font=("Arial", 10), width=15)
        self.part_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Revision:", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.revision_entry = tk.Entry(add_frame, font=("Arial", 10), width=10)
        self.revision_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # ฟังก์ชันแปลงเป็นตัวพิมพ์ใหญ่สำหรับ input fields
        def make_uppercase_handler(entry_widget):
            def on_key_release(event):
                current_text = entry_widget.get()
                if current_text != current_text.upper():
                    cursor_pos = entry_widget.index(tk.INSERT)
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, current_text.upper())
                    entry_widget.icursor(cursor_pos)
            return on_key_release
        
        # ผูก event handler กับทุก entry field
        self.digits_23_entry.bind('<KeyRelease>', make_uppercase_handler(self.digits_23_entry))
        self.digit_6_entry.bind('<KeyRelease>', make_uppercase_handler(self.digit_6_entry))
        self.part_entry.bind('<KeyRelease>', make_uppercase_handler(self.part_entry))
        self.revision_entry.bind('<KeyRelease>', make_uppercase_handler(self.revision_entry))
        
        # ปุ่มเพิ่มข้อมูล
        btn_add = tk.Button(add_frame, text="Add Data", 
                           command=self.add_data, bg="#4CAF50", fg="white")
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)
        
        # ตารางแสดงข้อมูล
        table_frame = tk.Frame(self.window)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # สร้าง Treeview
        columns = ("Key", "Digits 2-3", "Digit 6", "Part", "Revision", "Description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # กำหนดหัวคอลัมน์
        self.tree.heading("Key", text="Key")
        self.tree.heading("Digits 2-3", text="Digits 2-3")
        self.tree.heading("Digit 6", text="Digit 6")
        self.tree.heading("Part", text="Part Number")
        self.tree.heading("Revision", text="Revision")
        self.tree.heading("Description", text="Description")
        
        # กำหนดความกว้างคอลัมน์
        self.tree.column("Key", width=80)
        self.tree.column("Digits 2-3", width=80)
        self.tree.column("Digit 6", width=60)
        self.tree.column("Part", width=100)
        self.tree.column("Revision", width=80)
        self.tree.column("Description", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ปุ่มจัดการ
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        btn_edit = tk.Button(button_frame, text="Edit", 
                           command=self.edit_data, bg="#2196F3", fg="white")
        btn_edit.pack(side="left", padx=5)
        
        btn_delete = tk.Button(button_frame, text="Delete", 
                             command=self.delete_data, bg="#F44336", fg="white")
        btn_delete.pack(side="left", padx=5)
        
        btn_refresh = tk.Button(button_frame, text="Refresh", 
                              command=self.refresh_table, bg="#FF9800", fg="white")
        btn_refresh.pack(side="left", padx=5)
        
        # ตัวอย่างการใช้งาน
        example_frame = tk.LabelFrame(self.window, text="Example", 
                                    font=("Arial", 10))
        example_frame.pack(pady=10, padx=20, fill="x")
        
        example_text = """Example Lot Number: QSTZ8B2206
- Digits 2-3: ST (positions 2-3)
- Digit 6: B (position 6)
- Result Key: ST_B
- Part: D3022A, Revision: REV.B"""
        
        tk.Label(example_frame, text=example_text, font=("Arial", 9), 
                justify="left", fg="gray").pack(padx=10, pady=5)
    
    def add_data(self):
        """เพิ่มข้อมูลใหม่"""
        digits_23 = self.digits_23_entry.get().strip().upper()
        digit_6 = self.digit_6_entry.get().strip().upper()
        part = self.part_entry.get().strip()
        revision = self.revision_entry.get().strip()
        
        if not all([digits_23, digit_6, part, revision]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        if len(digits_23) != 2:
            messagebox.showwarning("Warning", "Digits 2-3 must be 2 characters")
            return
        
        if len(digit_6) != 1:
            messagebox.showwarning("Warning", "Digit 6 must be 1 character")
            return
        
        key = f"{digits_23}_{digit_6}"
        if key in self.data_manager.data:
            messagebox.showwarning("Warning", f"Key {key} already exists")
            return
        
        if self.data_manager.add_data(digits_23, digit_6, part, revision):
            messagebox.showinfo("Success", "Data added successfully")
            self.clear_entries()
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Failed to add data")
    
    def edit_data(self):
        """แก้ไขข้อมูล"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to edit")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        old_key = values[0]
        
        # เปิดหน้าต่างแก้ไข
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Data")
        edit_window.geometry("400x300")
        
        tk.Label(edit_window, text=f"Editing: {old_key}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Input fields frame
        input_frame = tk.Frame(edit_window)
        input_frame.pack(pady=10)
        
        # Digits 2-3
        tk.Label(input_frame, text="Digits 2-3:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        digits_23_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        digits_23_entry.insert(0, values[1])
        digits_23_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Digit 6
        tk.Label(input_frame, text="Digit 6:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        digit_6_entry = tk.Entry(input_frame, font=("Arial", 12), width=5)
        digit_6_entry.insert(0, values[2])
        digit_6_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Part Number
        tk.Label(input_frame, text="Part Number:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        part_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
        part_entry.insert(0, values[3])
        part_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Revision
        tk.Label(input_frame, text="Revision:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        revision_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        revision_entry.insert(0, values[4])
        revision_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # ฟังก์ชันแปลงเป็นตัวพิมพ์ใหญ่สำหรับ edit dialog
        def make_uppercase_handler_edit(entry_widget):
            def on_key_release(event):
                current_text = entry_widget.get()
                if current_text != current_text.upper():
                    cursor_pos = entry_widget.index(tk.INSERT)
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, current_text.upper())
                    entry_widget.icursor(cursor_pos)
            return on_key_release
        
        # ผูก event handler กับทุก entry field ใน edit dialog
        digits_23_entry.bind('<KeyRelease>', make_uppercase_handler_edit(digits_23_entry))
        digit_6_entry.bind('<KeyRelease>', make_uppercase_handler_edit(digit_6_entry))
        part_entry.bind('<KeyRelease>', make_uppercase_handler_edit(part_entry))
        revision_entry.bind('<KeyRelease>', make_uppercase_handler_edit(revision_entry))
        
        def save_edit():
            new_digits_23 = digits_23_entry.get().strip().upper()
            new_digit_6 = digit_6_entry.get().strip().upper()
            new_part = part_entry.get().strip()
            new_revision = revision_entry.get().strip()
            
            if not all([new_digits_23, new_digit_6, new_part, new_revision]):
                messagebox.showwarning("Warning", "Please fill all fields")
                return
            
            if len(new_digits_23) != 2:
                messagebox.showwarning("Warning", "Digits 2-3 must be 2 characters")
                return
            
            if len(new_digit_6) != 1:
                messagebox.showwarning("Warning", "Digit 6 must be 1 character")
                return
            
            new_key = f"{new_digits_23}_{new_digit_6}"
            
            # ถ้า key เปลี่ยนแปลง ให้ตรวจสอบว่า key ใหม่มีอยู่แล้วหรือไม่
            if new_key != old_key and new_key in self.data_manager.data:
                messagebox.showwarning("Warning", f"Key {new_key} already exists")
                return
            
            # ลบ key เก่าถ้า key เปลี่ยน
            if new_key != old_key:
                self.data_manager.delete_data(old_key)
            
            # เพิ่มข้อมูลใหม่หรืออัปเดต
            description = f"Digits 2-3: {new_digits_23}, Digit 6: {new_digit_6}"
            if self.data_manager.add_data(new_digits_23, new_digit_6, new_part, new_revision, description):
                messagebox.showinfo("Success", "Data updated successfully")
                edit_window.destroy()
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Failed to update data")
        
        tk.Button(edit_window, text="Save", command=save_edit, 
                 bg="#4CAF50", fg="white").pack(pady=20)
    
    def delete_data(self):
        """ลบข้อมูล"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to delete")
            return
        
        item = self.tree.item(selected[0])
        key = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {key}?"):
            if self.data_manager.delete_data(key):
                messagebox.showinfo("Success", "Data deleted successfully")
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Failed to delete data")
    
    def refresh_table(self):
        """รีเฟรชตาราง"""
        # ลบข้อมูลเก่า
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # เพิ่มข้อมูลใหม่
        for key, data in self.data_manager.data.items():
            if "_" in key:
                digits_23, digit_6 = key.split("_", 1)
            else:
                digits_23, digit_6 = key, ""
            
            self.tree.insert("", "end", values=(
                key,
                digits_23,
                digit_6,
                data["part"],
                data["revision"],
                data.get("description", "")
            ))
    
    def clear_entries(self):
        """ล้างข้อมูลในช่อง input"""
        self.digits_23_entry.delete(0, tk.END)
        self.digit_6_entry.delete(0, tk.END)
        self.part_entry.delete(0, tk.END)
        self.revision_entry.delete(0, tk.END)

def open_data_manager(parent=None):
    """เปิดหน้าจัดการข้อมูล"""
    DataManagerGUI(parent)

if __name__ == "__main__":
    # ทดสอบการใช้งาน
    app = DataManagerGUI()
    app.window.mainloop()

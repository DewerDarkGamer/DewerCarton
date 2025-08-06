
# -*- coding: utf-8 -*-
"""
ไฟล์ตั้งค่าการพิมพ์และรูปแบบหน้ากระดาษ
กำหนดขนาดกระดาษ ตำแหน่งข้อความ และการจัดรูปแบบ
"""

class PrinterConfig:
    """คลาสสำหรับตั้งค่าเครื่องปริ้น"""
    PRINTER_NAME = "MACarton"
    PRINTER_MODEL = "generic"

class PaperConfig:
    """คลาสสำหรับตั้งค่าขนาดและประเภทกระดาษ"""
    PAPER_SIZES = {
        "Label": {
            "width": 90,    # 9 ซม.
            "height": 40,   # 4 ซม.
            "code": "custom"
        }
    }
    ORIENTATION = {
        "landscape": "แนวนอน"      # แนวนอน
    }

class LabelFormat:
    """คลาสสำหรับรูปแบบป้ายกำกับ Lot Scanner"""
    
    LAYOUT_TEMPLATES = {
        "macarton_label": {
            "name": "รูปแบบ MACarton",
            "description": "ป้ายกำกับขนาด 9x4 ซม. ตามรูปแบบ MACarton",
            "format": "custom"
        }
    }

def format_label_text(lot, part, rev, time, template="macarton_label"):
    """
    จัดรูปแบบข้อความตามเทมเพลต MACarton สำหรับกระดาษขนาด 95x46mm
    
    Args:
        lot (str): หมายเลข Lot
        part (str): หมายเลขชิ้นส่วน  
        rev (str): เลขรุ่น
        time (str): เวลาที่สแกน
        template (str): ชื่อเทมเพลต
    
    Returns:
        str: ข้อความที่จัดรูปแบบแล้ว
    """
    # แยกวันที่และเวลา
    datetime_parts = time.split()
    date_part = datetime_parts[0] if len(datetime_parts) > 0 else ""
    time_part = datetime_parts[1] if len(datetime_parts) > 1 else ""
    
    # จัดรูปแบบวันที่ (เช่น 05/08/25)
    if date_part:
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_part, "%Y-%m-%d")
            date_display = date_obj.strftime("%d/%m/%y")
        except:
            date_display = date_part
    else:
        date_display = ""
    
    # จัดรูปแบบเวลา (เช่น 14:58)
    if time_part:
        time_display = time_part[:5]  # แสดงแค่ ชม:นาที
    else:
        time_display = ""
    
    # แสดง Revision แบบสั้น
    if rev and rev.strip():
        if "REV." in rev.upper():
            rev_display = rev.upper().replace("REV.", "")
        else:
            rev_display = rev
    else:
        rev_display = ""
    
    # สร้างบาร์โค้ดแบบง่าย
    barcode = f"*{lot}*"
    
    # รูปแบบแนวนอนขนาดเล็กสำหรับ 95x46mm (ประมาณ 30 ตัวอักษรต่อบรรทัด)
    label_text = f"""{part}
{lot}
{barcode}
{date_display} {time_display} {rev_display}"""
    
    return label_text

def get_print_command(filename, config_name="normal", paper_size="Label"):
    """
    สร้างคำสั่งสำหรับการพิมพ์ตามการตั้งค่า MACarton
    
    Args:
        filename (str): ชื่อไฟล์ที่จะพิมพ์
        config_name (str): ชื่อการตั้งค่า
        paper_size (str): ขนาดกระดาษ
    
    Returns:
        str: คำสั่งสำหรับการพิมพ์
    """
    import platform
    printer = PrinterConfig.PRINTER_NAME
    
    if platform.system().lower() == 'windows':
        # คำสั่งสำหรับ Windows - ใช้ print หรือ copy to printer port
        command = f'print /D:"{printer}" "{filename}"'
    else:
        # คำสั่งสำหรับ Linux/Unix - ใช้ lp
        command = f"lp -d {printer} -o media=custom.90x40mm -o orientation-requested=4 -o font=Times-New-Roman -o cpi=12 -o lpi=6 -o page-top=0 -o page-bottom=0 -o page-left=0 -o page-right=0 {filename}"
    
    return command

def get_paper_settings(paper_size="Label", orientation="landscape"):
    """
    ดึงการตั้งค่ากระดาษ
    
    Args:
        paper_size (str): ขนาดกระดาษ
        orientation (str): การวางแนวกระดาษ
    
    Returns:
        dict: การตั้งค่ากระดาษ
    """
    paper_config = PaperConfig.PAPER_SIZES.get(paper_size, PaperConfig.PAPER_SIZES["Label"])
    
    settings = {
        "size": paper_config,
        "orientation": orientation,
        "orientation_name": PaperConfig.ORIENTATION[orientation]
    }
    
    return settings

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # ทดสอบการจัดรูปแบบข้อความแบบ MACarton
    sample_text = format_label_text(
        lot="QSTZ8B2206",
        part="D3022A", 
        rev="B",
        time="2025-01-15 14:58:25",
        template="macarton_label"
    )
    
    print("ตัวอย่างป้ายกำกับ MACarton:")
    print(sample_text)
    print("\n" + "="*50)
    
    # ทดสอบคำสั่งพิมพ์
    print("\nคำสั่งพิมพ์:")
    print(get_print_command("test.txt", "normal"))

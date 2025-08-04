
# -*- coding: utf-8 -*-
"""
ไฟล์ตั้งค่าการพิมพ์และรูปแบบหน้ากระดาษ
กำหนดขนาดกระดาษ ตำแหน่งข้อความ และการจัดรูปแบบ
"""

class PrinterConfig:
    """คลาสสำหรับตั้งค่าเครื่องปริ้น"""
    
    # ตั้งค่าเครื่องปริ้น Epson L210
    PRINTER_NAME = "Epson_L210"
    PRINTER_MODEL = "epson"
    
    # ความละเอียดการพิมพ์ (DPI)
    PRINT_QUALITY = {
        "draft": "150dpi",      # ร่างงาน - ประหยัดหมึก
        "normal": "300dpi",     # ปกติ
        "high": "600dpi"        # คุณภาพสูง
    }
    
    # การตั้งค่าสี
    COLOR_MODE = {
        "color": "color",           # สี
        "grayscale": "grayscale",   # ขาวดำ
        "monochrome": "mono"        # ขาวดำล้วน
    }

class PaperConfig:
    """คลาสสำหรับตั้งค่าขนาดและประเภทกระดาษ"""
    
    # ขนาดกระดาษมาตรฐาน
    PAPER_SIZES = {
        "A4": {
            "width": 210,   # มิลลิเมตร
            "height": 297,  # มิลลิเมตร
            "code": "a4"
        },
        "A5": {
            "width": 148,
            "height": 210,
            "code": "a5"
        },
        "Letter": {
            "width": 216,
            "height": 279,
            "code": "letter"
        },
        "Label": {
            "width": 100,   # ป้ายกำกับขนาดเล็ก
            "height": 50,
            "code": "custom"
        }
    }
    
    # ประเภทกระดาษ
    PAPER_TYPES = {
        "plain": "กระดาษธรรมดา",
        "photo": "กระดาษโฟโต้", 
        "glossy": "กระดาษมันเงา",
        "matte": "กระดาษด้าน",
        "label": "กระดาษป้ายกำกับ"
    }
    
    # การวางแนวกระดาษ
    ORIENTATION = {
        "portrait": "แนวตั้ง",      # แนวตั้ง
        "landscape": "แนวนอน"      # แนวนอน
    }

class TextLayout:
    """คลาสสำหรับการจัดตำแหน่งและรูปแบบข้อความ"""
    
    # ระยะขอบกระดาษ (มิลลิเมตร)
    MARGINS = {
        "narrow": {     # ขอบแคบ
            "top": 5,
            "bottom": 5, 
            "left": 5,
            "right": 5
        },
        "normal": {     # ขอบปกติ
            "top": 10,
            "bottom": 10,
            "left": 10, 
            "right": 10
        },
        "wide": {       # ขอบกว้าง
            "top": 20,
            "bottom": 20,
            "left": 20,
            "right": 20
        }
    }
    
    # ขนาดตัวอักษร
    FONT_SIZES = {
        "small": 8,     # เล็ก
        "normal": 12,   # ปกติ
        "large": 16,    # ใหญ่
        "xlarge": 20    # ใหญ่มาก
    }
    
    # การจัดตำแหน่งข้อความ
    TEXT_ALIGN = {
        "left": "ชิดซ้าย",
        "center": "กึ่งกลาง", 
        "right": "ชิดขวา",
        "justify": "เต็มแนว"
    }
    
    # ระยะห่างระหว่างบรรทัด
    LINE_SPACING = {
        "single": 1.0,      # บรรทัดเดียว
        "onehalf": 1.5,     # หนึ่งเท่าครึ่ง
        "double": 2.0       # สองเท่า
    }

class LabelFormat:
    """คลาสสำหรับรูปแบบป้ายกำกับ Lot Scanner"""
    
    # รูปแบบการแสดงผล
    LAYOUT_TEMPLATES = {
        "compact": {
            "name": "แบบกะทัดรัด",
            "description": "ข้อมูลในบรรทัดเดียว",
            "format": "Lot: {lot} | Part: {part} | Rev: {rev} | {time}"
        },
        "standard": {
            "name": "แบบมาตรฐาน", 
            "description": "แยกบรรทัดชัดเจน",
            "format": """Lot Number: {lot}
Part Number: {part}
Revision: {rev}
Scan Time: {time}"""
        },
        "detailed": {
            "name": "แบบละเอียด",
            "description": "ข้อมูลครบถ้วนพร้อมหัวข้อ",
            "format": """================================
        LOT SCANNING REPORT
================================
Lot Number    : {lot}
Part Number   : {part}  
Revision      : {rev}
Scan Date/Time: {time}
System        : Lot Scanner v1.0
================================"""
        }
    }
    
    # ตำแหน่งของข้อมูลบนป้าย
    FIELD_POSITIONS = {
        "lot": {"x": 10, "y": 10},      # ตำแหน่ง Lot Number
        "part": {"x": 10, "y": 25},     # ตำแหน่ง Part Number  
        "revision": {"x": 10, "y": 40}, # ตำแหน่ง Revision
        "time": {"x": 10, "y": 55}      # ตำแหน่ง เวลา
    }

def get_print_command(filename, config_name="normal"):
    """
    สร้างคำสั่งสำหรับการพิมพ์ตามการตั้งค่า
    
    Args:
        filename (str): ชื่อไฟล์ที่จะพิมพ์
        config_name (str): ชื่อการตั้งค่า (normal, draft, high)
    
    Returns:
        str: คำสั่งสำหรับการพิมพ์
    """
    printer = PrinterConfig.PRINTER_NAME
    quality = PrinterConfig.PRINT_QUALITY.get(config_name, "300dpi")
    
    # คำสั่งสำหรับ Linux/Unix
    command = f"lp -d {printer} -o resolution={quality} -o media=a4 {filename}"
    
    return command

def format_label_text(lot, part, rev, time, template="standard"):
    """
    จัดรูปแบบข้อความตามเทมเพลตที่เลือก
    
    Args:
        lot (str): หมายเลข Lot
        part (str): หมายเลขชิ้นส่วน
        rev (str): เลขรุ่น
        time (str): เวลาที่สแกน
        template (str): ชื่อเทมเพลต
        
    Returns:
        str: ข้อความที่จัดรูปแบบแล้ว
    """
    template_config = LabelFormat.LAYOUT_TEMPLATES.get(template, 
                      LabelFormat.LAYOUT_TEMPLATES["standard"])
    
    formatted_text = template_config["format"].format(
        lot=lot,
        part=part, 
        rev=rev,
        time=time
    )
    
    return formatted_text

def get_paper_settings(paper_size="A4", orientation="portrait"):
    """
    ดึงการตั้งค่ากระดาษ
    
    Args:
        paper_size (str): ขนาดกระดาษ
        orientation (str): การวางแนวกระดาษ
        
    Returns:
        dict: การตั้งค่ากระดาษ
    """
    paper_config = PaperConfig.PAPER_SIZES.get(paper_size, 
                   PaperConfig.PAPER_SIZES["A4"])
    
    settings = {
        "size": paper_config,
        "orientation": orientation,
        "orientation_name": PaperConfig.ORIENTATION[orientation]
    }
    
    return settings

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # ทดสอบการจัดรูปแบบข้อความ
    sample_text = format_label_text(
        lot="TB123Q789",
        part="J3011", 
        rev="Rev.04",
        time="2024-01-15 14:30:25",
        template="detailed"
    )
    
    print("ตัวอย่างผลลัพธ์:")
    print(sample_text)
    
    # ทดสอบคำสั่งพิมพ์
    print("\nคำสั่งพิมพ์:")
    print(get_print_command("test.txt", "normal"))

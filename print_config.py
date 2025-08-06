
# -*- coding: utf-8 -*-
"""
ไฟล์ตั้งค่าการพิมพ์และรูปแบบหน้ากระดาษ
กำหนดขนาดกระดาษ ตำแหน่งข้อความ และการจัดรูปแบบ
"""

class PrinterConfig:
    """คลาสสำหรับตั้งค่าเครื่องปริ้น"""
    
    # ตั้งค่าเครื่องปริ้น MACanton (Default Printer)5
    PRINTER_NAME = "MACanton"
    PRINTER_MODEL = "generic"
    
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
            "width": 95,    # ป้ายกำกับขนาดที่กำหนด
            "height": 46,
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
        "tiny": 6,      # เล็กมาก (สำหรับป้ายกำกับ)
        "small": 8,     # เล็ก
        "normal": 10,   # ปกติ (ลดลงจาก 12)
        "large": 12,    # ใหญ่ (ลดลงจาก 16)
        "xlarge": 14    # ใหญ่มาก (ลดลงจาก 20)
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
        },
        "label_with_barcode": {
            "name": "ป้ายกำกับพร้อมบาร์โค้ด",
            "description": "ป้ายกำกับขนาด 95x46 มม. พร้อมบาร์โค้ด",
            "format": """{part} {rev_display}
{lot}
{date} {time}"""
        },
        "compact_label": {
            "name": "ป้ายกำกับแบบกะทัดรัด",
            "description": "ป้ายกำกับขนาดเล็ก 95x46 มม.",
            "format": """{part}|{rev_display}
{lot}
{date}|{time}"""
        }
    }
    
    # ตำแหน่งของข้อมูลบนป้าย
    FIELD_POSITIONS = {
        "lot": {"x": 10, "y": 10},      # ตำแหน่ง Lot Number
        "part": {"x": 10, "y": 25},     # ตำแหน่ง Part Number  
        "revision": {"x": 10, "y": 40}, # ตำแหน่ง Revision
        "time": {"x": 10, "y": 55}      # ตำแหน่ง เวลา
    }

def get_print_command(filename, config_name="normal", paper_size="Label"):
    """
    สร้างคำสั่งสำหรับการพิมพ์ตามการตั้งค่า
    
    Args:
        filename (str): ชื่อไฟล์ที่จะพิมพ์
        config_name (str): ชื่อการตั้งค่า (normal, draft, high)
        paper_size (str): ขนาดกระดาษ
    
    Returns:
        str: คำสั่งสำหรับการพิมพ์
    """
    printer = PrinterConfig.PRINTER_NAME
    quality = PrinterConfig.PRINT_QUALITY.get(config_name, "300dpi")
    
    # เลือกขนาดกระดาษตามการตั้งค่า
    if paper_size == "Label":
        media_option = "custom.95x46mm"  # ขนาดป้ายกำกับ 95x46 มม.
    else:
        paper_config = PaperConfig.PAPER_SIZES.get(paper_size, PaperConfig.PAPER_SIZES["A4"])
        media_option = paper_config["code"]
    
    # คำสั่งสำหรับ Linux/Unix พร้อมการตั้งค่าขนาดตัวอักษรเล็ก
    command = f"lp -d {printer} -o resolution={quality} -o media={media_option} -o cpi=16 -o lpi=8 {filename}"
    
    return command

def generate_barcode_text(lot):
    """
    สร้างบาร์โค้ดในรูปแบบข้อความ ASCII หรือไฟล์รูปภาพ
    
    Args:
        lot (str): หมายเลข Lot
        
    Returns:
        str: บาร์โค้ดในรูปแบบข้อความหรือชื่อไฟล์รูปภาพ
    """
    try:
        # ลองใช้ไลบรารี่ python-barcode สำหรับสร้างบาร์โค้ดจริง
        from barcode import Code128
        from barcode.writer import SVGWriter
        import io
        
        # สร้างบาร์โค้ด Code128
        code = Code128(lot, writer=SVGWriter())
        
        # สร้างบาร์โค้ดในรูปแบบข้อความ ASCII แทนไฟล์
        # เพื่อให้แสดงในข้อความได้
        barcode_ascii = "|||" + "||".join(["|" if c.isalnum() else "||" for c in lot]) + "|||"
        return barcode_ascii
        
    except ImportError:
        # ถ้าไม่มีไลบรารี่ จะใช้วิธีสร้างแบบง่าย ๆ
        barcode_lines = []
        for char in lot:
            if char.isalnum():
                ascii_val = ord(char.upper())
                pattern = f"|{'|' if ascii_val % 2 == 0 else '||'}|{'||' if ascii_val % 3 == 0 else '|'}|"
                barcode_lines.append(pattern)
        
        return ''.join(barcode_lines)

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
    
    if template in ["label_with_barcode", "compact_label"]:
        # แยกวันที่และเวลา
        datetime_parts = time.split()
        date_part = datetime_parts[0] if len(datetime_parts) > 0 else ""
        time_part = datetime_parts[1] if len(datetime_parts) > 1 else ""
        
        # จัดรูปแบบวันที่ให้สั้นลง (เช่น 05Aug25)
        if date_part:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date_part, "%Y-%m-%d")
                date_display = date_obj.strftime("%d%b%y")  # ลบช่องว่างออก
            except:
                date_display = date_part[:8]  # จำกัดความยาว
        else:
            date_display = ""
        
        # จัดรูปแบบเวลาให้สั้นลง (เช่น 14:58)
        if time_part:
            time_display = time_part[:5]  # แสดงแค่ ชม:นาที
        else:
            time_display = ""
        
        # แสดง REV แบบสั้น (เช่น B จาก REV.B)
        if rev and rev.strip():
            if "REV." in rev.upper():
                rev_display = rev.upper().replace("REV.", "")
            else:
                rev_display = rev[:3]  # จำกัดความยาว
        else:
            rev_display = ""
        
        if template == "label_with_barcode":
            # สร้างบาร์โค้ด
            barcode = generate_barcode_text(lot)
            formatted_text = template_config["format"].format(
                lot=lot,
                part=part,
                barcode=barcode,
                date=date_display,
                time=time_display,
                rev_display=rev_display
            )
        else:  # compact_label
            formatted_text = template_config["format"].format(
                lot=lot,
                part=part,
                date=date_display,
                time=time_display,
                rev_display=rev_display
            )
    else:
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
    # ทดสอบการจัดรูปแบบข้อความแบบป้ายกำกับ
    sample_text = format_label_text(
        lot="QSTZ8B2206",
        part="D3022A", 
        rev="REV.B",
        time="2025-08-05 14:58:25",
        template="label_with_barcode"
    )
    
    print("ตัวอย่างป้ายกำกับ:")
    print(sample_text)
    print("\n" + "="*50)
    
    # ทดสอบการจัดรูปแบบข้อความแบบละเอียด
    sample_text2 = format_label_text(
        lot="TB123Q789",
        part="J3011", 
        rev="Rev.04",
        time="2024-01-15 14:30:25",
        template="detailed"
    )
    
    print("ตัวอย่างแบบละเอียด:")
    print(sample_text2)
    
    # ทดสอบคำสั่งพิมพ์
    print("\nคำสั่งพิมพ์:")
    print(get_print_command("test.txt", "normal"))

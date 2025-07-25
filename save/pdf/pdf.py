import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def save_pdf(text, filename, font_path="/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"):
    """
    将文本内容保存为 PDF 文件，支持中文。
    默认字体为 Ubuntu 常见的文泉驿微米黑（WenQuanYi Micro Hei）。
    你也可以传入其它字体路径，如：
        /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    font_name = "WenQuanYiMicroHei"
    if font_path and os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    else:
        raise FileNotFoundError(f"Font file not found: {font_path}")

    c.setFont(font_name, 20)
    x = 50
    y = height - 50
    for line in text.split('\n'):
        c.drawString(x, y, line)
        y -= 30
        if y < 50:
            c.showPage()
            c.setFont(font_name, 20)
            y = height - 50
    c.save()
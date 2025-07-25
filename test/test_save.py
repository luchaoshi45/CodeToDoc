import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from save import save_png, save_pdf
if not os.path.exists("output"):
    os.makedirs("output")
save_png("你好，世界！\n这是第二行。", "output/output.png")
save_pdf("你好，世界！\n这是第二行。", "output/output.pdf")
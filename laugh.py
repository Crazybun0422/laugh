#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2025/4/29 19:15
# @Author：Malcolm
# @File : laugh.py
# @Software: PyCharm

from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = "@%#*+=-:. "


def pixel_to_char(pix):
    return ASCII_CHARS[int(pix / 255 * (len(ASCII_CHARS) - 1))]


def png_to_ascii_png(input_path, output_path, font_path=None, font_size=12):
    # 读取并灰度化
    img = Image.open(input_path).convert("RGBA")  # 使用 RGBA 模式读取图像（包括透明度）
    W, H = img.size

    # 加载字体
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    char_w, char_h = font.getsize("A")

    # 根据字符尺寸自动计算列数和行数
    cols = max(1, W // char_w)
    rows = max(1, H // char_h)

    # 缩放到 cols × rows
    img_small = img.resize((cols, rows))
    pixels = list(img_small.getdata())

    # 构造 ASCII 字符行
    ascii_str = ""
    for p in pixels:
        r, g, b, a = p
        # 如果像素的透明度为 0（完全透明），则跳过
        if a == 0:
            ascii_str += " "  # 透明区域使用空格
        else:
            # 计算灰度值并转换为字符
            gray = (r + g + b) / 3
            ascii_str += pixel_to_char(gray)

    ascii_lines = [ascii_str[i:i + cols] for i in range(0, len(ascii_str), cols)]

    # 渲染到新图像
    out_img = Image.new("RGBA", (cols * char_w, rows * char_h), (255, 255, 255, 0))  # 保持透明背景
    draw = ImageDraw.Draw(out_img)
    y = 0
    for line in ascii_lines:
        draw.text((0, y), line, fill=(0, 0, 0, 255), font=font)  # 使用不透明字符
        y += char_h

    # 保存为 PNG
    out_img.save(output_path)
    print(f"Saved ASCII art PNG to {output_path}")


# ——— 参数配置 ———
input_path = "laugh.png"  # 输入文件
output_path = "ascii_output.png"  # 输出文件
font_path = None  # 如需自定义字体，可填路径："Courier_New.ttf"
font_size = 16  # 自定义字体时生效

# 执行转换
png_to_ascii_png(input_path, output_path, font_path, font_size)

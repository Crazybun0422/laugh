#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2025/4/30 17:03
# @Author：Malcolm
# @File : laugh_gif.py.py
# @Software: PyCharm

import os
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import imageio.v2 as imageio  # 改用 imageio.v2 来保持旧版行为，去掉警告

# ——— 参数配置 ———
input_gif = "test.gif"  # 要处理的 GIF 路径
frames_dir = "frames"  # 提取的帧存放目录
ascii_dir = "ascii_frames"  # 转换后 ASCII 帧存放目录
output_gif = "ascii_output.gif"  # 最终输出的 ASCII GIF
font_path = None  # 可选：自定义等宽字体文件路径
font_size = 12  # 自定义字体大小，仅当指定 font_path 时生效
frame_duration = 0.1  # 每帧时长（秒）
ASCII_CHARS = "@%#*+=-:. "  # 字符映射表，从“浓”到“淡”


def pixel_to_char(pix):
    """把灰度值（0-255）映射到 ASCII_CHARS 中的字符。"""
    return ASCII_CHARS[int(pix / 255 * (len(ASCII_CHARS) - 1))]


def png_to_ascii_png(input_path, output_path, font_path=None, font_size=12):
    """
    把一张 PNG 图片转换成 ASCII 艺术图并保存为 PNG。
    """
    img = Image.open(input_path).convert("L")
    W, H = img.size

    # 载入字体
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    char_w, char_h = font.getsize("A")

    # 计算字符网格尺寸
    cols = max(1, W // char_w)
    rows = max(1, H // char_h)

    # 缩放并生成 ASCII 文本
    small = img.resize((cols, rows))
    pixels = small.getdata()
    ascii_str = "".join(pixel_to_char(p) for p in pixels)
    lines = [ascii_str[i:i + cols] for i in range(0, len(ascii_str), cols)]

    # 渲染到新图
    out_img = Image.new("L", (cols * char_w, rows * char_h), color=255)
    draw = ImageDraw.Draw(out_img)
    y = 0
    for line in lines:
        draw.text((0, y), line, fill=0, font=font)
        y += char_h

    out_img.save(output_path)


# 确保目录存在
os.makedirs(frames_dir, exist_ok=True)
os.makedirs(ascii_dir, exist_ok=True)

# 1. 拆解 GIF 到单帧 PNG
gif = Image.open(input_gif)
for idx, frame in enumerate(ImageSequence.Iterator(gif)):
    frame.save(os.path.join(frames_dir, f"frame_{idx:04d}.png"))

# 2. 转换每个 PNG 为 ASCII PNG
for fname in sorted(os.listdir(frames_dir)):
    inp = os.path.join(frames_dir, fname)
    outp = os.path.join(ascii_dir, fname)
    png_to_ascii_png(inp, outp, font_path, font_size)

# 3. 合成 ASCII GIF
ascii_frames = []
for fname in sorted(os.listdir(ascii_dir)):
    path = os.path.join(ascii_dir, fname)
    ascii_frames.append(imageio.imread(path))
imageio.mimsave(output_gif, ascii_frames, format="GIF", duration=frame_duration, loop=0)

print(f"ASCII GIF 已保存至: {output_gif}")

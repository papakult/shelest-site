#!/usr/bin/env python3
"""Общие функции обработки фото: обрезка плоских баннеров/шапок (текст, копирайты
спонсоров), сохранение в веб-размерах. Монохром применяется через CSS на сайте,
поэтому здесь фото остаются в естественном цвете."""
import numpy as np
from PIL import Image, ImageOps

def _row_std(arr):
    return arr.reshape(arr.shape[0], -1).std(axis=1)

def _col_std(arr):
    return arr.transpose(1, 0, 2).reshape(arr.shape[1], -1).std(axis=1)

def auto_trim_bars(im, thresh=10, max_frac=0.22):
    """Обрезает плоские (малодисперсные) полосы сверху/снизу — типично текстовые
    плашки, статус-бары телефона, копирайт-полосы спонсоров. Не трогает фото само по себе."""
    arr = np.asarray(im.convert('RGB'))
    h = arr.shape[0]
    rs = _row_std(arr)
    top = 0
    while top < h * max_frac and rs[top] < thresh:
        top += 1
    bot = h
    while bot > h * (1 - max_frac) and rs[bot - 1] < thresh:
        bot -= 1
    if bot - top < h * 0.5:
        return im
    return im.crop((0, top, arr.shape[1], bot))

def find_seam_x(im, lo=0.42, hi=0.58):
    """Ищет самый 'плоский' столбец рядом с центром — граница между до/после в диптихе."""
    arr = np.asarray(im.convert('RGB'))
    w = arr.shape[1]
    cs = _col_std(arr)
    lo_i, hi_i = int(w * lo), int(w * hi)
    seg = cs[lo_i:hi_i]
    return lo_i + int(np.argmin(seg))

def split_diptych(im, gap=6):
    x = find_seam_x(im)
    left = im.crop((0, 0, max(x - gap, 1), im.height))
    right = im.crop((min(x + gap, im.width - 1), 0, im.width, im.height))
    return left, right

def export(im, base, widths, out_dir='img'):
    im = ImageOps.exif_transpose(im)
    for w in widths:
        if im.width <= w:
            out = im
        else:
            ratio = w / im.width
            out = im.resize((w, max(1, int(im.height * ratio))), Image.LANCZOS)
        out.convert('RGB').save(f'{out_dir}/{base}-{w}.jpg', quality=85, progressive=True, optimize=True)
    # базовая (без суффикса) — самая крупная нужная ширина, используется как src по умолчанию
    biggest = max(widths)
    im2 = im if im.width <= biggest else im.resize((biggest, max(1, int(im.height * (biggest/im.width)))), Image.LANCZOS)
    im2.convert('RGB').save(f'{out_dir}/{base}.jpg', quality=87, progressive=True, optimize=True)

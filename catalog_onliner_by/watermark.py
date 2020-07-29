import os
from io import BytesIO
from PIL import Image

import numpy as np
import cv2 as cv

def compute_average_image_color(image):
    width, height = image.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = image.getpixel((x,y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    return (r_total/count, g_total/count, b_total/count)

def dominant_color(image):
    #Resizing parameters
    width, height = 150,150
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    #Get the most frequent color
    dominant_color = sorted_pixels[-1][1]
    return dominant_color

def del_watermark(image_name):
    # original_image = Image.open('5fdf7fb135ed95427b289bb55d593ce7.jpeg') ### BLACK
    original_image = Image.open(image_name) ### WHITE
    x, y = original_image.size

    if x > 190:
        watermark_peace = original_image.crop((x-190, y-80, x, y))
    else:
        watermark_peace = original_image.crop((x - 40, y - 190, x, y))
    watermark_peace_dominant_color = dominant_color(watermark_peace)
    # print(watermark_peace_dominant_color)
    if not type(watermark_peace_dominant_color) == tuple:
        watermark_peace_dominant_color = [watermark_peace_dominant_color, watermark_peace_dominant_color, watermark_peace_dominant_color]

    if len(watermark_peace_dominant_color) < 3:
        watermark_peace_dominant_color = [watermark_peace_dominant_color[0], watermark_peace_dominant_color[1], watermark_peace_dominant_color[1]]

    if watermark_peace_dominant_color[0] >130 or watermark_peace_dominant_color[1] >130 or watermark_peace_dominant_color[2] >130:
        ### if dominant color is LIGHT
        watermark = Image.open('catalog-onliner-by-mask-2.png').convert("RGBA")
        margin_x = 19
        margin_y = 12
    else:
        margin_x = 22
        margin_y = 16
        watermark = Image.open('catalog-onliner-by-mask.png').convert("RGBA")
    watermark_width, watermark_height = watermark.size

    if 190 >= x:
        watermark = watermark.rotate(90, expand=1)
        watermark_width, watermark_height = watermark.size
        # watermark.show()
        margin_x = 7
        margin_y = 14

    margin = 15
    # positions
    position_tl = (0 + margin, 0 + margin)
    position_tr = (x - margin - watermark_width, 0 + margin)
    position_bl = (0 + margin, y - margin - watermark_height)
    position_br = (x - margin_x - watermark_width, y - margin_y - watermark_height)

    image_with_watermark = Image.new('RGBA', (x, y), (0, 0, 0, 0))
    image_with_watermark.paste(watermark, position_br, mask=watermark)

    img = cv.imread(image_name)
    mask = cv.cvtColor(np.array(image_with_watermark), cv.COLOR_RGBA2GRAY)
    dst = cv.inpaint(img,mask,5,cv.INPAINT_TELEA)
    # cv.imshow('dst',dst)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    pil_image = cv.cvtColor(dst, cv.COLOR_BGRA2RGBA)
    pil_image = Image.fromarray(pil_image)
    return pil_image


def add_watermark(pil_image):
    # original_image = Image.open('080e859c436813fb68865c3e3111ec40.jpeg')
    original_image = pil_image
    watermark = Image.open('my-watermark.png').convert("RGBA")
    watermark_width, watermark_height = watermark.size
    x, y = original_image.size

    margin = 20
    margin_x = 19
    margin_y = 12
    if 190 >= x:
        watermark = watermark.rotate(90, expand=1)
        watermark_width, watermark_height = watermark.size
        margin_x = 1
        margin_y = 18

    # positions
    position_tl = (0 + margin, 0 + margin)
    position_tr = (x - margin - watermark_width, 0 + margin)
    position_bl = (0 + margin, y - margin - watermark_height)
    position_br = (x - margin_x - watermark_width, y - margin_y - watermark_height)

    image_with_watermark = Image.new('RGBA', (x, y), (0, 0, 0, 0))
    image_with_watermark.paste(original_image, (0, 0))
    image_with_watermark.paste(watermark, position_br, mask=watermark)

    return image_with_watermark
#
# image_name = "9cf4220cf9c1e03a326a529bcea0d1d6.jpeg"
# without_watermark = del_watermark(image_name)
# watermarked = add_watermark(without_watermark)
# # watermarked.convert('RGB').save(image_name)
# watermarked.show()

from PIL import Image, ImageDraw, ImageFont
import math
import cv2
import numpy as np
import os
import pytesseract
import functions




# reader = easyocr.Reader(['en'])



bewareOf = []




power = {}
tech = {}
helps = {}
building = {}
files = ["Images/tech.png"]
print("tech" in files[0])

res = functions.splitImage(Image.open(files[0]))
for i in res:
    print(functions.parseImages(i))
print(bewareOf)
print(tech)
# result = reader.readtext('output/User.1.png')

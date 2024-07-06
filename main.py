from PIL import Image, ImageDraw, ImageFont
import math
import cv2
import numpy as np
import os
import pytesseract



fillerColor = (27, 150, 206,255)
linePixel=(74, 170, 214,255)
def isSimilarColor(col1, col2, tolerance):
    array = []
    for i in range(3):
        array.append(abs(col1[i] - col2[i] <= tolerance))
    if False in array:
        return False
    else:
        return True
# reader = easyocr.Reader(['en'])
bewareOf = []
acceptableColorList = [[255,255,255],[27,150,206]]
def closest(colors,color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance[0]

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
def binarize(image):
    thresh, im_bw = cv2.threshold(image, 200, 230, cv2.THRESH_BINARY)
    return im_bw
def dilate(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image
power = {}
tech = {}
helps = {}
building = {}
files = ["Images/tech.png"]
print("tech" in files[0])
for imageName in files:
    im = Image.open(imageName)
    pixel = im.load()
    centerX = im.size[0]//2
    draw = ImageDraw.Draw(im) 
    font = ImageFont.load_default()
    diff = []
    alternate=0
    x=1
    override = []
    for i in range(im.size[1]):
        if i in override:
            continue
        if isSimilarColor(linePixel, pixel[centerX, i], 3):
            if alternate == 1:
                alternate = 0
                override = range(i, i+10)
                continue

            draw.line((0,i, im.size[0],i), fill=128)
            # draw.text((0,i), str(i), (255,255,255), font=font)
            diff.append((i, i+61))
            alternate = 1
            override = range(i, i+25)
    
    x=1
    with open("output.txt", "w+") as output:
        for i in diff:
            nim = im.crop((0,i[0]+10, im.size[0], i[1]-10))
            pixels = nim.load()
            open_cv_image = np.array(nim)
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            finalImg = binarize(grayscale(open_cv_image))
            cv2.imwrite(f"output/user-{x}.png", finalImg)
            ocr = str(pytesseract.image_to_string(finalImg)).replace("\n", " ").split(" ")
            # ocr = 5
            print(ocr)
            if len(ocr) < 2:
                if len(ocr) == 1:
                    bewareOf.append(ocr[0])
                if len(ocr) == 0:
                    bewareOf.append(f"Rank {x}")
            else:
                if "tech" in imageName:
                    tech[ocr[0]] = ocr[1]
                elif "building" in imageName:
                    building[ocr[0]] = ocr[1]
                elif "tech" in imageName:
                    tech[ocr[0]] = ocr[1]
                elif "power" in imageName:
                    power[ocr[0]] = ocr[1]
                    

            output.write(pytesseract.image_to_string(finalImg) + "\n")
            x+=1
    im.save("out.png")


print(bewareOf)
print(tech)
# result = reader.readtext('output/User.1.png')

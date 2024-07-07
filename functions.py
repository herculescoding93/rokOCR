import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import json

with open('table.json', 'r') as file:
    table = json.load(file)
    file.close()
acceptableColorList = [[255,255,255],[27,150,206]]
imageName = "Images/tech.png"

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

def splitImage(im):
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
        if isSimilarColor(linePixel, pixel[centerX, i], 15):
            if alternate == 1:
                alternate = 0
                override = range(i, i+10)
                continue

            draw.line((0,i, im.size[0],i), fill=128)
            # draw.text((0,i), str(i), (255,255,255), font=font)
            diff.append((i, i+61))
            alternate = 1
            override = range(i, i+25)
    im.save("out.png")

    x=1
    images = []
    for i in diff:
        nim = im.crop((0,i[0]+10, im.size[0], i[1]-10))
        pixels = nim.load()
        open_cv_image = np.array(nim)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        finalImg = binarize(grayscale(open_cv_image))
        cv2.imwrite(f"output/user-{x}.png", finalImg)
        # ocr = str(pytesseract.image_to_string(finalImg)).replace("\n", " ").split(" ")
        # ocr = 5
        images.append(finalImg)
        # output.write(pytesseract.image_to_string(finalImg) + "\n")
        x+=1
    return images


def updateTable(parsedName, name):
    table[parsedName] = name
def writeTable():
    with open("table.json", "w+") as output:
        json.dump(table, output)
        print('succesfully wrote table')
        output.close()

    

def parseImages(image, usetable):
    num = None
    code = 0
    ocr = str(pytesseract.image_to_string(image)).replace("\n", " ").replace(",", "").split(" ")
    name = ""
    print(f"DEBUG: {ocr}")
    for idx, i in enumerate(ocr):
        if len(i) <=2 and not i.isnumeric():
            del ocr[idx]
            continue
    for i in ocr:    
        if not i.isnumeric():
            name += i
        else:
            num = int(i)

    name = name.replace("Envoy", "").replace("Leader", "").replace("Warlord", "").replace("Saint", "")
    if num == None:
        num = 0
    if name == "":
        code = 3
    if usetable:
        if name in table:
            name = table[name]
        else:
            code = 1

    ocr = [name,num, code]
    
    
    return ocr





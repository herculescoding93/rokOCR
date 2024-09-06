import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import json
import os
import imagerec
with open('table.json', 'r') as file:
    table = json.load(file)
    file.close()
acceptableColorList = [[255,255,255],[27,150,206]]
imageName = "Images/tech.png"

fillerColor = (27, 150, 206,255)
linePixel=(74, 170, 214,255)
# linePixel=(217, 199, 171,255)




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




def similar(array,array1, tolerance):
    try:
        for i in range(len(array)):
            if abs(array[i]-array1[i]) > tolerance:
                return False
            return True
    except:
        print("failure huh")



def username(image):
    rows, cols, _ = image.shape
    image1 = image[0:rows, 0:int(cols//2.5)]
    bin = binarize(grayscale(image1))
    rows, cols = bin.shape
    biggest = 0
    for i in range(cols):
        color = bin[rows//2, i]
        if color == 230:
            if i > biggest:
                biggest = i
        
    return image[0+5:rows-7, 0:biggest+10]
    # return image.crop((0+6,0, image.width //3, image.height-5))

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
        # if similar(pixel[centerX, i], linePixel, 4):
        # if i%36 == 0:
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
        nim = im.crop((0,i[0]+10, im.size[0], i[1]-15))
        pixels = nim.load()
        open_cv_image = np.array(nim)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        finalImg = binarize(grayscale(open_cv_image))
        rows, cols = finalImg.shape
        finalImg = finalImg[0:rows, cols//3:cols]
        cv2.imwrite(f"output/user-{x}.png", finalImg)
        PIL_image = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
        
        
        open_cv_image = np.array(PIL_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        # finalImg2 = username(binarize(grayscale(open_cv_image)))
        finalImg2 = username(open_cv_image)
        # cv2.imshow("Define name for:", finalImg2)
        # cv2.waitKey(1)
        # name = input('Name?\n')
        # name = temp[x-1]
        # cv2.imwrite(f"imgStorage/{name}.png", finalImg2)
        # if temp[x-1] == "soleron":
        #     raise Exception
        #     exit()
        # ocr = str(pytesseract.image_to_string(finalImg)).replace("\n", " ").split(" ")
        # ocr = 5
        # images.append(finalImg)
        images.append([finalImg2, finalImg])
        # output.write(pytesseract.image_to_string(finalImg) + "\n")
        x+=1
    return images



def readNumber(image):

    out = str(pytesseract.image_to_string(image))
    if out.isnumeric():
        return out
    else:
        return [-1]

def updateTable(parsedName, name):
    table[parsedName] = name
def writeTable():
    with open("table.json", "w+") as output:
        json.dump(table, output)
        print('succesfully wrote table')
        output.close()


def updateImgTable(image, name):
    cv2.imwrite(f"imgStorage/{name}.png", image)
blacklist = []
def findMatch(image):
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    biggest = ["", 0]
    for i in os.listdir("imgStorage"):
        if i in blacklist:
            continue
        score = imagerec.similarityScore(open_cv_image, i)
        if score > biggest[1]:
            biggest = [i.replace(".png", ""), score]
        if score >= 95:
            break
    if biggest[1] < 85:
        biggest.append(1)
    else:
        biggest.append(0)
    blacklist.append(biggest[0]+".png")
    return biggest
    
def parseImages(image, usetable, crop=False):
    num = None
    code = 0
    if not crop:
        ocr = str(pytesseract.image_to_string(image)).replace("\n", " ").replace(",", "").split(" ")
    else:
        PIL_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) 
        ocr = str(pytesseract.image_to_string(PIL_image.crop((0+13,0, PIL_image.width //2.5, PIL_image.height-5)))).replace("\n", " ").replace(",", "").split(" ")
        ocr = ocr + str(pytesseract.image_to_string(PIL_image.crop((PIL_image.width //3,0, PIL_image.width, PIL_image.height-5)))).replace("\n", " ").replace(",", "").split(" ") 
    name = ""
    print(f"DEBUG {ocr}")
    test = "#0000"
    for idx, i in enumerate(ocr):
        if len(i) <=2 and not i.isnumeric():
            del ocr[idx]
            continue
    for i in ocr:
        if "#" in str(i):
            test = i
            del i
    for i in ocr:    
        f = i.replace(".", "")
        if not f.isnumeric():
            name += f
        else:
            num = int(f)
            print("Integer Defined")

    name = name.replace("Envoy", "").replace("Leader", "").replace("Warlord", "").replace("Saint", "")
    # print(f"EMERGENCY: {not any(c.isalpha() for c in name)}")
    if num == None and not crop:
        num = 0

    if usetable:
        if name in table:
            name = table[name]
        else:
            code = 1
    # print(f"hope: {name}, {not any(c.isalpha() for c in name)}")
    if not any(c.isalpha() for c in name) and not crop:
        print("emegency ran")
        return ["", 0, 4]
        
    ocr = [name,num, code, test]
    
    
    return ocr





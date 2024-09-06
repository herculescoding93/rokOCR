import functions
from PIL import Image
import time
import cv2
import json 

names = {}
for i in functions.splitImage(Image.open("Images/power.png")):
    time.sleep(0.1)
    cv2.imshow("OCR Table Maker", i)
    cv2.waitKey(1)
    res = input("What is the name of this user?\n")
    if res == "E":
        cv2.destroyAllWindows()
        break
    parse = functions.parseImages(i, False)
    names[parse[0]] = res
with open("table.json","w+") as tableFile:
    json.dump(names, tableFile)


    

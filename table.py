import functions
from PIL import Image
import time
import cv2


for i in functions.splitImage(Image.open("Images/tech.png")):
    cv2.imshow("OCR Table Maker", i)
    cv2.waitKey(1)
    res = input("What is the name of this user?\n")
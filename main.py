from PIL import Image, ImageDraw, ImageFont
import math
import cv2
import numpy as np
import os
import pytesseract
import functions



class User():
    def __init__(self, name:str):
        self.name = name
        self.tech = None
        self.building = None
        self.helps = None
        self.power = None
    def updatePower(self, power:int):
        self.power = power
    def updateTech(self, tech:int):
        self.tech = tech
    def updateBuilding(self, building:int):
        self.building = building
    def updateHelps(self, helps:int):
        self.building = helps
    def userInfo(self):
        return {"name": self.name, "power": self.power, "helps": self.helps, "tech": self.tech, "building": self.building}
# reader = easyocr.Reader(['en'])



bewareOf = []




data = {}
files = ["Images/tech.png"]
print("tech" in files[0])

res = functions.splitImage(Image.open(files[0]))
for i in res:
    parse = functions.parseImages(i, True)
    name = parse[0]
    value = parse[1]
    repCode = parse[2]
    if repCode == 1:
        realName = input("Lookup Failed, can you please type the name shown in the image?\n")
        functions.updateTable(parse[0], realName)
        print("Updated table")
        name = realName
    if name in data:
        data[name].updateTech(value)
    user = User(name)
    user.updateTech(value)
    data[name] = user

for i in data.values():
    res = i.userInfo()
    print(f"{res['name']}: {res['tech']}")


# result = reader.readtext('output/User.1.png')

from PIL import Image, ImageDraw, ImageFont
import math
import cv2
import numpy as np
import os
import pytesseract
import functions
import csv


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
        self.helps = helps
    def userInfo(self):
        return {"name": self.name, "power": self.power, "helps": self.helps, "tech": self.tech, "building": self.building}
# reader = easyocr.Reader(['en'])



bewareOf = []




data = {}
files = []

for i in os.listdir("Images"):
    files.append("Images/" + i)

for file in files:
    res = functions.splitImage(Image.open(file))
    for i in res:
        parse = functions.parseImages(i, True)
        name = parse[0]
        value = parse[1]
        repCode = parse[2]
        if repCode == 4:
            parse = functions.parseImages(i, True, crop=True)
            name = parse[0]
            value = parse[1]
            repCode = parse[2]
        if repCode == 1:
            cv2.imshow("Lookup Failure", i)
            cv2.waitKey(1)
            realName = input("Lookup Failed, can you please type the name shown in the image?\n")
            functions.updateTable(parse[0], realName)
            functions.writeTable()
            print("Updated table")
            name = realName
        if repCode == 3:
            cv2.imshow("Lookup Failure | NO NAME DETECTED!", i)
            cv2.waitKey(1)
            realName = input("Lookup Failed, can you please type the name shown in the image?\n")
            name = realName            
        
        if repCode == 2:
            value = 0
        if name in data:
            if "tech" in file.lower():
                data[name].updateTech(value)
            if "power" in file.lower():
                data[name].updatePower(value)
            if "building" in file.lower():
                data[name].updateBuilding(value)
            if "power" in file.lower():
                data[name].updatePower(value)
            if "helps" in file.lower():
                data[name].updateHelps(value)
        else:

            user = User(name)
            if "tech" in file.lower():
                user.updateTech(value)
            if "power" in file.lower():
                user.updatePower(value)
            if "building" in file.lower():
                user.updateBuilding(value)
            if "power" in file.lower():
                user.updatePower(value)
            if "helps" in file.lower():
                user.updateHelps(value)
            data[name] = user

for i in data.values():
    res = i.userInfo()
    print(f"{res['name']}, tech: {res['tech']}, building: {res['building']}")

alliance = "Earthquake"
with open('profiles1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    fields = ["username", "alliance", "power", "helps", "", "tech", "", "building"]
    writer.writerow(fields)
    for i in data.values():
        userData = i.userInfo()
        writer.writerow([userData["name"], alliance, userData["power"], userData["helps"], "", userData["tech"], "", userData["building"]])
# result = reader.readtext('output/User.1.png')

from PIL import Image, ImageDraw, ImageFont
import math
import cv2
import numpy as np
import os

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
    if os.path.isdir("Images/" + i):
        continue
    files.append("Images/" + i)


print("Initializing...")
for file in files:
    res = functions.splitImage(Image.open(file))
    for i in res:
        parse = functions.findMatch(i[0])
        print(parse)
        repCode= parse[2]
        name = parse[0]
        value = functions.readNumber(i[1])
        similarity = parse[1]
        if repCode == 1:
            cv2.imshow("Lookup Failure", i[0])
            cv2.waitKey(1)
            realName = input("Lookup Failed, can you please type the name shown in the image?\n").lower.replace(" ", "")
            functions.updateImgTable(i[0], realName)
        print(f"Name: {name}, Value: {value}")

        if name in data:
            if "tech" in file.lower():
                data[name].updateTech(value)
            if "power" in file.lower():
                data[name].updatePower(value)
                # data[name].updateHelps(parse[3])
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
                # user.updateHelps(parse[3])
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

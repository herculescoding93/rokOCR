import cv2
import numpy as np
import glob
import functions
from PIL import Image
import os
from datetime import datetime

# original = functions.splitImage(Image.open("Images/tech.png"))[10]
# cv2.imshow("test", original)
# cv2.waitKey(1)



import torch
import open_clip
from sentence_transformers import util
# image processing model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-16-plus-240', pretrained="laion400m_e32")
model.to(device)
def imageEncoder(img):
    img1 = Image.fromarray(img).convert('RGB')
    img1 = preprocess(img1).unsqueeze(0).to(device)
    img1 = model.encode_image(img1)
    return img1
def generateScore(image1, image2):
    test_img = image1
    data_img = cv2.imread(image2, cv2.IMREAD_UNCHANGED)
    
    img1 = imageEncoder(test_img)
    
    img2 = imageEncoder(data_img)
    # now = datetime.now()
    cos_scores = util.pytorch_cos_sim(img1, img2)
    # print(datetime.now() - now)
    score = round(float(cos_scores[0][0])*100, 2)
    return score
biggest = ("", 0)


def similarityScore(image1, image2):
    score = round(generateScore(image1, f"imgStorage/{image2}"), 2)
    return score


# for i in os.listdir("imgStorage"):
#     score = round(generateScore(original, f"imgStorage/{i}"), 2)
#     if score > biggest[1]:
#         biggest = (i, score)
    # print(f"similarity Score: ", str(score) + f" Name: {i.replace('.png', '')}")
# print(f"The biggest confidence is: {biggest}")
#similarity Score: 76.77
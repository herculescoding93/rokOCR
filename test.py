import functions
from PIL import Image
import pytesseract


im = Image.open("output/user-1.png")
im = im.crop((0+10, 0, im.width // 3.5, im.height))
print(pytesseract.image_to_string(im))
im.save("test.png")
# print(functions.parseImages(Image.open("output/user-50.png"), True))
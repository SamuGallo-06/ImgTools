from PIL import Image
from rembg import remove

def RemoveBgFromImage(inputFilePath, outputFilePath):
    
    img = Image.open(inputFilePath)
    img = remove(img)
    img.save(outputFilePath)
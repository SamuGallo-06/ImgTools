from PIL import Image
import os
import cairosvg

def ConvertToIco(inputFilePath, outputFilePath, resize = False, sizeX = 0, sizeY = 0, rotation=0):
    #check if file exists
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN") 
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")

    if(resize):
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
        
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1)
        
    inputImage.save(outputFilePath, format='ICO', bitmap_format='bmp')
    
def ConvertToJpeg(inputFilePath, outputFilePath, resize=False, sizeX=0, sizeY=0, rotation=0):
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN")
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")

    if(resize):
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
        
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1)
    
    inputImage = inputImage.convert("RGB")  # Ensure image is RGB, as JPEG does not support alpha
    inputImage.save(outputFilePath, format="JPEG")  
    
    
def ConvertToPng(inputFilePath, outputFilePath, resize = False, sizeX = 0, sizeY = 0, rotation=0):
    #check if file exists
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN")
        
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")

    if(resize):
        print("resizing image")
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
        
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1)
        
    inputImage.save(outputFilePath, format="PNG")
    
def ConvertToGif(inputFilePath, outputFilePath, resize = False, sizeX = 0, sizeY = 0, rotation=0):
    #check if file exists
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN")
        
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")

    if(resize):
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
        
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1)
        
    inputImage.save(outputFilePath, format="GIF")
    
def ConvertToBmp(inputFilePath, outputFilePath, resize = False, sizeX = 0, sizeY = 0, rotation=0):
    #check if file exists
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN")
        
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")

    if(resize):
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
        
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1)
        
    inputImage.save(outputFilePath, format="BMP")
    
def ConvertToWebp(inputFilePath, outputFilePath, resize = False, sizeX = 0, sizeY = 0, rotation=0):
    #check if file exists
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN")
        
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")

    if(resize):
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
       
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1) 
        
    inputImage.save(outputFilePath, format="WEBP")
    
def ConvertToSvg(inputFilePath, outputFilePath, resize = False, sizeX = 0, sizeY = 0, rotation=0):
    #check if file exists
    if not(os.path.exists(inputFilePath)):
        return("ERR_FILE_NOT_FOUND")
    if(inputFilePath == None):
        return("ERR_INPUT_NOT_GIVEN")
        
    if(outputFilePath == ""):
        return("ERR_OUTPUT_NOT_GIVEN")
    
    print("[INFO]: Converting " + inputFilePath + " to " + outputFilePath)
    print("[INFO]: Resize = " + str(resize))
        
    #START CONVERSION
    inputImage = Image.open(fp=inputFilePath, mode="r")
    if(resize):
        newSize = int(sizeX), int(sizeY)
        inputImage = inputImage.resize(newSize)
    inputImage = inputImage.rotate(rotation, Image.NEAREST, expand = 1)
      
    # Convert the image to PNG and then to SVG
    png_data = inputImage.convert("RGBA")
    png_bytes = png_data.tobytes()
    cairosvg.svg2svg(bytestring=png_bytes, write_to=outputFilePath)
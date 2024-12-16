from PIL import Image
import os
import subprocess
import time

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

def ConvertToSvg(inputFilePath, outputFilePath, resize=False, sizeX=0, sizeY=0, rotation=0):
    try:
        if not os.path.exists(inputFilePath):
            return "ERR_FILE_NOT_FOUND"
        if not outputFilePath.endswith(".svg"):
            return "ERR_INVALID_OUTPUT_PATH"
        
        print("[INFO]: Converting" + inputFilePath + "...")

        temp_file_path = "temp.pbm"
        img = Image.open(inputFilePath)
        
        if resize or rotation != 0:
            if resize:
                img = img.resize((sizeX, sizeY))
            if rotation != 0:
                img = img.rotate(rotation, expand=True)
                
        img = img.convert("1")
        img.save(temp_file_path)

        cmd = [
            "potrace",
            temp_file_path,
            "-s",
            "-o", outputFilePath
        ]
        subprocess.run(cmd, check=True)
        
        time.sleep(5)

        if temp_file_path == "temp.pbm":
            os.remove(temp_file_path)

        print(f"[INFO]: Conversion completed: {outputFilePath}")
    
    except subprocess.CalledProcessError as e:
        print(f"[ERROR]: Failed to execure potrace\n - {e}")
        return "ERR_POTRACE_FAILED"
    except Exception as e:
        print(f"[ERROR]: Unexpected error encountered - {e}")
        return "ERR_CONVERSION_FAILED"
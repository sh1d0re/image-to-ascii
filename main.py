import os
import sys
import json

from PIL import Image
try:
    print("["+"\x1b[32;1m"+"✔︎"+"\x1b[0m"+"] Successfully imported PIL (pillow)")
except ImportError:
    if input("Would you like to install pillow? [Y/N]: ").lower() == "y":
        installations = [
            os.system("python -m pip install --upgrade pip"), 
            os.system("pip3 install pillow")
        ]
        if 1 in installations:
            print("["+"\x1b[31;1m"+"✖"+"\x1b[0m"+"] Failed to install PIL (pillow)")
        else:
            print("["+"\x1b[32;1m"+"✔︎"+"\x1b[0m"+"] Successfully installed PIL (pillow)")

try:
    config = json.load(open(os.path.expanduser("~/.config/image-to-ascii/config.json")))
except Exception as e:
    print("Using default configurations. This is caused by the following errors:\n"+str(e))

if len(sys.argv) == 1:
    print("Image-to-ascii: Provide an image file name to operate.")
    exit()

filename = str(sys.argv[1])
img = Image.open(filename)
fillCharacters = config["fillCharacters"]
maximumLengthOfAFillCharacter = max([len(i) for i in fillCharacters])
splitter = config["splitter"]
colorMode = config["colorMode"]

width, height = img.size[0], img.size[1]
imageHeightWidthRatio = (height/width)

column, lines = os.get_terminal_size()
terminalColumnLinesRatio = (lines/column)

allBrightnessWeights = {
    "BT.601": [ # Default
        0.897, # 29.9% * 3 = 89.7%
        1.761, # 58.7% * 3 = 176.1%
        0.3423 # 11.41% * 3 = 34.23%
    ],
    "BT.709-6": [
        0.6378, # 0.2126 * 3 = 0.6378
        2.1456, # 0.7152 * 3 = 2.1456
        0.2166  # 0.0722 * 3 = 0.2166
    ],
    "NoBias": [
        1, # 0.33 * 3 = 1
        1, # 0.33 * 3 = 1
        1  # 0.33 * 3 = 1
    ],
    "SmallBias": [
        0.9, # 0.3 * 3 = 0.9
        1.5, # 0.5 * 3 = 1.5
        0.6  # 0.2 * 3 = 0.6 
    ]
}

def setResolutionToFit(fitMode = "auto"):
    if fitMode == "column":
        resolution = column // (maximumLengthOfAFillCharacter + len(splitter))
    elif fitMode == "auto":
        if round((lines/height) * width) >= (column // (maximumLengthOfAFillCharacter + len(splitter))):
            resolution = column // (maximumLengthOfAFillCharacter + len(splitter))
        else:
            resolution = (lines/height) * width
    return(round(resolution))

resolution = setResolutionToFit(config["fitMode"])
heightChunkMargin = round(height / (resolution * (height/width)))
widthChunkMargin = round(width / (resolution))

def convertRGBToLuma(red, green, blue, selectedBrightnessWeights = "BT.601"): # Rec. 601 (CCIR 601)
    if type(selectedBrightnessWeights) == list:
        brightnessWeight = selectedBrightnessWeights
    elif type(selectedBrightnessWeights) == str:
        brightnessWeight = allBrightnessWeights[selectedBrightnessWeights]
    else:
        brightnessWeight = allBrightnessWeights["BT.601"]
    brightnessWeightRed, brightnessWeightGreen, brightnessWeightBlue = brightnessWeight

    luma = sum([
        brightnessWeightRed * red,
        brightnessWeightGreen * green,
        brightnessWeightBlue * blue
    ]) / 3
    return(luma)

def getChunkAverageColor(resolutionWidth, resolutionHeight):
    global heightChunkMargin, widthChunkMargin
    chunkAverage = []
    colors = [[], [], []]
    for x in range(5):
        xStartPoint = (widthChunkMargin * resolutionWidth) - 2
        for y in range(5):
            yStartPoint = (heightChunkMargin * resolutionHeight) - 2
            try:
                pixelDetail = img.getpixel((x + xStartPoint, y + yStartPoint))
                colors[0].append(pixelDetail[0]) # Red
                colors[1].append(pixelDetail[1]) # Green
                colors[2].append(pixelDetail[2]) # Blue
            except:
                pass
    if (len(colors[0])+len(colors[1])+len(colors[2])) == 0:
        chunkAverage = None
    else:
        chunkAverage = [
            round(sum(colors[0]) / len(colors[0])),
            round(sum(colors[1]) / len(colors[1])),
            round(sum(colors[2]) / len(colors[2]))
        ]
    return(chunkAverage)
    
def getChunkAverageASCII(resolutionWidth, resolutionHeight):
    global heightChunkMargin, widthChunkMargin
    colors = []
    for x in range(5):
        xStartPoint = (widthChunkMargin * resolutionWidth) - 2
        for y in range(5):
            yStartPoint = (heightChunkMargin * resolutionHeight) - 2
            try:
                pixelDetail = img.getpixel((x + xStartPoint, y + yStartPoint))
                colors.append(convertRGBToLuma(
                    red = pixelDetail[0],
                    green = pixelDetail[1],
                    blue = pixelDetail[2],
                    selectedBrightnessWeights = config["brightnessWeight"]
                ))
            except:
                pass
    if not len(colors) == 0:
        chunkAverage = round(sum(colors) / len(colors))
        return(chunkAverage)
    else:
        return(None)

# Initially print image information
initialVariables = {
    "Image Name": f"{sys.argv[1]}",
    "Image Size": f"(x: {width}, y: {height})",
    "Output Size": f"(x: {column}, y: {lines})",
    "Image Ratio": f"(1:{imageHeightWidthRatio})"
}
initialOutput = ""
for variable in initialVariables.keys():
    initialOutput += f"""\x1b[30;47;1m {variable}: \x1b[30;47m{initialVariables[variable]} """
print(initialOutput+"\x1b[0m")

fillCharactersBrightnessMargin = 255 / len(fillCharacters)
for resolutionHeight in range(round(resolution*imageHeightWidthRatio) - 1):
    resulttxt = ""
    for resolutionWidth in range(int(resolution) - 1):
        if colorMode == "False":
            chunkBrightness = getChunkAverageASCII(resolutionWidth, resolutionHeight)
            if not chunkBrightness == None:
                for e in range(len(fillCharacters)):
                    if not((fillCharactersBrightnessMargin * e) < chunkBrightness):
                        resulttxt += fillCharacters[e] + splitter
                        break
                    if e == len(fillCharacters) - 1:
                        resulttxt += fillCharacters[-1] + splitter

        elif colorMode == "True":
            chunkRGB = getChunkAverageColor(resolutionWidth, resolutionHeight)
            if not chunkRGB == None:
                resulttxt += f"\x1b[48;2;{chunkRGB[0]};{chunkRGB[1]};{chunkRGB[2]}m{fillCharacters[0] + splitter}\x1b[0m"
            
        elif colorMode == "Mixed":
            chunkRGB = getChunkAverageColor(resolutionWidth, resolutionHeight)
            if not chunkRGB == None:
                chunkBrightness = convertRGBToLuma(
                    red = chunkRGB[0],
                    green = chunkRGB[1],
                    blue = chunkRGB[2],
                    selectedBrightnessWeights = config["brightnessWeight"]
                )
                for e in range(len(fillCharacters)):
                    if not((fillCharactersBrightnessMargin * e) < chunkBrightness):
                        resulttxt += f"\x1b[48;2;{chunkRGB[0]};{chunkRGB[1]};{chunkRGB[2]}m{fillCharacters[e] + splitter}\x1b[0m"
                        break
                    if e == len(fillCharacters) - 1:
                        resulttxt += f"\x1b[48;2;{chunkRGB[0]};{chunkRGB[1]};{chunkRGB[2]}m{fillCharacters[-1] + splitter}\x1b[0m"

    print(resulttxt)
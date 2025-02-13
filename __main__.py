import os, sys, json
try:
    from PIL import Image
    print("["+"\x1b[32;1m"+"✔︎"+"\x1b[0m"+"] Successfully imported PIL (pillow)")
except ImportError:
    installations = [
        os.system("python -m pip install --upgrade pip"), 
        os.system("pip3 install pillow")
    ]
    if 1 in installations:
        print("["+"\x1b[31;1m"+"✖"+"\x1b[0m"+"] Failed to install PIL (pillow)")
    else:
        print("["+"\x1b[32;1m"+"✔︎"+"\x1b[0m"+"] Successfully installed PIL (pillow)")

filename = str(sys.argv[1])
img = Image.open(filename)
fillCharacters = ["  ", "..", ".:", ":;", ";;", "==", "**", "*$", "$$", "@@", "##"]
maximumLengthOfAFillCharacter = max([len(i) for i in fillCharacters])
splitter = " "

width, height = img.size[0], img.size[1]
imageHeightWidthRatio = (height/width)

column, lines = os.get_terminal_size()
terminalColumnLinesRatio = (column/lines)

print(f"""Image size: (x: {width}p, y: {height}p) Output size: (x: {column}, y: {lines}) """)

def setResolution():
    resolution = column // (maximumLengthOfAFillCharacter + len(splitter))
    return(int(resolution))

resolution = column // (maximumLengthOfAFillCharacter + len(splitter))
heightChunkMargin = round(height / (resolution * (height/width)))
widthChunkMargin = round(width / (resolution))

def convertRGBToLuma(red, green, blue): # Rec. 601 (CCIR 601)
    brightnessWeightRed = 0.897 # 29.9% * 3 = 89.7%
    brightnessWeightGreen = 1.761 # 58.7% * 3 = 176.1%
    brightnessWeightBlue = 0.3423 # 11.41% * 3 = 34.23%
    luma = sum([brightnessWeightRed * red,
                   brightnessWeightGreen * green,
                   brightnessWeightBlue * blue]) / 3
    return(luma)

def getChunkAverage(resolutionWidth, resolutionHeight):
    global heightChunkMargin, widthChunkMargin
    colors = []
    for x in range(5):
        xStartPoint = (widthChunkMargin * resolutionWidth) - 2
        for y in range(5):
            yStartPoint = (heightChunkMargin * resolutionHeight) - 2
            try:
                pixelDetail = img.getpixel((x + xStartPoint, y + yStartPoint))
                colors.append(convertRGBToLuma(
                    pixelDetail[0], # Red
                    pixelDetail[1], # Blue
                    pixelDetail[2]  # Green
                ))
            except:
                pass
    if not len(colors) == 0:
        chunkAverage = round(sum(colors) / len(colors))
        return(chunkAverage)
    else:
        return(None)

fillCharactersBrightnessMargin = 255 / len(fillCharacters)
for resolutionHeight in range(round(resolution*imageHeightWidthRatio) - 1):
    resulttxt = ""
    for resolutionWidth in range(int(resolution) - 1):
        chunkBrightness = getChunkAverage(resolutionWidth, resolutionHeight)
        if not chunkBrightness == None:
            for e in range(len(fillCharacters)):
                if not((fillCharactersBrightnessMargin * e) < chunkBrightness):
                    resulttxt += fillCharacters[e] + splitter
                    break
                if e == len(fillCharacters) - 1:
                    resulttxt += fillCharacters[-1] + splitter
    print(resulttxt)
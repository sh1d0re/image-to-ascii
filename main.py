import os
os.system("clear")
try:
    from PIL import Image, ImageFilter
    print("["+"\x1b[32;1m"+"✔︎"+"\x1b[0m"+"] Successfully Imported PIL import")
except ImportError:
    os.system("python -m pip install --upgrade pip")
    os.system("pip3 install Pillow")
    print("["+"\x1b[32;1m"+"+"+"\x1b[0m"+"] Installed PIL import")
filename = input("Enter File Directory (Ex. C:\Documents\photos\sample.pdf / /Users/sh1d0re/Documents/photos/sample/pdf):\n>>> ")
img = Image.open(filename)
w, h, colors, resulttxt, num, prebrightness, resolution, a, b = img.size[0], img.size[1], [], "", 0, 0, int(input("Enter Resolution (Around 160 is reccomended):\n>>> ")), 0, 0
os.system("clear")
for c in range(resolution):
    for d in range(resolution):
        a, b, prebrightness = str(int(w/resolution)*d), str(int(h/resolution)*c), prebrightness + int(img.getpixel((int(a),int(b)))[0])+int(img.getpixel((int(a),int(b)))[1])+int(img.getpixel((int(a),int(b)))[2])/3
        fillcharacters=["  ","..",".,",",,",",-","--","~~","::",":;",";;",";/","//","~~","~>",">>",">+","++","+*","**","*&","&&","$&","$$","$%","%%","%@","@@","@#","##",]
        for e in range(len(fillcharacters)):
            if prebrightness//3 <= 10*(e+1):
                resulttxt+=fillcharacters[e]
                break
        prebrightness = 0
    resulttxt+="\n"   
print(resulttxt+"\n\n=========================\nPRINTED ASCII-ART\n=========================")

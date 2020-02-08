import os
from PIL import Image
from os import listdir
from os.path import isfile, join

def resize_rename_replace(mypath, new_path, new_name, extension, file):
    imageFiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and (f.endswith("G") or f.endswith("g"))]
    #liste = os.listdir(mypath)
    target = 1000
    txt = ""


    for im in imageFiles:
        im1 = Image.open(join(mypath, im))
        originalWidth, originalHeight = im1.size
        ratio = originalWidth / originalHeight
        if ratio > 1:
            width = target
            height = int(width / ratio)
        else:
            height = target
            width = int(height * ratio)

        im2 = im1.resize((width, height), Image.ANTIALIAS)  # linear interpolation in a 2x2 environment
        im3 = im2.save(join(new_path, (new_name + str(count) + '.' + extension)))
        txt = txt + "negatives/" + str(im3) + "\n"

        print(im, "redimensionnée…")

    print("Travail terminé !", len(imageFiles), "images redimensionnées.")
    file.write(txt)


now_path = "/media/mathias/MATHIAS/negatifs"
new_path = "negatives"

file = 'negatives.txt'
fichier = open(file, "w")

resize_rename_replace(now_path, new_path, 'image', "jpg", fichier)

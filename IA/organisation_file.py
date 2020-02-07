import os
from PIL import Image
from os import listdir
from os.path import isfile, join


def resize_rename_replace(mypath, new_path, new_name, extension):
    imageFiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and (f.endswith("G") or f.endswith("g"))]
    #liste = os.listdir(mypath)
    target = 100
    count = 1


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
        im2.save(join(new_path, (new_name + str(count) + '.' + extension)))
        count += 1
        print(im, "redimensionnée…")
    print("Travail terminé !", len(imageFiles), "images redimensionnées.")


def write_txt_images(file, path):
    liste = os.listdir(path)
    os.chdir(path)
    txt = ""
    for i in range(len(liste)):
        name = liste[i]
        txt = txt + "negatives/" + str(name) + "\n"
    file.write(txt)




now_path_neg = "/media/mathias/MATHIAS/negatifs"
new_path_neg = "/home/mathias/Documents/IA/negatives"

file = '/home/mathias/Documents/IA/negatives.txt'
fichier = open(file, "w")

resize_rename_replace(now_path_neg, new_path_neg, 'image', "jpg")
write_txt_images(fichier, new_path_neg)




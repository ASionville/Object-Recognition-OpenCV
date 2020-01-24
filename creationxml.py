import urllib.request
import os
import cv2
import numpy as np

img_link = 'htpp://image_net.org/synset?wnid=n04096066'
img_url = urllib.request.urlopen(img_link).read().decode()
num = 1
if not os.path.exists('negatif'):
    os.mkdir('negatif')
for i in img_url.split('\n'):
    try:
        print(i)
        urllib.request.urlrelative(i, "negatif/" + str(num) + ".jpg")
        img = cv2.read("negatif/" + str(num) + ".jpg", cv2.IMREAD_GRAYSCALE)
        redim_img = cv2.resize (img, (100,100))
        cv2.imwrite("negatif/" + str(num) + ".jpg", redim_img)
        num = num + 1
    except Exception as e:
        print(str(e))

import cv2
from matplotlib import pyplot as plt

img = cv2.imread("imagegoogle.png")
img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

Filtre_Stop = cv2.CascadeClassifier("data/cascade.xml")

stop = Filtre_Stop.detectMultiScale(img_gris, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

n = len(stop)

if n != 0:
    for (x, y, w, h) in stop:
        cv2.rectangle(img_rgb, (x, y), (x+h, y+w), (0, 255, 0), 5)
plt.subplot(1, 1, 1)
plt.imshow(img_rgb)
plt.show()

import cv2
from matplotlib import pyplot as plt

""" Ce programme compare une image avec un fichier XML
comptant des caractéristiques dans celui-ci un panneau stop.
Ensuite le programme met on évidence les point communs
qu'il a trouve par le biais d'un triangle vert
"""
image = cv2.imread("XML/images_test/roadstop.jpg")  # On ouvre l'image
image_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # On met l'image en noir et blanc
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # On met l'image en couleur

Filtre_Stop = cv2.CascadeClassifier(
    "XML/data/cascade.xml")  # On prends notre fichier xml qui nous permet de trouvé ce que l'on cherche dans l'image

stops = Filtre_Stop.detectMultiScale(image_gris, scaleFactor=1.1, minNeighbors=50,
                                     minSize=(20, 20))  # On compare les deux images pour trouver des similitudes

n = len(stops)

if n != 0:  # s'il repere des formes identiques il lance la boucle
    for (x, y, w, h) in stops:
        cv2.rectangle(image_rgb, (x, y), (x + h, y + w), (0, 255, 0), 5)  # On encadre les similitudes trouvees
plt.subplot(1, 1, 1)  # On initialise les echelles
plt.imshow(image_rgb)  # On montre l'image en couleur
plt.show()  # On affiche le triangle sur l'image

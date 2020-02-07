# Import des librairies
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import color as colorlib
import matplotlib as mpl
import matplotlib.pyplot as plt

# Fonction pour calculer la couleur du cadre
# en fonction du % de surete (vert - rouge)
def colorFader(mix=0):
    red=np.array(mpl.colors.to_rgb('red'))
    green=np.array(mpl.colors.to_rgb('green'))
    hexcolor = mpl.colors.to_hex((1-mix)*red + mix*green) # HEX colors
    rgbcolor = mpl.colors.to_rgb(hexcolor) # RGB colors
    output = (rgbcolor[2]*255, rgbcolor[1]*255, rgbcolor[0]*255) # BGR colors
    return output

# Liste des noms utilisés par le SSD pour l'entrainement
# On les utilise pour la detection puis on les a en
# français pour l'affichage
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

FRENCH = ["Rien", "Avion", "Velo", "Oiseau", "Bateau",
	"Bouteille", "Bus", "Voiture", "Chat", "Chaise", "Vache", "Table",
	"Chien", "Cheval", "Moto", "Personne", "Plante", "Mouton", "Canape", "Train", "TV"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# On modifie l'ordre des couleurs (RGB/BGR)
for color in COLORS:
	color = color[::-2]

# Messages d'info en console
print("[INFO] Chargement du modele...")


# On recupere les donnees du modele pour la reconnaissance
prototxt = "Models/MobileNetSSD_deploy.prototxt"
model = "Models/MobileNetSSD_deploy.caffemodel"
infos = cv2.dnn.readNetFromCaffe(prototxt, model)


print("[INFO] Chargement video...")

# On demarre le flux video, le chrono et les FPS
stream = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# Boucle frame par frame
while True:
	# On redimensionne l'image a partir du flux
	frame = stream.read()
	frame = imutils.resize(frame, width=1000)

	# On converti chaque image en database binaire (blob)
	(height, width) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# On utilise le modele pour detecter des objets
	# connus dans le blob
	infos.setInput(blob)
	detections = infos.forward()

	# On boucle sur chaque objet reconnus
	for i in np.arange(0, detections.shape[2]):
		# On recupere la probabilite
		# que la prediction soit bonne
		percent_sure = detections[0, 0, i, 2]

		# On ne prend que les choses les plus sures
		if percent_sure > 0.2:

			# Pour chaque objet, on recupere le nom,
			# la position et la taille sur x et y
			objX = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
			(startX, startY, endX, endY) = box.astype("int")

			# On encadre l'objet avec la bonne couleur
			cv2.rectangle(frame, (startX, startY), (endX, endY), colorFader(percent_sure), 2)

			# Si le cadre est trop haut, le texte
			# s'ecrira dedans, sinon au dessus
			y = startY - 15 if startY - 15 > 15 else startY + 15

			# On recupere le nom en francais
			label = "{}: {:.2f}%".format(FRENCH[objX],
				round(percent_sure * 100, 2))
			# Et on l'affiche
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, colorFader(percent_sure), 2)

	# On montre l'image et on attend que
	# l'utilisateur quitte
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# Si on appuie sur 'Q',
	# On sort de la boucle
	if key == ord("q"):
		break

	# On passe à la frame suivante
	fps.update()

# A la fin, on affiche la console et
# on ecrit la duree totale et les FPS moyens
fps.stop()
print("[INFO] Delta time : {:.2f}".format(fps.elapsed()))
print("[INFO] FPS :        {:.2f}".format(fps.fps()))

# On verifie qu'on ferme bien tout
cv2.destroyAllWindows()
stream.stop()

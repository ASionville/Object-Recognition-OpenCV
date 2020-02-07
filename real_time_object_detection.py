# import the necessary packages
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

def colorFader(mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    red=np.array(mpl.colors.to_rgb('red'))
    green=np.array(mpl.colors.to_rgb('green'))
    hexcolor = mpl.colors.to_hex((1-mix)*red + mix*green)
    rgbcolor = mpl.colors.to_rgb(hexcolor)
    output = (rgbcolor[2]*255, rgbcolor[1]*255, rgbcolor[0]*255) #BGR
    return output

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

FRENCH = ["Arriere plan", "Avion", "Velo", "Oiseau", "Bateau",
	"Bouteille", "Bus", "Voiture", "Chat", "Chaise", "Vache", "Table",
	"Chien", "Cheval", "Moto", "Personne", "Plante", "Mouton", "Canape", "Train", "TV"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

for color in COLORS:
	color = color[::-2]

print(COLORS[15])
# load our serialized model from disk
print("[INFO] Chargement du modele...")

prototxt = "Models/MobileNetSSD_deploy.prototxt"
model = "Models/MobileNetSSD_deploy.caffemodel"

infos = cv2.dnn.readNetFromCaffe(prototxt, model)

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] Chargement video...")
stream = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	frame = stream.read()
	frame = imutils.resize(frame, width=1000)

	# grab the frame dimensions and convert it to a blob
	(height, width) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	infos.setInput(blob)
	detections = infos.forward()

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the percent_sure (i.e., probability) associated with
		# the prediction
		percent_sure = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `percent_sure` is
		# greater than the minimum percent_sure
		if percent_sure > 0.4:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			objX = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(FRENCH[objX],
				round(percent_sure * 100, 2))

			cv2.rectangle(frame, (startX, startY), (endX, endY),
				colorFader(percent_sure), 2)

			y = startY - 15 if startY - 15 > 15 else startY + 15

			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, colorFader(percent_sure), 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] Delta time : {:.2f}".format(fps.elapsed()))
print("[INFO] FPS :        {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
stream.stop()

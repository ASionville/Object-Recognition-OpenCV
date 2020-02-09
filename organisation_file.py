import cv2
import os
from PIL import Image
from os import listdir
from os.path import isfile, join

def prerequis(path_folderxml):
    # Creation du dossier negatives s'il n'exsite pas
    if not os.path.exists(path_folderxml + 'negatives'):
        os.mkdir(path_folderxml + 'negatives')

    # Creation du dossier data s'il n'exsite pas
    if not os.path.exists(path_folderxml + 'data'):
        os.mkdir(path_folderxml + 'data')

    # Creation du dossier info s'il n'exsite pas
    if not os.path.exists(path_folderxml + 'info'):
        os.mkdir(path_folderxml + 'info')

    # Remise à zéro du fichier negatifs.txt
    if os.path.exists(path_folderxml + 'negatives.txt'):
        with open (path_folderxml + 'negatives.txt', 'w') as f:
            f.write('')

    # Creation du fichier negatives.txt s'il n'exsite pas 
    elif not os.path.exists(path_folderxml + 'negatives.txt'):
        f = open(path_folderxml + 'negatives.txt', 'w')
        f.close()


def orga_file(path_images, path_folderxml):
    liste = listdir(path_images) # Lecture des images dans leur dossier

    #Paramétres des images à  redimensionner
    count = 1
    extension = '.jpg'
    new_name  = 'image'
    dim = (100,100)
    
    #Boucle pour appliquer les paramètres à chaque image
    for i in range(len(liste)):
        # On essaye si c'est possible d'appliquer les paramètres 
        try :
            img = cv2.imread(path_images + liste[i], cv2.IMREAD_GRAYSCALE) # Lecture de l'image avec une echelle de gris
            img_resized = cv2.resize(img, dim) # Redimensionnement de l'image en fonction des paramètres de l'image
            path_newimages = path_folderxml+"negatives/"+str(count)+extension # Chemin pour la nouvelle image redimensionnée
            img_rename = cv2.imwrite(path_newimages, img_resized) # Enregistrement de l'image redimensionner avec le chemin précedent
            with open (path_folderxml + 'negatives.txt', 'a') as f: # Ouverture du fichier negativeS.txt pour inscrire le chemin de l'image
                f.write("negatives/"+str(count)+extension+'\n') 
            print(path_newimages)

        # On affiche l'erreur s'il y en a une
        except Exception as e:
            print(str(e))

        count += 1 
    f.close()

path_images = "/media/mathias/MATHIAS/negatifs/"
path_folderxml = "/home/mathias/Documents/IA/XML/"

prerequis(path_folderxml)
orga_file(path_images, path_folderxml)


#resize_rename_replace(now_path, new_path, 'image', "jpg", fichier)
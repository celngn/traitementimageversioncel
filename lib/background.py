from PIL import Image, ImageFilter
import time
from lib.util import readImages,normalize, printProgressBar
import os

def median_images(images):
    print("----------------------  INITIALISATION DES CALCULS POUR RECUPERER LE BACKGROUND 2/4 ------------------------------------------")
    images_normalized = normalize(images)
    img_dest = Image.new("RGB", images[0].size)
    dest = img_dest.load()
    N = len(images)

    images_pixels = []
    for img in images_normalized:
        images_pixels.append(img.load())

    printProgressBar(0, images_normalized[0].size[1], prefix = 'Progress:', suffix = 'Complete', length = 50)

    for y in range (images_normalized[0].size[1]):
        for x in range (images_normalized[0].size[0]):
            rp = []                     #listes pour les valeurs des pixels
            gp = []
            bp = []
            for i in range(N):          #pour travailler sur chaque pixel de chaque img
                pix = images_pixels[i]
                r1,g1,b1 = pix[x,y]
                rp.append(r1)           #valeurs rouge de chaque img
                gp.append(g1)           #valeurs verte de chaque img
                bp.append(b1)           #valeurs bleu de chaque img
            
            rp.sort()                   #trie des listes
            gp.sort()
            bp.sort()
            dest[x,y] = rp[N//2],gp[N//2],bp[N//2]     #la valeur med de chaque couleur
        printProgressBar(y+1, images_normalized[0].size[1], prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    print("---------------------- FIN DES CALCULS POUR RECUPERER LE BACKGROUND 2/4 ------------------------------------------")
    print()
    return img_dest	

   
def get_background_and_save(path_dir):
    if not os.path.isfile(os.path.join(path_dir, "background.png")):
        images =  readImages(1, path_dir)
        background = median_images(images)
        background.save(os.path.join(path_dir, "background.png"))

        return background
    else:
        print("Le fichier 'background.png' existe déjà !")
        return Image.open(os.path.join(path_dir, "background.png"))
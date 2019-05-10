from PIL import Image, ImageFilter
from lib.util import readImages,normalize, printProgressBar
import os
MASK_TRESHOLD = 50


def create_image(color, background):
    img = Image.new("RGB",(background.size[0], background.size[1]) )
    pixels = img.load()
    width = img.size[0]
    height = img.size[1]
    for x in range(width):
        for y in range(height):
            pixels[x,y] = color
    return img
   

def get_mask_old(bkg_img, img,img_result):
   
    _images = normalize([bkg_img, img,img_result])
    bkg_pixels  = _images[0].load()
    img_pixels  = _images[1].load()
    img_result_pixels = _images[2].load()
    width = _images[0].size[0]
    height = _images[0].size[1]
    
    for x in range(width):
        for y in range(height):
            r1,g1,b1 = bkg_pixels[x,y]
            r2,g2,b2 = img_pixels[x,y]
            is_background = abs(r1-r2) < MASK_TRESHOLD and abs(g1-g2) < MASK_TRESHOLD and abs(b1-b2) < MASK_TRESHOLD 
            if not is_background:
              img_result_pixels[x,y] = (0,0,0)
   

def get_mask(bkg_img, img):
   
    mask_image  =  create_image((255,255,255), bkg_img)
    _images = normalize([bkg_img, img,mask_image])
    bkg_pixels  = _images[0].load()
    img_pixels  = _images[1].load()
    img_mask_pixels = _images[2].load()
    width = _images[0].size[0]
    height = _images[0].size[1]
    
    for x in range(width):
        for y in range(height):
            r1,g1,b1 = bkg_pixels[x,y]
            r2,g2,b2 = img_pixels[x,y]
            is_background = abs(r1-r2) < MASK_TRESHOLD and abs(g1-g2) < MASK_TRESHOLD and abs(b1-b2) < MASK_TRESHOLD 
            if not is_background:
              img_mask_pixels[x,y] = (0,0,0)

    return mask_image


   
def get_mask_and_save(path_dir, background, frame_interval):
    images = readImages(frame_interval, path_dir)
    N = len(images)
    printProgressBar(0, N, prefix = 'Progress:', suffix = 'Complete', length = 50)
    cpt = 0
    print("----------------------  INITIALISATION DES CALCULS POUR RECUPERER LE MASK 3/4 ------------------------------------------")

    for im in images:
        mask = get_mask(background, im)
        fileparts  = im.filename.split('.')
        maskFileName = fileparts[0] + '_mask.' + fileparts[1]
        mask.save(maskFileName)
        cpt += 1
        printProgressBar(cpt, N, prefix = 'Progress:', suffix = 'Complete', length = 50)

    print("----------------------  FIN DES CALCULS POUR RECUPERER LE MASK 3/4  ------------------------------------------")
    print()
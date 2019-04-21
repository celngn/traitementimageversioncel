from PIL import Image, ImageFilter
from lib.util import readImages_and_masks,normalize, extract_frames_from_video, printProgressBar
from lib.background import get_background_and_save
from lib.mask import get_mask_and_save
import os
import argparse

def binary_merge(bkg_img, item,img_result):
    _images = normalize([bkg_img,item[0],item[1],img_result])
    bkg_pixels = _images[0].load()
    img_pixels = _images[1].load()
    mask_img = _images[2].load()
    width = _images[0].size[0]
    height = _images[0].size[1]
    img_result_pixels = _images[3].load()
       
    for x in range(width):
        for y in range(height):
            r1,g1,b1 = bkg_pixels[x,y]
            r2,g2,b2 = img_pixels[x,y]
            
            if mask_img[x,y] == (0,0,0):
                img_result_pixels[x,y] = (r2,g2,b2)
       
def photosequence(frame_interval, background, tmp_folder, path_video):
    images = readImages_and_masks(frame_interval, tmp_folder)
    img_result = background
    print("----------------------  DEBUT DE LA SAUVEGARDE DE L'IMAGE FINALE 4/4 ------------------------------------------")
    N = len(images)
    printProgressBar(0, N, prefix = 'Progress:', suffix = 'Complete', length = 50)
    cpt = 0

    for item in images:
        binary_merge(background, item, img_result)
        cpt += 1
        printProgressBar(cpt, N, prefix = 'Progress:', suffix = 'Complete', length = 50)

    img_result.save("photosequence_" + os.path.splitext(os.path.basename(path_video))[0] + ".png")
    print("---------------------- IMAGE SAUVEGARDEE !  ------------------------------------------")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--video", type=str, help="Chemin du fichier vidéo")
    parser.add_argument("-fi", "--frame_interval", type=int, default=4, help="Interval des frames à prendre pour le mask")
    args = parser.parse_args()

    FRAME_INTERVAL = args.frame_interval
    if args.video is not None:
        tmp_folder = extract_frames_from_video(args.video)   #Extract frames from video with ffmpeg
        background = get_background_and_save(tmp_folder) #get background from frames and save
        get_mask_and_save(tmp_folder, background, FRAME_INTERVAL)   #get mask and save
        photosequence(FRAME_INTERVAL, background, tmp_folder, args.video)   #save photosequence in main directory
    else:
        print("Aucun fichier vidéo n'a été donnée en entrée")
        exit(1)
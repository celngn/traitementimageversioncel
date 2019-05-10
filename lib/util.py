import os
from PIL import Image, ImageFilter
import ffmpeg


def readImages(nb, path_dir):
    images = []
    tmp = os.listdir(path_dir)  
    cpt = 0
    for img_name in tmp:
        if img_name.lower().find('_mask') != -1: continue
        if img_name.lower().find('png') != -1 and cpt%nb == 0  : 
            img =  Image.open(path_dir + '/' + img_name )
            images.append(img)
        cpt += 1

    return images 

def readImages_and_masks(nb, path_dir):
    images = []
    tmp = os.listdir(path_dir)  
    cpt = 0
    for img_name in tmp:
        if img_name.lower().find('_mask') != -1: continue
        if img_name.lower().find('png') != -1 and cpt%nb == 0  : 
            img =  Image.open(path_dir + '/' + img_name )
            fileParts = img_name.split('.')
            mask_file_name = path_dir + '/' + fileParts[0] + '_mask' + '.' +  fileParts[1] 
            img_mask =  Image.open(mask_file_name )
            images.append((img,img_mask))
        cpt += 1

    return images 


def normalize(images):
    minW = images[0].size[0]
    minH = images[0].size[1]
    maxW = images[0].size[0]
    maxH = images[0].size[1] #on initialise les variables min et max aux dimensions 
    #de la premiere image pour la comparer avec les suivantes   
    for i in images:
        nvimages = []
        hauteur = []
        largeur = []
        hauteur.append(i.size[1])
        largeur.append(i.size[0]) #pas obligatoire de faire un tableau pour hauteur et largeur (inutile?!)

        if(hauteur[0] <= minH ):
            minH = hauteur[0]
        elif (hauteur[0] >= maxH):
            maxH = hauteur[0]
                
        if (largeur[0] <= minW):
            minW = largeur[0]
        elif (largeur[0] >= maxW) :
            maxW = largeur[0]

    if (minW == maxW and minH == maxH):
        return images
    
    for i in images:
        nvimages.append(crop(i, 0, 0, minH, minW))
    
    return nvimages

def extract_frames_from_video(path_video):
    print("----------------------  EXTRACTION DES FRAMES AVEC FFMPEG 1/4 ------------------------------------------")

    if not os.path.isfile(path_video):
        print("Le fichier n'a pas été trouver !")
        exit(1)
    
    if not os.path.basename(path_video).lower().endswith(('.avi', '.mp4')):
        print("Le fichier n'est pas un fichier vidéo !")
        exit(1)

    if not os.path.exists('tmp/'):
        os.mkdir('tmp')

    tmp_folder = "tmp/" + os.path.splitext(os.path.basename(path_video))[0]

    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)
    else:
        #DELETE ALL FILES IN DIRECTORY 
        for file in os.listdir(tmp_folder):
            file_path = os.path.join(tmp_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    stream = ffmpeg.input(path_video)
    stream = ffmpeg.filter(stream, 'fps', fps=5)
    stream = ffmpeg.output(stream,  os.path.join(tmp_folder, 'image-%07d.png'), format="image2")

    ffmpeg.run(stream)

    print("----------------------  FIN D'EXTRACTION DES FRAMES AVEC FFMPEG 1/4 ------------------------------------------")
    print()
    return tmp_folder

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()
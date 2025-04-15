import numpy as np
from skimage.morphology import convex_hull_image
from skimage.measure import regionprops
from skimage import filters
from skimage.measure import shannon_entropy
from skimage.util import view_as_blocks


def dimentioanlity_reduction(X_train):
    X_experiment = []
    kernel = np.ones(3)  
    pool_size = 2       

    for raw in X_train:
        
        raw = raw.flatten()
        
        for _ in range(4):  
            
            raw = np.convolve(raw, kernel, mode='valid')
            
            
            raw = np.array([max(raw[i:i + pool_size]) for i in range(0, len(raw), pool_size)])
        
        
        X_experiment.append(raw)


    X_experiment = np.array(X_experiment)
    return X_experiment


def calcul_dev(img):
    std_red = np.std(img[:,:,0])
    std_blue = np.std(img[:,:,2])
    std_green = np.std(img[:,:,1])
    mean_red = np.mean(img[:,:,0])
    mean_blue = np.mean(img[:,:,2])
    mean_green = np.mean(img[:,:,1])
    return std_red,std_green,std_blue,mean_red,mean_green,mean_blue


def calculate_ch(image):
    threshhold = filters.threshold_otsu(image)
    bin_image = image > threshhold

    props = regionprops(bin_image.astype(int))

    convex_rat = []

    for prop in props:
        cov = convex_hull_image(prop.image)
        oba = prop.area
        h_a = np.sum(cov)

        if(h_a >0):
            convex_rat.append(oba / h_a)
    
    return np.mean(convex_rat) if convex_rat else 0

def calculate_entropy_variation_rhythm(image, window_size=8):
    blocks = view_as_blocks(image, block_shape=(window_size, window_size))
    entropy_map = np.zeros(blocks.shape[:2])

    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            entropy_map[i, j] = shannon_entropy(blocks[i, j])
    
    return entropy_map
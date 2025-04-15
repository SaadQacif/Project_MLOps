import pickle
import shutil
import sys
import os
import subprocess
import image_processing as im_proc
from PIL import Image
import numpy as np
import cv2
import util
from skimage.feature import hog


DEFAULT_IMAGES_PATH = "inputs/"
DEFAULT_SEGMENTER_PATH = "C:/Users/lenovo/Desktop/projects/ml/segmentation/target/release/segrs.exe"

# Load model
encoder = pickle.load(open(f"{os.getcwd()}/bin/encoder.pkl", 'rb'))
models_by_features = pickle.load(open(f"{os.getcwd()}/bin/models_by_features.pkl", 'rb'))

# Open images
images_path = DEFAULT_IMAGES_PATH
if len(sys.argv) > 1:
    images_path = sys.argv[1]

segmenter_path = DEFAULT_SEGMENTER_PATH
if len(sys.argv) > 2:
    segmenter_path = sys.argv[2]

files = filter(lambda f: os.path.isfile(os.getcwd() + '/' + images_path +'/'+f), os.listdir(images_path))

# make a temporary working directory
try:
    os.mkdir("tmp")
except FileExistsError:
    pass

tmp_dir = f"{os.getcwd()}/tmp"
log = ""
feature_aggregate = []
names = []

for file_name in files:
    file = f"{os.getcwd()}/{images_path}/{file_name}"
    # Open the image
    with Image.open(file) as im:
        im_arr = np.asarray(im)

    # filter the image
    contours = im_proc.contour(im_arr)
    cv2.imwrite("tmp/filtered.png", contours)
    # Crop the image
    subprocess.run([segmenter_path, "tmp/filtered.png", "tmp/cropped.png", file])

    with Image.open("tmp/cropped.png") as im:
        im_arr = np.asarray(im)
    
    # CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # Convert to LAB
    lab_im = cv2.cvtColor(im_arr, cv2.COLOR_RGB2LAB)
    # Apply CLAHE to lightness channel
    lab_im[:, :, 0] = clahe.apply(lab_im[:, :, 0])
    # Convert back to RGB
    im_arr = cv2.cvtColor(lab_im, cv2.COLOR_LAB2RGB)

    # maxpool
    pass

    # Feature extract
    rgb = util.calcul_dev(im_arr)
    # fd, hog_image = hog(
    #     im_arr,
    #     orientations=8,
    #     pixels_per_cell=(16, 16),
    #     cells_per_block=(1, 1),
    #     visualize=True,
    #     channel_axis=-1,
    # )
    names.append(file_name)
    feature_aggregate.append(rgb)

    for filename in os.listdir(tmp_dir):
        file_path = os.path.join(tmp_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Predict 
predictions = encoder.inverse_transform(models_by_features['rgb'].predict(np.array(feature_aggregate)))
for i, prediction in enumerate(predictions):
    log += f"image: {names[i]}. prediction: {prediction}\n"

with open(f"{os.getcwd()}/log.txt", "w") as f:
    f.write(log)
    

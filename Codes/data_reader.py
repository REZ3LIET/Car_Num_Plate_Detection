'''
This file runs plate_detector on all Pictures in Data
'''

import os
import cv2 as cv
from tqdm import tqdm

from plate_detector import PlateDetect
from Template_1 import numPlate

path = 'Car_Num_Plate_Detection\\Data\\Pictures'
files = os.listdir(path)

file_cnt = len(files)
print('Number of images: ', file_cnt)

detector = PlateDetect(verbose=False)
detected_images = []
for i, file in (enumerate(tqdm(files))):
    img_path = os.path.join(path, file)
    img = cv.imread(img_path)
    ret, plate_num = detector.detect_plate(img)
    # ret, plate_num = numPlate(path=img_path)
    if ret:
        detected_images.append((i, plate_num))

print(detected_images)
print(len(detected_images))

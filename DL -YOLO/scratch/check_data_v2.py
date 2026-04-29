import cv2
import os
import numpy as np

path = r'd:\current project\DL -YOLO\dataset\train\Happy'
files = [f for f in os.listdir(path) if f.endswith('.jpg')]

for i in range(min(5, len(files))):
    img = cv2.imread(os.path.join(path, files[i]))
    # Check if all 3 channels are identical
    is_gray = np.all(img[:,:,0] == img[:,:,1]) and np.all(img[:,:,0] == img[:,:,2])
    print(f"File: {files[i]}, Shape: {img.shape}, Is Grayscale: {is_gray}")

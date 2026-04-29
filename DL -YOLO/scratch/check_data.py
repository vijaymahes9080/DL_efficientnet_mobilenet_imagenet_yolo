import cv2
import os

path = r'd:\current project\DL -YOLO\dataset\train\Happy'
files = [f for f in os.listdir(path) if f.endswith('.jpg')]

for i in range(min(5, len(files))):
    img = cv2.imread(os.path.join(path, files[i]))
    print(f"File: {files[i]}, Shape: {img.shape}")

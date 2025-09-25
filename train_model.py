import cv2
import os
import numpy as np

dataset_path = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
labels = []
label_id = 0
label_dict = {}

for user in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user)
    label_dict[label_id] = user
    for img_name in os.listdir(user_path):
        img_path = os.path.join(user_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(label_id)
    label_id += 1

faces = np.array(faces)
labels = np.array(labels)
recognizer.train(faces, labels)
recognizer.save("trainer.yml")

from Esrgan import super_res
from person_detection import detect_person
from age_gender_race import person_characterstics
from face_allignment_recognition import verifyFace
import numpy as np
import cv2
import gc


img_path = 'ggg.jpg'
img_path_2 = 'sr_image.png'
img_2 = cv2.imread(img_path_2)
sr = super_res(img_path)
numpy_image = np.array(sr)
sr_img = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

detected_person,detect_face,flag = detect_person(sr_img)
if flag:
    predicted_age,predicted_gender,predicted_race = person_characterstics(detect_face)
    print(predicted_age)
    print(predicted_gender)
    print(predicted_race)
    verification = verifyFace(detected_person,img_2)
    print(verification)
else:
    print("No detected persons in this image")

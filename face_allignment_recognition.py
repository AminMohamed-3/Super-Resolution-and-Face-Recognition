import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from tensorflow import keras
from keras.layers import Activation, MaxPool2D, MaxPooling2D, Dropout, Flatten, Dense, ReLU, ZeroPadding2D, \
    Convolution2D
from keras.models import Sequential
import math
from retinaface import RetinaFace as RF
import gc
import tensorflow as tf

def preprocess_image(img):
    img = np.array(img, dtype=np.float16)
    img = np.expand_dims(img, axis=0)
    img /= 127.5
    img -= 1.
    return img


img_path = '/content/gdrive/MyDrive/de_niro_2.jpg'


def face_details(img):
    Face_details = RF.detect_faces(img)
    x1, y1 = Face_details["face_1"]["landmarks"]["right_eye"]
    x2, y2 = Face_details["face_1"]["landmarks"]["left_eye"]
    a = abs(y1 - y2)  # hieght of the right angeled triangle that lies betweeen the 2 eyes
    b = abs(x1 - x2)  # width  //  //  //     //      //      //   //    //      // // //
    c = math.sqrt(a * a + b * b)

    cos_alpha = (c * c + b * b - a * a) / (2 * b * c)
    alpha = np.arccos(cos_alpha)  # in radius so we need it to be degree
    alpha = (alpha * 180) / math.pi  # the angle in degrees that we should rotate the image with
    Modified_img = Image.fromarray(img)
    Modified_img = np.array(Modified_img.rotate(alpha))
    return Modified_img


def face_recognition_model():
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(224, 224, 3)))
    model.add(Convolution2D(64, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Convolution2D(4096, (7, 7), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(4096, (1, 1), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(2622, (1, 1)))
    model.add(Flatten())
    model.add(Activation('softmax'))

    model.load_weights('weights/vgg_face_weights.h5')
    vgg_face_descriptor = keras.Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)
    return vgg_face_descriptor


def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))





def verifyFace(img1, img2):
    epsilon = 0.40
    vgg_face_descriptor = face_recognition_model()
    img1_representation = vgg_face_descriptor.predict(preprocess_image(face_details(img1)))[0, :]
    img2_representation = vgg_face_descriptor.predict(preprocess_image(face_details(img2)))[0, :]
    del vgg_face_descriptor
    tf.keras.backend.clear_session()
    gc.collect()
    cosine_similarity = findCosineDistance(img1_representation, img2_representation)
    if (cosine_similarity < epsilon):
        return "verified... they are same person"
    else:
        return "unverified! they are not same person!"
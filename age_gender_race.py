import numpy as np
import pandas as pd
from keras import Model
import tensorflow as tf
from keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Conv2DTranspose, Concatenate, Input, \
    MaxPooling2D, Dropout, Flatten, Dense, ReLU, ZeroPadding2D, Convolution2D
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import gc

races = pd.Index(['Asian', 'Black', 'Indian', 'Latino_Hispanic', 'Middle Eastern', 'White'])


def loadVggFaceModel():
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

    return model


def genderModel():
    model = loadVggFaceModel()

    base_model_output = Sequential()
    base_model_output = Convolution2D(2, (1, 1), name='predictions')(model.layers[-4].output)
    base_model_output = Flatten()(base_model_output)
    base_model_output = Activation('softmax')(base_model_output)

    gender_model = Model(inputs=model.input, outputs=base_model_output)
    gender_model.load_weights("weights/gender_model_weights.h5")
    return gender_model


def RaceModel():
    model = loadVggFaceModel()

    base_model_output = Sequential()
    base_model_output = Convolution2D(6, (1, 1), name='predictions')(model.layers[-4].output)
    base_model_output = Flatten()(base_model_output)
    base_model_output = Activation('softmax')(base_model_output)

    race_model = Model(inputs=model.input, outputs=base_model_output)
    race_model.load_weights("weights/race_model_single_batch.h5")
    return race_model


def AgeModel():
    model = loadVggFaceModel()

    base_model_output = Sequential()
    base_model_output = Convolution2D(101, (1, 1), name='predictions')(model.layers[-4].output)
    base_model_output = Flatten()(base_model_output)
    base_model_output = Activation('softmax')(base_model_output)

    age_model = Model(inputs=model.input, outputs=base_model_output)

    age_model.load_weights("weights/age_model_weights.h5")

    return age_model


def Gender_Type(gender_distribution):
    gender_index = np.argmax(gender_distribution)
    if gender_index == 0:
        gender = "F"
    else:
        gender = "M"
    return gender


def Race_Type(race_distribution):
    # Race Descriptor
    prediction_classes = []
    prediction = np.argmax(race_distribution)
    prediction_classes.append(races[prediction])
    return races[prediction]


def Age_Estimation(Age_distribution):
    # Age Descriptor
    output_indexes = np.array([i for i in range(0, 101)])
    apparent_Age = str(int(np.floor(np.sum(Age_distribution * output_indexes, axis=1))[0]))
    return apparent_Age


def preprocess_image(img):
    img = np.array(img,dtype=np.float16)
    img = np.expand_dims(img, axis=0)
    img /= 127.5
    img -= 1.
    return img


def person_characterstics(img):
    Age_model = AgeModel()
    gender_model = genderModel()
    race_model = RaceModel()
    img = preprocess_image(img)

    Age_distributions = Age_model.predict(img)
    predicted_age = Age_Estimation(Age_distributions)

    predictions = race_model.predict(img)
    predicted_race = Race_Type(predictions)

    gender_distribution = gender_model.predict(img)
    predicted_gender = Gender_Type(gender_distribution)
    tf.keras.backend.clear_session()
    del Age_model
    del race_model
    del gender_model
    gc.collect()
    return predicted_age,predicted_gender,predicted_race

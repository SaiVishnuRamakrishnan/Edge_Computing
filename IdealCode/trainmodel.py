import tensorflow
import cv2
import numpy as np
import matplotlib.pyplot as pt
import os
import random
from tqdm import tqdm


DIRECTORY = "Dataset/Training/"


CATEGORIES = ["comfort","dettol","ponds","DaburRed"]

training_data = []


IMG_SIZE = 250

#Normalisation process and dataset preparation

for category in CATEGORIES:
    path = os.path.join(DIRECTORY,category)
    class_num = CATEGORIES.index(category)
    for image in tqdm(os.listdir(path)):
        image_array = cv2.imread(os.path.join(path,image))
        new_array = cv2.resize(image_array, (IMG_SIZE, IMG_SIZE))
        training_data.append([new_array, class_num])


# print(training_data[0])

#Shuffling the classes

random.shuffle(training_data)

for i in training_data[:10]:
    print(i[1])


X = []
Y = []
# exit()


#Extracting features and lables

for feature, label in training_data:
    X.append(feature)
    Y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3)

from keras.utils import to_categorical

Y = to_categorical(Y, num_classes=4)

# Saving the data for future use
import pickle

p_out = open("X.pickle","wb")
pickle.dump(X, p_out)
p_out.close()


p_out = open("Y.pickle","wb")
pickle.dump(Y, p_out)
p_out.close()


import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from keras import optimizers
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, ZeroPadding2D
from tensorflow.keras.layers import Convolution2D, MaxPooling2D

import pickle

#Loading the data

pickle_in = open("X.pickle","rb")
X = pickle.load(pickle_in)

pickle_in = open("Y.pickle","rb")
Y = pickle.load(pickle_in)

# X = X/255.0
#---------------------------------------------------------------------------------------------------#
print(X[0].shape)
#CNN Architecture

model = Sequential()
model.add(ZeroPadding2D((1, 1), input_shape=(IMG_SIZE,IMG_SIZE,3)))

#Filteration layers

model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_1'))
model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_2'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_1'))
model.add(ZeroPadding2D((1, 1)))
model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_2'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

#Image flattening

model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))
#Output layer of 4 neurons
model.add(Dense(4))
model.add(Activation('softmax'))

#Model compilation

model.compile(loss='categorical_crossentropy',
                optimizer= 'rmsprop',
                metrics=['accuracy'])

#Running for 20 epoches

model.fit(X, Y, batch_size=10, epochs=20, validation_split=0.3)

#Saving the model
model.save('64X3-CNN-FourClass.model')

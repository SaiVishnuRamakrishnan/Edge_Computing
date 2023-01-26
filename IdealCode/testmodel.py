import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as pt
import os
import random
from tqdm import tqdm


CATEGORIES = ["Comfort","Dettol","Ponds","DaburRed"]




IMG_SIZE = 250

#Preprocessing the image

def prepare(filepath):
        image_array = cv2.imread(filepath)
        new_array = cv2.resize(image_array, (IMG_SIZE, IMG_SIZE))
        return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)  
model = tf.keras.models.load_model("64X3-CNN-FourClass.model")

#Uplod the image for prediction
prediction = model.predict([prepare('path to image')]) 
print(prediction)

#Getting the maximum probability value and printing the product class as output
a  = max(prediction[0])

print(CATEGORIES[int(list(prediction[0]).index(a))])
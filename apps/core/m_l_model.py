import tensorflow as tf
from tensorflow import keras
import numpy as np
from numpy import argmax
import PIL
from PIL import Image


def imagepredict(path):
    imd = []
    image = Image.open(path)
    image = image.resize((256, 256))
    image = image.convert(mode='L')
    # image = tf.keras.preprocessing.image.load_img(path, color_mode='grayscale',
    # target_size=(256, 256))
    image = np.array(image)
    imd.append(image)
    d = np.array(imd)
    d = d.reshape((d.shape[0], 256, 256, 1))
    d = d.astype('float')
    d = d / 255.0
    d.flatten()
    model = keras.models.load_model('static/model/model.h5')
    y = model.predict(d)
    imd.pop()
    print(imd)
    return y

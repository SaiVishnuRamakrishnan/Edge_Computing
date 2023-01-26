

#############--------------EDGE SERVER_______________############################

from flask import Flask, render_template, request, jsonify
import tensorboard
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as pt
from tqdm import tqdm
from PIL import Image
import xlrd
import io
import base64
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def process():

    #Getting the Image from Javascript
    data = request.data
    data = data[22:]

    pad = len(data)%4
    data += b"="*pad

    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(data))
    fh.close()

    #Identifying the Product

    CATEGORIES = ["Comfort","Dettol","Ponds","DaburRed"]

    IMG_SIZE = 250

    def prepare(filepath):
            image_array = cv2.imread(filepath)
            new_array = cv2.resize(image_array, (IMG_SIZE, IMG_SIZE))
            return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3) 

    model = tf.keras.models.load_model("64X3-CNN-FourClass.model")
    prediction = model.predict([prepare('./imageToSave.png')])  

    print(prediction)
    a  = max(prediction[0])

    print(CATEGORIES[int(list(prediction[0]).index(a))])
    result = CATEGORIES[int(list(prediction[0]).index(a))]


    #Generate Bill for the product

    wb = xlrd.open_workbook('./product_details.xlsx')
    sheet = wb.sheet_by_index(0) 



    for i in range(sheet.nrows): 
        if sheet.cell_value(i, 1) == result:
            cost = sheet.cell_value(i,2)
            id = sheet.cell_value(i,0)
            response = {"Cost": cost, "Id": id, "Name": result}
            print(response)
            break
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="192.168.43.36",port="5000", debug=True)
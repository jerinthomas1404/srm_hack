from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app
import random
import os
# Just disables the warning, doesn't enable AVX/FMA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.applications.resnet50 import ResNet50
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


@app.route('/')

#WEIGTHS_PATH=(/home/jayesh/Downloads/CNNmodel2.h5)
#disease_list = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 'Edema', 'Emphysema', \
                  # 'Fibrosis', 'Effusion', 'Pneumonia', 'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', \
                  # 'Hernia']

@app.route('/upload')
def upload_file2():
   return render_template('index.html')
	
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
      print(os.getcwd())
      model= load_model('CNN3.h5')
      print(os.getcwd())
      #model.load_weights(WEIGTHS_PATH, by_name=True)
      img = image.load_img(path, target_size=(224,224))
      #x = image.img_to_array(img)
      #x = np.expand_dims(x, axis=0)
      #x = preprocess_input(x)
      preds = model.predict(img)
      preds_decoded = decode_predictions(preds, top=3)[0] 
      print(decode_predictions(preds, top=3)[0])
      f.save(path)
      return render_template('uploaded.html', title='Success', predictions=preds_decoded, user_image=f.filename)


@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

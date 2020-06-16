#!/usr/bin/env python
'''
github : https://github.com/liangxiao1/mini_demos

This tool is setup a quick flask server with restapi provided for recognizing image.

'''
from flask import Flask, send_file, render_template_string
from flask_restful import Resource, Api, reqparse
import time
import tempfile
import os
import werkzeug

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

app = Flask(__name__)
api = Api(app)

TASKS = {
    'resnet50': 'check what animal in image',
}

class TasksList(Resource):
    def get(self):
        return TASKS

class IdentifyImageResNet50(Resource):
    #def get(self):
    #    return TODOS

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

        args = parse.parse_args()
        imageFile = args['file']
        if imageFile == None:
            return {'Error': "please specify image file"}
        fh, tmp_image_file = tempfile.mkstemp(suffix='_up.jpg',  dir='files', text=False)
        imageFile.save(tmp_image_file)
        img_path = tmp_image_file
        model = ResNet50(weights='imagenet')
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        print('Predicted:', decode_predictions(preds, top=3)[0])
        return {'Predicted': decode_predictions(preds, top=3)[0][0][1]}

api.add_resource(TasksList, '/ops','/')
api.add_resource(IdentifyImageResNet50, '/ops/resnet50')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5902, debug=True)
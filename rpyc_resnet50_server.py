#!/usr/bin/env python
'''
github : https://github.com/liangxiao1/mini_demos

This demo is a simple rpc server with service provided for image recognization.

'''
import rpyc
from rpyc.utils.server import ThreadedServer
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

class AWSService(rpyc.Service):
    def exposed_write(self, contents):
        with open('test.jpg', 'wb') as fh:
            #fh.write(bytes(contents,'utf-8'))
            fh.write(contents)
    def exposed_resnet50(self, img_path):
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

if __name__ == "__main__":
    server = ThreadedServer(AWSService, port = 9002)
    server.start()

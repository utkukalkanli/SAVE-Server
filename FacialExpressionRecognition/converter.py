import sys, os
import tensorflow as tf
import traceback

from os.path                    import splitext, basename

print(tf.__version__)

mod_path = "model_weights.h5"
json_path = "model.json"

def load_model(path,custom_objects={},verbose=0):
    #from tf.keras.models import model_from_json

    with open('%s' % json_path,'r') as json_file:
        model_json = json_file.read()
    model = tf.keras.models.model_from_json(model_json, custom_objects=custom_objects)
    model.load_weights('%s' % mod_path)
    if verbose: print('Loaded from %s' % mod_path)
    return model

keras_mod = load_model(mod_path)

converter = tf.lite.TFLiteConverter.from_keras_model(keras_mod)
tflite_model = converter.convert()

# Save the TF Lite model.
with tf.io.gfile.GFile('model.tflite', 'wb') as f:
    f.write(tflite_model)
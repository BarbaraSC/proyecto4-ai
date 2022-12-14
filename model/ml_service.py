import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)

# TODO
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    image_i = image.load_img(os.path.join(settings.UPLOAD_FOLDER, image_name), target_size=(224,224))
    x = image.img_to_array(image_i)    
    x_batch = np.expand_dims(x, axis=0)
    x_batch = preprocess_input(x_batch)
    predictions = model.predict(x_batch)
    pred = decode_predictions(predictions, top=1)
    
    class_name = pred[0][0][1]
    pred_probability = round(pred[0][0][2], 4)

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        q = db.brpop(settings.REDIS_QUEUE)[1]
        
        #   2. Run your ML model on the given data
        q = json.loads(q.decode('utf-8'))
        class_name, pred_probability = predict(q['image'])

        #   3. Store model prediction in a dict with the following shape:
        pred = {
            "prediction": class_name,
            "score": float(pred_probability)
            }  
    
    
        print(pred)

        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        job_id = q['id']
        db.set(job_id, json.dumps(pred))

        # TODO

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

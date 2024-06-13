from fastapi import FastAPI, UploadFile, File
import numpy as np
import uvicorn
from io import BytesIO
from PIL import Image
import tensorflow as tf

import requests

app = FastAPI()

endpoint = endpoint = "http://localhost:8501/v1/models/seed_model:predict"


CLASS_NAMES = ["100%_Good_Seeds", "50%_Good_Seeds", "75%_Good_Seeds"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"


def read_file_as_image(data)->np.ndarray:
    print
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)

):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    json_data = {
        "instances": img_batch.tolist()
    }
    response = requests.post(endpoint, json=json_data)
    prediction = response.json()["predictions"][0]
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(prediction)
    return{
        "class": predicted_class,
        "confidence": float(confidence)
    }
    


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
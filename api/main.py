## uvicorn main:app --reload

from fastapi import FastAPI

from typing import Optional
from pydantic import BaseModel
import pickle
import pandas as pd

pickle_in = open('XGBoost_model.pkl', 'rb') 
model =pickle.load(pickle_in)

def get_prediction(duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo, genre):
    x = [[duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo,genre]]
    print(x)  # Add this line to see the value of x
    df = pd.DataFrame(x, columns=['duration_ms', 'key', 'mode', 'time_signature', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo','genre'])
    model = pickle.load(open("XGBoost_model.pkl", "rb"))
    prediction = model.predict(df)
    return prediction[0]


# initiate API
app = FastAPI()

# define model for post request.
class ModelParams(BaseModel):
    duration_ms:int
    key:int
    mode:int
    time_signature:int
    acousticness :float
    danceability:float
    energy:float 
    instrumentalness:float 
    liveness: float 
    loudness: float 
    speechiness: float 
    valence: float
    tempo: float
    genre:object

@app.post("/predict")
def predict(params: ModelParams):

    pred = get_prediction(params.duration_ms,
                          params.key,
                          params.mode,
                          params.time_signature,
                          params.acousticness,
                          params.danceability,
                          params.energy,
                          params.instrumentalness,
                          params.liveness,
                          params.loudness,
                          params.speechiness,
                          params.valence,
                          params.tempo,
                          params.genre
                          )

    return float(pred)

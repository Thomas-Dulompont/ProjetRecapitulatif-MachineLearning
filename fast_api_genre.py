## uvicorn fast_api_genre:app --reload

from fastapi import FastAPI
from sklearn.preprocessing import StandardScaler
from typing import Optional
from pydantic import BaseModel
import pickle
import pandas as pd
data = pd.read_csv("analyse2.csv")
scaler = StandardScaler()
pickle_in = open('modele_genre.pickle', 'rb') 
model =pickle.load(pickle_in)



# Charger le modèle de clustering
kmeans = pickle.load(open("/home/apprenant/Bureau/Projet/Recapitulatif/modele_cluster.pickle", "rb"))

# Définir une fonction pour prédire le genre_cluster
def predict_genre_cluster(duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo):
    # Préparer les données d'entrée pour le modèle de clustering
    x = [[duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo]]
    df = pd.DataFrame(x, columns=['duration_ms', 'key', 'mode', 'time_signature', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo'])
    X_scaled = scaler.fit_transform(x)
    X_scaled = scaler.transform(df)

    # Prédire le genre_cluster
    genre_cluster = kmeans.predict(X_scaled)[0]

    return genre_cluster

def get_prediction(duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo):
    x = [[duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo,]]
    print(x)  # Add this line to see the value of x
    df = pd.DataFrame(x, columns=['duration_ms', 'key', 'mode', 'time_signature', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo'])
    model = pickle.load(open("modele_genre.pickle", "rb"))
    df["genre_cluster"]  = predict_genre_cluster(duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo)
    prediction = model.predict(df)
    return prediction[0]



#genre_codes = pd.Categorical(data['genre']).codes
#genre_labels = pd.Categorical(data['genre']).categories

# Définir une fonction de conversion qui mappe les codes de catégorie en étiquettes de genre lisibles
import pandas as pd

# Charger les données
data = pd.read_csv('analyse2.csv')

# Définir une fonction de conversion qui mappe les codes de catégorie en étiquettes de genre lisibles
genre_map = dict(enumerate(data['genre'].astype('category').cat.categories))

def get_genre_label(genre_code):
    if genre_code in genre_map:
        return genre_map[genre_code]
    else:
        print(genre_code)
        print(genre_map)
        return genre_map
        





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
                          )

    return str(get_genre_label(int(pred)))
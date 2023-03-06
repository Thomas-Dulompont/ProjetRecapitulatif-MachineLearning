#Bibliothèques de prétraitement de données
import pandas as pd
import numpy as np
from sklearn.compose import make_column_selector, make_column_transformer,ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler,PolynomialFeatures,RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold

#bibliotheques pour la modélisation
from sklearn.linear_model import Ridge,LinearRegression,Lasso, ElasticNet
import xgboost as xgb
from sklearn.dummy import DummyRegressor

#bibliotheques pour la construction de pipelines 
from sklearn.pipeline import make_pipeline,Pipeline

#bibliothèques pour l'évaluation des modèles
from sklearn.model_selection import train_test_split,GridSearchCV,learning_curve, RandomizedSearchCV, cross_val_score, KFold
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from math import sqrt
from sklearn.model_selection import cross_validate

#bibliothèque pour enregistrer le modèle
import pickle
import mlflow

#Lecture du csv 
df_music_2022= pd.read_csv('audio_features_2022_genre.csv')
print(df_music_2022.columns)

#supprimer les doublons
df_music_2022 = df_music_2022.drop_duplicates()

# df_music_2022 = df_music_2022.sample(int(len(df_music_2022)/3))


#supprimer les colonnes inutiles
columnstodrop = ["name","artists","year"]
df_music_2022_num = df_music_2022.drop(columns=columnstodrop)


#supprimer les string dans la colonne popularity
df_music_2022_num = df_music_2022_num[df_music_2022_num["popularity"] != "popularity"]



#transformation des colonnes en int ou en float
columns_int = ["popularity","duration_ms","key","mode","time_signature"]
columns_float = ["acousticness","danceability","energy","instrumentalness","liveness","loudness","speechiness","valence","tempo"]
df_music_2022_num[columns_int] = df_music_2022_num[columns_int].astype(int)
df_music_2022_num[columns_float] = df_music_2022_num[columns_float].astype(float)


# Sélection des colonnes numériques
numeric_features = ["duration_ms","key","mode","time_signature","acousticness","danceability","energy","instrumentalness","liveness","loudness","speechiness","valence","tempo"]
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Sélection des colonnes catégorielles
categorical_features = ['genre']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        # ('poly', PolynomialFeatures(degree=2, include_bias=False), numeric_features),
    ]
    )

#Préparation des données à la modélisation
X = df_music_2022_num.drop(['popularity'], axis=1)
y = df_music_2022_num['popularity']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

params = {"learning_rate":0.2, "max_depth":15, "min_child_weight":15, "subsample":0.7, "gamma":0.2, "n_estimators":200, "n_jobs":-1}


model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    # ('polynomial_features', PolynomialFeatures(degree=2)),
    ('xgbregressor', xgb.XGBRegressor(learning_rate=params["learning_rate"], max_depth=params["max_depth"], 
                                   min_child_weight=params["min_child_weight"], subsample=params["subsample"], 
                                   gamma=params["gamma"], n_estimators=params["n_estimators"],n_jobs=params["n_jobs"]))
])


# Cross-validation
scores = cross_validate(model, X_train, y_train, cv=5, scoring=['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error'], return_train_score=True)

# Entrainement du modèle
model.fit(X_train, y_train)

# Prédiction sur les données de test
y_pred = model.predict(X_test)

R2score = r2_score(y_test, y_pred)
RMSE = sqrt(mean_squared_error(y_test, y_pred))
MAE = mean_absolute_error(y_test, y_pred)

# Evaluation de la performance du modèle
print('R2 score:', r2_score(y_test, y_pred))
print('RMSE:', sqrt(mean_squared_error(y_test, y_pred)))
print('MAE:', mean_absolute_error(y_test, y_pred))

# Scores
r2_train = scores['train_r2'].mean()
r2_test = scores['test_r2'].mean()
print("R2 sur l'ensemble d'entraînement : %.4f" % r2_train)
print("R2 sur l'ensemble de test : %.4f" % r2_test)

rmse_train = sqrt(-scores['train_neg_mean_squared_error'].mean())
rmse_test = sqrt(-scores['test_neg_mean_squared_error'].mean())
print("Root Mean Squared Error (RMSE) sur l'ensemble d'entraînement : {}".format(rmse_train))
print("Root Mean Squared Error (RMSE) sur l'ensemble de test : {}".format(rmse_test))

MAE_train = -scores['train_neg_mean_absolute_error'].mean()
MAE_test = -scores['test_neg_mean_absolute_error'].mean()
print('Le score de MAE sur l\'ensemble de train : {}'.format(MAE_train))
print('Le score de MAE sur l\'ensemble de test : {}'.format(MAE_test))

# Définir le chemin de suivi MLflow
mlflow.set_tracking_uri("http://localhost:5000")



# Commencer une nouvelle exécution de MLflow
with mlflow.start_run():

    # Enregistrer les paramètres
    mlflow.log_params(params)

    # Enregistrer le modèle
    mlflow.sklearn.log_model(model, "XGBRegressor_final")

   # Enregistrer les métriques
    mlflow.log_metric("MAE", MAE)
    mlflow.log_metric("r2_score", R2score)
    mlflow.log_metric("neg_mean_squared_error",RMSE)

# Save the model to a file
with open("XGBoost_model.pkl", "wb") as file:
    pickle.dump(model, file)

# model.fit(X_train, y_train)
# importances = model.named_steps['xgbregressor'].feature_importances_
# print(importances)
# Obtenir les noms de colonnes originales après la préparation des données

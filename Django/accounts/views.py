from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import UserFormCustom, MusicSearchForm
from .fonctions import ApiSpotify
from .models import SearchHistory
import requests
import pickle 
import json


def signup_page(request):
    form = UserFormCustom()

    if request.method == 'POST':
        form = UserFormCustom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été crée avec succès !')
            return redirect('login')
            
    context = {'form':form}
    return render (request=request, template_name="accounts/signup.html", context=context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profil')

    return TemplateView.as_view(template_name='accounts/login.html')(request)


from django.contrib.auth.decorators import login_required

@login_required
def search_music(request):
    form = MusicSearchForm()
    if request.method == 'POST':
        if 'search_music' in request.POST:

            music_name = request.POST.get('music_name')
            artist_name = request.POST.get('artist_name')

            # Appel de l'API Spotify pour obtenir les informations sur la musique
            data, album_image_url, preview_url = ApiSpotify(music_name, artist_name)

            # Ajout de l'information de genre à la donnée récupérée (samba=default)
            data['genre'] = 'samba'

            # Sélection des clés d'intérêt pour la prédiction
            liste_cle = ['duration_ms', 'key', 'mode', 'time_signature', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo', 'genre']

            # Sélection des données à envoyer pour la prédiction
            data_cleaned = {cle: data[cle] for cle in liste_cle}


            response = requests.post("http://20.199.58.185:8002/predict", json=data_cleaned)
            genre = json.loads(response.text)

            data['genre'] = genre
            print(genre)

            # Envoi de la requête POST à l'API de prédiction
            response = requests.post("http://20.199.58.188:8001/predict", json=data_cleaned)
            prediction = f"{int(round(json.loads(response.text),0))}/100"

            # Enregistrement de l'historique de recherche
            search_history = SearchHistory(
                user=request.user,
                song_title=music_name,
                artist_name=artist_name,
                prediction_score=prediction,
                search_date=timezone.now()
            )

            search_history.save()

            history = SearchHistory.objects.filter(user=request.user)

            # Ajout de l'image de l'album à la variable context
            context = {'form': form, 'prediction': prediction, 'album_image_url': album_image_url, 'preview_url': preview_url, 'history' : history}

            return render(request, 'accounts/profil.html', context)
    
        elif 'delete_history' in request.POST:
            
            history = SearchHistory.objects.filter(user=request.user)
            # Suppression de l'historique de recherche
            history.delete()

            return redirect('profil')

    history = SearchHistory.objects.filter(user=request.user)
    context = {'form':form, 'history': history }

    return render(request, 'accounts/profil.html', context)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)
    
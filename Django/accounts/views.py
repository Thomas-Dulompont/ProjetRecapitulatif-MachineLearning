from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserFormCustom
import requests


def signup_page(request):
    form = UserFormCustom()
    title = 'Inscription'

    if request.method == 'POST':
        form = UserFormCustom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été crée avec succès !')
            return redirect('login')
            
    context = {'form':form, 'title': title}
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


@login_required
def search_music(request):
    if request.method == 'POST':
        music_name = request.POST.get('music_name')
        artist_name = request.POST.get('artist_name')

        # Appel de l'API de Spotify pour récupérer les informations sur la musique
        url = f'https://api.spotify.com/v1/search?q=track:{music_name}+artist:{artist_name}&type=track'
        response = requests.get(url)
        data = response.json()

        # Exemple de données que vous pouvez récupérer
        track_name = data['tracks']['items'][0]['name']
        album_name = data['tracks']['items'][0]['album']['name']
        artist_name = data['tracks']['items'][0]['artists'][0]['name']
        preview_url = data['tracks']['items'][0]['preview_url']

        # Appel de votre API pour prédire le résultat
        # Préparez les données dont vous avez besoin pour effectuer la prédiction en fonction de votre modèle de prédiction
        # prediction = mon_api_de_prediction(data)

        # Création d'un objet Search pour enregistrer les informations de recherche
        # search = Search.objects.create(
        #     user=request.user,
        #     search_text=f'{music_name} by {artist_name}',
        #     success=prediction  # Remplacez par votre prédiction
        # )

        # Exemple de renvoi des données pour les afficher dans le template
        context = {
            'track_name': track_name,
            'album_name': album_name,
            'artist_name': artist_name,
            'preview_url': preview_url,
        }

        return render(request, 'accounts/profil.html', context)

    else:
        return render(request, 'accounts/profil.html')

from django.shortcuts import render
from .forms import ApiForm
import requests
import json

def home(request):
    form = ApiForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            data = json.dumps(form.cleaned_data)
            data_dict = json.loads(data)
            
            context = {'form' : form, 'data_dict': data_dict}
            return render(request, 'home/home.html', context=context )

    context = {'form' : form}
    return render(request, 'home/home.html', context=context )
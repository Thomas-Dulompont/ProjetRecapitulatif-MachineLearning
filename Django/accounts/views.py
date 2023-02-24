from django.shortcuts import redirect, render
from .forms import UserFormCustom
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login



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
            return redirect('home')

    return TemplateView.as_view(template_name='accounts/login.html')(request)

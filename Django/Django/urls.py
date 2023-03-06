from django.contrib import admin
from django.urls import path, include


handler404 = 'accounts.views.handler404'
handler500 = 'accounts.views.handler500'
handler400 = 'accounts.views.handler400'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls'))
]


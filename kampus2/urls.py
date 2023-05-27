from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('dosen/dashboard', dosen, name='dosen'),
    path('mahasiswa/dashboard', mahasiswa, name='mahasiswa'),
    path('pageAdmin/dashboard', pageAdmin, name='pageAdmin'),
    path('mahasiswa/update', update_profile, name='update-profile'),
    path('mahasiswa/profile', view_profile, name='view-profile'),
    # profile
    path('dosen/profile', dosenProfile, name='profile'),
]

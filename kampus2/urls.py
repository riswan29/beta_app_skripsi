from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('logout/', logoutUser, name="logout"),
    path('register/', register, name='register'),
    path('dosen/dashboard', dosen, name='dosen'),
    path('mahasiswa/dashboard', mahasiswa, name='mahasiswa'),
    path('pageAdmin/dashboard', pageAdmin, name='pageAdmin'),
    # profile
    path('dosen/profile', dosenProfile, name='profile_dsn'),
    path('dosen/edit', edit_dosen_profile, name='edit-dosen'),
    path('mahasiswa/profile', mahasiswaProfile, name='profile_mhs'),
    path('mahasiswa/edit', edit_mahasiswa_profile, name='edit-mahasiswa'),
    # chatbot
    path('', include("chatbot.urls")),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

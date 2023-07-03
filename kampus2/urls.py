from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from app.views import *
from app.views import change_password

urlpatterns = [
    # admin routes
    path('admin/', admin.site.urls),
    # admin themes
    path('jet', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('login/', login, name='login'),
    path('logout/', logoutUser, name="logout"),
    path('register/', register, name='register'),
    path('dosen/dashboard', dosen, name='dosen'),
    path('mahasiswa/dashboard', mahasiswa, name='mahasiswa'),
    # chatbot
    path('', include("chatbot.urls")),
    # user profile
    path('dosen/profile', dosenProfile, name='profile_dsn'),
    path('dosen/edit', edit_dosen_profile, name='edit-dosen'),
    path('mahasiswa/profile', mahasiswaProfile, name='profile_mhs'),
    path('mahasiswa/edit', edit_mahasiswa_profile, name='edit-mahasiswa'),
    path('buat_jadwal/', buat_jadwal, name='buat_jadwal'),
    path('lihat_jadwal/<int:user_id>/', lihat_jadwal, name='lihat_jadwal'),
    path('ganti_password/', change_password, name='ganti_password'),
    path('jadwal/', lihat_jadwal, name='jadwal'),
    path('buat-tugas/', buat_tugas, name='buat_tugas'),
    # download file
    path('download/<int:tugas_id>/', download_file, name='download_file'),
    # tugas
    path('tugas/', tampil_tugas, name='tugas'),
    path('kirim-tugas/<int:tugas_id>/', kirim_tugas, name='kirim_tugas'),
    path('berhasil-kirim-tugas/<int:tampung_id>/', berhasil_kirim_tugas, name='berhasil_kirim_tugas'),
    path('halaman-tugas-dosen/', halaman_tugas_dosen, name='halaman_tugas_dosen'),




]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

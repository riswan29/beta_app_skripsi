from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLES = (
        ('mahasiswa', 'Mahasiswa'),
        ('dosen', 'Dosen'),
        ('admin', 'Admin')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    nim_nidn = models.CharField(max_length=20)


    # Tambahkan bidang profil tambahan yang Anda perlukan

    def __str__(self):
        return self.user.username

class Mahasiswa(models.Model):
    foto_profil = models.ImageField(upload_to='profile_photos/')
    nama_lengkap = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mahasiswa_profile')

    # Tambahkan bidang profil tambahan yang Anda perlukan

    def __str__(self):
        return self.nama_lengkap

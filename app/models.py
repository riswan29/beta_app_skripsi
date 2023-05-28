from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLES = (
        ('mahasiswa', 'Mahasiswa'),
        ('dosen', 'Dosen'),
        ('admin', 'Admin')
    )

    full_name= models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    nim_nidn = models.CharField(max_length=20)
    gambar = models.ImageField(upload_to='profile_images/', blank=True)
    alamat = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


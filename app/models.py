from django.db import models
from datetime import datetime
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

class Jadwal(models.Model):
    METODE_PEMBELAJARAN_CHOICES = (
        ('luring', 'Luring'),
        ('daring', 'Daring')
    )
    HARI_CHOICES = (
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
    )

    JURUSAN_CHOICES = (
        ('Teknik Informatika', 'Teknik Informatika'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Farmasi', 'Farmasi'),
        # Tambahkan pilihan jurusan lainnya sesuai kebutuhan
    )

    SEMESTER_CHOICES = (
        ('semester1', 'Semester 1'),
        ('semester2', 'Semester 2'),
        ('semester3', 'Semester 3'),
        ('semester4', 'Semester 4'),
        ('semester5', 'Semester 5'),
        ('semester6', 'Semester 6'),
        ('semester7', 'Semester 7'),
        ('semester8', 'Semester 8'),
        # Tambahkan pilihan semester lainnya sesuai kebutuhan
    )

    # dosen = models.ForeignKey(User, on_delete=models.CASCADE)
    dosen = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'dosen'})
    hari = models.CharField(max_length=10, choices=HARI_CHOICES)
    waktu = models.CharField(max_length=20)
    kode_mata_kuliah = models.CharField(max_length=20)
    nama_mata_kuliah = models.CharField(max_length=100)
    sks = models.IntegerField()
    jurusan = models.CharField(max_length=50, choices=JURUSAN_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    ruangan = models.CharField(max_length=50)
    metode_pembelajaran = models.CharField(max_length=10, choices=METODE_PEMBELAJARAN_CHOICES)

    def __str__(self):
        return self.nama_mata_kuliah

class Tugas(models.Model):
    JURUSAN_CHOICES = (
        ('Teknik Informatika', 'Teknik Informatika'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Farmasi', 'Farmasi'),
        # Tambahkan pilihan jurusan lainnya sesuai kebutuhan
    )

    SEMESTER_CHOICES = (
        ('semester1', 'Semester 1'),
        ('semester2', 'Semester 2'),
        ('semester3', 'Semester 3'),
        ('semester4', 'Semester 4'),
        ('semester5', 'Semester 5'),
        ('semester6', 'Semester 6'),
        ('semester7', 'Semester 7'),
        ('semester8', 'Semester 8'),
        # Tambahkan pilihan semester lainnya sesuai kebutuhan
    )
    nama_pengguna = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    nama_tugas = models.CharField(max_length=100)
    tanggal_dibuat = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField()
    keterangan = models.TextField(blank=True)
    file_tugas = models.FileField(upload_to='tugas_files/')
    jurusan = models.CharField(max_length=50, choices=JURUSAN_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)

    def __str__(self):
        return self.nama_tugas

import os
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

class UserProfile(models.Model):
    USER_ROLES = (
        ('mahasiswa', 'Mahasiswa'),
        ('dosen', 'Dosen'),
        ('admin', 'Admin')
    )
    JURUSAN_CHOICES = (
        ('Teknik Informatika', 'Teknik Informatika'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Farmasi', 'Farmasi'),
    )

    SEMESTER_CHOICES = (
        ('Semester 1', 'Semester 1'),
        ('Semester 2', 'Semester 2'),
        ('Semester 3', 'Semester 3'),
        ('Semester 4', 'Semester 4'),
        ('Semester 5', 'Semester 5'),
        ('Semester 6', 'Semester 6'),
        ('Semester 7', 'Semester 7'),
        ('Semester 8', 'Semester 8'),
        # Tambahkan pilihan semester lainnya sesuai kebutuhan
    )
    full_name= models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jurusan = models.CharField(max_length=50, choices=JURUSAN_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    nim_nidn = models.CharField(max_length=20)
    gambar = models.ImageField(upload_to='profile_images/', blank=True)
    alamat = models.TextField(blank=True)


    def __str__(self):
        return self.user.username

    def update_username(self, new_username):
        self.user.username = new_username
        self.user.save()

class Jadwal(models.Model):
    METODE_PEMBELAJARAN_CHOICES = (
        ('Luring', 'Luring'),
        ('Daring', 'Daring')
    )
    HARI_CHOICES = (
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
    )

    JURUSAN_CHOICES = (
        ('Teknik Informatika', 'Teknik Informatika'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Farmasi', 'Farmasi'),
    )

    SEMESTER_CHOICES = (
        ('Semester1', 'Semester 1'),
        ('Semester2', 'Semester 2'),
        ('Semester3', 'Semester 3'),
        ('Semester4', 'Semester 4'),
        ('Semester5', 'Semester 5'),
        ('Semester6', 'Semester 6'),
        ('Semester7', 'Semester 7'),
        ('Semester8', 'Semester 8'),
        # Tambahkan pilihan semester lainnya sesuai kebutuhan
    )

    # dosen = models.ForeignKey(UserProfile, on_delete=models.CASCADE,limit_choices_to={'role': 'dosen'})
    # dosen = models.ForeignKey(User, on_delete=models.CASCADE)
    dosen = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'dosen'})
    hari = models.CharField(max_length=10, choices=HARI_CHOICES)
    waktu = models.TimeField()
    waktu_selesai=models.TimeField()
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
    JENIS_CHOICES = {
        ('tugas', 'Tugas'),
        ('materi', 'Materi'),
    }
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
    jenis = models.CharField(max_length=50, choices=JENIS_CHOICES)
    tanggal_dibuat = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField()
    keterangan = models.TextField(blank=True)
    file_tugas = models.FileField(upload_to='tugas_files/')
    jurusan = models.CharField(max_length=50, choices=JURUSAN_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    


    def __str__(self):
        return self.nama_tugas
    def get_file_url(self):
        return reverse('download_file', kwargs={'tugas_id': self.id})
    def get_file_path(self):
            return os.path.join('file_tugas', str(self.file_tugas))

class TampungTugas(models.Model):
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)
    mahasiswa = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal_kirim = models.DateTimeField(auto_now_add=True)
    file_tugas = models.FileField(upload_to='tugas_files/')

    def __str__(self):
        return f"Tugas: {self.tugas.nama_tugas} - Mahasiswa: {self.mahasiswa.username}"

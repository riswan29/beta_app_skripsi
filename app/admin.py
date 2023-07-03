from django.contrib import admin
from .models import *
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role', 'nim_nidn')
    list_filter = ('role',)  # Menambahkan filter berdasarkan role
    search_fields = ('full_name', 'user__username', 'nim_nidn')  # Menambahkan kolom pencarian
    ordering = ('full_name',)
admin.site.register(UserProfile,UserProfileAdmin)

class JadwalAdmin(admin.ModelAdmin):
    list_display = ('dosen', 'nama_mata_kuliah', 'hari')
    list_filter = ('dosen', 'nama_mata_kuliah', 'hari')
admin.site.register(Jadwal, JadwalAdmin)

class TugasAdmin(admin.ModelAdmin):
    list_display = ('nama_tugas', 'nama_pengguna', 'tanggal_dibuat', 'deadline')
admin.site.register(Tugas, TugasAdmin)

admin.site.register(TampungTugas)

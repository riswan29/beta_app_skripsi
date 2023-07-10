from django import forms
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.admin import widgets

class FormLogin(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
    )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form-control'}),
    )

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES)
    jurusan = forms.ChoiceField(choices=UserProfile.JURUSAN_CHOICES)
    semester = forms.ChoiceField(choices=UserProfile.SEMESTER_CHOICES)
    nim_nidn = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','jurusan', 'semester', 'nim_nidn', 'role']

class UserProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150)  # Menambahkan field username

    class Meta:
        model = UserProfile
        fields = ['username', 'full_name', 'gambar', 'alamat']  # Menambahkan field username


class BuatJadwalForm(forms.ModelForm):
    class Meta:
        model = Jadwal
        fields = ['hari', 'waktu', 'kode_mata_kuliah', 'nama_mata_kuliah', 'sks', 'jurusan', 'semester', 'ruangan', 'metode_pembelajaran']

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class TugasForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=widgets.AdminDateWidget())
    keterangan = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Tugas
        fields = ('nama_pengguna', 'nama_tugas', 'deadline', 'keterangan', 'semester', 'jurusan', 'file_tugas')
        widgets = {}

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(TugasForm, self).__init__(*args, **kwargs)
        if current_user:
            self.fields['nama_pengguna'].queryset = UserProfile.objects.filter(user=current_user)

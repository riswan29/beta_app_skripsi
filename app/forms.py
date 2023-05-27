from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from .models import *

class FormLogin(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
    )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class':'form-control'}),
    )


class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES)
    nim_nidn = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','nim_nidn', 'role']


class MahasiswaProfileForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['foto_profil', 'nama_lengkap', 'email']

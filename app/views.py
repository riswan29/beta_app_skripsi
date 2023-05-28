from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import *
from .models import *

def login(request):
    form = FormLogin()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.role == 'mahasiswa':
            return redirect('/mahasiswa/dashboard')
        elif user_profile.role == 'dosen':
            return redirect('/dosen/dashboard')
        elif user_profile.role == 'admin':
            return redirect('/admin/dashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            # Dapatkan objek UserProfile terkait
            user_profile = UserProfile.objects.get(user=user)

            if user_profile.role == 'mahasiswa':
                return redirect('/mahasiswa/dashboard')
            elif user_profile.role == 'dosen':
                return redirect('/dosen/dashboard')
            elif user_profile.role == 'admin':
                return redirect('/pageAdmin/dashboard')

    return render(request, 'login.html', {'form':form})


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nim_nidn = form.cleaned_data['nim_nidn']
            role = form.cleaned_data['role']

            # Cek apakah username atau nim sudah terdaftar
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username sudah terdaftar.')
                return redirect('register')

            if UserProfile.objects.filter(nim_nidn=nim_nidn).exists():
                messages.error(request, 'NIM/NIDN sudah terdaftar.')
                return redirect('register')

            # Username dan nim belum terdaftar, simpan objek User dan UserProfile
            user = User.objects.create_user(username=username, password=form.cleaned_data['password1'])
            user_profile = UserProfile(user=user, role=role, nim_nidn=nim_nidn)
            user_profile.save()

            django_login(request, user)
            if role == 'mahasiswa':
                return redirect('login')
            elif role == 'dosen':
                return redirect('login')
            elif role == 'admin':
                return redirect('login')

    return render(request, 'register.html', {'form': form})

@login_required(login_url="login")
def mahasiswa(request):
    return render(request, 'mahasiswa/dashboard.html')

@login_required(login_url="login")
def dosen(request):
    return render(request, 'dosen/dashboard.html')

@login_required(login_url="login")
def pageAdmin(request):
    return render(request, 'pageAdmin/dashboard.html')


@login_required(login_url="login")
def update_profile(request):
    mahasiswa = request.user.mahasiswa

    if request.method == 'POST':
        form = MahasiswaProfileForm(request.POST, request.FILES, instance=mahasiswa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui.')
            return redirect('/mahasiswa/dashboard')
    else:
        form = MahasiswaProfileForm(instance=mahasiswa)

    return render(request, 'mahasiswa/update_profile.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect("login")

################# Profiles dosen #################

def dosenProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    # print(user_profile)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'dosen/profile.html', context)

def edit_dosen_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_dsn')
    else:
        form = UserProfileEditForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'dosen/edit_profile.html', context)

################# Profiles mahasiswa #################
def mahasiswaProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    print(user_profile)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'mahasiswa/profile.html', context)

def edit_mahasiswa_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_mhs')
    else:
        form = UserProfileEditForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'mahasiswa/edit_profile.html', context)

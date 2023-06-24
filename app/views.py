from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import *
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.urls import reverse

def login(request):
    form = FormLogin()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.role == 'mahasiswa':
            return redirect('/mahasiswa/dashboard')
        elif user_profile.role == 'dosen':
            return redirect('/dosen/dashboard')
        elif user_profile.role == 'admin':
            return redirect('/pageAdmin/dashboard')

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
                return redirect('pageAdmin')

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


def pageAdmin(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'pageAdmin/add_jadwal.html', {'form': form})

def dosenList(request):
    dosen_users = User.objects.filter(userprofile__role='dosen')
    return render(request, 'pageAdmin/dashboard.html', {'dosen_users': dosen_users})

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

@login_required
def buat_jadwal(request):
    form = BuatJadwalForm()

    if request.method == 'POST':
        form = BuatJadwalForm(request.POST)
        if form.is_valid():
            jadwal = form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            jadwal.dosen = user_profile
            jadwal.save()
            return redirect('lihat_jadwal')

    context = {
        'form': form
    }

    return render(request, 'pageAdmin/buat_jadwal.html', context)



def lihat_jadwal(request):
    # Mengambil profil pengguna yang sedang login
    user_profile = UserProfile.objects.get(user=request.user)

    # Mengambil jadwal berdasarkan pengguna (user) yang sedang login
    jadwal = Jadwal.objects.filter(dosen=user_profile)
    print(jadwal)
    context = {
        'jadwal': jadwal
    }

    return render(request, 'dosen/lihat_jadwal.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('../login/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'mahasiswa/ganti.html', {'form': form})

def buat_tugas(request):
    if request.method == 'POST':
        form = TugasForm(request.POST, request.FILES)
        if form.is_valid():
            tugas = form.save(commit=False)
            tugas.file_tugas = request.FILES['file_tugas']  # Mengambil file yang diunggah
            tugas.save()
            return redirect('dosen')  # Ubah 'nama_rute_tampilan' dengan nama rute yang sesuai
    else:
        form = TugasForm()

    context = {
        'form': form
    }

    return render(request, 'dosen/buat_tugas.html', context)

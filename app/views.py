import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import *
from .models import UserProfile


def sidebar(request):
    return render(request, 'dosen/menu.html')
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


@staff_member_required(login_url='login')  # Hanya superuser atau admin yang dapat mengakses view ini
@login_required(login_url='login')
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nim_nidn = form.cleaned_data['nim_nidn']
            role = form.cleaned_data['role']
            jurusan = form.cleaned_data['jurusan']
            semester = form.cleaned_data['semester']

            # Cek apakah username atau nim sudah terdaftar
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username sudah terdaftar.')
                return redirect('register')

            if UserProfile.objects.filter(nim_nidn=nim_nidn).exists():
                messages.error(request, 'NIM/NIDN sudah terdaftar.')
                return redirect('register')

            # Username dan nim belum terdaftar, simpan objek User dan UserProfile
            user = User.objects.create_user(username=username, password=form.cleaned_data['password1'])
            user_profile = UserProfile(user=user, role=role, nim_nidn=nim_nidn, jurusan=jurusan, semester=semester)
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
            new_username = request.POST.get('username')  # Mendapatkan username baru dari request
            user_profile.update_username(new_username)  # Memperbarui username pada UserProfile
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
            new_username = request.POST.get('username')  # Mendapatkan username baru dari request
            user_profile.update_username(new_username)  # Memperbarui username pada UserProfile

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
        form = TugasForm(request.POST, request.FILES, current_user=request.user)
        if form.is_valid():
            tugas = form.save(commit=False)
            tugas.file_tugas = request.FILES['file_tugas']
            tugas.save()
            return redirect('dosen')  # Ubah 'dosen' dengan rute yang sesuai
    else:
        form = TugasForm(current_user=request.user)

    context = {
        'form': form
    }

    return render(request, 'dosen/buat_tugas.html', context)
# download file
def download_pdf(request, tugas_id):
    tugas = get_object_or_404(Tugas, id=tugas_id)
    file_path = tugas.file_tugas.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + tugas.file_tugas.name.split('/')[-1]
        return response
def download_file(request, tugas_id):
    tugas = get_object_or_404(Tugas, id=tugas_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(tugas.file_tugas))
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

def tampil_tugas(request):
    user = request.user  # Mendapatkan pengguna yang terautentikasi
    user_profile = UserProfile.objects.get(user=user)  # Mendapatkan profil pengguna

    # Mengambil jurusan dan semester dari profil pengguna
    jurusan = user_profile.jurusan
    semester = user_profile.semester

    # Filter objek Tugas sesuai dengan jurusan dan semester pengguna
    tugas = Tugas.objects.filter(jurusan=jurusan, semester=semester)
    print(tugas)
    context = {'tugas': tugas}
    return render(request, 'mahasiswa/tampil_tugas.html', context)

def kirim_tugas(request, tugas_id):
    tugas = get_object_or_404(Tugas, id=tugas_id)

    if request.method == 'POST':
        file_tugas = request.FILES.get('file_tugas')
        # Lakukan validasi dan penyimpanan file tugas di sini

        # Buat objek TampungTugas baru
        tampung_tugas = TampungTugas.objects.create(
            tugas=tugas,
            mahasiswa=request.user,
            file_tugas=file_tugas
        )

        # Redirect ke halaman berhasil mengirim tugas
        return redirect('berhasil_kirim_tugas', tampung_id=tampung_tugas.id)

    context = {'tugas': tugas}
    return render(request, 'mahasiswa/kirim_tugas.html', context)

def berhasil_kirim_tugas(request, tampung_id):
    tampung_tugas = get_object_or_404(TampungTugas, id=tampung_id)
    context = {'tampung_tugas': tampung_tugas}
    return render(request, 'mahasiswa/berhasil_kirim_tugas.html', context)
@login_required
def halaman_tugas_dosen(request):
    user_profile = UserProfile.objects.get(user=request.user)
    tugas_dosen = Tugas.objects.filter(nama_pengguna=user_profile)
    context = {'tugas_dosen': tugas_dosen}
    return render(request, 'dosen/halaman_tugas_dosen.html', context)

def detail_tugas(request, tugas_id):
    tugas = get_object_or_404(Tugas, id=tugas_id)
    context = {'tugas': tugas}
    return render(request, 'dosen/detail_tugas.html', context)

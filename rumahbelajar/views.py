from django.shortcuts import render, redirect
from .models import Absensi, Siswa, Guru, JadwalLes, OrangTua, MataPelajaran
from .forms import AbsensiForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
import qrcode
from keuangan.models import Siswa as SiswaKeuangan, Tagihan
from django.http import HttpResponse
from io import BytesIO
from datetime import date
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from keuangan.models import PembayaranSPP, Siswa, OrangTua
from keuangan.forms import BuktiPembayaranForm
from .models import JadwalLes
from .models import Kelas


# Dekorator custom
def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group, login_url='rumahbelajar:home')  # Redirect kalau gak sesuai grup

@login_required
@group_required('Siswa')
def absensi_siswa(request, siswa_id):
    if request.user.groups.filter(name='Siswa').exists():
        siswa = get_object_or_404(Siswa, id=siswa_id)
        if request.method == 'POST':
            form = AbsensiForm(request.POST)
            if form.is_valid():
                absensi = form.save(commit=False)
                absensi.siswa = siswa
                absensi.save()
                return redirect('rumahbelajar:absensi_siswa', siswa_id=siswa.id)  # ✅ Pakai namespace dan parameter
        else:
            form = AbsensiForm()
        return render(request, 'siswa/absensi_siswa.html', {'form': form})
    else:
        return redirect('rumahbelajar:home')  # FIX: fallback redirect ke root jika 'home' tidak ada


def lihat_absensi_sendiri(request):
    # Menampilkan data absensi atau apa pun yang perlu ditampilkan
    return render(request, 'absen/lihat_absensi_siswa.html')




@login_required
def jadwal_les(request):
    jadwal = JadwalLes.objects.all()
    return render(request, 'absen/jadwal_les.html', {'jadwals': jadwal})


@login_required
@group_required('Guru')
def absen_guru(request):
    if request.user.groups.filter(name='Guru').exists():
        guru = Guru.objects.get(user=request.user)
        if request.method == 'POST':
            form = AbsensiForm(request.POST)
            if form.is_valid():
                absensi = form.save(commit=False)
                absensi.guru = guru
                absensi.save()
                return redirect('absen_guru')  # Ganti dengan nama URL kamu
        else:
            form = AbsensiForm()
        return render(request, 'guru/absen_guru.html', {'form': form})
    else:
        return redirect('rumahbelajar:home')
    
@login_required
@group_required('Guru')
def absenkan_siswa(request, siswa_id):
    siswa = Siswa.objects.get(id=siswa_id)
    Absensi.objects.create(
        siswa=siswa,
        tanggal=date.today(),
        status='Hadir',
        metode_absensi='Input Manual'
    )
    return redirect('daftar_siswa.html')

@login_required
@group_required('Guru')
def lihat_absensi_siswa(request):
    absen = Absensi.objects.all().order_by('-tanggal')
    return render(request, 'guru/absensi_siswa.html', {'absen': absen})


@login_required
@group_required('Guru')
def lihat_jadwal_guru(request):
    jadwal = JadwalLes.objects.all()
    return render(request, 'guru/jadwal.html', {'jadwal': jadwal})



@login_required
@group_required('Admin')
def dashboard_admin(request):
    semua_absen = Absensi.objects.all()
    semua_jadwal = JadwalLes.objects.all()
    return render(request, 'admin/dashboard.html', {
        'absen': semua_absen,
        'jadwal': semua_jadwal
    })
    
def redirect_dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('rumahbelajar:dashboard_admin')
    elif request.user.groups.filter(name='Guru').exists():
        return redirect('rumahbelajar:dashboard_guru')
    elif request.user.groups.filter(name='Siswa').exists():
        return redirect('rumahbelajar:dashboard_Siswa')
    elif request.user.groups.filter(name='OrangTua').exists():
        return redirect('rumahbelajar:dashboard_OrangTua')
    else:
        return redirect('rumahbelajar:home')  # Jika role tidak terdaftar
 
def dashboard_guru(request):
    context = {
        'jumlah_siswa': Siswa.objects.count(),
        'jumlah_kelas': Kelas.objects.count(),
        'jumlah_mapel': MataPelajaran.objects.count(),
    }
    return render(request, 'guru/dashboard_guru.html', context)

@login_required
@group_required('Siswa')
def dashboard_siswa(request):
    return render(request, 'siswa/dashboard_Siswa.html')

@login_required
def dashboard_orangtua(request):
    anak = get_object_or_404(Siswa, orangtua=request.user)
    total_kehadiran = Absensi.objects.filter(siswa=anak, status='Hadir').count()
    total_tagihan = Tagihan.objects.filter(siswa=anak).aggregate(sum('jumlah'))['jumlah__sum'] or 0
    status_tagihan = 'Lunas' if not Tagihan.objects.filter(siswa=anak, status='Belum Lunas').exists() else 'Belum Lunas'

    context = {
        'anak': anak,
        'total_kehadiran': total_kehadiran,
        'total_tagihan': total_tagihan,
        'status_tagihan': status_tagihan,
    }
    return render(request, 'dashboard_orangtua.html', context)

def home(request):
    return render(request, 'absensi/home.html')

def logout_view(request):
    logout(request)
    return redirect('home') 

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rumahbelajar:redirect_dashboard')  # Ganti ke halaman utama lo
        else:
            messages.error(request, 'Username atau password salah!')
    return render(request, 'absensi/login.html')  # Pastikan ada template login.html


@login_required
@group_required('OrangTua')
def dashboard_orangtua(request):
    try:
        orang_tua = request.user.keuangan_orangtua  # Make sure the related name matches your model
        siswa_list = Siswa.objects.filter(orang_tua=orang_tua)
        tagihan_list = PembayaranSPP.objects.filter(siswa__in=siswa_list)

        context = {
            'orang_tua': orang_tua,
            'siswa': siswa_list,
            'tagihan': tagihan_list,
            'form': BuktiPembayaranForm(),  # if you're using the upload form
        }

        return render(request, 'orangtua/dashboard_orangtua.html', context)

    except OrangTua.DoesNotExist:
        return redirect('rumahbelajar:home')  # or handle differently


def jadwal_les(request):
    jadwals = JadwalLes.objects.all()  # Replace with actual model query
    return render(request, 'jadwal_les.html', {'jadwals': jadwals})

# rumahbelajar/views.py
from django.shortcuts import render

def daftar_siswa(request):
    siswa_list = Siswa.objects.all()  # Mengambil semua data siswa dari database
    return render(request, 'guru/daftar_siswa.html', {'siswa_list': siswa_list})

def akademik(request):
    # Ambil data kelas dan mata pelajaran dari database
    kelas_list = Kelas.objects.all()  # atau sesuaikan dengan query yang sesuai
    
    # Render halaman akademik dengan data kelas dan mata pelajaran
    return render(request, 'guru/akademik.html', {'kelas_list': kelas_list})

def akademik_siswa_view(request):
    return render(request, 'siswa/akademik_siswa.html')

def dashboard_admin(request):
    jumlah_siswa = Siswa.objects.count()
    jumlah_kelas = Kelas.objects.count()
    jumlah_mapel = MataPelajaran.objects.count()
    
    context = {
        'jumlah_siswa': jumlah_siswa,
        'jumlah_kelas': jumlah_kelas,
        'jumlah_mapel': jumlah_mapel,
    }
    return render(request, 'admin/dashboard_admin.html', context)



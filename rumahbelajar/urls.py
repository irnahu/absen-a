from django.urls import path
from . import views
from django.conf import settings

app_name = 'rumahbelajar'

urlpatterns = [
    path('', views.home, name='home'),
    path('absensi/siswa/<int:siswa_id>/', views.absensi_siswa, name='absensi_siswa'),
    path('jadwal/', views.jadwal_les, name='jadwal_les'),
    path('absen-guru/', views.absen_guru, name='absen_guru'),
    path('absenkan_siswa/<int:siswa_id>/', views.absenkan_siswa, name='absenkan_siswa'),
    path('lihat_absensi_siswa/', views.lihat_absensi_siswa, name='lihat_absensi_siswa'),
    path('lihat_jadwal_guru/', views.lihat_jadwal_guru, name='lihat_jadwal_guru'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('logout/',  views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('dashboard/guru/', views.dashboard_guru, name='dashboard_guru'),
    path('dashboard/siswa/', views.dashboard_siswa, name='dashboard_Siswa'),
    path('dashboard/OrangTua/', views.dashboard_orangtua, name='dashboard_OrangTua'),
    path('jadwal-les/', views.jadwal_les, name='jadwal_les'),
    path('absensi/siswa/', views.absensi_siswa, name='absensi_siswa'),
    path('daftar-siswa/', views.daftar_siswa, name='daftar_siswa'),
    path('akademik/', views.akademik, name='akademik'),
    path('akademik/siswa/', views.akademik_siswa_view, name='akademik_siswa'),

 
]

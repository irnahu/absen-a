from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'keuangan'

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('siswa/', views.daftar_siswa, name='daftar_siswa'),
    path('pemasukan/', views.daftar_pemasukan, name='daftar_pemasukan'),
    path('pengeluaran/', views.daftar_pengeluaran, name='daftar_pengeluaran'),
    path('rekap/', views.rekap_keuangan, name='rekap_keuangan'),
    path('export-pembayaran-excel/', views.export_pembayaran_excel, name='export_pembayaran_excel'),
    path('dashboard-admin/pembayaran/', views.kelola_pembayaran, name='kelola_pembayaran'),
    path('siswa/tagihan/', views.tagihan_spp, name='tagihan_spp'),
    path('tagihan/', views.tagihan_orangtua, name='tagihan'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
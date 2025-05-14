from django.db import models
from django.contrib.auth.models import User


# Model untuk siswa

class OrangTua(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='keuangan_orangtua')
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_telp = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

class Presensi(models.Model):
    siswa = models.CharField(max_length=100)
    tanggal = models.DateField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.siswa} - {self.tanggal}"

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='keuangan_siswa')
    nama = models.CharField(max_length=100)
    nis = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=10)
    orang_tua = models.ForeignKey(OrangTua, on_delete=models.CASCADE, related_name='anak')

    def __str__(self):
        return f"{self.nama} ({self.nis})"

# Model untuk pemasukan
class Pemasukan(models.Model):
    JENIS_PEMASUKAN = [
        ('SPP', 'SPP'),
        ('CATERING', 'Catering'),
        ('DAFTAR_ULANG', 'Daftar Ulang'),
        ('LAINNYA', 'Lain-lain'),
    ]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    jenis = models.CharField(max_length=20, choices=JENIS_PEMASUKAN)

    def __str__(self):
        return f"{self.jenis} - {self.jumlah}"

# Model untuk pengeluaran
class Pengeluaran(models.Model):
    keterangan = models.TextField()
    tanggal = models.DateField(auto_now_add=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.keterangan} - {self.jumlah}"

# Model tagihan siswa
class Tagihan(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    bulan = models.DateField()
    spp = models.BooleanField(default=False)
    catering = models.BooleanField(default=False)
    daftar_ulang = models.BooleanField(default=False)

    def __str__(self):
        return f"Tagihan {self.siswa.nama} - {self.bulan.strftime('%B %Y')}"

# Model rekapitulasi keuangan
class RekapitulasiKeuangan(models.Model):
    bulan = models.DateField()
    total_pemasukan = models.DecimalField(max_digits=12, decimal_places=2)
    total_pengeluaran = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Rekap {self.bulan.strftime('%B %Y')}"
    
    


class PembayaranSPP(models.Model):
    BULAN_CHOICES = [
    ('01', 'Januari'),
    ('02', 'Februari'),
    ('03', 'Maret'),
    ('04', 'April'),
    ('05', 'Mei'),
    ('06', 'Juni'),
    ('07', 'Juli'),
    ('08', 'Agustus'),
    ('09', 'September'),
    ('10', 'Oktober'),
    ('11', 'November'),
    ('12', 'Desember'),

]
    
    STATUS_CHOICES = [
    ('belum lunas', 'Belum Lunas'),
    ('lunas', 'Lunas'),
]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    bulan = models.CharField(max_length=2, choices=BULAN_CHOICES)
    jumlah_bayar = models.DecimalField(max_digits=10, decimal_places=2)
    status_bayar = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum lunas')
    tanggal_bayar = models.DateField(auto_now_add=True)
    bukti_pembayaran = models.ImageField(upload_to='bukti_pembayaran/', blank=True, null=True)

    def __str__(self):
        return f"{self.siswa.nama} - {self.get_bulan_display()} - {self.status_bayar}"
    
    

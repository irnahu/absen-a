from django.db import models
from django.contrib.auth.models import User
from keuangan.models import Presensi


class OrangTua(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rumahbelajar_orangtua')
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_telp = models.CharField(max_length=15)

    def __str__(self):
        return self.nama


class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rumahbelajar_siswa')
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10)
    orang_tua = models.ForeignKey(OrangTua, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama


class Guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=15)
    mata_pelajaran = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class JadwalLes(models.Model):
    hari = models.CharField(max_length=10)
    jam = models.CharField(max_length=20)  # Pastikan ada atribut jam
    guru = models.ForeignKey('Guru', on_delete=models.CASCADE)  # Pastikan ada atribut guru
    
    def __str__(self):
        return f"{self.hari} - {self.jam}"


class Absensi(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Tidak Hadir', 'Tidak Hadir'),
    ]

    METODE_ABSEN_CHOICES = [
        ('QR Code', 'QR Code'),
        ('Input Manual', 'Input Manual'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    metode_absensi = models.CharField(max_length=30, choices=METODE_ABSEN_CHOICES)

    def __str__(self):
        if self.siswa:
            return f"Absensi Siswa - {self.siswa.nama} - {self.tanggal}"
        elif self.guru:
            return f"Absensi Guru - {self.guru.nama} - {self.tanggal}"
        return "Absensi Tidak Lengkap"

# models.py
from django.db import models

class Kelas(models.Model):
    nama = models.CharField(max_length=100)  # Nama kelas, contoh: 'Kelas 1A'
    mata_pelajaran = models.CharField(max_length=100)  # Mata pelajaran yang diajarkan, contoh: 'Matematika'

    def __str__(self):
        return f"{self.nama} - {self.mata_pelajaran}"

class MataPelajaran(models.Model):
    nama_pelajaran = models.CharField(max_length=100)
    kelas = models.ForeignKey('Kelas', on_delete=models.CASCADE)
    
def ambil_presensi_siswa():
    from keuangan.models import Presensi
    data = Presensi.objects.all()
    return data



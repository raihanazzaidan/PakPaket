from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Paket, TrackingHistory, TipeLayanan, Gudang, User

@login_required(login_url='login') # Jika belum login, lempar ke halaman login
def index(request):
    return render(request, 'tracking/master/index.html')

def addTipeLayanan(request):
    """Controller untuk menambah Tipe Layanan Baru (Khusus ADMIN)"""
    
    if request.user.role != 'ADMIN':
        messages.error(request, "Akses ditolak! Hanya Admin yang diizinkan menambah layanan.")
        return redirect('index') 

    if request.method == 'POST':
        nama_layanan = request.POST.get('namaLayanan')
        harga = request.POST.get('hargaPerKg')
        estimasi = request.POST.get('estHari')

        if TipeLayanan.objects.filter(namaLayanan__iexact=nama_layanan).exists():
            messages.error(request, f"Gagal! Layanan dengan nama '{nama_layanan}' sudah ada.")
            return render(request, 'tracking/master/layanan_form.html', {'form_data': request.POST})

        try:
            TipeLayanan.objects.create(
                namaLayanan=nama_layanan,
                hargaPerKg=float(harga),
                estHari=int(estimasi)
            )
            messages.success(request, f"Layanan '{nama_layanan}' berhasil ditambahkan!")
            
            # TODO:
            return redirect('index') 
            
        except ValueError:
            messages.error(request, "Pastikan format Harga dan Estimasi Hari berupa angka yang valid!")
            return render(request, 'tracking/master/layanan_form.html', {'form_data': request.POST})

    # 3. Tangani GET: Tampilkan Form HTML kosong
    return render(request, 'tracking/master/addLayanan.html')
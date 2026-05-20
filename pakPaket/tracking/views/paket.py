from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Paket, TrackingHistory, TipeLayanan

def cek_resi(request):
    resi = request.GET.get('resi')
    
    context = {}

    if resi:
        try:
            paket = Paket.objects.get(resi=resi)
            riwayat = paket.history.all().order_by('-timestamp')
            context['paket'] = paket
            context['riwayat'] = riwayat
        except Paket.DoesNotExist:
            context['error'] = "Paket dengan nomor resi tersebut tidak ditemukan."

    return render(request, 'tracking/paket/cek_resi.html', context)

def cek_resi_api(request, resi):
    paket = get_object_or_404(Paket, resi=resi)
    return ({
        "id": str(paket.id),
        "status": paket.status,
        "resi": paket.resi,
        "pengirim": paket.pengirim.nama,
        "penerima": paket.penerima
    })

@login_required(login_url='login')
def kirim_paket(request):    
    if request.user.role != 'CUSTOMER':
        messages.error(request, "Hanya akun Pelanggan yang dapat membuat kiriman.")
        return redirect('index')
    
    pengirim = request.user.customer_profile

    if request.method == 'POST':
        deskripsi = request.POST.get('deskripsi')
        berat = float(request.POST.get('berat'))
        dimensi = int(request.POST.get('dimensi'))
        layanan_id = request.POST.get('tipeLayanan')
        
        penerima = request.POST.get('penerima')
        alamat = request.POST.get('alamatPenerima')
        kota = request.POST.get('kotaPenerima')
        no_hp = request.POST.get('noHpPenerima')

        tipe_layanan = get_object_or_404(TipeLayanan, id=layanan_id)
        berat_hitung = berat if berat >= 1.0 else 1.0
        ongkos_kirim = berat_hitung * tipe_layanan.hargaPerKg

        paket_baru = Paket.objects.create(
            deskripsi=deskripsi,
            berat=berat,
            dimensi=dimensi,
            tipeLayanan=tipe_layanan,
            ongkosKirim=ongkos_kirim,
            pengirim=pengirim,
            penerima=penerima,
            alamatPenerima=alamat,
            kotaPenerima=kota,
            noHpPenerima=no_hp,
            status='DIKEMAS' # Status awal
        )

        # 6. Otomatis catat ke Riwayat Perjalanan (Tracking History)
        TrackingHistory.objects.create(
            paket=paket_baru,
            status='DIKEMAS',
            lokasi=pengirim.kota,
            notes="Paket telah didaftarkan ke sistem dan sedang dikemas oleh pengirim."
        )

        messages.success(request, f"Berhasil! Paket Anda telah terdaftar dengan resi: {paket_baru.resi}")
        
        # Lempar ke halaman cek resi dengan membawa parameter ID paket yang baru dibuat
        return redirect(f"/paket/cek-resi/?id={paket_baru.id}")

    # --- Bagian GET Request ---
    # Tampilkan daftar layanan aktif agar bisa dipilih di Dropdown HTML
    daftar_layanan = TipeLayanan.objects.all()
    return render(request, 'tracking/paket/kirim_paket.html', {
        'daftar_layanan': daftar_layanan
    })

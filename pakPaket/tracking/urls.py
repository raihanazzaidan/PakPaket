from django.urls import path
from .views import paket, master, auth

urlpatterns = [
    path('', master.index, name='index'),
    
    # URL Paket
    path('paket/cek-resi/', paket.cek_resi, name='cek_resi_publik'),
    path('api/paket/<uuid:paket_id>/', paket.cek_resi_api, name='api_paket'),
    path('paket/kirim/', paket.kirim_paket, name='kirim_paket'),

    # URL Auth
    path('login/', auth.loginView, name='login'),
    path('logout/', auth.logoutView, name='logout'),
    path('register/', auth.customerRegister, name='register'),
    path('adm/register/', auth.adminRegister, name='admin_register'),

    # URL Master 
    path('layanan/add/', master.addTipeLayanan, name='tambah_layanan'),

]
from fitur_manage.tambah_barang import tambah_barang
from fitur_manage.hapus_barang import hapus_barang
from fitur_manage.get_daftar_barang import get_barang
from fitur_manage.update_stok import update_barang
from auth.login import login 
from auth.registrasi import registrasi
from fastapi import FastAPI

app=FastAPI()

@app.get('/data_barang')
def get_brg():
    return get_barang()

@app.post('/data_barang')
def tambah_brg(nama_barang:str,harga_barang:float,stok_barang:int):
    return tambah_barang(nama_barang,harga_barang,stok_barang)

@app.put('/data_barang')
def update_brg(nama_barang:str,harga_barang:float=None,stok_barang:int=None):
    return update_barang(nama_barang,harga_barang,stok_barang)

@app.delete('/data_barang')
def hapus_brg(nama_barang:str):
    return hapus_barang(nama_barang)

@app.post('/data_karyawan')
def registt(username:str,password:str):
    return registrasi(username,password)

@app.post('/data_karyawann')
def logg(username:str,password:str):
    return login(username,password)



from DB.db_setup import get_db, Barang

def update_barang(nama_barang:str,harga_barang:float,stok_barang:int):

    if nama_barang is None or str(nama_barang).strip() == "":
        return {"status": "error", "pesan": "nama_barang tidak boleh kosong."}

    if harga_barang is not None and harga_barang<=0:
        return {"status":"error","pesan":"input harga barang error"}

    if stok_barang is not None and stok_barang<=0:
        return {"status":"error","pesan":"input stok barang error"}

    session=get_db()
    barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
    if not barang:
        return {"status":"error","pesan":"barang tidak ditemukan"}


    if harga_barang is not None or stok_barang is not None:
            
        try:
            if harga_barang is not None and stok_barang is not None:
                if harga_barang == barang.harga_barang:
                    return {"status": "error", "pesan": "Gagal mengupdate data: harga barang sama dengan sebelumnya"}
                
                if stok_barang == barang.stok_barang:
                     return {"status": "error", "pesan": "Gagal mengupdate data: stok barang sama dengan sebelumnya"}
                
                barang.harga_barang=harga_barang
                barang.stok_barang=stok_barang

            elif harga_barang is not None:
                if harga_barang == barang.harga_barang:
                    return {"status": "error", "pesan": f"Gagal mengupdate data: harga barang sama dengan sebelumnya"}
                
                barang.harga_barang=harga_barang

            elif stok_barang is not None:
                if stok_barang == barang.stok_barang:
                    return {"status": "error", "pesan": "Gagal mengupdate data: stok barang sama dengan sebelumnya"}
                                
                barang.stok_barang=stok_barang

            session.commit()
            session.close()

            return {
                        "status": "sukses",
                        "pesan": f"Barang '{nama_barang}' berhasil diupdate.",
                        "data": {
                            "nama_barang": nama_barang,
                            "harga_barang": harga_barang,
                            "stok_barang": stok_barang,
                        },
                    }

        except Exception as e:
            session.rollback()
            return {"status": "error", "pesan": f"Gagal mengupdate data: {str(e)}"}

    

        


        

    

    

    
            

    
        
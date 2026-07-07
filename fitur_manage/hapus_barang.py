from DB.db_setup import get_db,Barang


def hapus_barang(nama_barang):

    if nama_barang is None or str(nama_barang).strip() == "":
            return {"status": "error", "pesan": "nama_barang tidak boleh kosong."}

    session=get_db()
    try:
        barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
        if not barang:
            if not barang:
                return {"status": "error", "pesan": f"{nama_barang} tidak ditemukan"}
        session.delete(barang)
        session.commit()

        return {
                    "status": "sukses",
                    "pesan": f"Barang '{nama_barang}' berhasil dihapus.",
                    "data": {
                        "nama_barang": barang.nama_barang,
                        "harga_barang": barang.harga_barang,
                        "stok_barang": barang.stok_barang,
                    },
                }

    except Exception as e:
        session.rollback()
        return{f"status":"error","pesan":f"gagal menghapus data {str(e)}"}

    finally:
        session.close()
    
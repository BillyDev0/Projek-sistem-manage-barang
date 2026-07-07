from DB.db_setup import Barang,get_db
from chatbot.tanya_ai import logging


def cek_stok_menipis(stok_max:int=100):
    session=get_db()
    try:
        if stok_max:
            cek_stok=session.query(Barang).filter(Barang.stok_barang<=stok_max).all()
            if not cek_stok:
                return {"status": "safe", "pesan": "stok barang aman"}

            return {
                    "status": "warning",
                    "pesan": f"{len(cek_stok)} barang stoknya menipis.",
                    "data": [{
                        "nama_barang": i.nama_barang,
                        "harga_barang": i.harga_barang,
                        "stok_barang": i.stok_barang,
                    }for i in cek_stok],
                }

    except Exception as e:
        logging.exception("gagal cek stok barang")
        return {"status":"error","pesan":f"gagal mengecek stok barang:{str(e)}"}

    finally:
        session.close()
    
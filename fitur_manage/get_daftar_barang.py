from DB.db_setup import get_db,Barang

def get_barang():
    session=get_db()
    data=session.query(Barang).all()
    if not data:
        return {'msg':'Data belum ada'}
    session.close()
    return "\n".join([f"nama_barang: {barang.nama_barang}, harga_barang: {barang.harga_barang}, stok_barang: {barang.stok_barang}"
            for barang in data])
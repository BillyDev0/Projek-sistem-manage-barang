from DB.db_setup import get_db,Barang

def tambah_stok(nama_barang:str,stok_tambahan:int):
    session=get_db()
    try:
        barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
        barang.stok_barang=barang.stok_barang+stok_tambahan
        session.commit()

        return {
                "status": "sukses",
                "pesan": f"Barang '{nama_barang}' berhasil menambah stok sebanyak {stok_tambahan}.",
                "data": {
                    "nama_barang": nama_barang,
                    "harga_barang": barang.harga_barang,
                    "stok_barang": barang.stok_barang,
                },
            }
    except Exception as e:
        return {"status":"error","pesan":f"gagal menambah stok barang: {str(e)}"}

    finally:
        session.close()

def diskon(min_stok:int=None,nama_barang:str=None,besar_diskon:float=20):
    session=get_db()
    try:
        if besar_diskon <=0:
            return {"status": "error", "pesan": f"'{besar_diskon}' diskon tidak valid"}
        
        if nama_barang is None and min_stok is None:
            return {"status": "error", "pesan": f"informasi barang tidak valid"}


        query=session.query(Barang)
        if nama_barang is not None:
            query=query.filter(Barang.nama_barang==(f"%{nama_barang}%"))

        if min_stok is not None:
            query=query.filter(Barang.stok_barang>=min_stok)

        barang=query.all()
        for i in barang:
            diskon=i.harga_barang*(besar_diskon/100)
            i.harga_barang=i.harga_barang-diskon
        session.commit()

        return {
                "status": "sukses",
                "pesan": f"berhasil menerapkan diskon sebesar {besar_diskon}%.",
                "data": [{
                    "nama_barang": i.nama_barang,
                    "harga_barang": i.harga_barang,
                    "stok_barang": i.stok_barang,
                    }for i in barang],
                }
    except Exception as e:
        session.rollback()
        return{'status':'error','pesan':f'diskon gagal diterapkan: {str(e)}'}

    finally:
        session.close()
    

    
        

    
        
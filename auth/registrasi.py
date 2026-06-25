from DB.db_setup import get_db,Karyawan
from passlib.hash import bcrypt


def registrasi(username: str, password: str):

    # ── Validasi kosong / None ────────────────────────────────────────────────
    if username is None or str(username).strip() == "":
        return {"status": "error", "pesan": "Username tidak boleh kosong."}

    if password is None or str(password).strip() == "":
        return {"status": "error", "pesan": "Password tidak boleh kosong."}

    if len(password) < 8:
        return {"status": "error", "pesan": "Password harus lebih dari 8 karakter."}
    
    username = username.strip()
    password = password.strip()

    # ── Cek username sudah terdaftar atau belum ───────────────────────────────
    session=get_db()
    try:
        sudah_ada = session.query(Karyawan).filter_by(username=username).first()

        if sudah_ada:
            return {"status": "error", "pesan": f"Username '{username}' sudah terdaftar."}

        # ── Hash Password ────────────────────────────────────────────────
        hashed_password=bcrypt.hash(password)

        # ── Tambah ke database ────────────────────────────────────────────────
        karyawan_baru = Karyawan(username=username, password=hashed_password)
        session.add(karyawan_baru)
        session.commit()
        session.refresh(karyawan_baru)

        return {
            "status": "sukses",
            "pesan": f"Karyawan '{username}' berhasil didaftarkan.",
            "data": {
                "username": karyawan_baru.username,
                "password": password
            },
        }

    except Exception as e:
        session.rollback()
        return {"status": "error", "pesan": f"Gagal menyimpan data: {str(e)}"}

    finally:
        session.close()
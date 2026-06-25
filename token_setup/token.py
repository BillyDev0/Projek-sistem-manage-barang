from jose import jwt,JWTError
from datetime import datetime,timedelta
from DB.db_setup import get_db, Karyawan
import secrets

SECRET_KEY=secrets.token_hex(32)
ALGORITHM="HS256"

def create_token(username):
    payload={
        "username":username,
        "exp":datetime.utcnow() + timedelta(hours=1)
    }

    try:
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return token
        
    except JWTError as e:
        return {"status": "error", "pesan": f"Gagal membuat token {str(e)}"}

def verify_token(token):
    try:
        session=get_db()
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        karyawan=session.query(Karyawan).filter(Karyawan.username==payload['username'])
        session.close()
        if not karyawan:
            return None
        return payload['username']
        
    except JWTError:
        return None
        
        

    

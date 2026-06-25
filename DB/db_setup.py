from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

url='sqlite:///DB/database.db'
engine=create_engine(url)
session_lokal=sessionmaker(bind=engine)
base=declarative_base()

def get_db():
    return session_lokal()

class Barang(base):
    __tablename__='data_barang'

    nama_barang=Column(String,primary_key=True)
    harga_barang=Column(Integer)
    stok_barang=Column(Integer)

class Karyawan(base):
    __tablename__='data_karyawan'

    username=Column(String,primary_key=True)
    password=Column(String)

base.metadata.create_all(engine)
import requests
from fitur_manage.get_daftar_barang import get_barang
from fitur_manage.hapus_barang import hapus_barang
from fitur_manage.tambah_barang import tambah_barang
from fitur_manage.update_stok import update_barang
import json
from DB.history_manage import save_history,get_history
from fitur_manage.manage_stok_harga import tambah_stok,diskon
from fitur_manage.batas_stok import cek_stok_menipis
import logging
from logger_config import *

logger = logging.getLogger(__name__)

AI_server="http://localhost:11434/api/generate"

def jawab_chat(prompt):
    prompt = f"""Kamu adalah asisten toko yang ramah dan helpful. 
    Jawab pertanyaan atau sapaan user berikut dengan singkat dan natural dalam bahasa Indonesia.

    prompt user: {prompt}
"""
    payload={
        "model":"qwen2.5:7b",
        "prompt":prompt,
        "stream":False,
        "options":{
            "temperature":0.3,
            "num_predict":150,
            "top_p":0.5
        }
    }

    try:
        res=requests.post(AI_server,json=payload)
        jawaban=res.json()['response']
        return jawaban

    except requests.exceptions.ConnectionError:
        return{f"status":"error","pesan":f"server ollama belum dijalankan"}
    


def tanya_ai(username,prompt):
    logger.info(f"username {username} mengirim prompt {prompt}")
    
    history=get_history(username)
    message = f"""Ubah kalimat user menjadi JSON. Balas HANYA JSON mentah (mulai {{ akhir }}), tanpa markdown/penjelasan.

Input: {prompt}
Konteks (jika relevan): {history}

ATURAN:
- Pilih action paling sesuai
- Semua nilai WAJIB dari INPUT USER, jangan mengarang, jangan pakai isi contoh
- Field yang tidak disebutkan user: JANGAN disertakan

ACTION:
1. tambah_barang — nambah barang baru
   "Tambah indomie, harga 3500, stok 100" -> {{"action":"tambah_barang","nama_barang":"indomie","harga_barang":3500,"stok_barang":100}}

2. update_barang — ubah harga/stok (boleh salah satu atau keduanya)
   "Ubah harga indomie 3500 dan stoknya 50" -> {{"action":"update_barang","nama_barang":"indomie","harga_barang":3500,"stok_barang":50}}
   "update harga indomie jadi 4000" -> {{"action":"update_barang","nama_barang":"indomie","harga_barang":4000}}
   "update stok indomie jadi 50" -> {{"action":"update_barang","nama_barang":"indomie","stok_barang":50}}
   
3. get_barang — lihat/cari barang (nama_barang opsional)
   "Cari indomie" -> {{"action":"get_barang","nama_barang":"indomie"}}
   "tampilkan semua barang" -> {{"action":"get_barang"}}
   "cari barang dengan harga dibawah 50000 dan diatas 25000" -> {{"action":"get_barang","max_harga":50000,"min_harga":25000}}
   "cari barang dengan harga dibawah 50000" -> {{"action":"get_barang","max_harga":50000}}
   "cari barang dengan harga diatas 40000" -> {{"action":"get_barang","min_harga":40000}}
   
4. hapus_barang — hapus barang
   "Hapus indomie" -> {{"action":"hapus_barang","nama_barang":"indomie"}}

5. tambah_stok — tambah stok barang
   "untuk kopi, tambah stok nya 20" -> {{"action":"tambah_stok","nama_barang":"kopi","stok_tambahan":20}}

6. diskon_barang — berikan diskon pada barang
   "berikan diskon 20% pada susu" -> {{"action":"diskon_barang","nama_barang":"susu","besar_diskon":20}}
   "berikan diskon 20% pada barang yang stoknya lebih dari 100" -> {{"action":"diskon_barang","min_stok":100,"besar_diskon":20}}
   "berikan diskon 10% pada susu yang stoknya diatas 50" -> {{"action":"diskon_barang","min_stok":50,"nama_barang":"susu","besar_diskon":10}}

7. cek_stok_barang — cari barang yang stoknya kurang dari batas stok
   "cari barang yang stoknya dibawah 10" -> {{"action":"cek_stok_barang","max_stok":10}}

8. chat — di luar topik barang (salam, tanya umum, dll)
   "Halo" -> {{"action":"chat","message":"Halo"}}

JSON:"""
    
    payload={
        "model":"qwen2.5:7b",
        "prompt":message,
        "stream":False,
        "options":{
            "temperature":0,
            "num_predict":80,
            "top_p":0.5
        }
    }

    try:
        save_history(username,"User",prompt)
        res=requests.post(AI_server,json=payload)
        if res.status_code!=200:
            return res.text
        text=res.json()['response']
        text=text.replace("```json","")
        jawaban=text.replace("```","").strip()
        logger.info({f"output AI to function: {jawaban}"})

        data=json.loads(jawaban)
        if data["action"]=="tambah_barang":
            jawaban = tambah_barang(
                data["nama_barang"],
                data["harga_barang"],
                data["stok_barang"]
            )
            logger.info(f"mengirim request ke func tambah_barang")
    
        elif data["action"]=="hapus_barang":
            jawaban = hapus_barang(
                data["nama_barang"]
            )
            logger.info(f"mengirim request ke func hapus_barang")
    
        elif data["action"]=="update_barang":
            jawaban = update_barang(
                data["nama_barang"],
                data.get("harga_barang"),
                data.get("stok_barang")
            )
            logger.info(f"mengirim request ke func update_barang")
    
        elif data["action"]=="get_barang":
            jawaban = get_barang(data.get("nama_barang"),
                                 data.get("max_harga"),
                                 data.get("min_harga"))
            logger.info(f"mengirim request ke func tambah_barang")

        elif data["action"]=="tambah_stok":
            jawaban = tambah_stok(
                data["nama_barang"],
                data["stok_tambahan"])
            logger.info(f"mengirim request ke func tambah_stok")
            
        elif data["action"]=="diskon_barang":
            jawaban = diskon(data.get("min_stok"),
                             data.get("nama_barang"),
                             data["besar_diskon"])
            logger.info(f"mengirim request ke func diskon_barang")

        elif data["action"]=="cek_stok_barang":
            jawaban = cek_stok_menipis(data["max_stok"])
            logger.info(f"mengirim request ke func cek_stok")
            
        elif data["action"] == "chat":
            jawaban = jawab_chat(data['message'])
            logger.info(f"mengirim request ke func chat")

        else:
            jawaban = {'msg':'action tidak diketahui'}
            logger.warning(f"action tidak diketahui")

        save_history(username,"AI",json.dumps(jawaban))
        return jawaban

    except Exception as e:
        logger.exception(f"Error tidak terduga: {str(e)}")
        return {"status": "error", "pesan": "terjadi kesalahan pada sistem"}







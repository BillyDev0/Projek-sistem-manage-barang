import requests
from fitur_manage.get_daftar_barang import get_barang
from fitur_manage.hapus_barang import hapus_barang
from fitur_manage.tambah_barang import tambah_barang
from fitur_manage.update_stok import update_barang
import json
from DB.history_manage import save_history,get_history

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

3. get_barang — lihat/cari barang (nama_barang opsional)
   "Cari indomie" -> {{"action":"get_barang","nama_barang":"indomie"}}

4. hapus_barang — hapus barang
   "Hapus indomie" -> {{"action":"hapus_barang","nama_barang":"indomie"}}

5. chat — di luar topik barang (salam, tanya umum, dll)
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

        data=json.loads(jawaban)
        if data["action"]=="tambah_barang":
            jawaban = tambah_barang(
                data["nama_barang"],
                data["harga_barang"],
                data["stok_barang"]
            )
    
        elif data["action"]=="hapus_barang":
            jawaban = hapus_barang(
                data["nama_barang"]
            )
    
        elif data["action"]=="update_barang":
            jawaban = update_barang(
                data["nama_barang"],
                data.get("harga_barang"),
                data.get("stok_barang")
            )
    
        elif data["action"]=="get_barang":
            jawaban = get_barang()
    
        elif data["action"] == "chat":
            jawaban = jawab_chat(data['message'])

        else:
            jawaban = {'msg':'action tidak diketahui'}

        save_history(username,"AI",json.dumps(jawaban))
        return jawaban
    
    except requests.exceptions.ConnectionError:
        return{f"status":"error","pesan":f"server ollama belum dijalankan"}







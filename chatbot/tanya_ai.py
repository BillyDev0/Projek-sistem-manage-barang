import requests
from fitur_manage.get_daftar_barang import get_barang
from fitur_manage.hapus_barang import hapus_barang
from fitur_manage.tambah_barang import tambah_barang
from fitur_manage.update_stok import update_barang
import json
from DB.history_manage import save_history,get_history

AI_server="http://localhost:11434/api/generate"

def tanya_ai(username,prompt):
    history=get_history(username)
    message = f"""
Ubah kalimat berikut menjadi JSON.

Input:
{prompt}

gunakan konteks ini jika relevan:
{history}

ATURAN:
- Balas HANYA JSON mentah, tanpa markdown, tanpa penjelasan
- Karakter pertama HARUS {{ dan karakter terakhir HARUS }}
- Pilih action yang PALING SESUAI dengan maksud user
- Isi field sesuai apa yang disebutkan user, jangan mengarang nilai
- SEMUA nilai (nama_barang, harga_barang, stok_barang, message) WAJIB diambil dari INPUT USER, BUKAN dari contoh
- Contoh di bawah HANYA untuk menunjukkan FORMAT, bukan isi
- Jika suatu nilai tidak disebutkan user, JANGAN sertakan field tersebut sama sekali


DAFTAR ACTION & CONTOH FORMAT (isi contoh ini hanya ilustrasi, abaikan isinya):

1. TAMBAH BARANG — gunakan jika user ingin menambah/mendaftarkan barang baru
contoh Input: "Tambah barang indomie, harga 3500, stok 100"
contoh format:
{{
  "action": "tambah_barang",
  "nama_barang": "indomie",
  "harga_barang": 3500,
  "stok_barang": 100
}}

2. UPDATE BARANG — gunakan jika user ingin mengubah harga, stok, atau keduanya
contoh Input: "Ganti harga indomie jadi 5000"
contoh format:
{{
  "action": "update_barang",
  "nama_barang": "indomie",
  "harga_barang": 5000
}}

contoh Input: "Update stok mie goreng jadi 200"
contoh format:
{{
  "action": "update_barang",
  "nama_barang": "mie goreng",
  "stok_barang": 200
}}

contoh Input: "Ubah harga indomie 3500 dan stoknya 50"
contoh format:
{{
  "action": "update_barang",
  "nama_barang": "indomie",
  "harga_barang": 3500,
  "stok_barang": 50
}}

3. LIHAT/CARI BARANG — gunakan jika user ingin melihat daftar atau info barang
contoh Input: "Tampilkan semua barang"
contoh format:
{{
  "action": "get_barang"
}}

contoh Input: "Cari indomie"
contoh format:
{{
  "action": "get_barang",
  "nama_barang": "indomie"
}}

4. HAPUS BARANG — gunakan jika user ingin menghapus atau menghilangkan barang
contoh Input: "Hapus indomie dari daftar"
contoh format:
{{
  "action": "hapus_barang",
  "nama_barang": "indomie"
}}

5. CHAT — gunakan jika input TIDAK berkaitan dengan barang sama sekali (salam, pertanyaan umum, dll)
contoh Input: "Halo"
contoh format:
{{
  "action": "chat",
  "message": "Halo"
}}

contoh Input: "Apa yang bisa kamu bantu?"
contoh format:
{{
  "action": "chat",
  "message": "Apa yang bisa kamu bantu?"
}}

Sekarang proses input ini dan balas HANYA dengan JSON:
"""
    
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
        save_history(username,"AI",jawaban)
        return jawaban
    
    except requests.exceptions.ConnectionError:
        return{f"status":"error","pesan":f"server ollama belum dijalankan"}

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
    

def func_calling(response_AI):
    data=json.loads(response_AI)

    if data["action"]=="tambah_barang":
        return tambah_barang(
            data["nama_barang"],
            data["harga_barang"],
            data["stok_barang"]
        )

    elif data["action"]=="hapus_barang":
        return hapus_barang(
            data["nama_barang"]
        )

    elif data["action"]=="update_barang":
        return update_barang(
            data["nama_barang"],
            data.get("harga_barang"),
            data.get("stok_barang")
        )

    elif data["action"]=="get_barang":
        return get_barang()

    elif data["action"] == "chat":
        return jawab_chat(data['message'])

    else:
        return {'msg':'action tidak diketahui'}

jawaban=tanya_ai('tampilkan semua data barang')
# print(jawaban)
print(func_calling(jawaban))




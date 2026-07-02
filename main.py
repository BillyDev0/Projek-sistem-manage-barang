from chatbot.tanya_ai import tanya_ai,func_calling
from token_setup.token import verify_token
from fastapi import FastAPI 
from auth.login import login
from auth.registrasi import registrasi

app=FastAPI()

@app.post('/tanyaa_AI')
def chatbot_AI(prompt:str):
    respon_ai=tanya_ai(prompt)
    jawaban=func_calling(respon_ai)
    return jawaban

@app.post('/data_karyawan')
def loginn(username:str,password:str):
    return login(username,password)

@app.post('/data_karyawann')
def registt(username:str,password:str):
    return registrasi(username,password)
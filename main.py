from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os

My_user = 'admin'
My_password = 'admin'

security = HTTPBasic()

app = FastAPI()

Dict_tarefinhas = {}

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

def autenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, My_user)
    is_password_correct = secrets.compare_digest(credentials.password, My_password)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code = 401,
            detail = "Usuario ou senha incorretas",
            headers={"WWW-Authenticate": "Basic"}
        )


@app.get("/")
def read_root():
    return {"message": "Tarefas"}

@app.get("/tarefinhas")
def get_tarefinhas(page: int=1, limit: int=10, credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    
    if page < 1 or limit< 1:
        raise HTTPException(status_code=400, detail="Não é possível acessar paginas menores que 0")

    if not Dict_tarefinhas:
        return { "detail": "Não há tarefas cadastradas"}
    

    start = (page - 1) * limit
    end = start + limit
    
    
    tarefinhas_paginadas = [
        {"nome": nome , "descricao": tarefa["descricao"], "concluida": tarefa["concluida"]}
        for nome, tarefa in list(Dict_tarefinhas.items())[start:end]
    ]

    return {
        "page": page,
        "limit": limit,
        "tarefinhas": tarefinhas_paginadas,
        "total": len(Dict_tarefinhas)
    }

@app.post("/adiciona")
def add_tarefa(tarefa: Tarefa , credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    if tarefa.nome in Dict_tarefinhas:
        raise HTTPException(status_code=400, detail="Tarefa já existe")
    Dict_tarefinhas[tarefa.nome] = tarefa.dict()

    return {"message": "Tarefa adicionada com sucesso"}

@app.put("/concluida/{nome}")
def tarefa_concluida(nome: str, credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    if nome not in Dict_tarefinhas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    Dict_tarefinhas[nome]["concluida"] = True
    return {"message": "Tarefa marcada como concluída", "tarefa": Dict_tarefinhas[nome]}

@app.delete("/delete/{nome}")
def delete_tarefa(nome: str, credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    if nome in Dict_tarefinhas:
        del Dict_tarefinhas[nome]
        return {"message": "Tarefa excluída com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
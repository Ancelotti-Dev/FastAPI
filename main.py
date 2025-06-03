from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tarefas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

My_user = 'admin'
My_password = 'admin'

security = HTTPBasic()

app = FastAPI()

Dict_tarefinhas = {}

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, default=False)
Base.metadata.create_all(bind=engine)


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
def get_tarefinhas(
    page: int = 1,
    limit: int = 10,
    sort_by: str = "nome",
    credentials: HTTPBasicCredentials = Depends(autenticate_user)
):
    
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Não é possível acessar paginas menores que 0")

    if not Dict_tarefinhas:
        return { "detail": "Não há tarefas cadastradas"}
    

    start = (page - 1) * limit
    end = start + limit
    
    # Ordena as tarefas pelo campo escolhido
    if sort_by not in ["nome", "descricao"]:
        raise HTTPException(status_code=400, detail="Campo de ordenação inválido")

    if sort_by == "nome":
        Tarefas_ordenadas = sorted(Dict_tarefinhas.items(), key=lambda x: x[0])
    else:
        Tarefas_ordenadas = sorted(Dict_tarefinhas.items(), key=lambda x: x[1]["descricao"])
    
    tarefinhas_paginadas = [
        {"nome": nome , "descricao": tarefa["descricao"], "concluida": tarefa["concluida"]}
        for nome, tarefa in Tarefas_ordenadas[start:end]
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
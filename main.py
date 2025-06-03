from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

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

class TarefaModel(BaseModel):
    nome: str
    descricap: str
    concluida: bool = False

Base.metadata.create_all(bind=engine)

# Função para manipular o Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticate_user)
):
    
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Não é possível acessar paginas menores que 0")


    tarefas = db.query(Tarefa).offset((page - 1) * limit).limit(limit).all()


    if not Dict_tarefinhas:
        return { "detail": "Não há tarefas cadastradas"}
    
    total_tarefas = db.query(Tarefa).count()
    # Cria um dicionário com as tarefas

    return {
        "page": page,
        "limit": limit,
        "total": len(Dict_tarefinhas),
        "tarefinhas": [{"nome": tarefa.nome, "descricao": tarefa.descricao, "cocluida": tarefa.concluida} for tarefa in tarefas]
    }

@app.post("/adiciona")
def add_tarefa(tarefa: TarefaModel, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    db_tarefa = db.query(Tarefa)(Tarefa.nome == TarefaModel.nome, Tarefa.descricao == TarefaModel.descricao).first()
    
    if db_tarefa:
        raise HTTPException(status_code=400, detail="Essa Tarefa já existe irmão!!!")
    
    new_tarefa = Tarefa(nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(new_tarefa)
    db.commit()
    db.refresh(new_tarefa)

    return {"message": "Tarefa foi adicionada com sucesso!", "tarefa": new_tarefa}

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
import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuração do banco de dados SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

# Criação do engine e sessão do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Usuário e senha para autenticação básica
My_user = os.getenv("My_user")
My_password = os.getenv("My_password")

security = HTTPBasic()

app = FastAPI(
    title="Gerenciador de Tarefas",
    description="API para gerenciar tarefas com autenticação básica",
    version="1.1.0"
)

# Modelo da tabela Tarefa no banco de dados (SQLAlchemy)
class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    nome = Column(String, unique=True, index=True)      # Nome da tarefa (único)
    descricao = Column(String, index=True)              # Descrição da tarefa
    concluida = Column(Boolean, default=False)          # Status de conclusão

# Modelo Pydantic para validação de entrada/saída de dados
class TarefaModel(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(bind=engine)

# Função para obter uma sessão do banco de dados (usada como dependência)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função de autenticação básica HTTP
def autenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, My_user)
    is_password_correct = secrets.compare_digest(credentials.password, My_password)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code = 401,
            detail = "Usuario ou senha incorretas",
            headers={"WWW-Authenticate": "Basic"}
        )

# Rota raiz apenas para teste
@app.get("/")
def read_root():
    return {"message": "Tarefas"}

# Rota para listar tarefas com paginação
@app.get("/tarefinhas")
def get_tarefinhas(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticate_user)
):
    # Validação dos parâmetros de paginação
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Não é possível acessar paginas menores que 0")

    # Busca tarefas no banco de dados com offset e limit para paginação
    tarefas = db.query(Tarefa).offset((page - 1) * limit).limit(limit).all()

    # Se não houver tarefas cadastradas
    if not tarefas:
        return { "detail": "Não há tarefas cadastradas"}
    
    total_tarefas = db.query(Tarefa).count()  # Conta o total de tarefas

    # Retorna as tarefas paginadas e informações de paginação
    return {
        "page": page,
        "limit": limit,
        "total": total_tarefas,
        "tarefinhas": [
            {"id": tarefa.id, "nome": tarefa.nome, "descricao": tarefa.descricao, "cocluida": tarefa.concluida}
            for tarefa in tarefas
        ]
    }

# Rota para adicionar uma nova tarefa
@app.post("/adiciona")
def add_tarefa(tarefa: TarefaModel, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    # Verifica se já existe uma tarefa com o mesmo nome e descrição
    db_tarefa = db.query(Tarefa).filter(Tarefa.nome == tarefa.nome, Tarefa.descricao == tarefa.descricao).first()
    if db_tarefa:
        raise HTTPException(status_code=400, detail="Essa Tarefa já existe irmão!!!")
    
    # Cria uma nova tarefa e adiciona ao banco de dados
    new_tarefa = Tarefa(nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(new_tarefa)
    db.commit()
    db.refresh(new_tarefa)

    # Retorna mensagem de sucesso e dados da tarefa criada
    return {"message": "Tarefa foi adicionada com sucesso!", "tarefa": {
        "nome": new_tarefa.nome,
        "descricao": new_tarefa.descricao,
        "concluida": new_tarefa.concluida
    }}

# Rota para marcar uma tarefa como concluída pelo id
@app.put("/concluida/{id}")
def tarefa_concluida(id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    # Busca a tarefa pelo id
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Não foi possivel encontrar uma tarefa")
    
    # Marca como concluída e salva no banco
    db_tarefa.concluida = True
    db.commit()
    db.refresh(db_tarefa)
    
    return {"message": "Tarefa marcada como concluída"}

# Rota para deletar uma tarefa pelo id
@app.delete("/delete/{id}")
def delete_tarefa(id: int, db: Session= Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticate_user)):
    # Busca a tarefa pelo id
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == id).first()
    if not db_tarefa:
         raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Deleta a tarefa do banco de dados
    db.delete(db_tarefa)
    db.commit()

    return {"message": "Tarefa deletada com sucesso"}

# ACID
 # A - Atomicidade: Todas as operações de uma transação são concluídas com sucesso ou nenhuma delas é aplicada.
 # C - Consistência: O banco de dados permanece em um estado consistente antes e depois da transação.
 # I - Isolamento: As transações são isoladas umas das outras, garatindo que uma transição não afete a outra.
 # D - Durabilidade: Uma vez que uma transição é confirmada, sua alteração é permanente, mesmo em caso de falha da aplicação ou do sistema.

# ORM - Object Relational Mapping: É uma tecnica que permite mapear objetos de uma linguagem de programação para 
# tabelas de um banco de dados relacional, facilitando a interação entre o codigo e o banco de dados.

# SQLAlchemy: É uma biblioteca do Python que permite trabalhar com banco de dados relacionais de forma mais fácil,
# ultilizando o conceito de ORM. Ela fornece uma camada de abstração para interagir com o banco de dados.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

Dict_tarefinhas = {}

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

@app.get("/")
def read_root():
    return {"message": "ANCELA API de Dict_tarefinhas"}

@app.get("/tarefinhas")
def get_Dict_tarefinhas():
    if not Dict_tarefinhas:
        return {"message": "Não há nenhuma tarefa ainda"}
    return Dict_tarefinhas

@app.post("/adiciona")
def add_tarefa(tarefa: Tarefa):
    if tarefa.nome in Dict_tarefinhas:
        raise HTTPException(status_code=400, detail="Tarefa já existe")
    Dict_tarefinhas[tarefa.nome] = tarefa.dict()
    return {"message": "Tarefa adicionada com sucesso"}

@app.put("/concluida/{nome}")
def tarefa_concluida(nome: str):
    if nome not in Dict_tarefinhas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    Dict_tarefinhas[nome]["concluida"] = True
    return {"message": "Tarefa marcada como concluída", "tarefa": Dict_tarefinhas[nome]}

@app.delete("/delete/{nome}")
def delete_tarefa(nome: str):
    if nome in Dict_tarefinhas:
        del Dict_tarefinhas[nome]
        return {"message": "Tarefa excluída com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
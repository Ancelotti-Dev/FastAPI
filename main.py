from fastapi import FastAPI, HTTPException

app = FastAPI()

tarefas = {}

@app.get("/")
def read_root():
    return {"message": "ANCELA API de Tarefas"}

@app.get('/tarefas')
def get_tarefas():
    return tarefas

@app.post("/adiciona")  
def add_tarefa(nome: str, descricao: str):
    if nome in tarefas:
        raise HTTPException(status_code=400, detail="Tarefa já existe")
    tarefas[nome] = {"descricao": descricao, "concluida": False}
    return {"message": "Tarefa adicionada com sucesso", "tarefa": tarefas[nome]}

@app.put("/concluida/{nome}")
def tarefa_concluida(nome: str, concluida: bool = True):
    if nome not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefas[nome]["concluida"] = concluida
    return {"message": "Status da tarefa atualizado", "tarefa": tarefas[nome]}

@app.delete("/delete/{nome}")
def delete_tarefa(nome: str):
    if nome in tarefas:
        del tarefas[nome]
        return {"message": "Tarefa excluida com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Tarefa não encontarada")
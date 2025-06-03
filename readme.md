# Atividade 11 - FastAPI: Gerenciador de Tarefas

Este projeto é uma API REST para gerenciamento de tarefas (ToDo) desenvolvida com [FastAPI](https://fastapi.tiangolo.com/), utilizando autenticação básica HTTP e persistência de dados com SQLite via SQLAlchemy.

## Funcionalidades

- **Listar tarefas** com paginação
- **Adicionar nova tarefa**
- **Marcar tarefa como concluída**
- **Deletar tarefa**
- **Autenticação básica** para todas as rotas

## Estrutura do Projeto

- `main.py`: Código principal da API.
- `tarefas.db`: Banco de dados SQLite criado automaticamente.
- `readme.md`: Este arquivo de explicação.

## Como executar

1. **Instale as dependências**:
   ```bash
   pip install fastapi uvicorn sqlalchemy
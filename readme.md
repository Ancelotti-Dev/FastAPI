# Atividade - FastAPI: Gerenciador de Tarefas

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
- `Dockerfile` e `docker-compose.yml`: Arquivos para execução em containers Docker.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd FastAPI-2
```

### 2. Instalar as dependências (modo local)

```bash
pip install fastapi uvicorn sqlalchemy
```

### 3. Rodar a aplicação

```bash
uvicorn main:app --reload
```

Acesse em: [http://localhost:8000/docs](http://localhost:8000/docs) para a documentação interativa.

---

## Executando com Docker

### 1. Usando Docker Compose

```bash
docker-compose up --build
```

### 2. Usando apenas Docker

```bash
docker build -t fastapi-tarefas .
docker run -p 8000:8000 fastapi-tarefas
```

---

## Exemplo de uso

### Adicionar uma tarefa

```http
POST /tarefas
Authorization: Basic <base64-usuario:senha>
Content-Type: application/json

{
  "titulo": "Estudar FastAPI",
  "descricao": "Ler a documentação oficial"
}
```

### Listar tarefas

```http
GET /tarefas
Authorization: Basic <base64-usuario:senha>
```

---

## Autenticação

Todas as rotas exigem autenticação básica HTTP. Use seu usuário e senha definidos no ambiente ou código.

---

## Licença

Este projeto é apenas para fins educacionais.
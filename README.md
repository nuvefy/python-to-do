# To-Do API

API REST de to-do em Python com FastAPI, PostgreSQL e migrations Alembic, com interface web para CRUD. Pronta para deploy no Railway.

## Stack

- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- psycopg 3
- uvicorn
- Jinja2 + HTMX (UI)

## Setup local

### 1. Subir o PostgreSQL

```bash
docker compose up -d
```

O banco fica em `localhost:5434` (porta mapeada para evitar conflito com outros Postgres locais).

### 2. Ambiente Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Migrations

```bash
alembic upgrade head
```

### 4. Rodar a aplicação

```bash
uvicorn app.main:app --reload --port 8000
```

- UI: http://localhost:8000/ui (também em `/`)
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

A UI em `/ui` cobre criar, listar, filtrar, editar, concluir/reabrir e excluir to-dos. A API JSON em `/todos` continua disponível para clientes programáticos.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Redirect para `/ui` |
| `GET` | `/ui` | Interface gráfica de CRUD |
| `POST` | `/todos` | Criar to-do |
| `GET` | `/todos` | Listar (`?completed=true\|false` opcional) |
| `GET` | `/todos/{id}` | Buscar por id |
| `PATCH` | `/todos/{id}` | Atualizar parcial |
| `DELETE` | `/todos/{id}` | Remover |
| `GET` | `/health` | Healthcheck |

### Exemplos

```bash
# Criar
curl -X POST http://localhost:8000/todos \
  -H 'Content-Type: application/json' \
  -d '{"title":"Comprar leite","description":"2 litros","due_date":"2026-09-10"}'

# Listar
curl http://localhost:8000/todos

# Concluir
curl -X PATCH http://localhost:8000/todos/<id> \
  -H 'Content-Type: application/json' \
  -d '{"completed":true}'

# Remover
curl -X DELETE http://localhost:8000/todos/<id>
```

## Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `DATABASE_URL` | URL do PostgreSQL (`postgresql://` ou `postgresql+psycopg://`) |
| `PORT` | Porta HTTP (default `8000`) |

A aplicação normaliza `postgres://` e `postgresql://` para `postgresql+psycopg://` (compatível com Railway).

## Deploy no Railway

1. Crie um projeto no [Railway](https://railway.app).
2. Adicione o plugin **PostgreSQL**.
3. Faça deploy deste repositório (Dockerfile + `railway.toml`).
4. Confirme que `DATABASE_URL` está linkada ao serviço da API.
5. No boot, `scripts/start.sh` roda `alembic upgrade head` e sobe o uvicorn em `$PORT`.
6. Healthcheck: `/health`.

Arquivos de deploy:

- `Dockerfile` — imagem Python 3.12
- `railway.toml` — build Docker, start command e healthcheck
- `scripts/start.sh` — migrate + serve

## Estrutura

```
app/
  main.py
  config.py
  database.py
  models/
  schemas/
  routers/
    todos.py
    ui.py
  crud/
  templates/
  static/
alembic/
  versions/
scripts/start.sh
Dockerfile
railway.toml
docker-compose.yml
```

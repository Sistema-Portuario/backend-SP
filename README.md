# Backend - Gerenciador de Sistema Portuário

Este é o repositório do backend para o sistema de gerenciamento portuário. O projeto utiliza Python com o ORM SQLAlchemy para se conectar a um banco de dados PostgreSQL.

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em sua máquina:

* **Python** (versão 3.8 ou superior)
* **PostgreSQL** (versão 14 ou superior)
* **Git**

---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar o ambiente de desenvolvimento localmente.

### 1. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd gerenciador-portuario
```

### 2. Criar e Ativar um Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados PostgreSQL

1. Crie o banco:

   ```sql
   CREATE DATABASE sistema_portuario;
   ```
2. Garanta que o usuário e senha tenham acesso ao banco.

### 5. Configurar as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e edite com suas credenciais:

```
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_secreta
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sistema_portuario
SECRET_KEY=sua_chave_supersecreta
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Criar as Tabelas

```bash
python create_tables.py
```

### 7. Popular as Tabelas
  
  cd src
  python3 popular_banco.py  (RESETA O BD E CRIA OS DADOS NOVAMENTE)

  Nota: O script gera senhas aleatórias. Para testar o login especificamente, recomenda-se criar um usuário manualmente via API ou ajustar o script para fixar uma senha conhecida.
---

##  Como Testar os Endpoints da API

Após configurar o ambiente, siga os passos abaixo para testar o módulo de usuários.

### 1. Iniciar o Servidor

```bash
uvicorn src.main:app --reload
```

A aplicação rodará em:

```
http://127.0.0.1:8000
```

### ⚠️ Observação Importante

> Todas as rotas de criação, atualização e deleção **recebem os dados via parâmetros de query**, e **não em JSON**.
> Exemplo:
> `POST /usuarios/?nome=bruno&senha=1234&cargo_id=...`

---

### 2. Criar um Cargo

**Método:** `POST /cargos/`
**Parâmetros (query):**

* `nome`: string
* `descricao`: string

Exemplo:

```bash
curl -X POST "http://127.0.0.1:8000/cargos/?nome=<cargo>&descricao=<descricao>"
```

### 3. Listar Cargos

**Método:** `POST /cargos/`

```bash
curl http://127.0.0.1:8000/cargos/
```

---

### 4. Criar um Usuário

**Método:** `POST /usuarios/`
**Parâmetros (query):**

* `nome`: string
* `senha`: string
* `cargo_id`: UUID

Exemplo:

```bash
curl -X POST "http://127.0.0.1:8000/usuarios/?nome=bruno&senha=1234&cargo_id=<ID_DO_CARGO>"
```

---

### 5. Listar Usuários

**Método:** `GET /usuarios/`

```bash
curl http://127.0.0.1:8000/usuarios/
```

---

### 6. Buscar Usuário por ID

**Método:** `GET /usuarios/{usuario_id}`

```bash
curl http://127.0.0.1:8000/usuarios/<ID_DO_USUARIO>
```

---

### 7. Atualizar Usuário

**Método:** `PUT /usuarios/{usuario_id}`
**Parâmetros (query):** `nome`, `senha`, `cargo_id` (opcionais)

```bash
curl -X PUT "http://127.0.0.1:8000/usuarios/<ID_DO_USUARIO>?nome=novoNome&senha=novaSenha"
```

---

### 8. Deletar Usuário

**Método:** `DELETE /usuarios/{usuario_id}`

```bash
curl -X DELETE "http://127.0.0.1:8000/usuarios/<ID_DO_USUARIO>"
```

---

### 9. Fazer Login

**Método:** `POST /usuarios/login`
**Envia dados via formulário (`OAuth2PasswordRequestForm`):**

```bash
curl -X POST -F "username=bruno" -F "password=1234" http://127.0.0.1:8000/usuarios/login
```

**Resposta esperada:**

```json
{
  "access_token": "<TOKEN_JWT>",
  "token_type": "bearer"
}
```

---

### 10. Acessar Rota Protegida

**Método:** `GET /usuarios/me`
Use o token JWT retornado no login:

```bash
TOKEN=<TOKEN_JWT>
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/usuarios/me
```

**Resposta:**

```json
{
  "id": "UUID_DO_USUARIO",
  "nome": "bruno"
}
```


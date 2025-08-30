# Backend - Gerenciador de Sistema Portuário

Este é o repositório do backend para o sistema de gerenciamento portuário. O projeto utiliza Python com o ORM SQLAlchemy para se conectar a um banco de dados PostgreSQL.

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em sua máquina:
- **Python** (versão 3.8 ou superior)
- **PostgreSQL** (versão 14 ou superior)
- **Git**

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar o ambiente de desenvolvimento localmente.

### 1. Clonar o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd gerenciador-portuario
```

### 2. Criar e Ativar um Ambiente Virtual
É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no Linux/macOS
source venv/bin/activate
```

### 3. Instalar as Dependências
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias.
```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados PostgreSQL
Você precisa ter um servidor PostgreSQL rodando e criar um banco de dados para a aplicação.

1.  Abra o pgAdmin ou use o terminal (`psql`).
2.  Crie um novo banco de dados. O nome padrão utilizado no projeto é `sistema_portuario`.
    ```sql
    CREATE DATABASE sistema_portuario;
    ```
3.  Certifique-se de que você tem um usuário e senha com permissão para acessar este banco.

### 5. Configurar as Variáveis de Ambiente
O projeto usa um arquivo `.env` para guardar as credenciais do banco de dados.

1.  Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`.
    ```bash
    # No Windows (prompt de comando)
    copy .env.example .env

    # No Linux/macOS
    cp .env.example .env
    ```
2.  Abra o arquivo `.env` e substitua os valores pelas suas credenciais do PostgreSQL.

    ```
    DB_USER=seu_usuario_postgres
    DB_PASSWORD=sua_senha_secreta
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=sistema_portuario
    ```

### 6. Criar as Tabelas no Banco
O último passo é executar o script que cria toda a estrutura de tabelas no banco de dados que você configurou.

```bash
python create_tables.py
```

Após a execução, você deverá ver a mensagem "Tabelas criadas com sucesso!" e poderá verificar as tabelas no seu pgAdmin.

---

Pronto! O ambiente está configurado e o banco de dados está pronto para receber as chamadas da API.
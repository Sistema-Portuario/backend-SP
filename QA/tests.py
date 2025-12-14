"""
Suíte de Testes de QA Completa para a API Gerenciador de Sistema Portuário.
Versão 3: Hooks movidos para conftest.py

Este script usa o pytest para rodar uma suíte completa de testes automatizados, cobrindo:
1.  Caminho Feliz (Cenários Simples)
2.  Cenários de Limite e Erro (401, 404, 409, 422)
3.  Cenários Avançados de Limite e Lógica de Estado

Para rodar este arquivo e gerar um relatório:
1.  Garanta que o servidor da API esteja rodando.
2.  Instale as dependências: pip install pytest requests pytest-html
3.  Execute no terminal:
    python -m pytest tests.py --html=report.html --self-contained-html
"""

import requests
import pytest
import uuid
import datetime

# --- Configuração ---

BASE_URL = "http://127.0.0.1:8000"

def get_unique_name(prefix="test"):
    """Função auxiliar para gerar nomes únicos para os testes."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

# --- Pytest Fixtures (Funções Auxiliares) ---

@pytest.fixture(scope="module")
def module_cargo():
    """
    Fixture que roda UMA VEZ por módulo.
    Cria um único 'Cargo' compartilhado para testes que precisam de um cargo_id válido.
    """
    cargo_data = {
        "nome": get_unique_name("module_cargo"),
        "descricao": "Cargo para testes de escopo do módulo"
    }
    response = requests.post(f"{BASE_URL}/cargos/", params=cargo_data)
    assert response.status_code == 200, "Fixture: Falha ao criar o cargo a nível de módulo"
    
    cargo = response.json()
    yield cargo
    
    # Teardown (Limpeza)
    # O README não especifica um DELETE /cargos/, então a limpeza do cargo é pulada.
    # Se um endpoint DELETE /cargos/{id} existir, ele deve ser adicionado aqui.

@pytest.fixture(scope="function")
def function_user(module_cargo):
    """
    Fixture que roda UMA VEZ por função de teste.
    Cria um único 'Usuario' e o limpa (deleta) depois.
    """
    user_data = {
        "nome": get_unique_name("user"),
        "senha": "strongpassword123",
        "cargo_id": module_cargo["id"]
    }
    response = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
    assert response.status_code == 200, "Fixture: Falha ao criar o usuário a nível de função"
    
    user = response.json()
    # Adiciona a senha ao dict para que o teste possa usá-la para login
    user["password_plain"] = user_data["senha"] 
    
    yield user
    
    # Teardown (Limpeza)
    requests.delete(f"{BASE_URL}/usuarios/{user['id']}")

# --- Classes de Teste ---

class TestSimpleHappyPath:
    """Testa a funcionalidade básica e esperada (CRUD e Autenticação)."""

    def test_create_and_list_cargos(self):
        """Teste: Consegue criar um cargo e verifica se ele aparece na lista."""
        cargo_data = {
            "nome": get_unique_name("list_cargo_test"),
            "descricao": "Test create-and-list cargo"
        }
        
        # 1. Criar Cargo
        response_create = requests.post(f"{BASE_URL}/cargos/", params=cargo_data)
        assert response_create.status_code == 200
        created_cargo = response_create.json()
        assert created_cargo["nome"] == cargo_data["nome"]
        assert "id" in created_cargo

        # 2. Listar Cargos
        response_list = requests.get(f"{BASE_URL}/cargos/")
        assert response_list.status_code == 200
        all_cargos = response_list.json()
        assert isinstance(all_cargos, list)
        
        # 3. Verificar
        assert any(c["id"] == created_cargo["id"] for c in all_cargos), "Cargo criado não encontrado na lista"

    def test_user_full_lifecycle(self, module_cargo):
        """Teste: Cobre Criar, Ler, Atualizar e Deletar (CRUD) para um Usuário."""
        user_data = {
            "nome": get_unique_name("lifecycle_user"),
            "senha": "password123",
            "cargo_id": module_cargo["id"]
        }
        
        # 1. Criar Usuário
        response_create = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
        assert response_create.status_code == 200
        user_id = response_create.json()["id"]

        # 2. Ler (Buscar por ID)
        response_get = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        assert response_get.status_code == 200
        assert response_get.json()["nome"] == user_data["nome"]

        # 3. Atualizar Usuário
        update_data = {"nome": "updated_name"}
        response_update = requests.put(f"{BASE_URL}/usuarios/{user_id}", params=update_data)
        assert response_update.status_code == 200
        assert response_update.json()["nome"] == "updated_name"

        # 4. Deletar Usuário
        response_delete = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response_delete.status_code == 200

        # 5. Verificar Deleção
        response_get_deleted = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        assert response_get_deleted.status_code == 404

    def test_full_auth_flow(self, function_user):
        """Teste: Um usuário consegue fazer login e acessar uma rota protegida?"""
        
        # 1. Fazer Login
        # Nota: O README especifica dados de formulário (form data) para o login
        login_form_data = {
            "username": function_user["nome"],
            "password": function_user["password_plain"]
        }
        response_login = requests.post(f"{BASE_URL}/usuarios/login", data=login_form_data)
        assert response_login.status_code == 200, "Login falhou"
        
        token_data = response_login.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

        # 2. Acessar Rota Protegida
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response_me = requests.get(f"{BASE_URL}/usuarios/me", headers=headers)
        
        assert response_me.status_code == 200
        assert response_me.json()["nome"] == function_user["nome"]


class TestLimitAndErrorScenarios:
    """Testa os "limites" e casos de falha esperados (erros 4xx)."""

    @pytest.mark.parametrize("invalid_name", ["", "   ", None])
    def test_create_cargo_invalid_name(self, invalid_name):
        """Teste: API rejeita cargo com nome vazio, apenas com espaços, ou nulo."""
        response = requests.post(f"{BASE_URL}/cargos/", params={"nome": invalid_name, "descricao": "Invalid test"})
        # Espera 422 Unprocessable Entity
        assert response.status_code == 422

    def test_create_user_invalid_cargo_id_format(self):
        """Teste: API rejeita criação de usuário se o cargo_id não for um UUID válido."""
        user_data = {
            "nome": "test_user",
            "senha": "password",
            "cargo_id": "not-a-valid-uuid"
        }
        response = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
        assert response.status_code == 422

    def test_create_user_non_existent_cargo_id(self):
        """Teste: API rejeita criação de usuário se o cargo_id for um UUID válido, mas não existir."""
        non_existent_uuid = str(uuid.uuid4())
        user_data = {
            "nome": "test_user",
            "senha": "password",
            "cargo_id": non_existent_uuid
        }
        response = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
        # Espera 404 (Not Found) ou 400 (Bad Request)
        assert response.status_code in [404, 400, 422]

    def test_get_non_existent_user(self):
        """Teste: API retorna 404 ao buscar um usuário que não existe."""
        non_existent_uuid = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/usuarios/{non_existent_uuid}")
        assert response.status_code == 404

    def test_delete_non_existent_user(self):
        """Teste: API retorna 404 ao deletar um usuário que não existe."""
        non_existent_uuid = str(uuid.uuid4())
        response = requests.delete(f"{BASE_URL}/usuarios/{non_existent_uuid}")
        assert response.status_code == 404

    def test_login_wrong_password(self, function_user):
        """Teste: API retorna 401 ao fazer login com uma senha incorreta."""
        login_form_data = {
            "username": function_user["nome"],
            "password": "THIS_IS_THE_WRONG_PASSWORD"
        }
        response = requests.post(f"{BASE_URL}/usuarios/login", data=login_form_data)
        assert response.status_code == 401 # Unauthorized

    @pytest.mark.parametrize("invalid_token", [None, "Bearer 12345", "Bearer "])
    def test_access_protected_route_invalid_token(self, invalid_token):
        """Teste: API retorna 401 ao acessar rota protegida com token inválido ou sem token."""
        headers = {}
        if invalid_token:
            headers = {"Authorization": invalid_token}
            
        response = requests.get(f"{BASE_URL}/usuarios/me", headers=headers)
        assert response.status_code == 401 # Unauthorized

    def test_create_duplicate_cargo(self, module_cargo):
        """Teste: API retorna 409 Conflict ao criar um cargo com nome duplicado."""
        # Este teste depende do cargo criado pela fixture 'module_cargo'
        duplicate_data = {
            "nome": module_cargo["nome"], # Usa o *mesmo nome*
            "descricao": "Tentativa de cargo duplicado"
        }
        response = requests.post(f"{BASE_URL}/cargos/", params=duplicate_data)
        
        # Espera 409 Conflict. Se falhar, a API permite nomes duplicados, o que é um bug.
        assert response.status_code == 409


class TestAdvancedScenarios:
    """
    Testa valores de limite avançados (ex: strings longas) e
    lógica de negócio/integridade de estado (ex: constraints de chave estrangeira).
    """

    def test_create_user_with_extremely_long_name(self, module_cargo):
        """Teste: API deve rejeitar um nome de usuário que excede os limites do banco/modelo."""
        long_name = "a" * 1000  # string de 1000 caracteres
        user_data = {
            "nome": long_name,
            "senha": "password123",
            "cargo_id": module_cargo["id"]
        }
        response = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
        # Espera 422 (Unprocessable Entity) ou 413 (Payload Too Large)
        # Um erro 500 aqui seria um bug.
        assert response.status_code in [422, 413, 400]

    @pytest.mark.parametrize("missing_param_data", [
        {"senha": "pw", "cargo_id": "uuid"},  # Faltando 'nome'
        {"nome": "user", "cargo_id": "uuid"},  # Faltando 'senha'
        {"nome": "user", "senha": "pw"}        # Faltando 'cargo_id'
    ])
    def test_create_user_missing_required_params(self, missing_param_data, module_cargo):
        """Teste: API rejeita criação de usuário se parâmetros obrigatórios estiverem faltando."""
        # Corrige o cargo_id se não for ele o parâmetro faltante
        if "cargo_id" in missing_param_data and missing_param_data["cargo_id"] == "uuid":
            missing_param_data["cargo_id"] = module_cargo["id"]
            
        response = requests.post(f"{BASE_URL}/usuarios/", params=missing_param_data)
        assert response.status_code == 422

    def test_create_user_with_empty_password(self, module_cargo):
        """Teste: API deve rejeitar um usuário com senha vazia."""
        user_data = {
            "nome": get_unique_name("empty_pass_user"),
            "senha": "", # Senha vazia
            "cargo_id": module_cargo["id"]
        }
        response = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
        assert response.status_code == 422

    def test_login_with_non_existent_user(self):
        """Teste: API retorna 401/404 ao fazer login com um usuário inexistente."""
        login_form_data = {
            "username": "ghost_user_that_does_not_exist",
            "password": "password"
        }
        response = requests.post(f"{BASE_URL}/usuarios/login", data=login_form_data)
        # O padrão OAuth2 geralmente retorna 401 para usuário *ou* senha errados
        # para evitar que atacantes adivinhem nomes de usuário válidos. 404 também é aceitável.
        assert response.status_code in [401, 404]

    def test_update_user_to_invalid_name(self, function_user):
        """Teste: API rejeita um UPDATE que tenta definir um nome inválido."""
        user_id = function_user["id"]
        
        # Tenta atualizar o nome do usuário para uma string vazia
        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", params={"nome": ""})
        
        # Espera 422. Se retornar 200, é um bug.
        assert response.status_code == 422

    def test_delete_cargo_while_in_use(self, module_cargo):
        """
        Teste: (CRÍTICO) API deve impedir a deleção de um Cargo se um Usuário estiver atribuído a ele.
        NOTA: Este teste assume que um endpoint 'DELETE /cargos/{id}' existe,
        o que não foi especificado no README. Se este teste falhar com 404/405,
        significa que o endpoint está faltando, o que também é um achado válido.
        """
        # 1. Criar um novo usuário temporário atribuído ao cargo compartilhado
        user_data = {
            "nome": get_unique_name("temp_user_for_delete_test"),
            "senha": "password",
            "cargo_id": module_cargo["id"]
        }
        response_user = requests.post(f"{BASE_URL}/usuarios/", params=user_data)
        assert response_user.status_code == 200
        user_id = response_user.json()["id"]

        # 2. Tentar deletar o Cargo enquanto o usuário está atribuído a ele
        response_delete_cargo = requests.delete(f"{BASE_URL}/cargos/{module_cargo['id']}")
        
        # 3. Esperar 409 (Conflict). Um erro 500 é um bug crítico.
        assert response_delete_cargo.status_code == 409, \
            "API deveria retornar 409 Conflict ao deletar um recurso em uso."
            
        # 4. Limpar o usuário para que outros testes não sejam afetados
        requests.delete(f"{BASE_URL}/usuarios/{user_id}")


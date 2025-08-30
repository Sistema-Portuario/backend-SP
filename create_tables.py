from src.database.connection import engine
from src.models import Base

def create_all_tables():
    print("Iniciando a criação das tabelas no banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao criar as tabelas: {e}")

if __name__ == "__main__":
    create_all_tables()
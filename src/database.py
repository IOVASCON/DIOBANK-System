from sqlalchemy import create_engine, MetaData, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# URL de conexão do banco de dados SQLite
DATABASE_URL = "sqlite:///./banco.db"

# Metadados do banco de dados
metadata = MetaData()
# Criação do mecanismo de conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Configuração da fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Classe base declarativa para os modelos
Base = declarative_base(metadata=metadata)

def init_db():
    """
    Inicializa o banco de dados e cria todas as tabelas definidas nos modelos.
    """
    import src.models.cliente  # Importa o modelo Cliente
    import src.models.conta  # Importa o modelo Conta
    import src.models.historico  # Importa o modelo Historico
    Base.metadata.create_all(bind=engine, checkfirst=True)  # Cria as tabelas no banco de dados

def update_db():
    """
    Atualiza o esquema do banco de dados, adicionando colunas que não existem.
    Verifica se a coluna 'tipo' está presente na tabela 'clientes', e a adiciona se não estiver.
    """
    connection = engine.connect()  # Conecta ao banco de dados
    inspector = inspect(engine)  # Inspetor do banco de dados para verificar o esquema
    columns = [column['name'] for column in inspector.get_columns('clientes')]  # Obtém as colunas da tabela 'clientes'
    if 'tipo' not in columns:  # Verifica se a coluna 'tipo' não existe
        try:
            connection.execute(text("ALTER TABLE clientes ADD COLUMN tipo STRING;"))  # Adiciona a coluna 'tipo'
        except OperationalError as e:
            print(f"Ocorreu um erro ao tentar adicionar a coluna 'tipo': {e}")
    connection.close()  # Fecha a conexão

def clear_db():
    """
    Limpa todos os dados das tabelas 'historicos', 'contas' e 'clientes'.
    """
    connection = engine.connect()  # Conecta ao banco de dados
    trans = connection.begin()  # Inicia uma transação
    try:
        connection.execute(text("DELETE FROM historicos"))  # Deleta todos os registros da tabela 'historicos'
        connection.execute(text("DELETE FROM contas"))  # Deleta todos os registros da tabela 'contas'
        connection.execute(text("DELETE FROM clientes"))  # Deleta todos os registros da tabela 'clientes'
        trans.commit()  # Confirma a transação
        print("Base de dados limpa com sucesso.")
    except Exception as e:
        trans.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao limpar a base de dados: {e}")
    finally:
        connection.close()  # Fecha a conexão

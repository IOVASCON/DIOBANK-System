import pytest  # Importa a biblioteca pytest para criação e execução de testes
from src.models.cliente import Cliente  # Importa o modelo Cliente
from src.database import SessionLocal, init_db  # Importa a função de inicialização do banco de dados e a fábrica de sessões

# Fixture que inicializa o banco de dados e fornece uma sessão de banco de dados para os testes
@pytest.fixture(scope='module')
def db():
    init_db()  # Inicializa o banco de dados e cria as tabelas
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    yield db  # Fornece a sessão para os testes
    db.close()  # Fecha a sessão após os testes

# Teste para criação de um cliente
def test_create_cliente(db):
    # Cria um novo cliente
    new_cliente = Cliente(nome="Teste Cliente", cpf="123.456.789-00", endereco="Rua Teste", tipo="Pessoa Física")
    db.add(new_cliente)  # Adiciona o cliente à sessão do banco de dados
    db.commit()  # Comita a transação, salvando o cliente no banco de dados

    # Consulta o cliente recém-criado no banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="123.456.789-00").first()
    # Verifica se o cliente foi encontrado e se os dados estão corretos
    assert cliente_from_db is not None
    assert cliente_from_db.nome == "Teste Cliente"
    assert cliente_from_db.endereco == "Rua Teste"
    assert cliente_from_db.tipo == "Pessoa Física"

# Teste para atualização de um cliente
def test_update_cliente(db):
    # Consulta o cliente no banco de dados
    cliente = db.query(Cliente).filter_by(cpf="123.456.789-00").first()
    cliente.nome = "Teste Cliente Atualizado"  # Atualiza o nome do cliente
    db.commit()  # Comita a transação, salvando as alterações no banco de dados

    # Consulta novamente o cliente no banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="123.456.789-00").first()
    # Verifica se o nome foi atualizado corretamente
    assert cliente_from_db.nome == "Teste Cliente Atualizado"

# Teste para exclusão de um cliente
def test_delete_cliente(db):
    # Consulta o cliente no banco de dados
    cliente = db.query(Cliente).filter_by(cpf="123.456.789-00").first()
    db.delete(cliente)  # Exclui o cliente da sessão do banco de dados
    db.commit()  # Comita a transação, removendo o cliente do banco de dados

    # Consulta novamente o cliente no banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="123.456.789-00").first()
    # Verifica se o cliente foi removido corretamente
    assert cliente_from_db is None

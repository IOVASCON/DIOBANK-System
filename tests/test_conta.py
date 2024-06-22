import pytest  # Importa a biblioteca pytest para criação e execução de testes
from src.models.conta import Conta  # Importa o modelo Conta
from src.models.cliente import Cliente  # Importa o modelo Cliente
from src.models.historico import Historico  # Importa o modelo Historico
from src.database import SessionLocal, init_db  # Importa a função de inicialização do banco de dados e a fábrica de sessões

# Fixture que inicializa o banco de dados e fornece uma sessão de banco de dados para os testes
@pytest.fixture(scope='module')
def db():
    init_db()  # Inicializa o banco de dados e cria as tabelas
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    yield db  # Fornece a sessão para os testes
    db.close()  # Fecha a sessão após os testes

# Teste para criação de uma conta
def test_create_conta(db):
    # Cria um novo cliente
    new_cliente = Cliente(nome="Teste Cliente", cpf="987.654.321-00", endereco="Avenida Teste", tipo="Pessoa Física")
    db.add(new_cliente)  # Adiciona o cliente à sessão do banco de dados
    db.commit()  # Comita a transação, salvando o cliente no banco de dados

    # Consulta o cliente recém-criado no banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="987.654.321-00").first()
    # Cria uma nova conta para o cliente
    new_conta = Conta(tipo="Pessoa Física", agencia="0001", num="1234", id_cliente=cliente_from_db.id, saldo=1000.0)
    db.add(new_conta)  # Adiciona a conta à sessão do banco de dados
    db.commit()  # Comita a transação, salvando a conta no banco de dados

    # Consulta a conta recém-criada no banco de dados
    conta_from_db = db.query(Conta).filter_by(num="1234").first()
    # Verifica se a conta foi encontrada e se os dados estão corretos
    assert conta_from_db is not None
    assert conta_from_db.tipo == "Pessoa Física"
    assert conta_from_db.agencia == "0001"
    assert conta_from_db.saldo == 1000.0

# Teste para criação de um histórico de transação
def test_create_historico(db):
    # Consulta a conta no banco de dados
    conta = db.query(Conta).filter_by(num="1234").first()
    # Cria um novo histórico de transação para a conta
    new_historico = Historico(historico="Depósito", saldo=1500.0, conta=conta)
    db.add(new_historico)  # Adiciona o histórico à sessão do banco de dados
    db.commit()  # Comita a transação, salvando o histórico no banco de dados

    # Consulta o histórico recém-criado no banco de dados
    historico_from_db = db.query(Historico).filter_by(conta_id=conta.id).first()
    # Verifica se o histórico foi encontrado e se os dados estão corretos
    assert historico_from_db is not None
    assert historico_from_db.historico == "Depósito"
    assert historico_from_db.saldo == 1500.0

# Teste para exclusão de uma conta e seu cliente
def test_delete_conta(db):
    # Consulta a conta no banco de dados
    conta = db.query(Conta).filter_by(num="1234").first()
    db.delete(conta)  # Exclui a conta da sessão do banco de dados
    db.commit()  # Comita a transação, removendo a conta do banco de dados

    # Consulta novamente a conta no banco de dados
    conta_from_db = db.query(Conta).filter_by(num="1234").first()
    # Verifica se a conta foi removida corretamente
    assert conta_from_db is None

    # Consulta o cliente no banco de dados
    cliente = db.query(Cliente).filter_by(cpf="987.654.321-00").first()
    db.delete(cliente)  # Exclui o cliente da sessão do banco de dados
    db.commit()  # Comita a transação, removendo o cliente do banco de dados

    # Consulta novamente o cliente no banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="987.654.321-00").first()
    # Verifica se o cliente foi removido corretamente
    assert cliente_from_db is None

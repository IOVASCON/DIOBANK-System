import pytest  # Importa a biblioteca pytest para criação e execução de testes
import tkinter as tk  # Importa a biblioteca tkinter para criar a interface gráfica
from src.ui.interface import App  # Importa a classe App da interface
from src.database import SessionLocal, init_db  # Importa a função de inicialização do banco de dados e a fábrica de sessões
from src.models.cliente import Cliente  # Importa o modelo Cliente
from src.models.conta import Conta  # Importa o modelo Conta

# Fixture que inicializa a aplicação e fornece uma instância da interface para os testes
@pytest.fixture(scope='module')
def app():
    root = tk.Tk()  # Cria a janela principal do tkinter
    app = App(root)  # Cria uma instância da classe App
    yield app  # Fornece a instância da interface para os testes
    root.destroy()  # Destroi a janela principal após os testes

# Fixture que inicializa o banco de dados e fornece uma sessão de banco de dados para os testes
@pytest.fixture(scope='module')
def db():
    init_db()  # Inicializa o banco de dados e cria as tabelas
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    yield db  # Fornece a sessão para os testes
    db.close()  # Fecha a sessão após os testes

# Teste para cadastrar um cliente através da interface
def test_cadastrar_cliente(app, db):
    app.cadastrar_cliente()  # Chama a função de cadastro de cliente na interface
    app.main_frame.winfo_children()[1].insert(0, "Teste Interface")  # Insere o nome do cliente
    app.main_frame.winfo_children()[3].insert(0, "111.222.333-44")  # Insere o CPF do cliente
    app.main_frame.winfo_children()[5].insert(0, "Rua de Teste")  # Insere o endereço do cliente
    app.main_frame.winfo_children()[7].set("Pessoa Física")  # Define o tipo de cliente
    app.main_frame.winfo_children()[9].invoke()  # Clica no botão de cadastro

    # Verifica se o cliente foi cadastrado no banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="111.222.333-44").first()
    assert cliente_from_db is not None
    assert cliente_from_db.nome == "Teste Interface"
    assert cliente_from_db.endereco == "Rua de Teste"
    assert cliente_from_db.tipo == "Pessoa Física"

# Teste para cadastrar uma conta através da interface
def test_cadastrar_conta(app, db):
    cliente_from_db = db.query(Cliente).filter_by(cpf="111.222.333-44").first()
    app.cadastrar_conta()  # Chama a função de cadastro de conta na interface
    app.main_frame.winfo_children()[1].set("Pessoa Física")  # Define o tipo de conta
    app.main_frame.winfo_children()[3].insert(0, "0001")  # Insere a agência da conta
    app.main_frame.winfo_children()[5].insert(0, cliente_from_db.cpf)  # Insere o CPF do cliente
    app.main_frame.winfo_children()[7].insert(0, "R$ 1000,00")  # Insere o saldo da conta
    app.main_frame.winfo_children()[9].invoke()  # Clica no botão de cadastro

    # Verifica se a conta foi cadastrada no banco de dados
    conta_from_db = db.query(Conta).filter_by(id_cliente=cliente_from_db.id).first()
    assert conta_from_db is not None
    assert conta_from_db.agencia == "0001"
    assert conta_from_db.saldo == 1000.0

# Teste para visualizar clientes através da interface
def test_visualizar_clientes(app):
    app.visualizar_clientes()  # Chama a função de visualização de clientes na interface
    assert app.main_frame.winfo_children()[0].cget("text") == "Clientes"  # Verifica se o título da tela é "Clientes"

# Teste para visualizar contas através da interface
def test_visualizar_contas(app):
    app.visualizar_contas()  # Chama a função de visualização de contas na interface
    assert app.main_frame.winfo_children()[0].cget("text") == "Contas"  # Verifica se o título da tela é "Contas"

# Teste para excluir um cliente através da interface
def test_excluir_cliente(app, db):
    app.excluir_cliente()  # Chama a função de exclusão de cliente na interface
    app.main_frame.winfo_children()[1].insert(0, "111.222.333-44")  # Insere o CPF do cliente
    app.main_frame.winfo_children()[3].invoke()  # Clica no botão de exclusão

    # Verifica se o cliente foi excluído do banco de dados
    cliente_from_db = db.query(Cliente).filter_by(cpf="111.222.333-44").first()
    assert cliente_from_db is None

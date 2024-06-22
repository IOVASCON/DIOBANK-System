from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

# A classe Cliente representa a tabela 'clientes' no banco de dados.
# Ela herda de Base, que é uma classe base declarativa do SQLAlchemy.
class Cliente(Base):
    __tablename__ = 'clientes'  # Define o nome da tabela no banco de dados
    
    # Define as colunas da tabela 'clientes'
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    nome = Column(String, index=True)  # Coluna para o nome do cliente
    cpf = Column(String(14), unique=True, index=True)  # Coluna para o CPF do cliente, deve ser único
    endereco = Column(String, index=True)  # Coluna para o endereço do cliente
    tipo = Column(String, index=True)  # Coluna para o tipo do cliente (Pessoa Física ou Pessoa Jurídica)
    
    # Define a relação com a tabela 'contas'
    contas = relationship("Conta", back_populates="cliente", cascade="all, delete-orphan")
    # A relação 'contas' indica que um cliente pode ter várias contas.
    # O parâmetro 'back_populates' define a propriedade na classe relacionada que completa esta relação.
    # O parâmetro 'cascade' define que as contas associadas serão deletadas se o cliente for deletado.

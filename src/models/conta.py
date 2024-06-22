from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from src.database import Base

# A classe Conta representa a tabela 'contas' no banco de dados.
# Ela herda de Base, que é uma classe base declarativa do SQLAlchemy.
class Conta(Base):
    __tablename__ = 'contas'  # Define o nome da tabela no banco de dados
    
    # Define as colunas da tabela 'contas'
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    tipo = Column(String)  # Coluna para o tipo da conta (Pessoa Física ou Pessoa Jurídica)
    agencia = Column(String)  # Coluna para a agência da conta
    num = Column(String(4))  # Número da conta com 4 dígitos
    id_cliente = Column(Integer, ForeignKey('clientes.id'))  # Chave estrangeira referenciando a tabela 'clientes'
    saldo = Column(Numeric)  # Coluna para o saldo da conta
    
    # Define a relação com a tabela 'clientes'
    cliente = relationship("Cliente", back_populates="contas")
    # A relação 'cliente' indica que cada conta pertence a um cliente.
    # O parâmetro 'back_populates' define a propriedade na classe relacionada que completa esta relação.
    
    # Define a relação com a tabela 'historico'
    historico = relationship("Historico", back_populates="conta", cascade="all, delete-orphan")
    # A relação 'historico' indica que uma conta pode ter várias entradas no histórico.
    # O parâmetro 'back_populates' define a propriedade na classe relacionada que completa esta relação.
    # O parâmetro 'cascade' define que os históricos associados serão deletados se a conta for deletada.

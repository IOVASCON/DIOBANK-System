from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime

# A classe Historico representa a tabela 'historicos' no banco de dados.
# Ela herda de Base, que é uma classe base declarativa do SQLAlchemy.
class Historico(Base):
    __tablename__ = 'historicos'  # Define o nome da tabela no banco de dados
    
    # Define as colunas da tabela 'historicos'
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    data = Column(DateTime, default=datetime.utcnow)  # Data da transação, com valor padrão sendo a data e hora atuais
    historico = Column(String)  # Descrição do histórico da transação
    saldo = Column(Numeric)  # Saldo após a transação
    conta_id = Column(Integer, ForeignKey('contas.id'))  # Chave estrangeira referenciando a tabela 'contas'
    
    # Define a relação com a tabela 'contas'
    conta = relationship("Conta", back_populates="historico")
    # A relação 'conta' indica que cada histórico pertence a uma conta.
    # O parâmetro 'back_populates' define a propriedade na classe relacionada que completa esta relação.

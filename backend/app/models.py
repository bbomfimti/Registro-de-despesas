from sqlalchemy import Column, Integer, String, Numeric

from .database import Base


class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    dia = Column(Integer, nullable=False)
    tipo = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DespesaBase(BaseModel):
    ano: int
    mes: int
    dia: int
    tipo: str
    descricao: str
    valor: Decimal


class DespesaCreate(DespesaBase):
    pass


class DespesaResponse(DespesaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

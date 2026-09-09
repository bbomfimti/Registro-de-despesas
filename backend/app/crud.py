from sqlalchemy.orm import Session

from . import models, schemas


def criar_despesa(
    db: Session,
    despesa: schemas.DespesaCreate
):
    db_despesa = models.Despesa(**despesa.model_dump())

    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)

    return db_despesa


def listar_despesas(db: Session):
    return db.query(models.Despesa).all()

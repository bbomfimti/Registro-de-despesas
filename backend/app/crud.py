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

def remover_despesa(db: Session, despesa_id: int):
    despesa = (
        db.query(models.Despesa)
        .filter(models.Despesa.id == despesa_id)
        .first()
    )

    if despesa is None:
        return None

    db.delete(despesa)
    db.commit()

    return despesa

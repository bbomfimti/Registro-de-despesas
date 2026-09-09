from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Registro de Despesas API",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "registro-de-despesas-api"
    }


@app.post("/despesas", response_model=schemas.DespesaResponse)
def criar_despesa(
    despesa: schemas.DespesaCreate,
    db: Session = Depends(get_db)
):
    return crud.criar_despesa(db, despesa)


@app.get("/despesas", response_model=list[schemas.DespesaResponse])
def listar_despesas(
    db: Session = Depends(get_db)
):
    return crud.listar_despesas(db)

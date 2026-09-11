from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal

app = FastAPI(
    title="Registro de Despesas API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post("/api/despesas", response_model=schemas.DespesaResponse)
def criar_despesa(
    despesa: schemas.DespesaCreate,
    db: Session = Depends(get_db)
):
    return crud.criar_despesa(db, despesa)


@app.get("/api/despesas", response_model=list[schemas.DespesaResponse])
def listar_despesas(
    db: Session = Depends(get_db)
):
    return crud.listar_despesas(db)


@app.delete("/api/despesas/{despesa_id}")
def remover_despesa(
    despesa_id: int,
    db: Session = Depends(get_db)
):
    despesa = crud.remover_despesa(db, despesa_id)

    if despesa is None:
        raise HTTPException(
            status_code=404,
            detail="Despesa não encontrada"
        )

    return {
        "message": "Despesa removida com sucesso",
        "id": despesa_id
    }
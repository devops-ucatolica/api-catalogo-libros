from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional
from datetime import datetime
import os, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Catálogo de Libros",
    description="CRUD de Libros con FastAPI y despliegue en Azure",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db: Dict[int, Dict] = {
    1: {"id": 1, "titulo": "Don Quijote", "autor": "Cervantes", "isbn": "9788491050296"},
    2: {"id": 2, "titulo": "Cien años de soledad", "autor": "García Márquez", "isbn": "9780307474728"},
}

class Libro(BaseModel):
    titulo: str
    autor: str
    isbn: str
    anio_publicacion: Optional[int] = None
    genero: Optional[str] = None

@app.get("/")
def root():
    return {"status": "ok", "total_libros": len(db)}

@app.get("/libros")
def listar_libros():
    return list(db.values())

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def crear_libro(libro: Libro):
    nuevo_id = max(db.keys()) + 1 if db else 1
    db[nuevo_id] = {"id": nuevo_id, **libro.model_dump()}
    return db[nuevo_id]

import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# --- Configuración de Base de Datos ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/users_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Modelo de Base de Datos ---
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

# --- Esquemas Pydantic ---
class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True

# --- Métricas de Prometheus ---
usuarios_creados_total = Counter(
    "usuarios_creados_total",
    "Total de usuarios creados en el sistema"
)

# --- Instancia FastAPI ---
app = FastAPI(
    title="User CRUD & Monitoring API",
    description="API con soporte de persistencia en PostgreSQL y métricas de Prometheus"
)

# Inyección de dependencia para la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoint de Métricas ---
@app.get("/metrics")
def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# --- Rutas CRUD de Usuarios ---
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Incrementa la métrica para Prometheus
    usuarios_creados_total.inc()
    return db_user

@app.get("/users", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(UserModel).offset(skip).limit(limit).all()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
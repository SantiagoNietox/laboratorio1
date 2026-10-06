from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Base
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Inicialización de la API con documentación en español
app = FastAPI(
    title="API de Gestión de Usuarios y Monitoreo",
    description="Sistema CRUD para la administración de usuarios con métricas para Prometheus",
    version="1.0.0"
)

# Métrica para contar los usuarios creados
USER_CREATED = Counter("usuarios_creados_total", "Cantidad total de usuarios registrados")

# Creación de tablas en la base de datos
Base.metadata.create_all(bind=engine)

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/usuarios", summary="Obtener lista de usuarios", tags=["Usuarios"])
def obtener_usuarios(db: Session = Depends(obtener_db)):
    """Retorna todos los usuarios registrados en la base de datos."""
    return db.query(User).all()

@app.post("/usuarios", summary="Crear un nuevo usuario", tags=["Usuarios"])
def crear_usuario(
    nombre: str = Query(..., description="Nombre del usuario"),
    edad: int = Query(..., description="Edad del usuario"),
    db: Session = Depends(obtener_db)
):
    """Registra un nuevo usuario e incrementa el contador de métricas."""
    usuario = User(name=nombre, age=edad)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    USER_CREATED.inc()
    return {
        "mensaje": "Usuario creado con éxito",
        "id": usuario.id,
        "nombre": usuario.name,
        "edad": usuario.age
    }

@app.get("/metricas", summary="Métricas de Prometheus", tags=["Monitoreo"])
def metricas():
    """Expone las métricas para ser recolectadas por Prometheus."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
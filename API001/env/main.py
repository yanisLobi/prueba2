from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# --- CONEXIÓN A LA BASE DE DATOS ---
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/db_escuela"  # Cambia TU_CONTRASEÑA por la tuya
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- INICIALIZAR FASTAPI Y CORS ---
app = FastAPI(title="API Escolar - Alumnos y Maestros")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 1. MODELOS Y CRUD DE ALUMNOS
# ==========================================

class Alumno(Base):
    __tablename__ = "alumnos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    carrera = Column(String(100), nullable=False)

class AlumnoSchema(BaseModel):
    nombre: str = Field(..., min_length=2)
    edad: int = Field(..., ge=16, le=99)
    carrera: str

class AlumnoOut(AlumnoSchema):
    id: int

    class Config:
        from_attributes = True


@app.post("/alumnos/", response_model=AlumnoOut)
def crear_alumno(datos: AlumnoSchema):
    db = SessionLocal()
    nuevo = Alumno(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return nuevo

@app.get("/alumnos/", response_model=List[AlumnoOut])
def listar_alumnos():
    db = SessionLocal()
    resultado = db.query(Alumno).all()
    db.close()
    return resultado

@app.get("/alumnos/{id}", response_model=AlumnoOut)
def obtener_alumno(id: int):
    db = SessionLocal()
    alumno = db.query(Alumno).filter(Alumno.id == id).first()
    db.close()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno

@app.put("/alumnos/{id}", response_model=AlumnoOut)
def actualizar_alumno(id: int, datos: AlumnoSchema):
    db = SessionLocal()
    alumno = db.query(Alumno).filter(Alumno.id == id).first()
    if not alumno:
        db.close()
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    for key, value in datos.dict().items():
        setattr(alumno, key, value)
    db.commit()
    db.refresh(alumno)
    db.close()
    return alumno

@app.delete("/alumnos/{id}")
def eliminar_alumno(id: int):
    db = SessionLocal()
    alumno = db.query(Alumno).filter(Alumno.id == id).first()
    if not alumno:
        db.close()
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    db.delete(alumno)
    db.commit()
    db.close()
    return {"mensaje": "Alumno eliminado"}


# ==========================================
# 2. MODELOS Y CRUD DE MAESTROS (RETO)
# ==========================================

class Maestro(Base):
    __tablename__ = "maestros"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=False)
    experiencia = Column(Integer, nullable=False)
    correo = Column(String(100), nullable=False)

class MaestroSchema(BaseModel):
    nombre: str = Field(..., min_length=2)
    especialidad: str = Field(..., min_length=3)
    experiencia: int = Field(..., ge=0, le=50)
    correo: EmailStr

class MaestroOut(MaestroSchema):
    id: int

    class Config:
        from_attributes = True


@app.post("/maestros/", response_model=MaestroOut)
def crear_maestro(datos: MaestroSchema):
    db = SessionLocal()
    nuevo = Maestro(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return nuevo

@app.get("/maestros/", response_model=List[MaestroOut])
def listar_maestros():
    db = SessionLocal()
    resultado = db.query(Maestro).all()
    db.close()
    return resultado

@app.get("/maestros/{id}", response_model=MaestroOut)
def obtener_maestro(id: int):
    db = SessionLocal()
    maestro = db.query(Maestro).filter(Maestro.id == id).first()
    db.close()
    if not maestro:
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    return maestro

@app.put("/maestros/{id}", response_model=MaestroOut)
def actualizar_maestro(id: int, datos: MaestroSchema):
    db = SessionLocal()
    maestro = db.query(Maestro).filter(Maestro.id == id).first()
    if not maestro:
        db.close()
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    for key, value in datos.dict().items():
        setattr(maestro, key, value)
    db.commit()
    db.refresh(maestro)
    db.close()
    return maestro

@app.delete("/maestros/{id}")
def eliminar_maestro(id: int):
    db = SessionLocal()
    maestro = db.query(Maestro).filter(Maestro.id == id).first()
    if not maestro:
        db.close()
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    db.delete(maestro)
    db.commit()
    db.close()
    return {"mensaje": "Maestro eliminado"}


# --- CREAR TABLAS EN LA BASE DE DATOS ---
Base.metadata.create_all(bind=engine)
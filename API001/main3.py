from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict

app = FastAPI()

class Alumno(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    edad: int = Field(..., ge=5, le=100)
    correo: EmailStr
    grupo: str = Field(..., min_length=1)
    origen: Optional[str] = None


base_alumnos: List[Alumno] = []

@app.post("/registrar")
def registrar_alumno(alumno: Alumno):
    if any(a.correo == alumno.correo for a in base_alumnos):
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    base_alumnos.append(alumno)
    return {"mensaje": f"Alumno {alumno.nombre} registrado correctamente en el grupo {alumno.grupo}"}


@app.get("/listar")
def listar_alumnos(grupo: Optional[str] = None, edad_minima: Optional[int] = None):
    resultado = base_alumnos
    if grupo:
        resultado = [a for a in resultado if a.grupo == grupo]
    if edad_minima:
        resultado = [a for a in resultado if a.edad >= edad_minima]
    return resultado

@app.get("/estadisticas")
def obtener_estadisticas():
    
    total_alumnos = len(base_alumnos)
    
   
    total_por_grupo: Dict[str, int] = {}
    total_por_origen: Dict[str, int] = {}
    
    for a in base_alumnos:
    
        total_por_grupo[a.grupo] = total_por_grupo.get(a.grupo, 0) + 1
        
        origen_key = a.origen if a.origen else "no especificada"
        total_por_origen[origen_key] = total_por_origen.get(origen_key, 0) + 1
        
    return {
        "total_alumnos": total_alumnos,
        "total_por_grupo": total_por_grupo,
        "total_por_origen": total_por_origen
        fgsd
    }
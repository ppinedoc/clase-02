from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from typing import List

app = FastAPI()

# Database connection
DATABASE = "veterinaria.db"

def init_db():
    """Inicializa la base de datos con las tablas"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla de servicios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            costo REAL NOT NULL
        )
    """)
    
    # Tabla de atenciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atenciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_dueño TEXT NOT NULL,
            mascota TEXT NOT NULL,
            servicio_id INTEGER NOT NULL,
            fecha_servicio DATETIME NOT NULL,
            FOREIGN KEY (servicio_id) REFERENCES servicios(id)
        )
    """)
    
    conn.commit()
    conn.close()

# Modelos Pydantic
class Servicio(BaseModel):
    nombre: str
    costo: float

class ServicioResponse(BaseModel):
    id: int
    nombre: str
    costo: float

class Atencion(BaseModel):
    nombre_dueño: str
    mascota: str
    servicio_id: int

class AtencionResponse(BaseModel):
    id: int
    nombre_dueño: str
    mascota: str
    servicio_id: int
    fecha_servicio: str

# Inicializar base de datos al arrancar
init_db()

# ENDPOINTS

@app.post("/servicios", response_model=ServicioResponse)
def agregar_servicio(servicio: Servicio):
    """Agrega un nuevo servicio a la veterinaria"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO servicios (nombre, costo) VALUES (?, ?)",
            (servicio.nombre, servicio.costo)
        )
        
        conn.commit()
        servicio_id = cursor.lastrowid
        conn.close()
        
        return ServicioResponse(
            id=servicio_id,
            nombre=servicio.nombre,
            costo=servicio.costo
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El servicio ya existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/servicios", response_model=List[ServicioResponse])
def listar_servicios():
    """Lista todos los servicios disponibles"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre, costo FROM servicios")
        servicios = cursor.fetchall()
        conn.close()
        
        return [
            ServicioResponse(id=s[0], nombre=s[1], costo=s[2])
            for s in servicios
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/atenciones", response_model=AtencionResponse)
def agregar_atencion(atencion: Atencion):
    """Agrega una nueva atención. La fecha se captura automáticamente del servidor"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verificar que el servicio existe
        cursor.execute("SELECT id FROM servicios WHERE id = ?", (atencion.servicio_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        
        # Capturar fecha actual del servidor
        fecha_servicio = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO atenciones (nombre_dueño, mascota, servicio_id, fecha_servicio) VALUES (?, ?, ?, ?)",
            (atencion.nombre_dueño, atencion.mascota, atencion.servicio_id, fecha_servicio)
        )
        
        conn.commit()
        atencion_id = cursor.lastrowid
        conn.close()
        
        return AtencionResponse(
            id=atencion_id,
            nombre_dueño=atencion.nombre_dueño,
            mascota=atencion.mascota,
            servicio_id=atencion.servicio_id,
            fecha_servicio=fecha_servicio
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/atenciones", response_model=List[AtencionResponse])
def listar_atenciones():
    """Lista todas las atenciones registradas"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre_dueño, mascota, servicio_id, fecha_servicio FROM atenciones")
        atenciones = cursor.fetchall()
        conn.close()
        
        return [
            AtencionResponse(
                id=a[0],
                nombre_dueño=a[1],
                mascota=a[2],
                servicio_id=a[3],
                fecha_servicio=a[4]
            )
            for a in atenciones
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    """Endpoint raíz para verificar que el servidor está activo"""
    return {"mensaje": "Backend Veterinaria activo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

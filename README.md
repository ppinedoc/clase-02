# Backend Veterinaria - FastAPI

Backend sencillo para una veterinaria usando FastAPI y SQLite.

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
python main.py
```

El servidor estará disponible en: `http://localhost:8000`

## Documentación Interactiva

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Disponibles

### Servicios

**Agregar servicio**
- `POST /servicios`
- Body:
```json
{
  "nombre": "Vacunación",
  "costo": 50.00
}
```

**Listar servicios**
- `GET /servicios`

### Atenciones

**Agregar atención**
- `POST /atenciones`
- Body:
```json
{
  "nombre_dueño": "Juan Pérez",
  "mascota": "Max",
  "servicio_id": 1
}
```
La fecha se captura automáticamente del servidor.

**Listar atenciones**
- `GET /atenciones`

## Base de Datos

Se utiliza SQLite. El archivo `veterinaria.db` se crea automáticamente al ejecutar la aplicación.

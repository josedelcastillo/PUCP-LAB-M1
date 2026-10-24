# PUCP-LAB-M1

API de inventario en memoria construida con FastAPI y Python 3.12.

## Qué hace la API

Mantiene una lista de items en memoria y permite consultar y retirar stock.

| Método | Ruta                    | Descripción                                                       |
|--------|-------------------------|-------------------------------------------------------------------|
| GET    | `/health`               | Estado del servicio: `{"status": "ok"}`                           |
| GET    | `/items`                | Lista de items con `id`, `name` y `qty`                           |
| POST   | `/items/{id}/withdraw`  | Retira stock. Body: `{"qty": 3}`. Responde 400 si no hay stock suficiente y 404 si el item no existe |
| GET    | `/version`              | Versión y entorno: `{"version": "...", "env": "..."}`             |
| GET    | `/debug/config`         | Configuración activa del servicio                                 |

Variables de entorno:

| Variable             | Uso                                          | Valor por defecto |
|----------------------|----------------------------------------------|-------------------|
| `APP_VERSION`        | Versión que reporta `/version`               | `dev`             |
| `APP_ENV`            | Entorno que reporta `/version`               | `local`           |
| `NOTIFY_WEBHOOK_URL` | URL que recibe un aviso cuando el stock baja | sin definir       |

La documentación interactiva queda disponible en `http://localhost:8000/docs`.

## Cómo correrla en local

Requisitos: Python 3.12 y `make`.

```bash
make install   # crea .venv e instala dependencias
make run       # levanta uvicorn con recarga en http://localhost:8000
```

Ejemplo:

```bash
curl http://localhost:8000/items
curl -X POST http://localhost:8000/items/1/withdraw \
  -H "Content-Type: application/json" -d '{"qty": 2}'
```

También se puede abrir el repositorio en un Dev Container: el entorno ejecuta `make install` al crearse y expone el puerto 8000.

Otros comandos disponibles:

| Comando             | Descripción                                          |
|---------------------|------------------------------------------------------|
| `make lint`         | Revisa estilo y formato con ruff                     |
| `make docker-build` | Construye la imagen de contenedor                    |
| `make site`         | Genera una página estática con la versión en `site/` |

## Cómo correr los tests

```bash
make test
```

Ejecuta pytest sobre `tests/` y muestra el reporte de cobertura del paquete `app/`.

## Estructura del repositorio

```
.
├── app/
│   ├── main.py          # definición de rutas FastAPI
│   ├── inventory.py     # lógica del inventario
│   ├── config.py        # parámetros de configuración
│   ├── notify.py        # avisos de stock bajo vía webhook
│   └── version.py       # versión y entorno
├── tests/
│   └── test_api.py      # tests de la API
├── scripts/
│   └── build_site.py    # generador de la página estática
├── .devcontainer/
│   └── devcontainer.json
├── Dockerfile
├── Makefile
├── pyproject.toml       # configuración de ruff y pytest
├── requirements.txt
└── requirements-dev.txt
```

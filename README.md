# PUCP-LAB-M1

API de inventario en memoria construida con **FastAPI** (Python 3.12).

## Endpoints

| Método | Ruta                       | Descripción                                                      |
|--------|----------------------------|------------------------------------------------------------------|
| GET    | `/health`                  | Estado del servicio → `{"status": "ok"}`                         |
| GET    | `/items`                   | Lista de items `{id, name, qty}`                                 |
| POST   | `/items/{id}/withdraw`     | Body `{"qty": int}`. Descuenta stock. `400` sin stock, `404` si no existe |
| GET    | `/version`                 | `{"version": APP_VERSION or "dev", "env": APP_ENV or "local"}`   |
| GET    | `/debug/config`            | Configuración activa del servicio                                |

## Variables de entorno

| Variable             | Uso                                         | Default |
|----------------------|---------------------------------------------|---------|
| `APP_VERSION`        | Versión reportada por `/version`            | `dev`   |
| `APP_ENV`            | Entorno reportado por `/version`            | `local` |
| `NOTIFY_WEBHOOK_URL` | Webhook que recibe alertas de stock bajo    | —       |

## Estructura

```
app/
  main.py        # rutas FastAPI
  inventory.py   # lógica de inventario
  config.py      # configuración
  notify.py      # alertas de stock bajo vía webhook
  version.py     # versión y entorno
tests/
  test_api.py
scripts/
  build_site.py  # genera el sitio estático en site/
```

## Desarrollo local

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

uvicorn app.main:app --reload
# http://localhost:8000/docs
```

## Calidad

```bash
pytest --cov=app --cov-report=term-missing   # tests + cobertura
ruff check .                                 # lint
ruff format --check .                        # formato
bandit -c pyproject.toml -r app              # análisis estático de seguridad
pip-audit -r requirements.txt                # vulnerabilidades en dependencias
pre-commit install                           # hooks locales
```

## Contenedor

```bash
docker build --build-arg APP_VERSION=v0.1.0 -t pucp-lab-m1 .
docker run --rm -p 8000:8000 -e APP_ENV=staging pucp-lab-m1
```

## Sitio estático

```bash
python scripts/build_site.py --version v1.0.0 --env staging
python scripts/build_site.py --version v1.0.0 --env production
```

Genera `site/index.html` y `site/version.json`.

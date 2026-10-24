"""Información de versión y entorno de despliegue."""

import os


def get_version() -> dict[str, str]:
    return {
        "version": os.getenv("APP_VERSION", "dev"),
        "env": os.getenv("APP_ENV", "local"),
    }

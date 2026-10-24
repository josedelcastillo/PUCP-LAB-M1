"""Notificaciones de stock bajo vía webhook."""

import logging
import os
from datetime import UTC, datetime

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 5


def _webhook_url() -> str | None:
    return os.getenv("NOTIFY_WEBHOOK_URL")


def build_payload(item: dict) -> dict:
    return {
        "event": "low_stock",
        "item_id": item["id"],
        "name": item["name"],
        "qty": item["qty"],
        "sent_at": datetime.now(UTC).isoformat(),
    }


def notify_low_stock(item: dict) -> bool:
    """Envía un POST al webhook configurado. Devuelve True si se entregó."""
    url = _webhook_url()
    if not url:
        return False

    payload = build_payload(item)
    try:
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("No se pudo notificar stock bajo de %s: %s", item["id"], exc)
        return False

    logger.info("Notificación de stock bajo enviada para %s", item["id"])
    return True

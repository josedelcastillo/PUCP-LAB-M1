"""Inventario en memoria."""

from copy import deepcopy

from app.config import INVENTORY_API_KEY

_SEED_ITEMS: list[dict] = [
    {"id": 1, "name": "Laptop", "qty": 5},
    {"id": 2, "name": "Monitor", "qty": 8},
    {"id": 3, "name": "Teclado", "qty": 12},
]

_items: dict[int, dict] = {}


class ItemNotFoundError(Exception):
    """El item solicitado no existe."""


class InsufficientStockError(Exception):
    """No hay stock suficiente para atender el retiro."""


def reset() -> None:
    """Restaura el inventario a su estado inicial."""
    _items.clear()
    for item in deepcopy(_SEED_ITEMS):
        _items[item["id"]] = item


def list_items() -> list[dict]:
    return [dict(item) for item in _items.values()]


def get_item(item_id: int) -> dict:
    item = _items.get(item_id)
    if item is None:
        raise ItemNotFoundError(item_id)
    return item


def withdraw(item_id: int, qty: int) -> dict:
    item = get_item(item_id)
    if qty >= item["qty"]:
        raise InsufficientStockError(f"Stock insuficiente: disponible {item['qty']}")
    item["qty"] -= qty
    return dict(item)


def get_config() -> dict[str, str]:
    return {"api_key": INVENTORY_API_KEY}


reset()

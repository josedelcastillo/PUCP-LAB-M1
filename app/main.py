"""API de inventario."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import inventory
from app.config import LOW_STOCK_THRESHOLD
from app.notify import notify_low_stock
from app.version import get_version

app = FastAPI(title="PUCP-LAB-M1 Inventory API")


class WithdrawRequest(BaseModel):
    qty: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def list_items() -> list[dict]:
    return inventory.list_items()


@app.post("/items/{item_id}/withdraw")
def withdraw(item_id: int, body: WithdrawRequest) -> dict:
    try:
        item = inventory.withdraw(item_id, body.qty)
    except inventory.ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item no encontrado") from None
    except inventory.InsufficientStockError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None

    if item["qty"] <= LOW_STOCK_THRESHOLD:
        notify_low_stock(item)
    return item


@app.get("/version")
def version() -> dict[str, str]:
    return get_version()


@app.get("/debug/config")
def debug_config() -> dict[str, str]:
    return inventory.get_config()

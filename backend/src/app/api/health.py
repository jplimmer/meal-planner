"""Liveness endpoint: is this process up and serving?

Deliberately does not touch storage, so a slow query cannot take the container
healthcheck down with it.
"""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class Health(BaseModel):
    status: Literal["ok"]


@router.get("/health")
async def read_health() -> Health:
    return Health(status="ok")

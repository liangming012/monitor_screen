from typing import Any
from fastapi import APIRouter
router = APIRouter()


@router.get("/")
def healthy(
) -> Any:
    """
    check healthy
    """

    return {"status": "healthy"}


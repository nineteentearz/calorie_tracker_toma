import json
from pathlib import Path
from uuid import UUID
from typing import Optional
from ..config import SESSION_FILE

def save_current_user_id(user_id: UUID) -> None:
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": str(user_id)}, f)

def get_current_user_id() -> Optional[UUID]:
    if not SESSION_FILE.exists():
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return UUID(data["user_id"])

def clear_session() -> None:
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
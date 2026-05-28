import json
from functools import lru_cache
from pathlib import Path
from app.config import DATA_DIR

@lru_cache(maxsize=None)
def load_json(name: str):
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def by_id(items: list[dict], key: str):
    return {item[key]: item for item in items}

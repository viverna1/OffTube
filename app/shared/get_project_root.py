# get_project_root.py
from pathlib import Path

def get_project_root(marker='requirements.txt') -> str | None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker).exists():
            return str(parent)
    return None

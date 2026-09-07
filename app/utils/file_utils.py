# file_utils.py
import os
import logging
from pathlib import Path

from app.application.config_service import configService

log = logging.getLogger(__name__)

def get_file_name(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]


def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)


def validate_application_path() -> bool:
    app_path = get_project_root()
    config_app_path = configService.get_setting("application_path")
    if config_app_path != app_path:
        log.warning(f"Wrong application path: {config_app_path}")

        configService.set_setting("application_path", app_path)

        log.warning(f"The new path is set: {app_path}")
        return False
    return True


def get_project_root(marker='requirements.txt') -> str | None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker).exists():
            return str(parent)
    return None
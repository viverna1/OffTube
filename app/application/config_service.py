# config_service.py
import logging
from typing import Any

from app.infrastructure.repository.config_repository import ConfigRepository
from app.shared.get_project_root import get_project_root


log = logging.getLogger(__name__)

class ConfigService:
    def __init__(self, config_repository: ConfigRepository):
        self._repo = config_repository

    def get_setting(self, key: str) -> Any:
        return self._repo.get_setting(key)

    def get_all(self) -> dict:
        return self._repo.get_all()

    def set_setting(self, key: str, value: Any) -> None:
        self._repo.set_setting(key, value)
  
    def fix_application_path(self) -> None:
      app_path = get_project_root()
      
      config_app_path = self._repo.get_setting('application_path')

      if config_app_path != app_path:
          log.warning(f"Wrong application path: {config_app_path}")

          self._repo.set_setting('application_path', app_path)

          log.warning(f"The new path is set: {app_path}")

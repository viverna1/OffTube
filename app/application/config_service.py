# config_service.py
from app.infrastructure.config_storage import ConfigStorage
from app.shared.get_project_root import get_project_root

import logging

log = logging.getLogger(__name__)

class ConfigService:
    def __init__(self, config_storage: ConfigStorage):
        self._storage = config_storage
  
    def fix_application_path(self) -> None:
      app_path = get_project_root()
      
      config_app_path = self._storage.get_setting('application_path')

      if config_app_path != app_path:
          log.warning(f"Wrong application path: {config_app_path}")

          self._storage.set_setting('application_path', app_path)

          log.warning(f"The new path is set: {app_path}")

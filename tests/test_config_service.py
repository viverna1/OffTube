# test_config_service.py
import pytest

from app.infrastructure.file_storage import FileStorage
from app.infrastructure.config_storage import ConfigStorage
from app.application.config_service import ConfigService

FUCK = "G:\\Git\\Dev\\OffTube"


# ==================== Fixtures ====================

@pytest.fixture
def mock_cache_storage(mocker):
    mock_load = mocker.patch.object(FileStorage, 'load', return_value={ "application_path": "X:\\OffTube" })
    mock_save = mocker.patch.object(FileStorage, 'save_in_file')
    return mock_load, mock_save

@pytest.fixture
def file_storage(mock_cache_storage):
    return FileStorage("")

@pytest.fixture
def config_storage(file_storage):
    return ConfigStorage(file_storage)

@pytest.fixture
def config_service(config_storage):
    return ConfigService(config_storage)


# ==================== Tests ====================

def test_fix_app_path(config_service, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage
    config_service.fix_application_path()
    mock_save.assert_called_once_with({"application_path": FUCK})

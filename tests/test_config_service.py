# test_config_service.py
import pytest

from app.infrastructure.repository.json_repository import JsonRepository
from app.infrastructure.repository.config_repository import ConfigRepository
from app.application.config_service import ConfigService

FUCK = "G:\\Git\\Dev\\OffTube"


# ==================== Fixtures ====================

@pytest.fixture
def mock_cache_repository(mocker):
    mock_load = mocker.patch.object(JsonRepository, 'load', return_value={ "application_path": "X:\\OffTube" })
    mock_save = mocker.patch.object(JsonRepository, 'save_in_file')
    return mock_load, mock_save

@pytest.fixture
def json_repository(mock_cache_repository):
    return JsonRepository("")

@pytest.fixture
def config_repository(json_repository):
    return ConfigRepository(json_repository)

@pytest.fixture
def config_service(config_repository):
    return ConfigService(config_repository)


# ==================== Tests ====================

def test_fix_app_path(config_service, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository
    config_service.fix_application_path()
    mock_save.assert_called_once_with({"application_path": FUCK})

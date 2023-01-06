from decouple import Config
from unittest.mock import MagicMock, patch
from func.src.domain.models.device_info import DeviceInfo


@patch.object(Config, "__call__")
def test_init(mocked_env):
    dummy = MagicMock()
    DeviceInfo.__init__(dummy, dummy, dummy)
    dummy.device_info.update.assert_not_called()


@patch.object(Config, "__call__")
def test_init_no_precision(mocked_env):
    dummy = MagicMock()
    dummy.get.return_value = None
    mocked_env.return_value = 1
    DeviceInfo.__init__(dummy, dummy, dummy)
    dummy.device_info.update.assert_called_once_with({"precision": 1.0})

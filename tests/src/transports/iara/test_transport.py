from unittest.mock import MagicMock, patch

import pytest
from etria_logger import Gladsheim
from iara_client import Iara

from func.src.transports.iara.transport import IaraTransport

stub_user = MagicMock()


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
@patch.object(Gladsheim, "error")
async def test_send_to_sinacor_update_queue(mocked_logger, mocked_lib):
    mocked_lib.return_value = True, None
    await IaraTransport.send_to_sinacor_update_queue(stub_user)
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
@patch.object(Gladsheim, "error")
async def test_send_to_sinacor_update_queue_with_errors(mocked_logger, mocked_lib):
    dummy_value = "value"
    mocked_lib.return_value = False, dummy_value
    await IaraTransport.send_to_sinacor_update_queue(stub_user)
    mocked_logger.assert_called_once()


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
@patch.object(Gladsheim, "error")
async def test_send_to_drive_wealth_update_queue(mocked_logger, mocked_lib):
    mocked_lib.return_value = True, None
    await IaraTransport.send_to_drive_wealth_update_queue(stub_user)
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
@patch.object(Gladsheim, "error")
async def test_send_to_drive_wealth_update_queue_with_errors(mocked_logger, mocked_lib):
    dummy_value = "value"
    mocked_lib.return_value = False, dummy_value
    await IaraTransport.send_to_drive_wealth_update_queue(stub_user)
    mocked_logger.assert_called_once()

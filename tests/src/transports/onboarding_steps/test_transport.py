# Standards
from http import HTTPStatus
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

# Third party
from decouple import config
from etria_logger import Gladsheim
from httpx import AsyncClient

from func.src.domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk
from func.src.transports.onboarding_steps.transport import OnboardingSteps


dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__")
@patch.object(Gladsheim, "error")
async def test_get_customer_steps(
    mocked_logger,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.get = AsyncMock()
    mocked_client_enter.return_value.get.return_value = MagicMock()
    mocked_client_enter.return_value.get.return_value.status_code = HTTPStatus.OK
    result = await OnboardingSteps._get_customer_steps(dummy_value, dummy_value)
    mocked_client_enter.return_value.get.assert_called_once_with(
        dummy_value, headers={"x-thebes-answer": dummy_value}
    )
    mocked_logger.assert_not_called()
    assert result == (
        mocked_client_enter.return_value.get.return_value.json.return_value.get.return_value.get.return_value
    )


def raise_second(*args):
    raise args[1]


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Gladsheim, "error")
async def test_get_customer_steps_with_error(
    mocked_logger,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.get = AsyncMock()
    mocked_client_enter.return_value.get.return_value = MagicMock()
    mocked_client_enter.return_value.get.return_value.status_code = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
    with pytest.raises(OnboardingStepsStatusCodeNotOk):
        await OnboardingSteps._get_customer_steps(dummy_value, dummy_value)
    mocked_client_enter.return_value.get.assert_called_once_with(
        dummy_value, headers={"x-thebes-answer": dummy_value}
    )
    mocked_logger.assert_called_once_with(
        message=OnboardingStepsStatusCodeNotOk.msg,
        status=mocked_client_enter.return_value.get.return_value.status_code,
        content=mocked_client_enter.return_value.get.return_value.content,
    )

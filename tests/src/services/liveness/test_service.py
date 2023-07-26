from unittest.mock import MagicMock, patch

import pytest
from decouple import Config
from koh import Koh, KohStatus

from func.src.domain.exceptions.exceptions import ErrorInLiveness, LivenessRejected
from func.src.services.liveness import LivenessService


@pytest.mark.asyncio
@patch.object(Koh, "check_face")
@patch.object(Config, "__call__")
async def test_validate(mocked_env, mocked_validator):
    dummy = MagicMock()
    mocked_validator.return_value = True, KohStatus.SUCCESS
    await LivenessService.validate(dummy, dummy)
    mocked_validator.assert_called_once_with(
        dummy, dummy.liveness, mocked_env.return_value
    )


@pytest.mark.asyncio
@patch.object(Koh, "check_face")
@patch.object(Config, "__call__")
async def test_validate_koh_error(mocked_env, mocked_validator):
    dummy = MagicMock()
    mocked_validator.return_value = True, None
    with pytest.raises(ErrorInLiveness):
        await LivenessService.validate(dummy, dummy)
    mocked_validator.assert_called_once_with(
        dummy, dummy.liveness, mocked_env.return_value
    )


@pytest.mark.asyncio
@patch.object(Koh, "check_face")
@patch.object(Config, "__call__")
async def test_validate_koh_rejected(mocked_env, mocked_validator):
    dummy = MagicMock()
    mocked_validator.return_value = False, KohStatus.SUCCESS
    with pytest.raises(LivenessRejected):
        await LivenessService.validate(dummy, dummy)
    mocked_validator.assert_called_once_with(
        dummy, dummy.liveness, mocked_env.return_value
    )

from unittest.mock import MagicMock, patch

import pytest
from koh import Koh, KohStatus

from src.domain.exceptions.exceptions import ErrorInLiveness, LivenessRejected
from src.services.liveness import LivenessService


@pytest.mark.asyncio
@patch.object(Koh, "check_face")
async def test_validate(mocked_validator):
    dummy = MagicMock()
    mocked_validator.return_value = True, KohStatus.SUCCESS
    await LivenessService.validate(dummy, dummy)
    mocked_validator.assert_called_once_with(
        dummy, dummy.liveness
    )


@pytest.mark.asyncio
@patch.object(Koh, "check_face")
async def test_validate_koh_error(mocked_validator):
    dummy = MagicMock()
    mocked_validator.return_value = True, None
    with pytest.raises(ErrorInLiveness):
        await LivenessService.validate(dummy, dummy)
    mocked_validator.assert_called_once_with(
        dummy, dummy.liveness
    )


@pytest.mark.asyncio
@patch.object(Koh, "check_face")
async def test_validate_koh_rejected(mocked_validator):
    dummy = MagicMock()
    mocked_validator.return_value = False, KohStatus.SUCCESS
    with pytest.raises(LivenessRejected):
        await LivenessService.validate(dummy, dummy)
    mocked_validator.assert_called_once_with(
        dummy, dummy.liveness
    )

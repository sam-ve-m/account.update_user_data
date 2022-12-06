from unittest.mock import patch

import pytest

from func.src.domain.exceptions.exceptions import ErrorOnDecodeJwt
from func.src.services.jwt import JwtService
from tests.src.services.jwt.stubs import (
    stub_heimdall_response,
    stub_heimdall_response_failure,
)


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.Heimdall.decode_payload", return_value=stub_heimdall_response
)
async def test_when_valid_jwt_then_return_user_unique_id(mock_heimdall):
    result = await JwtService.decode_jwt(jwt="123")

    assert isinstance(result, dict)
    assert result == {"user": {"unique_id": "451baf5a-9cd5-4037-aa17-fbd0fcef66c8"}}


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.Heimdall.decode_payload",
    return_value=stub_heimdall_response_failure,
)
async def test_when_invalid_jwt_then_raises(mock_heimdall):
    with pytest.raises(ErrorOnDecodeJwt):
        await JwtService.decode_jwt(jwt="123")

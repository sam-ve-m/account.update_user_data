from unittest.mock import patch

import pytest

from func.src.domain.exceptions.exceptions import ErrorOnSendIaraMessage
from func.src.transports.iara.transport import IaraClient
from tests.src.services.user_review.stubs import stub_user_review_model


@pytest.mark.asyncio
@patch("func.src.transports.iara.transport.Iara.send_to_iara", return_value=(1, 0))
async def test_when_success_to_record_message_then_return_true(mock_record_message):
    result = await IaraClient.send_to_sinacor_registration_queue(
        user_model=stub_user_review_model
    )

    assert result is True


@pytest.mark.asyncio
@patch("func.src.transports.iara.transport.Iara.send_to_iara", return_value=(0, 0))
async def test_when_fail_to_record_message_then_raises(mock_record_message):
    with pytest.raises(ErrorOnSendIaraMessage):
        await IaraClient.send_to_sinacor_registration_queue(
            user_model=stub_user_review_model
        )

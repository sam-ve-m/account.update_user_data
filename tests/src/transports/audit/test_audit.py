# Jormungandr - Onboarding
from func.src.domain.exceptions.exceptions import ErrorOnSendAuditLog
from func.src.transports.audit.transport import Audit
from tests.src.services.user_review.stubs import stub_user_review_model

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(1, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_success_to_record_message_then_return_true(
    mock_config, mock_persephone
):
    result = await Audit.record_message_log_to_update_registration_data(
        user_review_model=stub_user_review_model
    )

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(0, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_fail_to_record_message_then_raises(mock_config, mock_persephone):
    with pytest.raises(ErrorOnSendAuditLog):
        await Audit.record_message_log_to_update_registration_data(
            user_review_model=stub_user_review_model
        )

from datetime import datetime
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from etria_logger import Gladsheim
from regis import Regis, RiskValidations, RiskRatings, RegisResponse

from func.src.domain.enums.user_review import UserOnboardingStep
from func.src.domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    ErrorToUpdateUser,
    InvalidOnboardingCurrentStep,
    FailedToGetData,
    InconsistentUserData,
)
from func.src.domain.user_review.model import UserReviewModel
from func.src.services.user_review import UserReviewDataService
from func.src.transports.onboarding_steps.transport import OnboardingSteps
from func.src.domain.thebes_answer.model import ThebesAnswer
from tests.src.services.user_review.stubs import (
    stub_unique_id,
    stub_payload_validated,
    stub_user_from_database,
    stub_user_updated,
    stub_user_not_updated,
    stub_user_review_model,
    stub_device_info,
)


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.get_user",
    return_value={"data": True},
)
async def test_when_get_user_successfully_then_return_user_data(mock_repository):
    user_data = await UserReviewDataService._get_user_data(unique_id=stub_unique_id)

    assert isinstance(user_data, dict)
    assert user_data.get("data") is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.get_user",
    return_value=None,
)
async def test_when_not_found_an_user_then_raises(mock_repository):
    with pytest.raises(UserUniqueIdNotExists):
        await UserReviewDataService._get_user_data(unique_id=stub_unique_id)


@pytest.mark.asyncio
@patch("func.src.services.user_review.IaraTransport.send_to_drive_wealth_update_queue")
@patch("func.src.services.user_review.IaraTransport.send_to_sinacor_update_queue")
@patch("func.src.services.user_review.UserReviewDataService.rate_client_risk")
@patch("func.src.services.user_review.UserReviewDataService._update_user")
@patch(
    "func.src.services.user_review.Audit.record_message_log_to_update_registration_data"
)
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch(
    "func.src.services.user_review.UserReviewDataService._get_user_data",
    return_value=stub_user_from_database,
)
@patch.object(UserReviewModel, "__new__")
async def test_when_apply_rules_successfully_then_return_true(
    mocked_model,
    mock_get_user,
    mock_audit_registration_data,
    mock_audit_pld,
    mock_update,
    rate_risk,
    iara_mock_sinacor,
    iara_mock_dw,
):
    mocked_model.return_value = AsyncMock()
    result = await UserReviewDataService.update_user_data(
        unique_id=stub_unique_id,
        payload_validated=stub_payload_validated.dict(),
    )

    assert mocked_model.mock_calls[0].kwargs["device_info"] is None
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_updated,
)
async def test_when_update_user_successfully_then_return_true(mock_update_user):
    result = await UserReviewDataService._update_user(
        unique_id=stub_unique_id, new_user_registration_data=stub_user_from_database
    )
    mock_update_user.assert_called_once()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_updated,
)
async def test__update_user_when_user_has_inconsistent_data(mock_update_user):
    with pytest.raises(InconsistentUserData):
        result = await UserReviewDataService._update_user(
            unique_id=stub_unique_id, new_user_registration_data={}
        )


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_not_updated,
)
async def test_when_failure_to_update_user_then_raises(mock_update_user):
    with pytest.raises(ErrorToUpdateUser):
        await UserReviewDataService._update_user(
            unique_id=stub_unique_id, new_user_registration_data=stub_user_from_database
        )


dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(UserReviewDataService, "_check_if_able_to_update_br")
@patch.object(UserReviewDataService, "_check_if_able_to_update_us")
async def test_check_if_able_to_update_only_br(
    mocked_us_validation,
    mocked_br_validation,
):
    dummy_value.external_exchange_account_us = True
    await UserReviewDataService.check_if_able_to_update(
        dummy_value, dummy_value, dummy_value
    )
    mocked_br_validation.assert_called_once_with(dummy_value)
    mocked_us_validation.assert_called_once_with(dummy_value)


@pytest.mark.asyncio
@patch.object(UserReviewDataService, "_check_if_able_to_update_br")
@patch.object(UserReviewDataService, "_check_if_able_to_update_us")
async def test_check_if_able_to_update_br_and_us(
    mocked_us_validation,
    mocked_br_validation,
):
    dummy_value.external_exchange_account_us = False
    await UserReviewDataService.check_if_able_to_update(
        dummy_value, dummy_value, dummy_value
    )
    mocked_br_validation.assert_called_once_with(dummy_value)
    mocked_us_validation.assert_not_called()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_br")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_br(mocked_logger, mocked_transport):
    mocked_transport.return_value = UserOnboardingStep.FINISHED
    await UserReviewDataService._check_if_able_to_update_br(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_br")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_br_with_warning(mocked_logger, mocked_transport):
    mocked_transport.return_value = dummy_value
    with pytest.raises(InvalidOnboardingCurrentStep):
        await UserReviewDataService._check_if_able_to_update_br(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_called_once()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_us")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_us(mocked_logger, mocked_transport):
    mocked_transport.return_value = UserOnboardingStep.FINISHED
    await UserReviewDataService._check_if_able_to_update_us(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_us")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_us_with_warning(mocked_logger, mocked_transport):
    mocked_transport.return_value = dummy_value
    with pytest.raises(InvalidOnboardingCurrentStep):
        await UserReviewDataService._check_if_able_to_update_us(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_called_once()


@pytest.mark.asyncio
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch.object(
    Regis,
    "rate_client_risk",
)
@patch.object(Gladsheim, "warning")
async def test_rate_client_risk(mock_warning, rate_client_risk, audit_log):
    risk_data_stub = RegisResponse(
        risk_score=1,
        risk_rating=RiskRatings.LOW_RISK,
        risk_approval=True,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    rate_client_risk.return_value = risk_data_stub
    result = await UserReviewDataService.rate_client_risk(
        stub_user_review_model, stub_user_from_database
    )
    mock_warning.assert_not_called()
    rate_client_risk.assert_called_with(
        patrimony=500000.0,
        address_city=5150,
        profession=155,
        is_pep=False,
        is_pep_related=False,
    )


@pytest.mark.asyncio
@patch.object(Gladsheim, "warning")
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch.object(
    Regis,
    "rate_client_risk",
)
async def test_rate_client_risk_when_risk_is_not_aprroved(
    rate_client_risk, audit_log, etria_warning
):
    risk_data_stub = RegisResponse(
        risk_score=19,
        risk_rating=RiskRatings.CRITICAL_RISK,
        risk_approval=False,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    rate_client_risk.return_value = risk_data_stub
    result = await UserReviewDataService.rate_client_risk(
        stub_user_review_model, stub_user_from_database
    )
    assert etria_warning.called
    assert rate_client_risk.called


@pytest.mark.asyncio
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch.object(
    Regis,
    "rate_client_risk",
)
async def test_rate_client_risk_when_exception_happens(rate_client_risk, audit_log):
    rate_client_risk.side_effect = Exception()
    with pytest.raises(FailedToGetData):
        result = await UserReviewDataService.rate_client_risk(
            stub_user_review_model, {}
        )
    assert rate_client_risk.called

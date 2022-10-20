from unittest.mock import patch, MagicMock

import pytest
from etria_logger import Gladsheim

from func.src.domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    ErrorOnUpdateUser, InvalidOnboardingCurrentStep,
)
from func.src.services.user_review import UserReviewDataService
from func.src.domain.enums.user_review import UserOnboardingStep
from func.src.transports.onboarding_steps.transport import OnboardingSteps
from tests.src.services.user_review.stubs import (
    stub_unique_id,
    stub_payload_validated,
    stub_user_from_database,
    stub_user_updated,
    stub_user_not_updated,
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
@patch("func.src.services.user_review.UserReviewDataService._update_user")
@patch("func.src.services.user_review.Audit.record_message_log")
@patch(
    "func.src.services.user_review.UserReviewDataService._get_user_data",
    return_value=stub_user_from_database,
)
async def test_when_apply_rules_successfully_then_return_true(
    mock_get_user,
    mock_audit,
    mock_update,
):
    result = await UserReviewDataService.update_user_data(
        unique_id=stub_unique_id, payload_validated=stub_payload_validated
    )

    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_updated,
)
async def test_when_update_user_successfully_then_return_true(mock_update_user):
    result = await UserReviewDataService._update_user(
        unique_id=stub_unique_id, new_user_registration_data={}
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_not_updated,
)
async def test_when_failure_to_update_user_then_raises(mock_update_user):
    with pytest.raises(ErrorOnUpdateUser):
        await UserReviewDataService._update_user(
            unique_id=stub_unique_id, new_user_registration_data={}
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
    await UserReviewDataService.check_if_able_to_update(dummy_value, dummy_value)
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
    await UserReviewDataService.check_if_able_to_update(dummy_value, dummy_value)
    mocked_br_validation.assert_called_once_with(dummy_value)
    mocked_us_validation.assert_not_called()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_br")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_br(
        mocked_logger,
        mocked_transport
):
    mocked_transport.return_value = UserOnboardingStep.FINISHED
    await UserReviewDataService._check_if_able_to_update_br(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_br")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_br_with_warning(
        mocked_logger,
        mocked_transport
):
    mocked_transport.return_value = dummy_value
    with pytest.raises(InvalidOnboardingCurrentStep):
        await UserReviewDataService._check_if_able_to_update_br(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_called_once()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_us")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_us(
        mocked_logger,
        mocked_transport
):
    mocked_transport.return_value = UserOnboardingStep.FINISHED
    await UserReviewDataService._check_if_able_to_update_us(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_customer_steps_us")
@patch.object(Gladsheim, "warning")
async def test_check_if_able_to_update_us_with_warning(
        mocked_logger,
        mocked_transport
):
    mocked_transport.return_value = dummy_value
    with pytest.raises(InvalidOnboardingCurrentStep):
        await UserReviewDataService._check_if_able_to_update_us(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    mocked_logger.assert_called_once()

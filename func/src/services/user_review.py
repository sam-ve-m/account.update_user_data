from etria_logger import Gladsheim

from ..domain.enums.user_review import UserOnboardingStep
from ..domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    ErrorOnUpdateUser,
    InvalidOnboardingCurrentStep,
)

from ..domain.user_review.model import UserReviewModel
from ..domain.user_review.validator import UserUpdateData
from ..repositories.mongo_db.user.repository import UserRepository
from ..services.builders.user_registration_update import (
    UpdateCustomerRegistrationBuilder,
)
from ..transports.audit.transport import Audit
from ..transports.iara.transport import IaraTransport
from ..transports.onboarding_steps.transport import OnboardingSteps


class UserReviewDataService:
    @staticmethod
    async def check_if_able_to_update(payload_validated: UserUpdateData, jwt: str):
        await UserReviewDataService._check_if_able_to_update_br(jwt)
        if payload_validated.external_exchange_account_us:
            await UserReviewDataService._check_if_able_to_update_us(jwt)

    @staticmethod
    async def _check_if_able_to_update_br(jwt: str):
        customer_steps = await OnboardingSteps.get_customer_steps_br(jwt=jwt)
        if customer_steps != UserOnboardingStep.FINISHED:
            Gladsheim.warning(
                message=InvalidOnboardingCurrentStep.msg + " in BR",
                onboarding_step=customer_steps,
                jwt=jwt,
            )
            raise InvalidOnboardingCurrentStep()

    @staticmethod
    async def _check_if_able_to_update_us(jwt: str):
        customer_steps = await OnboardingSteps.get_customer_steps_us(jwt=jwt)
        if customer_steps != UserOnboardingStep.FINISHED:
            Gladsheim.warning(
                message=InvalidOnboardingCurrentStep.msg + " in US",
                onboarding_step=customer_steps,
                jwt=jwt,
            )
            raise InvalidOnboardingCurrentStep()

    @staticmethod
    async def update_user_data(unique_id: str, payload_validated: UserUpdateData):
        user_data = await UserReviewDataService._get_user_data(unique_id=unique_id)
        (
            new_user_registration_data,
            modified_register_data,
        ) = UpdateCustomerRegistrationBuilder(
            old_personal_data=user_data,
            new_personal_data=payload_validated,
            unique_id=unique_id,
        ).build()
        user_review_model = UserReviewModel(
            user_review_data=payload_validated,
            unique_id=unique_id,
            modified_register_data=modified_register_data,
            new_user_registration_data=new_user_registration_data,
        )
        await Audit.record_message_log(user_review_model=user_review_model)
        new_user_template = await user_review_model.get_new_user_data()

        await UserReviewDataService._update_user(
            unique_id=unique_id,
            new_user_registration_data=new_user_template,
        )
        await IaraTransport.send_to_sinacor_update_queue(user_review_model)
        await IaraTransport.send_to_drive_wealth_update_queue(user_review_model)

    @staticmethod
    async def _get_user_data(unique_id: str) -> dict:
        user_data = await UserRepository.get_user(unique_id=unique_id)
        if not user_data:
            raise UserUniqueIdNotExists()
        return user_data

    @staticmethod
    async def _update_user(unique_id: str, new_user_registration_data: dict):
        user_updated = await UserRepository.update_user(
            unique_id=unique_id, new_user_registration_data=new_user_registration_data
        )
        if not user_updated.matched_count:
            raise ErrorOnUpdateUser()

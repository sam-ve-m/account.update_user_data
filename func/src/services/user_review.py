from datetime import datetime

from etria_logger import Gladsheim
from regis import Regis, RegisResponse

from ..domain.enums.user_review import UserOnboardingStep
from ..domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    ErrorToUpdateUser,
    InvalidOnboardingCurrentStep,
    FailedToGetData,
    InconsistentUserData,
)
from ..domain.models.device_info import DeviceInfo
from ..domain.thebes_answer.model import ThebesAnswer
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
    async def check_if_able_to_update(
        payload_validated: UserUpdateData, thebes_answer: ThebesAnswer, jwt: str
    ):
        thebes_answer.check_if_account_br_is_blocked()
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
    async def rate_client_risk(user_review_model: UserReviewModel, old_user_data: dict):
        new_user_data = user_review_model.new_user_registration_data
        current_pld_rating = old_user_data.get("pld", {}).get("rating")
        try:
            regis_response: RegisResponse = await Regis.rate_client_risk(
                patrimony=new_user_data["assets"]["patrimony"],
                address_city=new_user_data["address"]["city"],
                profession=new_user_data["occupation"]["activity"],
                is_pep=bool(new_user_data.get("is_politically_exposed_person")),
                is_pep_related=bool(
                    new_user_data.get("is_correlated_to_politically_exposed_person")
                ),
            )
        except Exception as error:
            Gladsheim.error(error=error, message="Error trying to rate client risk.")
            raise FailedToGetData()

        if not regis_response.risk_approval:
            message = (
                "Updated client now has CRITICAL RISK -> "
                f"unique_id: {user_review_model.unique_id,}, "
                f"score: {regis_response.risk_score}"
            )
            Gladsheim.warning(message=message)

        risk_rating_changed = current_pld_rating != regis_response.risk_rating.value
        user_review_model.add_risk_data(
            risk_data=regis_response, risk_rating_changed=risk_rating_changed
        )

        await Audit.record_message_log_to_rate_client_risk(
            user_review_model=user_review_model
        )
        user_review_model.update_new_data_with_risk_data()
        user_review_model.update_new_data_with_expiration_dates()

    @classmethod
    async def update_user_data(
        cls, unique_id: str, payload_validated: dict, device_info: DeviceInfo = None
    ):
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
            device_info=device_info,
        )

        await cls.rate_client_risk(user_review_model, user_data)
        await Audit.record_message_log_to_update_registration_data(
            user_review_model=user_review_model
        )

        new_user_template = await user_review_model.get_new_user_data()
        await cls._update_user(
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
        try:
            new_user_registration_data["record_date_control"]["registry_updates"][
                "last_registration_data_update"
            ] = datetime.utcnow()
        except KeyError:
            raise InconsistentUserData()
        user_updated = await UserRepository.update_user(
            unique_id=unique_id, new_user_registration_data=new_user_registration_data
        )
        if not user_updated.matched_count:
            raise ErrorToUpdateUser()

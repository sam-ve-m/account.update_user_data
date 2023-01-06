# Standards
from http import HTTPStatus

# Third party
from decouple import config
from etria_logger import Gladsheim
from httpx import AsyncClient

from func.src.domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk


class OnboardingSteps:
    @staticmethod
    async def _get_customer_steps(host: str, jwt: str) -> str:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.get(host, headers=headers)
            if not request_result.status_code == HTTPStatus.OK:
                Gladsheim.error(
                    message=OnboardingStepsStatusCodeNotOk.msg,
                    status=request_result.status_code,
                    content=request_result.content,
                )
                raise OnboardingStepsStatusCodeNotOk()
            user_current_step = (
                request_result.json().get("result", {}).get("current_step")
            )
        return user_current_step

    @staticmethod
    async def get_customer_steps_br(jwt: str) -> str:
        host = config("ONBOARDING_STEPS_BR_URL")
        return await OnboardingSteps._get_customer_steps(host, jwt)

    @staticmethod
    async def get_customer_steps_us(jwt: str) -> str:
        host = config("ONBOARDING_STEPS_US_URL")
        return await OnboardingSteps._get_customer_steps(host, jwt)

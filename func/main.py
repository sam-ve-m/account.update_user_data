from http import HTTPStatus

from etria_logger import Gladsheim
import flask

from src.domain.enums.code import InternalCode
from src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    UserUniqueIdNotExists,
    ErrorOnSendAuditLog,
    ErrorOnUpdateUser,
    InvalidNationality,
    InvalidCity,
    InvalidState,
    InvalidEmail,
    InvalidActivity,
    InvalidMaritalStatus,
    InvalidCountryAcronym,
    ErrorOnGetUniqueId,
    HighRiskActivityNotAllowed,
    OnboardingStepsStatusCodeNotOk,
    InvalidOnboardingCurrentStep,
)
from src.domain.response.model import ResponseModel
from src.domain.user_review.validator import UserUpdateData
from src.services.jwt import JwtService
from src.services.user_enumerate_data import UserEnumerateService
from src.services.user_review import UserReviewDataService


async def update_user_data() -> flask.Response:
    msg_error = "Unexpected error occurred"
    jwt = flask.request.headers.get("x-thebes-answer")
    try:
        raw_payload = flask.request.json
        payload_validated = UserUpdateData(**raw_payload)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        await UserEnumerateService(
            payload_validated=payload_validated
        ).validate_enumerate_params()
        await UserReviewDataService.check_if_able_to_update(payload_validated, jwt)
        await UserReviewDataService.update_user_data(
            unique_id=unique_id, payload_validated=payload_validated
        )
        response = ResponseModel(
            success=True,
            message="User data successfully updated",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Error when trying to decode jwt",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND,
            message="There is no user with this unique_id",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (
        InvalidNationality,
        InvalidCity,
        InvalidState,
        InvalidEmail,
        InvalidActivity,
        InvalidMaritalStatus,
        InvalidCountryAcronym,
    ) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except HighRiskActivityNotAllowed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="High risk occupation not allowed",
        ).build_http_response(status=HTTPStatus.FORBIDDEN)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="Invalid Onboarding Step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (
        ErrorOnSendAuditLog,
        ErrorOnUpdateUser,
        OnboardingStepsStatusCodeNotOk,
    ) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

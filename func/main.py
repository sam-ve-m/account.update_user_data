import asyncio
from http import HTTPStatus

import flask
from decouple import config
from etria_logger import Gladsheim

from func.src.domain.thebes_answer.model import ThebesAnswer
from func.src.domain.enums.code import InternalCode
from func.src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    UserUniqueIdNotExists,
    ErrorOnSendAuditLog,
    ErrorToUpdateUser,
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
    FinancialCapacityNotValid,
    ErrorOnGetAccountBrIsBlocked,
    BrAccountIsBlocked,
    InconsistentUserData,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
    LivenessRejected,
    ErrorInLiveness, InvalidApiKey,
)
from func.src.domain.response.model import ResponseModel
from func.src.domain.user_review.validator import UserUpdateData
from func.src.services.jwt import JwtService
from func.src.services.liveness import LivenessService
from func.src.services.user_enumerate_data import UserEnumerateService
from func.src.services.user_review import UserReviewDataService
from func.src.transports.device_info.transport import DeviceSecurity


async def _update_user_update_data_legacy(jwt: str):
    encoded_device_info = flask.request.headers.get("x-device-info")
    raw_payload = flask.request.json

    payload_validated = UserUpdateData(**raw_payload)
    jwt_data = await JwtService.decode_jwt(jwt=jwt)
    thebes_answer = ThebesAnswer(jwt_data=jwt_data)
    device_info = await DeviceSecurity.get_device_info(encoded_device_info)
    validations = (
        LivenessService.validate(
            thebes_answer.unique_id,
            payload_validated,
        ),
        UserEnumerateService(
            payload_validated=payload_validated, unique_id=thebes_answer.unique_id
        ).validate_enumerate_params(),
        UserReviewDataService.check_if_able_to_update(
            payload_validated, thebes_answer, jwt
        ),
    )
    await asyncio.gather(*validations)

    await UserReviewDataService.update_user_data(
        unique_id=thebes_answer.unique_id,
        payload_validated=payload_validated.dict(),
        device_info=device_info,
    )


async def _append_user_risk_validation(api_key: str):
    if config("API_KEY") != api_key:
        raise InvalidApiKey()
    if not (unique_id := flask.request.headers.get("unique_id")):
        raise ValueError("Missing unique id")
    await UserReviewDataService.update_user_data(
        unique_id=unique_id,
        payload_validated={},
    )


async def update_user_data() -> flask.Response:
    msg_error = "Unexpected error occurred"
    try:
        if jwt := flask.request.headers.get("x-thebes-answer"):
            await _update_user_update_data_legacy(jwt)
        elif api_key := flask.request.headers.get("x-api-key"):
            await _append_user_risk_validation(api_key)
        else:
            raise ErrorOnDecodeJwt()

        response = ResponseModel(
            success=True,
            message="User data successfully updated",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidApiKey as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Invalid Api Key",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Error when trying to decode jwt",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except (ErrorOnGetUniqueId, ErrorOnGetAccountBrIsBlocked) as ex:
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

    except FinancialCapacityNotValid as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.FINANCIAL_CAPACITY_NOT_VALID,
            message="Insufficient financial capacity",
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
        LivenessRejected,
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

    except BrAccountIsBlocked as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ACCOUNT_BR_IS_BLOCKED,
            message="Account br is blocked",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except (
        ErrorOnSendAuditLog,
        ErrorToUpdateUser,
        ErrorInLiveness,
        OnboardingStepsStatusCodeNotOk,
    ) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InconsistentUserData as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="User data is inconsistent",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoRequestFailed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
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

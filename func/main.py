from http import HTTPStatus

import flask
from etria_logger import Gladsheim

from src.domain.thebes_answer.model import ThebesAnswer
from src.domain.enums.code import InternalCode
from src.domain.exceptions.exceptions import (
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
)
from src.domain.response.model import ResponseModel
from src.domain.user_review.validator import UserUpdateData
from src.services.jwt import JwtService
from src.services.user_enumerate_data import UserEnumerateService
from src.services.user_review import UserReviewDataService
from src.transports.device_info.transport import DeviceSecurity


async def update_user_data() -> flask.Response:
    msg_error = "Unexpected error occurred"
    try:
        jwt = flask.request.headers.get("x-thebes-answer")
        encoded_device_info = flask.request.headers.get("x-device-info")
        raw_payload = flask.request.json

        payload_validated = UserUpdateData(**raw_payload)
        jwt_data = await JwtService.decode_jwt(jwt=jwt)
        thebes_answer = ThebesAnswer(jwt_data=jwt_data)
        device_info = await DeviceSecurity.get_device_info(encoded_device_info)

        await UserEnumerateService(
            payload_validated=payload_validated, unique_id=thebes_answer.unique_id
        ).validate_enumerate_params()
        await UserReviewDataService.check_if_able_to_update(
            payload_validated, thebes_answer, jwt
        )

        await UserReviewDataService.update_user_data(
            unique_id=thebes_answer.unique_id,
            payload_validated=payload_validated,
            device_info=device_info,
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

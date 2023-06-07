class InvalidApiKey(Exception):
    msg = "Jormungandr-Onboarding::Invalid x-api-key supplied"


class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique id,"
        " jwt not decoded successfully"
    )


class ErrorOnSendAuditLog(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error when trying to send log audit on "
        "Persephone"
    )


class ErrorOnSendIaraMessage(Exception):
    msg = "Jormungandr-Onboarding::send_to_sinacor_registration_queue::Error when trying send message to Iara"


class ErrorToUpdateUser(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error on trying to update user in mongo_db::"
        "User not exists, or unique_id invalid"
    )


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user_data with this unique_id"


class FinancialCapacityNotValid(Exception):
    msg = "Jormungandr-Account::Insufficient financial capacity"


class InvalidEmail(Exception):
    msg = "Invalid email address"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"


class FailedToGetData(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: internal server error"


class InvalidActivity(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid activity"


class HighRiskActivityNotAllowed(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: suitability"


class CriticalRiskClientNotAllowed(Exception):
    msg = "Jormungandr-Onboarding::validators::Critical risk client not allowed"


class InvalidState(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid state"


class InvalidCity(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid city"


class InvalidNationality(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid nationality"


class InvalidMaritalStatus(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid marital status"


class InvalidCountryAcronym(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid country acronym"


class OnboardingStepsStatusCodeNotOk(Exception):
    msg = "Jormungandr-Onboarding::transports::Bad response: status not Ok returned form onboarding steps"


class InvalidOnboardingCurrentStep(Exception):
    msg = "Jormungandr-Onboarding::validators::Ivalid Step: Invalid user step, it must have be finished"


class ErrorOnGetAccountBrIsBlocked(Exception):
    msg = "Jormungandr-Onboarding::get_account_br_is_blocked::Account Br Is Blocked"


class BrAccountIsBlocked(Exception):
    msg = "Jormungandr-Onboarding::validators::Br Account: Brazilian account is blocked"


class InconsistentUserData(Exception):
    msg = "Jormungandr-Onboarding::service::User data is inconsistent"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"


class LivenessRejected(Exception):
    msg = "Liveness rejected"


class ErrorInLiveness(Exception):
    msg = "Internal Server Error in Liveness"

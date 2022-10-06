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


class ErrorOnUpdateUser(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error on trying to update user in mongo_db::"
        "User not exists, or unique_id invalid"
    )


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user_data with this unique_id"


class InvalidEmail(Exception):
    msg = "Invalid email address"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"


class InternalServerError(Exception):
    pass


class InvalidActivity(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid activity"


class HighRiskActivityNotAllowed(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: suitability"


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

from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    ONBOARDING_STEP_INCORRECT = 70
    ONBOARDING_STEP_REQUEST_FAILURE = 71
    JWT_INVALID = 30
    DATA_ALREADY_EXISTS = 98
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100

    def __repr__(self):
        return self.value

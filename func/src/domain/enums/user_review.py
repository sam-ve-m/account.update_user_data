from strenum import StrEnum


class PersonGender(StrEnum):
    MASCULINE = "M"
    FEMININE = "F"


class DocumentTypes(StrEnum):
    RG = "RG"
    CH = "CH"
    RN = "RN"


class UserOnboardingStep(StrEnum):
    FINISHED = "finished"

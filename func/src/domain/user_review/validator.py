import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, constr, validator, root_validator

from ..enums.employment_position_us import EmploymentPositionUs
from ..enums.employment_status_us import EmploymentStatusUs
from ..enums.employment_type_us import EmploymentTypeUs
from ..enums.high_risk_activity import HighRiskActivity
from ..enums.time_experience_us import TimeExperienceUs
from ..exceptions.exceptions import InvalidEmail, HighRiskActivityNotAllowed
from ...domain.enums.user_review import PersonGender, DocumentTypes


class Source(BaseModel):
    source: str


class ActivitySource(Source):
    value: int

    @validator("value")
    def occupation_cannot_be_high_risk(cls, occupation):
        try:
            HighRiskActivity(occupation)
        except ValueError:
            return occupation
        raise HighRiskActivityNotAllowed()


class AddressNumberSource(Source):
    value: str


class UsPersonSource(Source):
    value: bool


class BirthDateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        try:
            date = datetime.fromtimestamp(value, tz=timezone.utc)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class CelPhoneSource(Source):
    value: constr(regex=r"^\+\d+", min_length=14, max_length=14)


class CompanyNameSource(Source):
    value: str


class CnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def format_cnpj(cls, cnpj):
        return list(re.sub(r"[^0-9]", "", cnpj))

    @validator("value", always=True, allow_reuse=True)
    def cnpj_is_not_a_sequence(cls, cnpj):
        if cnpj == cnpj[::-1]:
            raise ValueError("Invalid CNPJ")
        return cnpj

    @validator("value", always=True, allow_reuse=True)
    def cnpj_calculation(cls, new_cnpj):
        first_digit_calculation_array = [
            "5",
            "4",
            "3",
            "2",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
        ]
        second_digit_calculation_array = [
            "6",
            "5",
            "4",
            "3",
            "2",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
        ]
        cnpj_origin = deepcopy(new_cnpj)
        del new_cnpj[-2:]

        calc_cnpj = 11 - (
            (
                sum(
                    [
                        int(x) * int(y)
                        for x, y in zip(first_digit_calculation_array, new_cnpj)
                    ]
                )
            )
            % 11
        )
        calc_cnpj = calc_cnpj if calc_cnpj < 10 else 0
        new_cnpj.append(str(calc_cnpj))

        calc_cnpj = 11 - (
            (
                sum(
                    [
                        int(x) * int(y)
                        for x, y in zip(second_digit_calculation_array, new_cnpj)
                    ]
                )
            )
            % 11
        )
        calc_cnpj = calc_cnpj if calc_cnpj < 10 else 0
        new_cnpj.append(str(calc_cnpj))

        if not cnpj_origin == new_cnpj:
            raise ValueError("Invalid CNPJ")
        new_cnpj_string = "".join(new_cnpj)
        return new_cnpj_string


class CpfSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str):
        cpf = re.sub("[^0-9]", "", cpf)
        return cpf

    @validator("value", always=True, allow_reuse=True)
    def cpf_is_not_a_sequence(cls, cpf):
        if cpf == cpf[::-1]:
            raise ValueError("Invalid CPF")
        return cpf

    @validator("value", always=True, allow_reuse=True)
    def cpf_calculation(cls, cpf: str):
        cpf_last_digits = cpf[:-2]
        cont_reversed = 10
        total = 0

        for index in range(19):
            if index > 8:
                index -= 9
            total += int(cpf_last_digits[index]) * cont_reversed
            cont_reversed -= 1

            if cont_reversed < 2:
                cont_reversed = 11
                digits = 11 - (total % 11)

                if digits > 9:
                    digits = 0
                total = 0
                cpf_last_digits += str(digits)
        if not cpf == cpf_last_digits:
            raise ValueError("Invalid CPF")
        return cpf


class CountrySource(Source):
    value: constr(min_length=3, max_length=3)


class CountySource(Source):
    value: int


class DateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        try:
            date = datetime.fromtimestamp(value)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class DocumentNumberSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        return value.replace(".", "").replace("-", "").replace("/", "")


class DocumentTypesSource(Source):
    value: DocumentTypes


class EmailSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_email(cls, email: str):
        regex = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{2,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$"
        if not re.search(regex, email):
            raise InvalidEmail()
        return email


class GenderSource(Source):
    value: PersonGender


class IncomeSource(Source):
    value: float


class IssuerSource(Source):
    value: str


class NameSource(Source):
    value: constr(regex=r"^[a-zA-Z\sáéíóúãẽĩõũâêîôûç]+$", max_length=60)


class NationalitySource(Source):
    value: int


class NeighborhoodSource(Source):
    value: constr(min_length=3, max_length=18)


class NickNameSource(Source):
    value: str


class MaritalStatusSource(Source):
    value: int


class PatrimonySource(Source):
    value: float


class PhoneSource(Source):
    value: constr(regex=r"^\+\d+", min_length=13, max_length=14)


class SpouseSource(BaseModel):
    name: NameSource
    cpf: CpfSource
    nationality: NationalitySource


class StateSource(Source):
    value: constr(min_length=2, max_length=2)


class StreetNameSource(Source):
    value: constr(min_length=3, max_length=30)


class TaxResidence(BaseModel):
    country: constr(min_length=3, max_length=3)
    tax_number: str


class TaxResidenceSource(Source):
    value: List[TaxResidence]


class ZipCodeSource(Source):
    value: constr(regex=r"^[0-9]{5}-[\d]{3}")


class ComplementSource(Source):
    value: constr(max_length=20)


class PoliticallyExposed(Source):
    value: bool


class ExchangeMember(Source):
    value: bool


class CompanyDirector(Source):
    value: bool


class CompanyDirectorOf(Source):
    value: str


class EmployedStatusSource(Source):
    value: EmploymentStatusUs


class EmployedTypeSource(Source):
    value: EmploymentTypeUs


class EmployedPositionSource(Source):
    value: EmploymentPositionUs


class EmployCompanyName(Source):
    value: str


class TimeExperience(Source):
    value: TimeExperienceUs


class UserPersonalDataUpdate(BaseModel):
    name: Optional[NameSource]
    nick_name: Optional[NickNameSource]
    birth_date: Optional[BirthDateSource]
    gender: Optional[GenderSource]
    father_name: Optional[NameSource]
    mother_name: Optional[NameSource]
    email: Optional[EmailSource]
    phone: Optional[CelPhoneSource]
    nationality: Optional[NationalitySource]
    occupation_activity: Optional[ActivitySource]
    company_name: Optional[CompanyNameSource]
    company_cnpj: Optional[CnpjSource]
    patrimony: Optional[PatrimonySource]
    income: Optional[IncomeSource]
    foreign_account_tax: Optional[TaxResidenceSource]
    us_person: Optional[UsPersonSource]
    birth_place_country: Optional[CountrySource]
    birth_place_state: Optional[StateSource]
    birth_place_city: Optional[CountySource]


class UserMaritalDataUpdate(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[SpouseSource]


class UserDocumentsDataUpdate(BaseModel):
    cpf: Optional[CpfSource]
    identity_type: Optional[DocumentTypesSource]
    identity_number: Optional[DocumentNumberSource]
    expedition_date: Optional[DateSource]
    issuer: Optional[IssuerSource]
    state: Optional[StateSource]


class UserAddressDataUpdate(BaseModel):
    country: Optional[CountrySource]
    state: Optional[StateSource]
    city: Optional[CountySource]
    neighborhood: Optional[NeighborhoodSource]
    street_name: Optional[StreetNameSource]
    number: Optional[AddressNumberSource]
    zip_code: Optional[ZipCodeSource]
    phone: Optional[PhoneSource]
    complement: Optional[ComplementSource]


class ExternalExchangeAccountUsUpdate(BaseModel):
    is_politically_exposed: Optional[PoliticallyExposed]
    is_exchange_member: Optional[ExchangeMember]
    time_experience: Optional[TimeExperience]
    is_company_director: Optional[CompanyDirector]
    is_company_director_of: Optional[CompanyDirectorOf]
    user_employ_status: Optional[EmployedStatusSource]
    user_employ_type: Optional[EmployedTypeSource]
    user_employ_position: Optional[EmployedPositionSource]
    user_employ_company_name: Optional[EmployCompanyName]

    @root_validator()
    def validate(cls, values: Dict[str, Any]):
        is_company_director = values.get("is_company_director", {}).get("value")
        company_name_meta = values.get("is_company_director_of", {})
        if is_company_director and not company_name_meta:
            company_name = company_name_meta.get("value")
            if not company_name:
                raise ValueError(
                    "Need to inform the field company_director_of if you are a company director"
                )
        return values


class UserUpdateData(BaseModel):
    personal: Optional[UserPersonalDataUpdate]
    marital: Optional[UserMaritalDataUpdate]
    documents: Optional[UserDocumentsDataUpdate]
    address: Optional[UserAddressDataUpdate]
    external_exchange_account_us: Optional[ExternalExchangeAccountUsUpdate]

    @root_validator()
    def validate(cls, values: Dict[str, Any]):
        for key, value in values.items():
            if value is not None:
                return values
        raise ValueError("At least one update is required")

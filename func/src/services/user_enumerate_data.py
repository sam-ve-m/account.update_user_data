from func.src.domain.exceptions.exceptions import (
    InvalidNationality,
    InvalidMaritalStatus,
    InvalidCountryAcronym,
    InvalidState,
    InvalidCity,
    InvalidActivity,
    FinancialCapacityNotValid,
)
from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.domain.user_review.validator import UserUpdateData
from func.src.repositories.mongo_db.user.repository import UserRepository
from func.src.repositories.oracle.repository import EnumerateRepository

from typing import List


class UserEnumerateService:
    def __init__(self, payload_validated: UserUpdateData, unique_id: str):
        self.unique_id = unique_id
        self.user_enumerate_model = UserEnumerateDataModel(
            payload_validated=payload_validated
        )

    async def validate_enumerate_params(self):
        activity_code = await self.user_enumerate_model.get_activity()
        await self._validate_activity(activity_code=activity_code)
        state = await self.user_enumerate_model.get_document_state()
        await self._validate_state(state=state)
        nationalities = await self.user_enumerate_model.get_nationalities()
        await self._validate_nationality(nationalities=nationalities)
        countries = await self.user_enumerate_model.get_country_tax_residences()
        await self._validate_country_acronym(countries=countries)
        marital_code = await self.user_enumerate_model.get_marital_status()
        await self._validate_marital_status(marital_code=marital_code)
        address_combination = await self.user_enumerate_model.get_combination_address()
        await self._validate_combination_place(combination_place=address_combination)
        birth_place_combination = (
            await self.user_enumerate_model.get_combination_birth_place()
        )
        await self._validate_combination_place(
            combination_place=birth_place_combination
        )
        await self._validate_financial_capacity(
            user_enumerate_model=self.user_enumerate_model, unique_id=self.unique_id
        )

    @staticmethod
    async def _validate_financial_capacity(
        user_enumerate_model: UserEnumerateDataModel, unique_id: str
    ):
        user = await UserRepository.get_user(unique_id=unique_id)

        patrimony = user_enumerate_model.get_patrimony()
        if not patrimony:
            patrimony = user["assets"]["patrimony"]

        income = user_enumerate_model.get_income()
        if not income:
            income = user["assets"]["income"]

        financial_capacity = patrimony + income

        if financial_capacity < 1000:
            raise FinancialCapacityNotValid()
        return

    @staticmethod
    async def _validate_activity(activity_code: int):
        if not activity_code:
            return
        result = await EnumerateRepository.get_activity(activity_code=activity_code)
        if not result:
            raise InvalidActivity()

    @staticmethod
    async def _validate_country_acronym(countries):
        if not countries:
            return
        for country in countries:
            result = await EnumerateRepository.get_country(country_acronym=country)
            if not result:
                raise InvalidCountryAcronym()

    @staticmethod
    async def _validate_marital_status(marital_code: int):
        if not marital_code:
            return
        result = await EnumerateRepository.get_marital_status(marital_code=marital_code)
        if not result:
            raise InvalidMaritalStatus()

    @staticmethod
    async def _validate_nationality(nationalities: List):
        if not nationalities:
            return
        for nationality_code in nationalities:
            result = await EnumerateRepository.get_nationality(
                nationality_code=nationality_code
            )
            if not result:
                raise InvalidNationality()

    @staticmethod
    async def _validate_state(state: str):
        if not state:
            return
        result = await EnumerateRepository.get_state(state=state)
        if not result:
            raise InvalidState()

    @staticmethod
    async def _validate_combination_place(combination_place: dict):
        if not combination_place:
            return
        result = await EnumerateRepository.get_city(
            country=combination_place.get("country"),
            state=combination_place.get("state"),
            id_city=combination_place.get("city"),
        )
        if not result:
            raise InvalidCity()

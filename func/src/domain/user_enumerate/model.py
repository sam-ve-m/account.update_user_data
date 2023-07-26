from func.src.domain.user_review.validator import UserUpdateData

from typing import Optional, Any


class UserEnumerateDataModel:
    def __init__(self, payload_validated: UserUpdateData):
        self.user_review_data = payload_validated.dict()

    async def get_activity(self) -> Optional[int]:
        activity_code = self.get_value("personal.occupation_activity.value")
        return activity_code

    async def get_combination_birth_place(self) -> Optional[dict]:
        if self.user_review_data.get("personal") is None:
            return

        personal_country = self.get_value("personal.birth_place_country.value")
        personal_state = self.get_value("personal.birth_place_state.value")
        personal_city = self.get_value("personal.birth_place_city.value")
        birth_place_combination = {
            "country": personal_country,
            "state": personal_state,
            "city": personal_city,
        }
        if personal_country or personal_state or personal_state:
            if not all([personal_city, personal_state, personal_country]):
                raise ValueError("Birth place values are required")
            return birth_place_combination

    async def get_combination_address(self) -> Optional[dict]:
        if self.user_review_data.get("address") is None:
            return

        country_address = self.get_value("address.country.value")
        state_address = self.get_value("address.state.value")
        city_address = self.get_value("address.city.value")
        address_combination = {
            "country": country_address,
            "state": state_address,
            "city": city_address,
        }
        if city_address or state_address or country_address:
            if not all([city_address, state_address, country_address]):
                raise ValueError("Address values are required")
            return address_combination

    async def get_country_tax_residences(self) -> Optional[list]:
        tax_residences = (self.user_review_data.get("personal") or {}).get(
            "tax_residences"
        )
        if not tax_residences:
            return
        tax_residences_list = tax_residences["value"]
        countries = [tax_residence["country"] for tax_residence in tax_residences_list]
        return countries

    async def get_document_state(self) -> Optional[str]:
        document_state = self.get_value("documents.state.value")
        return document_state

    async def get_marital_status(self) -> Optional[int]:
        marital_code = self.get_value("marital.status.value")
        return marital_code

    async def get_nationalities(self) -> Optional[list]:
        nationalities = []
        personal_nationality = self.get_value("personal.nationality.value")
        current_marital_status = self.get_value("marital.spouse")
        if personal_nationality:
            nationalities.append(personal_nationality)
        if current_marital_status:
            spouse_nationality = current_marital_status["nationality"]["value"]
            nationalities.append(spouse_nationality)
        return nationalities

    def get_value(self, field: str) -> Any:
        parent_value = self.user_review_data
        for field in field.split(sep="."):
            parent_value = parent_value.get(field)
            if parent_value is None:
                return
        return parent_value

    def get_patrimony(self) -> tuple:
        patrimony = self.get_value("personal.patrimony.value")
        return patrimony

    def get_income(self) -> tuple:
        income = self.get_value("personal.income.value")
        return income

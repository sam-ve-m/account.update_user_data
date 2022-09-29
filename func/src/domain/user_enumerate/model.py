from ...domain.user_review.validator import UserUpdateData

from typing import Optional


class UserEnumerateDataModel:
    def __init__(self, payload_validated: UserUpdateData):
        self.user_review_data = payload_validated.dict()

    async def get_activity(self) -> Optional[int]:
        activity_code = (
            (self.user_review_data.get("personal") or {})
            .get("occupation_activity", {})
            .get("value")
        )
        return activity_code

    async def get_combination_birth_place(self) -> Optional[dict]:
        if self.user_review_data.get("personal") is None:
            return

        personal_country = (
            self.user_review_data.get("personal")
            .get("birth_place_country", {})
            .get("value")
        )
        personal_state = (
            self.user_review_data.get("personal")
            .get("birth_place_state", {})
            .get("value")
        )
        personal_city = (
            self.user_review_data.get("personal")
            .get("birth_place_city", {})
            .get("value")
        )
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

        country_address = (
            self.user_review_data.get("address").get("country", {}).get("value")
        )
        state_address = (
            self.user_review_data.get("address").get("state", {}).get("value")
        )
        city_address = (
            self.user_review_data.get("address").get("city", {}).get("value")
        )
        address_combination = {
            "country": country_address,
            "state": state_address,
            "city": city_address,
        }
        if city_address or state_address or country_address:
            if not all([city_address, state_address, country_address]):
                raise ValueError("Address values are required")
            return address_combination

    async def get_country_foreign_account_tax(self) -> Optional[list]:
        foreign_account_tax = (
            (self.user_review_data.get("personal") or {})
            .get("foreign_account_tax")
        )
        if not foreign_account_tax:
            return
        foreign_account_tax_list = foreign_account_tax.get("value")
        countries = [
            tax_residence.get("country") for tax_residence in foreign_account_tax_list
        ]
        return countries

    async def get_document_state(self) -> Optional[str]:
        if self.user_review_data.get("documents") is None:
            return
        document_state = (
            self.user_review_data.get("documents").get("state", {}).get("value")
        )
        return document_state

    async def get_marital_status(self) -> Optional[int]:
        if self.user_review_data.get("marital") is None:
            return
        marital_code = (
            self.user_review_data.get("marital").get("status", {}).get("value")
        )
        return marital_code

    async def get_nationalities(self) -> Optional[list]:
        nationalities = []
        personal_nationality = (
            (self.user_review_data.get("personal") or {})
            .get("nationality", {})
            .get("value")
        )
        current_marital_status = (self.user_review_data.get("marital") or {}).get("spouse")
        if personal_nationality:
            nationalities.append(personal_nationality)
        if current_marital_status:
            spouse_nationality = (
                current_marital_status.get("nationality")
            )
            nationalities.append(spouse_nationality)
        return nationalities

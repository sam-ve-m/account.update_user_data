from func.src.domain.exceptions.exceptions import (
    ErrorOnGetUniqueId,
    BrAccountIsBlocked,
    ErrorOnGetAccountBrIsBlocked,
)


class ThebesAnswer:
    def __init__(self, jwt_data: dict):
        self.jwt_data = jwt_data

    @property
    def unique_id(self):
        unique_id = self.jwt_data.get("user", {}).get("unique_id")
        if not unique_id:
            raise ErrorOnGetUniqueId()
        return unique_id

    def check_if_account_br_is_blocked(self):
        account_br_is_blocked = self.jwt_data.get("user", {}).get(
            "account_br_is_blocked"
        )
        if account_br_is_blocked is None:
            raise ErrorOnGetAccountBrIsBlocked()

        if account_br_is_blocked:
            raise BrAccountIsBlocked()

        return account_br_is_blocked

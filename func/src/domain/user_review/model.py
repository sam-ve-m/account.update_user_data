from .validator import UserUpdateData


class UserReviewModel:
    def __init__(
        self,
        user_review_data: UserUpdateData,
        unique_id: str,
        modified_register_data: dict,
        new_user_registration_data: dict,
    ):
        self.user_review_data = user_review_data.dict()
        self.unique_id = unique_id
        self.modified_register_data = modified_register_data
        self.new_user_registration_data = new_user_registration_data

    async def get_audit_template(self):
        audit_template = {
            "unique_id": self.unique_id,
            "modified_register_data": self.modified_register_data,
            "update_customer_registration_data": self.user_review_data,
        }
        return audit_template

    async def get_new_user_data(self):
        del self.new_user_registration_data["_id"]
        return self.new_user_registration_data

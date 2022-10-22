from regis import RegisResponse

from .validator import UserUpdateData


class UserReviewModel:
    def __init__(
        self,
        user_review_data: UserUpdateData,
        unique_id: str,
        modified_register_data: dict,
        new_user_registration_data: dict,
        risk_data: RegisResponse = None,
    ):
        self.user_review_data = user_review_data.dict()
        self.unique_id = unique_id
        self.modified_register_data = modified_register_data
        self.new_user_registration_data = new_user_registration_data
        self.risk_data = risk_data

    def add_risk_data(self, risk_data: RegisResponse):
        self.risk_data = risk_data

    def update_new_data_with_risk_data(self):
        risk_data_template = {
            "pld": {
                "rating": self.risk_data.risk_rating.value,
                "score": self.risk_data.risk_score,
            }
        }
        self.new_user_registration_data.update(risk_data_template)

    async def get_audit_template_to_update_registration_data(self) -> dict:
        audit_template = {
            "unique_id": self.unique_id,
            "modified_register_data": self.modified_register_data,
            "update_customer_registration_data": self.user_review_data,
        }
        return audit_template

    async def get_audit_template_to_update_risk_data(self) -> dict:
        audit_template = {
            "unique_id": self.unique_id,
            "score": self.risk_data.risk_score,
            "rating": self.risk_data.risk_rating.value,
            "approval": self.risk_data.risk_approval,
            "validations": self.risk_data.risk_validations.to_dict(),
        }
        if not audit_template["approval"]:
            audit_template.update({"user_data": self.new_user_registration_data})
        return audit_template

    async def get_new_user_data(self) -> dict:
        del self.new_user_registration_data["_id"]
        return self.new_user_registration_data
from copy import deepcopy
from datetime import datetime
from typing import Optional

from regis import RegisResponse

from .validator import UserUpdateData
from ..exceptions.exceptions import InconsistentUserData
from ..models.device_info import DeviceInfo


class UserReviewModel:
    def __init__(
        self,
        user_review_data: dict,
        unique_id: str,
        modified_register_data: dict,
        new_user_registration_data: dict,
        device_info: Optional[DeviceInfo],
        risk_data: RegisResponse = None,
        risk_rating_changed: bool = None,
    ):
        self.user_review_data = user_review_data
        self.unique_id = unique_id
        self.modified_register_data = modified_register_data
        self.new_user_registration_data = new_user_registration_data
        self.device_info = device_info
        self.risk_data = risk_data
        self.risk_rating_changed = risk_rating_changed

    def add_risk_data(self, risk_data: RegisResponse, risk_rating_changed: bool):
        self.risk_data = risk_data
        self.risk_rating_changed = risk_rating_changed

    def update_new_data_with_risk_data(self):
        risk_data_template = {
            "pld": {
                "rating": self.risk_data.risk_rating.value,
                "score": self.risk_data.risk_score,
            },
        }
        if self.risk_rating_changed:
            try:
                self.new_user_registration_data["record_date_control"][
                    "current_pld_risk_rating_defined_in"
                ] = datetime.utcnow()
            except KeyError:
                raise InconsistentUserData()
        self.new_user_registration_data.update(risk_data_template)

    def update_new_data_with_expiration_dates(self):
        expiration_dates_template = {
            "record_date_control": {
                **(self.new_user_registration_data.get("record_date_control", {}) or {}),
                "current_pld_risk_rating_defined_in": self.risk_data.expiration_date
            },
            "expiration_dates": {
                "suitability": self.risk_data.expiration_date,
                "register": self.risk_data.expiration_date,
            }
        }
        self.new_user_registration_data.update(expiration_dates_template)

    async def get_audit_template_to_update_registration_data(self) -> dict:
        audit_template = {
            "unique_id": self.unique_id,
            "modified_register_data": self.modified_register_data,
            "update_customer_registration_data": self.user_review_data,
        }
        if self.device_info:
            audit_template.update({
                "device_info": self.device_info.device_info,
                "device_id": self.device_info.device_id
            })
        return audit_template

    async def get_audit_template_to_update_risk_data(self) -> dict:
        audit_template = {
            "unique_id": deepcopy(self.unique_id),
            "score": deepcopy(self.risk_data.risk_score),
            "rating": deepcopy(self.risk_data.risk_rating.value),
            "approval": deepcopy(self.risk_data.risk_approval),
            "validations": deepcopy(self.risk_data.risk_validations.to_dict()),
        }
        if self.device_info:
            audit_template.update({
                "device_info": self.device_info.device_info,
                "device_id": self.device_info.device_id
            })
        if not audit_template["approval"]:
            audit_template.update(
                {"user_data": deepcopy(self.new_user_registration_data)}
            )
        return audit_template

    async def get_new_user_data(self) -> dict:
        del self.new_user_registration_data["_id"]
        return self.new_user_registration_data

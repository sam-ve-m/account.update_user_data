from ...domain.enums.types import QueueTypes
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.user_review.model import UserReviewModel

from decouple import config
from etria_logger import Gladsheim
from nidavellir import Sindri
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, user_review_model: UserReviewModel):
        message = await user_review_model.get_audit_template()
        Sindri.dict_to_primitive_types(message)
        partition = QueueTypes.USER_UPDATE_REGISTER_DATA
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_USER_REVIEW_SCHEMA")
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            Gladsheim.error(
                message="Audit::register_user_log::Error on trying to register log"
            )
            raise ErrorOnSendAuditLog
        return True

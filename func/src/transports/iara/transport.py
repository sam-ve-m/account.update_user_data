from ...domain.exceptions.exceptions import ErrorOnSendIaraMessage
from ...domain.user_review.model import UserReviewModel

from etria_logger import Gladsheim
from iara_client import Iara, IaraTopics, SchemaTypes


class IaraClient:
    @staticmethod
    async def send_to_sinacor_registration_queue(user_model: UserReviewModel):
        message = await user_model.get_iara_message_template()
        topic = IaraTopics.SINACOR_REGISTRATION
        schema_type = SchemaTypes.SINACOR_REGISTRATION

        success, status_sent_to_iara = await Iara.send_to_iara(
            message=message,
            schema_type=schema_type,
            topic=topic,
        )
        if not success:
            Gladsheim.error(
                message=f"Iara_client::send_to_email_verification_queue::Error when trying to send to"
                f" iara::{message=}::{schema_type=}::{topic=}"
            )
            raise ErrorOnSendIaraMessage()
        return True

from ...domain.user_review.model import UserReviewModel

from etria_logger import Gladsheim
from iara_client import Iara, IaraTopics


class IaraTransport:
    @staticmethod
    async def send_to_sinacor_update_queue(user_model: UserReviewModel):
        message = {"unique_id": user_model.unique_id}
        topic = IaraTopics.SINACOR_UPDATE

        success, status_sent_to_iara = await Iara.send_to_iara(
            message=message,
            topic=topic,
        )
        if not success:
            Gladsheim.error(
                message=f"Failed to send user to queue of Sinacor account update",
                status_sent_to_iara=status_sent_to_iara,
            )

    @staticmethod
    async def send_to_drive_wealth_update_queue(user_model: UserReviewModel):
        message = {"unique_id": user_model.unique_id}
        topic = IaraTopics.DW_UPDATE

        success, status_sent_to_iara = await Iara.send_to_iara(
            message=message,
            topic=topic,
        )
        if not success:
            Gladsheim.error(
                message=f"Failed to send user to queue of DriveWealth account update",
                status_sent_to_iara=status_sent_to_iara,
            )

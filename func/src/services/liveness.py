from decouple import config
from koh import Koh, KohStatus

from func.src.domain.exceptions.exceptions import ErrorInLiveness, LivenessRejected
from func.src.domain.user_review.validator import UserUpdateData


class LivenessService:

    @staticmethod
    async def validate(unique_id: str, liveness: UserUpdateData):
        approved, status = await Koh.check_face(
            unique_id,
            liveness.liveness,
            config("KOH_FEATURE_UPDATE_USER_DATA")
        )
        if status != KohStatus.SUCCESS:
            raise ErrorInLiveness()
        if not approved:
            raise LivenessRejected()

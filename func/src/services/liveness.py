from koh import Koh, KohStatus

from src.domain.exceptions.exceptions import ErrorInLiveness, LivenessRejected
from src.domain.user_review.validator import UserUpdateData


class LivenessService:

    @staticmethod
    async def validate(unique_id: str, liveness: UserUpdateData):
        approved, status = await Koh.check_face(unique_id, liveness.liveness)
        if status != KohStatus.SUCCESS:
            raise ErrorInLiveness()
        if not approved:
            raise LivenessRejected()

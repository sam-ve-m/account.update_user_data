from ..domain.exceptions.exceptions import ErrorOnDecodeJwt, ErrorOnGetUniqueId

from heimdall_client import Heimdall
from heimdall_client.src.domain.enums.heimdall_status_responses import (
    HeimdallStatusResponses,
)


class JwtService:
    @staticmethod
    async def decode_jwt_and_get_unique_id(jwt: str):
        jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt)
        if not HeimdallStatusResponses.SUCCESS.value == heimdall_status_response.value:
            raise ErrorOnDecodeJwt
        unique_id = jwt_content.get("decoded_jwt", {}).get("user", {}).get("unique_id")
        if not unique_id:
            raise ErrorOnGetUniqueId
        return unique_id

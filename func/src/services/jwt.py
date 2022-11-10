from ..domain.exceptions.exceptions import ErrorOnDecodeJwt, ErrorOnGetUniqueId

from heimdall_client import Heimdall
from heimdall_client.src.domain.enums.heimdall_status_responses import (
    HeimdallStatusResponses,
)


class JwtService:
    @staticmethod
    async def decode_jwt(jwt: str) -> dict:
        jwt_decoded, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt)
        if not HeimdallStatusResponses.SUCCESS.value == heimdall_status_response.value:
            raise ErrorOnDecodeJwt()

        jwt_data = jwt_decoded["decoded_jwt"]
        return jwt_data

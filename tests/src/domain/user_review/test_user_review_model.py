from tests.src.services.user_review.stubs import stub_user_review_model

# Third party
import pytest


@pytest.mark.asyncio
async def test_when_get_new_user_data_then_remove_pymongo_id():
    result = await stub_user_review_model.get_new_user_data()

    assert isinstance(result, dict)
    assert result.get("_id") is None

from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from func.src.domain.exceptions.exceptions import (
    InvalidCity,
    InvalidState,
    InvalidMaritalStatus,
    InvalidActivity,
    InvalidNationality,
    InvalidCountryAcronym,
    FinancialCapacityNotValid,
)


from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.repositories.mongo_db.user.repository import UserRepository
from func.src.services.user_enumerate_data import UserEnumerateService
from tests.src.services.user_review.stubs import (
    stub_payload_validated,
    stub_payload_missing_data,
    StubUserReview,
)
from tests.src.services.enumerate.stubs import (
    user_review_stub_missing_params,
    user_review_stub_missing_country,
)

# Third party
from pytest import fixture


@fixture(scope="function")
def enumerate_service_missing_some_data():
    service = UserEnumerateService(
        payload_validated=stub_payload_validated,
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
    )
    return service


@fixture(scope="function")
def enumerate_service():
    service = UserEnumerateService(
        payload_validated=stub_payload_validated,
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
    )
    return service


@fixture(scope="function")
def enumerate_model():
    enumerate_model = UserEnumerateDataModel(payload_validated=stub_payload_validated)
    return enumerate_model


@fixture(scope="function")
def enumerate_model_missing_some_data():
    enumerate_model = UserEnumerateDataModel(payload_validated=StubUserReview)
    return enumerate_model


@fixture(scope="function")
def enumerate_model_missing_tax_residences_value():
    enumerate_model = UserEnumerateDataModel(
        payload_validated=user_review_stub_missing_params
    )
    return enumerate_model


@fixture(scope="function")
def enumerate_model_missing_country_and_spouse():
    enumerate_model = UserEnumerateDataModel(
        payload_validated=user_review_stub_missing_country
    )
    return enumerate_model


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_city",
    return_value=1,
)
async def test_when_combination_place_is_valid_then_return_none(
    mock_validate_city, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_combination_place(
        combination_place={
            "country": "value",
            "state": "value",
            "city": "value",
        }
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_city",
    return_value=1,
)
async def test_when_combination_place_is_valid_none(
    mock_validate_city, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_combination_place(
        combination_place=None
    )
    mock_validate_city.assert_not_called()
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_city",
    return_value=None,
)
async def test_when_combination_place_is_invalid_then_raises(
    mock_validate_city, enumerate_service_missing_some_data
):
    with pytest.raises(InvalidCity):
        await enumerate_service_missing_some_data._validate_combination_place(
            combination_place={
                "country": "value",
                "state": "value",
                "city": "value",
            }
        )


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_state",
    return_value=True,
)
async def test_when_valid_state_then_return_none(
    mock_validate_state, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_state(state="SP")
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_state",
    return_value=True,
)
async def test_when_valid_state_none(
    mock_validate_state, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_state(state=None)
    assert result is None
    mock_validate_state.assert_not_called()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_state",
    return_value=False,
)
async def test_when_invalid_state_then_raises(
    mock_validate_state, enumerate_service_missing_some_data
):
    with pytest.raises(InvalidState):
        await enumerate_service_missing_some_data._validate_state(state="SPAA")


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_marital_status",
    return_value=True,
)
async def test_when_valid_marital_status_then_return_none(
    mock_validate_marital, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_marital_status(
        marital_code=1
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_marital_status",
    return_value=True,
)
async def test_when_valid_marital_status_none(
    mock_validate_marital, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_marital_status(
        marital_code=None
    )
    mock_validate_marital.assert_not_called()
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_marital_status",
    return_value=False,
)
async def test_when_invalid_marital_status_then_raises(
    mock_validate_marital, enumerate_service_missing_some_data
):
    with pytest.raises(InvalidMaritalStatus):
        await enumerate_service_missing_some_data._validate_marital_status(
            marital_code=999
        )


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_activity",
    return_value=True,
)
async def test_when_valid_activity_code_then_return_none(
    mock_validate_activity, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_activity(
        activity_code=100
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_activity",
    return_value=True,
)
async def test_when_valid_activity_code_none(
    mock_validate_activity, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_activity(
        activity_code=None
    )
    mock_validate_activity.assert_not_called()
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_activity",
    return_value=False,
)
async def test_when_invalid_activity_then_raises(
    mock_validate_activity, enumerate_service_missing_some_data
):
    with pytest.raises(InvalidActivity):
        await enumerate_service_missing_some_data._validate_activity(activity_code=999)


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    side_effect=[True, True],
)
async def test_when_valid_nationality_then_return_none(
    mock_validate_nationality, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_nationality(
        nationalities=[1, 2]
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    side_effect=[True, True],
)
async def test_when_valid_nationality_none(
    mock_validate_nationality, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_nationality(
        nationalities=None
    )
    mock_validate_nationality.assert_not_called()
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    side_effect=[False, True],
)
async def test_when_invalid_nationality_then_raises(
    mock_validate_nationality, enumerate_service_missing_some_data
):
    with pytest.raises(InvalidNationality):
        await enumerate_service_missing_some_data._validate_nationality(
            nationalities=[1, 2]
        )


@pytest.mark.asyncio
async def test_when_no_countries_then_return_none_(enumerate_service_missing_some_data):
    result = await enumerate_service_missing_some_data._validate_country_acronym(
        countries=None
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_country",
    side_effect=[True, True],
)
async def test_when_valid_countries_then_return_none(
    mock_validate_countries, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_country_acronym(
        countries=[1, 2]
    )
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_country",
    side_effect=[True, True],
)
async def test_when_valid_countries_none(
    mock_validate_countries, enumerate_service_missing_some_data
):
    result = await enumerate_service_missing_some_data._validate_country_acronym(
        countries=None
    )
    mock_validate_countries.assert_not_called()
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_country",
    side_effect=[False, True],
)
async def test_when_invalid_country_then_raises(
    mock_validate_countries, enumerate_service_missing_some_data
):
    with pytest.raises(InvalidCountryAcronym):
        await enumerate_service_missing_some_data._validate_country_acronym(
            countries=[1, 2]
        )


@pytest.mark.asyncio
async def test_when_success_to_validate_enumerate_params_then_return_true(
    enumerate_service,
):
    fake_instance = AsyncMock()
    result = await UserEnumerateService.validate_enumerate_params(fake_instance)
    assert fake_instance.user_enumerate_model.get_activity.called
    assert fake_instance.user_enumerate_model.get_document_state.called
    assert fake_instance.user_enumerate_model.get_nationalities.called
    assert fake_instance.user_enumerate_model.get_country_tax_residences.called
    assert fake_instance.user_enumerate_model.get_marital_status.called
    assert fake_instance.user_enumerate_model.get_combination_address.called


stub_get_user_greater_than_a_thousand_and_two_values = {
    "assets": {"patrimony": 0, "income": 0}
}


@pytest.mark.asyncio
@patch.object(UserEnumerateDataModel, "get_patrimony", return_value=500)
@patch.object(UserEnumerateDataModel, "get_income", return_value=500)
@patch.object(
    UserRepository,
    "get_user",
    return_value=stub_get_user_greater_than_a_thousand_and_two_values,
)
@patch.object(FinancialCapacityNotValid, "__init__")
async def test__validate_financial_capacity_false_false_false(
    mock___init__, mock_get_user, mock_get_patrimony, mock_get_income
):
    response = await UserEnumerateService._validate_financial_capacity(
        user_enumerate_model=UserEnumerateDataModel(MagicMock()),
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
    )
    mock___init__.assert_not_called()


stub_get_user_greater_than_a_thousand_and_two_values02 = {
    "assets": {"patrimony": 500, "income": 0}
}


@pytest.mark.asyncio
@patch.object(UserEnumerateDataModel, "get_patrimony", return_value=None)
@patch.object(UserEnumerateDataModel, "get_income", return_value=500)
@patch.object(
    UserRepository,
    "get_user",
    return_value=stub_get_user_greater_than_a_thousand_and_two_values02,
)
@patch.object(FinancialCapacityNotValid, "__init__")
async def test__validate_financial_capacity_true_false_false(
    mock___init__, mock_get_user, mock_get_patrimony, mock_get_income
):
    response = await UserEnumerateService._validate_financial_capacity(
        user_enumerate_model=UserEnumerateDataModel(MagicMock()),
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
    )
    mock___init__.assert_not_called()


stub_get_user_greater_than_a_thousand_and_two_values03 = {
    "assets": {"patrimony": 0, "income": 500}
}


@pytest.mark.asyncio
@patch.object(UserEnumerateDataModel, "get_patrimony", return_value=500)
@patch.object(UserEnumerateDataModel, "get_income", return_value=None)
@patch.object(
    UserRepository,
    "get_user",
    return_value=stub_get_user_greater_than_a_thousand_and_two_values03,
)
@patch.object(FinancialCapacityNotValid, "__init__")
async def test__validate_financial_capacity_false_true_false(
    mock___init__, mock_get_user, mock_get_patrimony, mock_get_income
):
    response = await UserEnumerateService._validate_financial_capacity(
        user_enumerate_model=UserEnumerateDataModel(MagicMock()),
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
    )
    mock_get_user["assets"]["patrimony"].assert_not_called()
    mock___init__.assert_not_called()


stub_get_user_greater_than_a_thousand_and_two_values05 = {
    "assets": {"patrimony": 500, "income": 500}
}


@pytest.mark.asyncio
@patch.object(UserEnumerateDataModel, "get_patrimony", return_value=None)
@patch.object(UserEnumerateDataModel, "get_income", return_value=None)
@patch.object(
    UserRepository,
    "get_user",
    return_value=stub_get_user_greater_than_a_thousand_and_two_values05,
)
@patch.object(FinancialCapacityNotValid, "__init__")
async def test__validate_financial_capacity_true_true_false(
    mock___init__, mock_get_user, mock_get_patrimony, mock_get_income
):
    response = await UserEnumerateService._validate_financial_capacity(
        user_enumerate_model=UserEnumerateDataModel(MagicMock()),
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
    )
    mock___init__.assert_not_called()


stub_get_user_greater_than_a_thousand_and_two_values01 = {
    "assets": {"patrimony": 100, "income": 800}
}


@pytest.mark.asyncio
@patch.object(UserEnumerateDataModel, "get_patrimony", return_value=None)
@patch.object(UserEnumerateDataModel, "get_income", return_value=None)
@patch.object(
    UserRepository,
    "get_user",
    return_value=stub_get_user_greater_than_a_thousand_and_two_values01,
)
@patch.object(FinancialCapacityNotValid, "__init__")
async def test__validate_financial_capacity_false_false_true(
    mock___init__, mock_get_user, mock_get_patrimony, mock_get_income
):
    with pytest.raises(Exception):
        response = await UserEnumerateService._validate_financial_capacity(
            user_enumerate_model=UserEnumerateDataModel(MagicMock()),
            unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
        )
    mock___init__.assert_called()

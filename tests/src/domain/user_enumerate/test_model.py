from copy import deepcopy
from unittest.mock import patch

import pytest

from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.domain.user_review.validator import UserUpdateData

user_data_dummy = {
    "personal": {
        "nationality": {"source": "app", "value": 1},
        "occupation_activity": {"source": "app", "value": 101},
        "birth_place_country": {"source": "app", "value": "BRA"},
        "birth_place_state": {"source": "app", "value": "PA"},
        "birth_place_city": {"source": "app", "value": 2412},
        "foreign_account_tax": {"source": "app", "value": [{"country": "USA", "tax_number": "132"}]},
    },
    "marital": {
        "status": {"source": "app", "value": 1},
        "spouse": {
            "nationality": {"source": "app", "value": 2},
            "cpf": {"source": "app", "value": "88663481047"},
            "name": {"source": "app", "value": "fulana"},

        }
        },
    "documents": {
        "state": {"source": "app", "value": "SP"},
    },
    "address": {
        "country": {"source": "app", "value": "BRA"},
        "state": {"source": "app", "value": "SP"},
        "city": {"source": "app", "value": 5051},
    },
}


@pytest.mark.asyncio
async def test_get_activity():
    model = UserEnumerateDataModel(UserUpdateData(**user_data_dummy))
    result = await model.get_activity()
    expected_result = 101
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_combination_birth_place():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_combination_birth_place()
    expected_result = {'country': 'BRA', 'state': 'PA', 'city': 2412}
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_combination_birth_place_when_there_is_no_personal_data():
    user_data = deepcopy(user_data_dummy)
    user_data.pop("personal")
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_combination_birth_place()
    expected_result = None
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_combination_birth_place_when_a_value_is_missing():
    user_data = deepcopy(user_data_dummy)
    user_data["personal"].pop("birth_place_country")
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    with pytest.raises(ValueError):
        result = await model.get_combination_birth_place()


@pytest.mark.asyncio
async def test_get_combination_address():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_combination_address()
    expected_result = {'country': 'BRA', 'state': 'SP', 'city': 5051}
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_combination_address_when_there_is_no_personal_data():
    user_data = deepcopy(user_data_dummy)
    user_data.pop("address")
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_combination_address()
    expected_result = None
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_combination_address_when_a_value_is_missing():
    user_data = deepcopy(user_data_dummy)
    user_data["address"].pop("country")
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    with pytest.raises(ValueError):
        result = await model.get_combination_address()


@pytest.mark.asyncio
async def test_get_country_foreign_account_tax():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_country_foreign_account_tax()
    expected_result = ["USA"]
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_country_foreign_account_tax_when_personal_is_none():
    user_data = deepcopy(user_data_dummy)
    user_data.pop("personal")
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_country_foreign_account_tax()
    expected_result = None
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_document_state():
    model = UserEnumerateDataModel(UserUpdateData(**user_data_dummy))
    result = await model.get_document_state()
    expected_result = "SP"
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_marital_status():
    model = UserEnumerateDataModel(UserUpdateData(**user_data_dummy))
    result = await model.get_marital_status()
    expected_result = 1
    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize("option", [1, 2, 3, 4])
async def test_get_nationalities(option):
    user_data = deepcopy(user_data_dummy)
    if option == 1:
        user_data["marital"].pop("spouse")
        expected_result = [1]
    if option == 2:
        user_data["marital"].pop("spouse")
        user_data["personal"].pop("nationality")
        expected_result = []
    if option == 3:
        expected_result = [1, 2]
    if option == 4:
        user_data["personal"].pop("nationality")
        expected_result = [2]
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_nationalities()
    assert result == expected_result
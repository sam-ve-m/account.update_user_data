from copy import deepcopy
from unittest.mock import patch, MagicMock

import pytest

from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.domain.user_review.validator import UserUpdateData

user_data_dummy = {
    "liveness": "",
    "personal": {
        "nationality": {"source": "app", "value": 1},
        "occupation_activity": {"source": "app", "value": 101},
        "birth_place_country": {"source": "app", "value": "BRA"},
        "birth_place_state": {"source": "app", "value": "PA"},
        "birth_place_city": {"source": "app", "value": 2412},
        "tax_residences": {
            "source": "app",
            "value": [{"country": "USA", "tax_number": "132"}],
        },
        "patrimony": {"source": "app", "value": 1000},
        "income": {"source": "app", "value": 1000},
    },
    "marital": {
        "status": {"source": "app", "value": 1},
        "spouse": {
            "nationality": {"source": "app", "value": 2},
            "cpf": {"source": "app", "value": "88663481047"},
            "name": {"source": "app", "value": "fulana de tal"},
        },
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
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_activity()
    expected_result = 101
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_combination_birth_place():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_combination_birth_place()
    expected_result = {"country": "BRA", "state": "PA", "city": 2412}
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
    expected_result = {"country": "BRA", "state": "SP", "city": 5051}
    assert result == expected_result


fake_instance = MagicMock()


@pytest.mark.asyncio
async def test_get_combination_birth_place_without_birth_place():
    fake_instance.user_review_data.get.return_value = None
    result = await UserEnumerateDataModel.get_combination_birth_place(fake_instance)
    fake_instance.get_value.assert_not_called()
    assert result is None


@pytest.mark.asyncio
async def test_get_combination_address_without_address():
    fake_instance.user_review_data.get.return_value = None
    result = await UserEnumerateDataModel.get_combination_address(fake_instance)
    fake_instance.get_value.assert_not_called()
    assert result is None


@pytest.mark.asyncio
async def test_get_combination_birth_place_without_combination():
    fake_instance.user_review_data.get.return_value = True
    fake_instance.get_value.return_value = None
    result = await UserEnumerateDataModel.get_combination_birth_place(fake_instance)
    fake_instance.get_value.assert_called()
    assert result is None


@pytest.mark.asyncio
async def test_get_combination_address_without_combination():
    fake_instance.user_review_data.get.return_value = True
    fake_instance.get_value.return_value = None
    result = await UserEnumerateDataModel.get_combination_address(fake_instance)
    fake_instance.get_value.assert_called()
    assert result is None


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
async def test_get_country_tax_residences():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_country_tax_residences()
    expected_result = ["USA"]
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_country_tax_residences_when_personal_is_none():
    user_data = deepcopy(user_data_dummy)
    user_data.pop("personal")
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    result = await model.get_country_tax_residences()
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


def test_get_patrimony():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    response = model.get_patrimony()
    assert response == 1000


def test_get_income():
    user_data = deepcopy(user_data_dummy)
    model = UserEnumerateDataModel(UserUpdateData(**user_data))
    response = model.get_income()
    assert response == 1000

import pytest

from func.src.domain.exceptions.exceptions import HighRiskActivityNotAllowed
from func.src.domain.user_review.validator import UserUpdateData

register_dummy = {
    "personal": {
        "name": {"source": "app", "value": "Rosa Jessica"},
        "nick_name": {"source": "app", "value": "Rosinha"},
        "birth_date": {"source": "app", "value": 158986800},
        "gender": {"source": "app", "value": "F"},
        "father_name": {"source": "app", "value": "Foi Eu"},
        "mother_name": {"source": "app", "value": "Rosa Mae"},
        "email": {"source": "app", "value": "brabo04@abraaoz.tk"},
        "phone": {"source": "app", "value": "+5577998636716"},
        "nationality": {"source": "app", "value": 1},
        "occupation_activity": {"source": "app", "value": 101},
        "patrimony": {"source": "app", "value": 12000},
        "income": {"source": "app", "value": 10000},
        "birth_place_country": {"source": "app", "value": "BRA"},
        "birth_place_state": {"source": "app", "value": "PA"},
        "birth_place_city": {"source": "app", "value": 2412},
        "us_person": {"source": "app", "value": True},
    },
    "marital": {"status": {"source": "app", "value": 1}},
    "documents": {
        "cpf": {"source": "app", "value": "72772117073"},
        "identity_type": {"source": "app", "value": "CH"},
        "identity_number": {"source": "app", "value": "06713096255"},
        "expedition_date": {"source": "app", "value": 1600697312},
        "issuer": {"source": "app", "value": "SSP"},
        "state": {"source": "app", "value": "SP"},
    },
    "address": {
        "country": {"source": "app", "value": "BRA"},
        "state": {"source": "app", "value": "SP"},
        "city": {"source": "app", "value": 5051},
        "neighborhood": {"source": "app", "value": "Centro"},
        "street_name": {"source": "app", "value": "Praça Padre Domingos Segurado "},
        "number": {"source": "app", "value": "142"},
        "zip_code": {"source": "app", "value": "12980-970"},
        "complement": {"source": "app", "value": "complemento"},
    },
}


@pytest.mark.asyncio
async def test_validator_when_is_all_ok():
    data_validated = UserUpdateData(**register_dummy)


@pytest.mark.asyncio
async def test_validator_when_occupation_is_high_risk():
    register_stub = register_dummy.copy()
    register_stub["personal"]["occupation_activity"]["value"] = 1
    with pytest.raises(HighRiskActivityNotAllowed):
        data_validated = UserUpdateData(**register_dummy)

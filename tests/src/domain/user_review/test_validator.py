import pytest

from func.src.domain.exceptions.exceptions import (
    HighRiskActivityNotAllowed,
    InvalidEmail,
)
from func.src.domain.user_review.validator import (
    UserUpdateData,
    CnpjSource,
    EmailSource,
    CpfSource,
    ExternalExchangeAccountUsUpdate,
    OptionalDataBlock,
)

register_dummy = {
    "liveness": "",
    "personal": {
        "name": {"source": "app", "value": "Rosa Jessica"},
        "nick_name": {"source": "app", "value": "Rosinha"},
        "birth_date": {"source": "app", "value": 158986800},
        "gender": {"source": "app", "value": "F"},
        "father_name": {"source": "app", "value": "Foi Eu"},
        "company_cnpj": {"source": "app", "value": "02916265000160"},
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


def test_validator_when_is_all_ok():
    data_validated = UserUpdateData(**register_dummy)


def test_validator_when_occupation_is_high_risk():
    register_stub = register_dummy.copy()
    register_stub["personal"]["occupation_activity"]["value"] = 1
    with pytest.raises(HighRiskActivityNotAllowed):
        data_validated = UserUpdateData(**register_dummy)


def test_invalid_cpf_last_digit():
    with pytest.raises(ValueError) as error:
        CpfSource.cpf_calculation("44820841821")
        assert error == "Invalid CPF"


def test_invalid_cpf_first_digit():
    with pytest.raises(ValueError) as error:
        CpfSource.cpf_calculation("44820841813")
        assert error == "Invalid CPF"


def test_invalid_cpf_short():
    with pytest.raises(ValueError) as error:
        CpfSource.cpf_calculation("")
        assert error == "Invalid CPF"


def test_invalid_cpf_sequence():
    with pytest.raises(ValueError) as error:
        CpfSource.cpf_is_not_a_sequence("11111111111")
        assert error == "Invalid CPF"


def test_invalid_cnpj():
    with pytest.raises(ValueError) as error:
        CnpjSource.cnpj_calculation(list("02916265000150"))
        assert error == "Invalid CPNJ"


def test_cnpj_is_not_a_sequence():
    with pytest.raises(ValueError) as error:
        CnpjSource.cnpj_is_not_a_sequence(list("11111111111111"))
        assert error == "Invalid CPNJ"


def test_invalid_email():
    with pytest.raises(InvalidEmail):
        EmailSource.validate_email("svm.gmail.com")


def test_company_director_without_company_name():
    with pytest.raises(ValueError):
        ExternalExchangeAccountUsUpdate.validate(
            {
                "is_company_director": {"value": True},
                "is_company_director_of": {"value": False},
            }
        )


def test_company_director():
    ExternalExchangeAccountUsUpdate.validate(
        {
            "is_company_director": {"value": True},
            "is_company_director_of": {"value": True},
        }
    )


def test_root_validator():
    OptionalDataBlock.at_least_one_field(
        {
            "is_company_director": True,
        }
    )


def test_root_validator_invalid_value():
    with pytest.raises(ValueError):
        OptionalDataBlock.at_least_one_field(
            {
                "is_company_director_of": None,
            }
        )

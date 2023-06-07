from func.src.domain.user_review.validator import UserUpdateData
from func.src.domain.user_review.model import UserReviewModel
from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.services.builders.user_registration_update import (
    UpdateCustomerRegistrationBuilder,
)

import datetime

from func.src.domain.models.device_info import DeviceInfo

stub_unique_id = "451baf5a-9cd5-4037-aa17-fbd0fcef66c8"

stub_payload = {
    "liveness": "",
    "personal": {
        "name": {"value": "Fulaninho da Silva Sauro", "source": "by_test"},
        "nick_name": {"value": "RAST3", "source": "by_test"},
        "birth_date": {"value": 750124800.0, "source": "by_test"},
        "gender": {"value": "M", "source": "by_test"},
        "father_name": {"value": "Pai da Silva Sauro", "source": "by_test"},
        "mother_name": {"value": "Mãe da Silva Sauro", "source": "by_test"},
        "email": {"value": "teste_mock@lionx.com.br", "source": "by_test"},
        "us_person": {"value": False, "source": "by_test"},
        "phone": {"value": "+5511952909942", "source": "by_test"},
        "nationality": {"value": 1, "source": "by_test"},
        "occupation_activity": {"value": 155, "source": "by_test"},
        "company_name": {"value": "LionX", "source": "by_test"},
        "company_cnpj": {"value": "36923006000188", "source": "by_test"},
        "patrimony": {"value": 500000.0, "source": "by_test"},
        "income": {"value": 200000.0, "source": "by_test"},
        "tax_residences": {
            "value": [
                {"country": "EUA", "tax_number": "abc123"},
                {"country": "ING", "tax_number": "abc123"},
            ],
            "source": "by_test",
        },
        "birth_place_country": {"value": "BRA", "source": "by_test"},
        "birth_place_city": {"value": 5150, "source": "by_test"},
        "birth_place_state": {"value": "SP", "source": "by_test"},
    },
    "marital": {
        "spouse": {
            "name": {"value": "Maria da Silva", "source": "by_test"},
            "cpf": {"value": "796.107.250-07", "source": "by_test"},
            "nationality": {"value": 1, "source": "by_test"},
        },
        "status": {"value": 1, "source": "by_test"},
    },
    "documents": {
        "cpf": {"value": "53845387084", "source": "by_test"},
        "identity_type": {"value": "RG", "source": "by_test"},
        "identity_number": {"value": "385722594", "source": "by_test"},
        "issuer": {"value": "SSP", "source": "by_test"},
        "state": {"value": "SP", "source": "by_test"},
    },
    "address": {
        "country": {"value": "BRA", "source": "by_test"},
        "number": {"value": "451", "source": "by_test"},
        "street_name": {"value": "Rua Imbuia", "source": "by_test"},
        "city": {"value": 5150, "source": "by_test"},
        "neighborhood": {"value": "Cidade das Flores", "source": "by_test"},
        "zip_code": {"value": "06184-110", "source": "by_test"},
        "state": {"value": "SP", "source": "by_test"},
        "phone": {"value": "+5511952909942", "source": "by_test"},
    },
}

stub_payload_missing_data = {
    "liveness": "",
    "personal": {
        "name": {"value": "Fulaninho da Silva Sauro", "source": "by_test"},
        "nick_name": {"value": "RAST3", "source": "by_test"},
        "birth_date": {"value": 750124800.0, "source": "by_test"},
        "gender": {"value": "M", "source": "by_test"},
        "father_name": None,
        "mother_name": {"value": "Mãe da Silva Sauro", "source": "by_test"},
        "email": {"value": "teste_mock@lionx.com.br", "source": "by_test"},
        "phone": {"value": "+5511952909942", "source": "by_test"},
        "nationality": {"value": 1, "source": "by_test"},
        "occupation_activity": {},
        "company_name": None,
        "company_cnpj": None,
        "patrimony": {"value": 500000.0, "source": "by_test"},
        "income": {"value": 200000.0, "source": "by_test"},
        "tax_residences": None,
        "birth_place_country": {},
        "birth_place_city": {},
        "birth_place_state": {},
    },
    "marital": {
        "spouse": {"name": "test"},
        "status": {"source": "by_test"},
    },
    "documents": {
        "cpf": {"value": "53845387084", "source": "by_test"},
        "identity_type": {"value": "RG", "source": "by_test"},
        "identity_number": {"value": "385722594", "source": "by_test"},
        "issuer": {"value": "SSP", "source": "by_test"},
        "state": {"source": "by_test"},
    },
    "address": {
        "country": {},
        "number": {"value": "451", "source": "by_test"},
        "street_name": {"value": "Rua Imbuia", "source": "by_test"},
        "city": {"value": 5150, "source": "by_test"},
        "neighborhood": {"value": "Cidade das Flores", "source": "by_test"},
        "zip_code": {"value": "06184-110", "source": "by_test"},
        "state": {},
        "phone": None,
    },
}

stub_user_from_database = {
    "_id": "626ed82fd70bbff3a36d5e72",
    "pin": None,
    "nick_name": "RAST3",
    "email": "testeteste@lionx.com.br",
    "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
    "created_at": datetime.datetime(2022, 1, 2, 5, 59, 22, 598000),
    "scope": {
        "view_type": "default",
        "user_level": "client",
        "features": ["default", "realtime"],
    },
    "is_active_user": True,
    "must_do_first_login": False,
    "use_magic_link": True,
    "token_valid_after": datetime.datetime(2022, 10, 2, 8, 59, 22, 598000),
    "terms": {
        "term_application": {
            "version": 17,
            "date": datetime.datetime(2022, 8, 17, 19, 40, 28, 66000),
            "is_deprecated": False,
        },
        "term_open_account": None,
        "term_retail_liquid_provider": None,
        "term_refusal": {
            "version": 4,
            "date": datetime.datetime(2022, 6, 28, 14, 53, 7, 674000),
            "is_deprecated": False,
        },
        "term_non_compliance": {
            "version": 4,
            "date": datetime.datetime(2022, 6, 29, 16, 42, 7, 692000),
            "is_deprecated": False,
        },
        "term_application_dw": {
            "version": 3,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 56, 210000),
            "is_deprecated": False,
        },
        "term_open_account_dw": {
            "version": 3,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 56, 20000),
            "is_deprecated": False,
        },
        "term_and_privacy_policy_data_sharing_policy_dw": {
            "version": 4,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 56, 455000),
            "is_deprecated": False,
        },
        "term_disclosures_and_disclaimers": {
            "version": 1,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 56, 644000),
            "is_deprecated": False,
        },
        "term_gringo_world": {
            "version": 1,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 57, 27000),
            "is_deprecated": False,
        },
        "term_gringo_world_general_advices": {
            "version": 1,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 57, 81000),
            "is_deprecated": False,
        },
        "term_money_corp": {
            "version": 1,
            "date": datetime.datetime(2022, 5, 5, 13, 43, 56, 840000),
            "is_deprecated": False,
        },
    },
    "suitability": {
        "score": 1.0,
        "submission_date": datetime.datetime(2022, 8, 17, 19, 40, 27, 886000),
        "suitability_version": 7,
    },
    "identifier_document": {
        "cpf": "53845387084",
        "document_data": {
            "type": "RG",
            "number": "385722594",
            "date": datetime.datetime(1993, 10, 9, 0, 0),
            "issuer": "SSP",
            "state": "SP",
        },
    },
    "phone": "+5511952909942",
    "tax_residences": [],
    "bureau_status": "approved",
    "client_type": 1,
    "connected_person": "N",
    "cosif_tax_classification": 21,
    "investor_type": 101,
    "is_bureau_data_validated": True,
    "marital": {
        "status": 1,
        "spouse": {"cpf": "36390612095", "nationality": 1, "name": "Ciclaninho"},
    },
    "person_type": "F",
    "address": {
        "country": "BRA",
        "street_name": "Rua Imbuia",
        "city": 5150,
        "number": "153",
        "zip_code": "06184-110",
        "neighborhood": "Cidade das Flores",
        "state": "SP",
    },
    "assets": {
        "patrimony": 500000.0,
        "income_tax_type": 1,
        "date": datetime.datetime(2022, 8, 17, 18, 48, 3, 186000),
        "income": 200000.0,
    },
    "birth_date": datetime.datetime(1993, 10, 9, 0, 0),
    "father_name": "Pai de ciclaninho",
    "gender": "M",
    "mother_name": "Mãe de ciclaninho",
    "name": "Ciclaninho da Silva",
    "nationality": 1,
    "occupation": {
        "activity": 155,
        "company": {"cnpj": "36923006000188", "name": "LionX"},
    },
    "can_be_managed_by_third_party_operator": False,
    "is_active_client": True,
    "is_managed_by_third_party_operator": False,
    "last_modified_date": {
        "concluded_at": datetime.datetime(2022, 2, 3, 13, 36, 26, 306000)
    },
    "sinacor": True,
    "sincad": True,
    "solutiontech": "sync",
    "third_party_operator": {
        "is_third_party_operator": False,
        "details": {},
        "third_party_operator_email": "string",
    },
    "electronic_signature": "ea73ced01f94d96f7f46682055d6e3915b626a2ebbf98818a09ea2efb6af1a9e",
    "electronic_signature_wrong_attempts": 0,
    "is_blocked_electronic_signature": False,
    "portfolios": {
        "default": {
            "br": {
                "bovespa_account": "000000014-6",
                "created_at": datetime.datetime(2022, 1, 1, 3, 0),
                "bmf_account": "14",
            },
            "us": {
                "dw_id": "89c69304-018a-40b7-be5b-2121c16e109e",
                "created_at": datetime.datetime(2022, 1, 1, 3, 0),
                "dw_display_account": "LX01000002",
                "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
            },
        },
        "vnc": {
            "br": [
                {
                    "bovespa_account": "000000071-5",
                    "created_at": datetime.datetime(2022, 1, 1, 3, 0),
                    "bmf_account": "71",
                },
                {
                    "bovespa_account": "000000018-9",
                    "created_at": datetime.datetime(2022, 1, 1, 3, 0),
                    "bmf_account": "18",
                },
            ]
        },
    },
    "is_admin": True,
    "external_exchange_requirements": {
        "us": {
            "is_politically_exposed": False,
            "is_exchange_member": False,
            "is_company_director": False,
            "is_company_director_of": None,
            "user_employ_company_name": "asdasdasd",
            "user_employ_position": "ADMINISTRATOR",
            "user_employ_status": "EMPLOYED",
            "user_employ_type": "UTILITIES",
            "w8_confirmation": True,
            "external_fiscal_tax_confirmation": True,
            "time_experience": "NONE",
        }
    },
    "dw": "KYC_APPROVED",
    "bank_accounts": [
        {
            "bank": "Teste 1",
            "account_type": "Conta corrente",
            "agency": "12412412412-4",
            "account_number": "3523-5",
            "account_name": "Banco teste 1",
            "id": "f4e37976-7b1e-434c-ba19-c49bca507093",
            "status": "disabled",
        },
        {
            "bank": "Banco Original",
            "account_type": "Conta corrente",
            "agency": "1241241241",
            "account_number": "3523-5",
            "account_name": "wetwet",
            "id": "a33d10ad-bdf9-4d95-9b2b-c669e077cf93",
            "status": "disabled",
        },
        {
            "bank": "Teste 2",
            "account_type": "Conta de pagamentos",
            "agency": "12412412412-4",
            "account_number": "3523-5",
            "account_name": "Conta teste  2",
            "id": "44f107ce-8dc8-49a1-b409-e72975966a24",
            "status": "disabled",
        },
        {
            "bank": "Teste 3",
            "account_type": "Conta corrente",
            "agency": "23-5",
            "account_number": "3523-5",
            "account_name": "wetwet",
            "id": "84250b38-1292-493a-9bb7-7b018c09adf1",
            "status": "disabled",
        },
        {
            "bank": "Teste 3",
            "account_type": "Conta de pagamentos",
            "agency": "23-5",
            "account_number": "3523-5",
            "account_name": "wetwet",
            "id": "2113f95c-f138-45d6-a5a5-61edf20b75ba",
            "status": "disabled",
        },
        {
            "bank": "039",
            "account_type": "Conta corrente",
            "agency": "124124124",
            "account_number": "12345",
            "account_name": "235",
            "id": "c32f8581-55f3-4c4e-b317-43496efcb2e0",
            "status": "active",
        },
        {
            "bank": "039",
            "account_type": "Conta de pagamentos",
            "agency": "0001",
            "account_number": "12345",
            "account_name": "235",
            "id": "0b1e64d9-2d5e-43ce-9a8a-ba3b6e4477b8",
            "status": "active",
        },
        {
            "bank": "12412412412",
            "account_type": "Conta corrente",
            "agency": "12412412412-4",
            "account_number": "12412412412",
            "account_name": "12412412412",
            "id": "226e9919-5a30-40f7-bef3-e2f19dc13e66",
            "status": "disabled",
        },
        {
            "bank": "Teste 4",
            "account_type": "Conta corrente",
            "agency": "0001",
            "account_number": "25423-5",
            "account_name": "Teste 4",
            "id": "1d5c0767-6393-4a30-958a-45038fb1db5e",
            "status": "disabled",
        },
        {
            "bank": "Teste 6346",
            "account_type": "Conta poupança",
            "agency": "0001",
            "account_number": "25423-5",
            "account_name": "Teste 4",
            "id": "b1262e91-d2f9-4f30-ace4-957a1a49b2f7",
            "status": "disabled",
        },
        {
            "bank": "Teste 5",
            "account_type": "Conta corrente",
            "agency": "0001",
            "account_number": "12345",
            "account_name": "Teste 6",
            "id": "7afb72fe-b510-4b21-9dfe-63665dc190f2",
            "status": "disabled",
        },
        {
            "bank": "Teste 333",
            "account_type": "Conta poupança",
            "agency": "0001",
            "account_number": "25423-5",
            "account_name": "Teste 4",
            "id": "50500ce2-c682-4673-96e2-a78f4a8becb1",
            "status": "disabled",
        },
        {
            "bank": "Teste ",
            "account_type": "Conta poupança",
            "agency": "0001",
            "account_number": "12345",
            "account_name": "Teste 6",
            "id": "97b9adae-ba68-4c13-98f5-76413a7feb18",
            "status": "disabled",
        },
        {
            "bank": "Teste 401",
            "account_type": "Conta poupança",
            "agency": "0001",
            "account_number": "3523-5",
            "account_name": "Teste 400",
            "id": "0bb330c6-2ba6-499c-97ce-2d2adbff730f",
            "status": "disabled",
        },
        {
            "bank": "Teste 5",
            "account_type": "Conta corrente",
            "agency": "12412412412-4",
            "account_number": "3523-5",
            "account_name": "wetwet",
            "id": "86525937-b433-465a-a294-f14d51ea9b7e",
            "status": "disabled",
        },
        {
            "bank": "039",
            "account_type": "poupanca",
            "agency": "0022",
            "account_number": "000000050-0",
            "account_name": "minha_3",
            "id": "c39a9a6e-96f7-486c-be6f-13793762c101",
            "status": "active",
        },
        {
            "bank": "039",
            "account_type": "poupanca",
            "agency": "0022",
            "account_number": "000000060-0",
            "account_name": "123456789",
            "id": "ecb607a7-b18b-47da-82fb-880a197e2677",
            "status": "disabled",
        },
        {
            "bank": "212",
            "account_type": "null",
            "agency": "null",
            "account_number": "",
            "account_name": "null",
            "id": "78638cb9-574b-4586-b3f1-6d1c6c29b76f",
            "status": "active",
        },
        {
            "bank": "039",
            "account_type": "poupanca",
            "agency": "0001",
            "account_number": "12345",
            "account_name": "minha",
            "id": "25309e31-88e6-42a4-acb1-c52767035087",
            "status": "active",
        },
    ],
    "birth_place_city": 5150,
    "birth_place_country": "BRA",
    "birth_place_state": "SP",
    "record_date_control": {
        "registry_updates": {"last_registration_data_update": 0},
        "current_pld_risk_rating_defined_in": 0,
    },
}


stub_payload_validated = UserUpdateData(**stub_payload)
stub_device_info = DeviceInfo({"precision": 1}, "")

(
    stub_new_registration_data,
    stub_modified_register_data,
) = UpdateCustomerRegistrationBuilder(
    old_personal_data=stub_user_from_database,
    new_personal_data=stub_payload_validated.dict(),
    unique_id=stub_unique_id,
).build()

stub_user_review_model = UserReviewModel(
    user_review_data=stub_payload_validated.dict(),
    unique_id=stub_unique_id,
    new_user_registration_data=stub_new_registration_data,
    modified_register_data=stub_modified_register_data,
    device_info=stub_device_info,
)
stub_user_enumerate_model = UserEnumerateDataModel(
    payload_validated=stub_payload_validated
)


class StubUserReview:
    @staticmethod
    def dict():
        return stub_payload_missing_data


class UserUpdated:
    def __init__(self, matched_count=None):
        self.matched_count = matched_count


stub_user_not_updated = UserUpdated(matched_count=0)
stub_user_updated = UserUpdated(matched_count=1)

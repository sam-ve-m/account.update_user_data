# Jormungandr - Onboarding
from func.src.domain.user_enumerate.model import UserEnumerateDataModel
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
    service = UserEnumerateService(payload_validated=stub_payload_validated)
    return service


@fixture(scope="function")
def enumerate_service():
    service = UserEnumerateService(payload_validated=stub_payload_validated)
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
def enumerate_model_missing_foreign_account_tax_value():
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

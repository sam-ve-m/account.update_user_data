from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from regis import RegisResponse, RiskValidations, RiskRatings

from func.src.domain.exceptions.exceptions import InconsistentUserData
from func.src.domain.user_review.model import UserReviewModel
from tests.src.services.user_review.stubs import stub_user_review_model


@pytest.mark.asyncio
async def test_when_get_new_user_data_then_remove_pymongo_id():
    result = await stub_user_review_model.get_new_user_data()
    assert isinstance(result, dict)
    assert result.get("_id") is None
    assert stub_user_review_model.risk_data is None
    assert stub_user_review_model.risk_rating_changed is None


@pytest.mark.asyncio
async def test_get_audit_template_to_update_risk_data_when_is_not_approved():
    model_stub = stub_user_review_model
    risk_data_stub = RegisResponse(
        risk_score=19,
        risk_rating=RiskRatings.CRITICAL_RISK,
        risk_approval=False,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    model_stub.add_risk_data(risk_data=risk_data_stub, risk_rating_changed=False)
    result = await model_stub.get_audit_template_to_update_risk_data()
    expected_result = {
        "unique_id": model_stub.unique_id,
        "score": 19,
        "rating": "D",
        "approval": False,
        "validations": {
            "has_big_patrymony": True,
            "lives_in_frontier_city": True,
            "has_risky_profession": True,
            "is_pep": True,
            "is_pep_related": True,
        },
        "device_info": model_stub.device_info.device_info,
        "device_id": model_stub.device_info.device_id,
        "user_data": model_stub.new_user_registration_data,
    }
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_audit_template_to_update_risk_data_when_is_approved():
    model_stub = stub_user_review_model
    risk_data_stub = RegisResponse(
        risk_score=1,
        risk_rating=RiskRatings.LOW_RISK,
        risk_approval=True,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    model_stub.add_risk_data(risk_data=risk_data_stub, risk_rating_changed=False)
    result = await model_stub.get_audit_template_to_update_risk_data()
    expected_result = {
        "unique_id": model_stub.unique_id,
        "score": 1,
        "rating": "A",
        "approval": True,
        "validations": {
            "has_big_patrymony": True,
            "lives_in_frontier_city": True,
            "has_risky_profession": True,
            "is_pep": True,
            "is_pep_related": True,
        },
        "device_info": model_stub.device_info.device_info,
        "device_id": model_stub.device_info.device_id,
    }
    assert result == expected_result


@pytest.mark.asyncio
async def test_update_new_data_with_risk_data():
    model_stub = stub_user_review_model
    risk_data_stub = RegisResponse(
        risk_score=1,
        risk_rating=RiskRatings.LOW_RISK,
        risk_approval=True,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    model_stub.add_risk_data(risk_data=risk_data_stub, risk_rating_changed=False)
    pld_data_expected = {
        "rating": risk_data_stub.risk_rating.value,
        "score": risk_data_stub.risk_score,
    }
    result = model_stub.update_new_data_with_risk_data()
    assert pld_data_expected == model_stub.new_user_registration_data.get("pld")
    assert model_stub.new_user_registration_data["record_date_control"]["current_pld_risk_rating_defined_in"] == 0


@pytest.mark.asyncio
async def test_update_new_data_with_risk_data_when_rating_changed():
    model_stub = stub_user_review_model
    risk_data_stub = RegisResponse(
        risk_score=1,
        risk_rating=RiskRatings.LOW_RISK,
        risk_approval=True,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    model_stub.add_risk_data(risk_data=risk_data_stub, risk_rating_changed=True)
    pld_data_expected = {
        "rating": risk_data_stub.risk_rating.value,
        "score": risk_data_stub.risk_score,
    }
    result = model_stub.update_new_data_with_risk_data()
    pld_defined_inf = model_stub.new_user_registration_data.get(
        "record_date_control", {}
    ).get("current_pld_risk_rating_defined_in")
    assert isinstance(pld_defined_inf, datetime)
    assert pld_data_expected == model_stub.new_user_registration_data.get("pld")


@pytest.mark.asyncio
async def test_update_new_data_with_risk_data_when_user_data_is_inconsistent():
    model_stub = deepcopy(stub_user_review_model)
    risk_data_stub = RegisResponse(
        risk_score=1,
        risk_rating=RiskRatings.LOW_RISK,
        risk_approval=True,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    model_stub.add_risk_data(risk_data=risk_data_stub, risk_rating_changed=True)
    model_stub.new_user_registration_data = {}
    with pytest.raises(InconsistentUserData):
        result = model_stub.update_new_data_with_risk_data()


@pytest.mark.asyncio
async def test_get_templates_without_device_id():
    stub = MagicMock()
    result = await UserReviewModel.get_audit_template_to_update_registration_data(stub)
    expected_result = {
        "unique_id": stub.unique_id,
        "modified_register_data": stub.modified_register_data,
        "update_customer_registration_data": stub.user_review_data,
        "device_info": stub.device_info.device_info,
        "device_id": stub.device_info.device_id
    }
    assert result == expected_result
    stub.device_info = None
    result = await UserReviewModel.get_audit_template_to_update_registration_data(stub)
    expected_result = {
        "unique_id": stub.unique_id,
        "modified_register_data": stub.modified_register_data,
        "update_customer_registration_data": stub.user_review_data,
    }
    assert result == expected_result
    result = await UserReviewModel.get_audit_template_to_update_risk_data(stub)
    expected_result = {
        "unique_id": stub.unique_id,
        "score": stub.risk_data.risk_score,
        "rating": stub.risk_data.risk_rating.value,
        "approval": stub.risk_data.risk_approval,
        "validations": stub.risk_data.risk_validations.to_dict(),
    }
    assert result == expected_result

import pytest


@pytest.mark.asyncio
async def test_when_valid_activity_then_returns_activity_code(enumerate_model):
    activity_code = await enumerate_model.get_activity()

    assert isinstance(activity_code, int)
    assert activity_code == 155


@pytest.mark.asyncio
async def test_when_invalid_activity_then_raises(enumerate_model_missing_some_data):
    with pytest.raises(ValueError):
        await enumerate_model_missing_some_data.get_activity()


@pytest.mark.asyncio
async def test_when_valid_birth_place_then_return_combination_birth_place(
    enumerate_model,
):
    birth_place_combination = await enumerate_model.get_combination_birth_place()

    assert isinstance(birth_place_combination, dict)
    assert birth_place_combination.get("country") == "BRA"
    assert birth_place_combination.get("state") == "SP"
    assert birth_place_combination.get("city") == 5150


@pytest.mark.asyncio
async def test_when_invalid_birth_place_combination_then_raises(
    enumerate_model_missing_some_data,
):
    with pytest.raises(ValueError):
        await enumerate_model_missing_some_data.get_combination_birth_place()


@pytest.mark.asyncio
async def test_when_valid_address_then_return_address_combination(enumerate_model):
    address_combination = await enumerate_model.get_combination_address()

    assert isinstance(address_combination, dict)
    assert address_combination.get("country") == "BRA"
    assert address_combination.get("state") == "SP"
    assert address_combination.get("city") == 5150


@pytest.mark.asyncio
async def test_when_invalid_address_combination_then_raises(
    enumerate_model_missing_some_data,
):
    with pytest.raises(ValueError):
        await enumerate_model_missing_some_data.get_combination_address()


@pytest.mark.asyncio
async def test_when_have_foreign_account_tax_then_return_countries(enumerate_model):
    countries = await enumerate_model.get_country_foreign_account_tax()

    assert isinstance(countries, list)
    assert countries[0] == "EUA"
    assert countries[1] == "ING"


@pytest.mark.asyncio
async def test_when_no_foreign_account_tax_then_return_empty_list(
    enumerate_model_missing_some_data,
):
    countries = (
        await enumerate_model_missing_some_data.get_country_foreign_account_tax()
    )

    assert isinstance(countries, list)
    assert countries == []


@pytest.mark.asyncio
async def test_when_foreign_tax_missing_value_then_raises(
    enumerate_model_missing_foreign_account_tax_value,
):
    with pytest.raises(ValueError, match="Value key is required"):
        await enumerate_model_missing_foreign_account_tax_value.get_country_foreign_account_tax()


@pytest.mark.asyncio
async def test_when_invalid_foreign_tax_missing_country_then_raises(
    enumerate_model_missing_country_and_spouse,
):
    with pytest.raises(
        ValueError, match="Country from foreign account tax value is required"
    ):
        await enumerate_model_missing_country_and_spouse.get_country_foreign_account_tax()


@pytest.mark.asyncio
async def test_when_valid_document_state_then_return_document_state(enumerate_model):
    document_state = await enumerate_model.get_document_state()

    assert isinstance(document_state, str)
    assert document_state == "SP"


@pytest.mark.asyncio
async def test_when_valid_marital_status_then_return_marital_code(enumerate_model):
    marital_code = await enumerate_model.get_marital_status()

    assert isinstance(marital_code, int)
    assert marital_code == 1


@pytest.mark.asyncio
async def test_when_valid_nationalities_then_return_all_nationalities(enumerate_model):
    nationalities = await enumerate_model.get_nationalities()

    assert isinstance(nationalities, list)
    assert nationalities[0] == 1


@pytest.mark.asyncio
async def test_when_valid_nationality_and_no_spouse_then_return_one_nationality(
    enumerate_model_missing_country_and_spouse,
):
    nationalities = await enumerate_model_missing_country_and_spouse.get_nationalities()

    assert isinstance(nationalities, list)
    assert len(nationalities) == 1


@pytest.mark.asyncio
async def test_when_missing_spouse_nationality_then_raises(
    enumerate_model_missing_some_data,
):
    with pytest.raises(ValueError, match="Nationality value is required"):
        await enumerate_model_missing_some_data.get_nationalities()


@pytest.mark.asyncio
async def test_when_missing_document_state_then_raises(
    enumerate_model_missing_some_data,
):
    with pytest.raises(ValueError, match="State value is required"):
        await enumerate_model_missing_some_data.get_document_state()


@pytest.mark.asyncio
async def test_when_missing_marital_status_then_raises(
    enumerate_model_missing_some_data,
):
    with pytest.raises(ValueError, match="Marital status is required"):
        await enumerate_model_missing_some_data.get_marital_status()

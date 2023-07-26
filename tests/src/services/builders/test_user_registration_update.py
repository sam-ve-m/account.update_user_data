from unittest.mock import MagicMock, patch

import pytest

from func.src.services.builders.user_registration_update import (
    UpdateCustomerRegistrationBuilder,
)


dummy_simple_value = "value"
dummy_current_arg_id = 0


def test_dictionary_insert_without_levels():
    dummy_current_dict_level = {}
    result = UpdateCustomerRegistrationBuilder._dictionary_insert_with_levels(
        _value=dummy_simple_value, _current_dict_level=dummy_current_dict_level
    )
    assert result is None


def test_dictionary_insert_with_last_level():
    dummy_current_dict_level = {}
    result = UpdateCustomerRegistrationBuilder._dictionary_insert_with_levels(
        dummy_simple_value,
        _value=dummy_simple_value,
        _current_dict_level=dummy_current_dict_level,
    )
    assert result is None
    assert dummy_current_dict_level == {dummy_simple_value: dummy_simple_value}


def test_dictionary_insert_with_levels():
    dummy_current_dict_level = {dummy_simple_value: None}
    result = UpdateCustomerRegistrationBuilder._dictionary_insert_with_levels(
        dummy_simple_value,
        dummy_simple_value,
        _value=dummy_simple_value,
        _current_dict_level=dummy_current_dict_level,
    )
    assert result is None
    assert dummy_current_dict_level == {
        dummy_simple_value: {dummy_simple_value: dummy_simple_value}
    }


def test_dictionary_insert_with_levels_raising():
    dummy_current_dict_level = {dummy_simple_value: dummy_simple_value}
    with pytest.raises(TypeError):
        UpdateCustomerRegistrationBuilder._dictionary_insert_with_levels(
            dummy_simple_value,
            dummy_simple_value,
            _value=dummy_simple_value,
            _current_dict_level=dummy_current_dict_level,
        )


fake_instance = MagicMock()
dummy_sub_partition, dummy_field_name = "sub_partition", "field_name"


def test_get_new_value_empty_sub_partition():
    fake_instance._UpdateCustomerRegistrationBuilder__new_personal_data.get.return_value = (
        None
    )
    result = UpdateCustomerRegistrationBuilder._get_new_value(
        fake_instance, dummy_sub_partition, dummy_field_name
    )
    assert result is None


def test_get_new_value_empty_source():
    fake_instance._UpdateCustomerRegistrationBuilder__new_personal_data.get.return_value = (
        {}
    )
    result = UpdateCustomerRegistrationBuilder._get_new_value(
        fake_instance, dummy_sub_partition, dummy_field_name
    )
    assert result is None


def test_get_new_value():
    fake_instance._UpdateCustomerRegistrationBuilder__new_personal_data.get.return_value = {
        dummy_field_name: dummy_field_name
    }
    result = UpdateCustomerRegistrationBuilder._get_new_value(
        fake_instance, dummy_sub_partition, dummy_field_name
    )
    assert result == dummy_field_name


def test_get_new_value_wrapped():
    fake_instance._UpdateCustomerRegistrationBuilder__new_personal_data.get.return_value = {
        dummy_field_name: {"value": dummy_field_name}
    }
    result = UpdateCustomerRegistrationBuilder._get_new_value(
        fake_instance, dummy_sub_partition, dummy_field_name
    )
    assert result == dummy_field_name


fake_instance._get_new_value.return_value = None


def test_personal_name_empty():
    UpdateCustomerRegistrationBuilder.personal_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_nick_name_empty():
    UpdateCustomerRegistrationBuilder.personal_nick_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_birth_date_empty():
    UpdateCustomerRegistrationBuilder.personal_birth_date(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_birth_place_country_empty():
    UpdateCustomerRegistrationBuilder.personal_birth_place_country(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_birth_place_city_empty():
    UpdateCustomerRegistrationBuilder.personal_birth_place_city(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_birth_place_state_empty():
    UpdateCustomerRegistrationBuilder.personal_birth_place_state(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_gender_empty():
    UpdateCustomerRegistrationBuilder.personal_gender(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_us_person_empty():
    UpdateCustomerRegistrationBuilder.personal_us_person(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_father_name_empty():
    UpdateCustomerRegistrationBuilder.personal_father_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_mother_name_empty():
    UpdateCustomerRegistrationBuilder.personal_mother_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_email_empty():
    UpdateCustomerRegistrationBuilder.personal_email(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_phone_empty():
    UpdateCustomerRegistrationBuilder.personal_phone(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_nationality_empty():
    UpdateCustomerRegistrationBuilder.personal_nationality(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_occupation_activity_empty():
    UpdateCustomerRegistrationBuilder.personal_occupation_activity(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_occupation_cnpj_empty():
    UpdateCustomerRegistrationBuilder.personal_occupation_cnpj(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_company_name_empty():
    UpdateCustomerRegistrationBuilder.personal_company_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_patrimony_empty():
    UpdateCustomerRegistrationBuilder.personal_patrimony(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_income_empty():
    UpdateCustomerRegistrationBuilder.personal_income(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_personal_tax_residences_empty():
    UpdateCustomerRegistrationBuilder.personal_tax_residences(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_marital_status_empty():
    UpdateCustomerRegistrationBuilder.marital_status(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_marital_cpf_empty():
    UpdateCustomerRegistrationBuilder.marital_cpf(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_marital_nationality_empty():
    UpdateCustomerRegistrationBuilder.marital_nationality(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_marital_spouse_name_empty():
    UpdateCustomerRegistrationBuilder.marital_spouse_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_documents_cpf_empty():
    UpdateCustomerRegistrationBuilder.documents_cpf(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_documents_identity_type_empty():
    UpdateCustomerRegistrationBuilder.documents_identity_type(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_documents_identity_number_empty():
    UpdateCustomerRegistrationBuilder.documents_identity_number(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_documents_issuer_empty():
    UpdateCustomerRegistrationBuilder.documents_issuer(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_documents_state_empty():
    UpdateCustomerRegistrationBuilder.documents_state(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_country_empty():
    UpdateCustomerRegistrationBuilder.address_country(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_state_empty():
    UpdateCustomerRegistrationBuilder.address_state(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_city_empty():
    UpdateCustomerRegistrationBuilder.address_city(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_neighborhood_empty():
    UpdateCustomerRegistrationBuilder.address_neighborhood(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_street_name_empty():
    UpdateCustomerRegistrationBuilder.address_street_name(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_number_empty():
    UpdateCustomerRegistrationBuilder.address_number(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_zip_code_empty():
    UpdateCustomerRegistrationBuilder.address_zip_code(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_phone_empty():
    UpdateCustomerRegistrationBuilder.address_phone(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_address_complement_empty():
    UpdateCustomerRegistrationBuilder.address_complement(fake_instance)
    fake_instance._update_modified_data.assert_not_called()


def test_update_assets_update_date():
    UpdateCustomerRegistrationBuilder.update_assets_update_date(fake_instance)
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_politically_exposed_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_politically_exposed_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_exchange_member_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_exchange_member_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_time_experience_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_time_experience_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_company_director_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_company_director_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_is_company_director_of_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_is_company_director_of(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_user_employ_company_name_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_company_name_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_user_employ_position_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_position_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_user_employ_type_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_type_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_external_exchange_account_user_employ_status_us_empty():
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_status_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_once()


def test_personal_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("name",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_nick_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_nick_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("nick_name",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_birth_date():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_birth_date(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("birth_date",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_birth_place_country():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_birth_place_country(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("birth_place_country",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_birth_place_city():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_birth_place_city(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("birth_place_city",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_birth_place_state():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_birth_place_state(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("birth_place_state",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_gender():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_gender(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("gender",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_us_person():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_us_person(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("us_person",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_father_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_father_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("father_name",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_mother_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_mother_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("mother_name",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_email():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_email(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("email",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_phone():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_phone(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("phone",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_nationality():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_nationality(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("nationality",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_occupation_activity():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_occupation_activity(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("occupation", "activity"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_occupation_cnpj():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_occupation_cnpj(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("occupation", "company", "cnpj"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_company_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_company_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("occupation", "company", "name"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_patrimony():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_patrimony(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("assets", "patrimony"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_income():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_income(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("assets", "income"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_personal_tax_residences():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.personal_tax_residences(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("tax_residences",),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_marital_status():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.marital_status(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "status"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_marital_cpf():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.marital_cpf(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "spouse", "cpf"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value.get.return_value.get.return_value,
    )


def test_marital_nationality():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.marital_nationality(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "spouse", "nationality"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value.get.return_value.get.return_value,
    )


def test_marital_spouse_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.marital_spouse_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "spouse", "name"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value.get.return_value.get.return_value,
    )


def test_documents_cpf():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.documents_cpf(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("identifier_document", "cpf"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_documents_identity_type():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.documents_identity_type(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("identifier_document", "document_data", "type"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_documents_identity_number():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.documents_identity_number(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("identifier_document", "document_data", "number"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_documents_issuer():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.documents_issuer(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("identifier_document", "document_data", "issuer"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_documents_state():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.documents_state(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("identifier_document", "document_data", "state"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_country():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_country(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "country"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_state():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_state(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "state"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_city():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_city(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "city"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_neighborhood():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_neighborhood(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "neighborhood"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_street_name():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_street_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "street_name"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_number():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_number(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "number"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_zip_code():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_zip_code(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "zip_code"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_phone():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_phone(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "phone"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_address_complement():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.address_complement(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("address", "complement"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_politically_exposed_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_politically_exposed_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "is_politically_exposed"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_exchange_member_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_exchange_member_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "is_exchange_member"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_time_experience_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_time_experience_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "time_experience"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_company_director_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_company_director_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "is_company_director"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_is_company_director_of():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_is_company_director_of(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "is_company_director_of"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_user_employ_company_name_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_company_name_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "user_employ_company_name"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_user_employ_position_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_position_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "user_employ_position"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_user_employ_type_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_type_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "user_employ_type"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_external_exchange_account_user_employ_status_us():
    fake_instance._get_new_value.return_value = MagicMock()
    UpdateCustomerRegistrationBuilder.external_exchange_account_user_employ_status_us(
        fake_instance
    )
    fake_instance._update_modified_data.assert_called_with(
        levels=("external_exchange_requirements", "us", "user_employ_status"),
        old_field=fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value.get.return_value,
        new_filed=fake_instance._get_new_value.return_value,
    )


def test_marital_cpf_empty_spouse():
    fake_instance._get_new_value.return_value = MagicMock()
    fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value = (
        False
    )
    UpdateCustomerRegistrationBuilder.marital_cpf(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "spouse", "cpf"),
        old_field=None,
        new_filed=fake_instance._get_new_value.return_value.get.return_value.get.return_value,
    )


def test_marital_nationality_empty_spouse():
    fake_instance._get_new_value.return_value = MagicMock()
    fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value = (
        False
    )
    UpdateCustomerRegistrationBuilder.marital_nationality(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "spouse", "nationality"),
        old_field=None,
        new_filed=fake_instance._get_new_value.return_value.get.return_value.get.return_value,
    )


def test_marital_spouse_name_empty_spouse():
    fake_instance._get_new_value.return_value = MagicMock()
    fake_instance._UpdateCustomerRegistrationBuilder__old_personal_data.get.return_value.get.return_value = (
        False
    )
    UpdateCustomerRegistrationBuilder.marital_spouse_name(fake_instance)
    fake_instance._update_modified_data.assert_called_with(
        levels=("marital", "spouse", "name"),
        old_field=None,
        new_filed=fake_instance._get_new_value.return_value.get.return_value.get.return_value,
    )

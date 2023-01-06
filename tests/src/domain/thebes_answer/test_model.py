from unittest.mock import MagicMock

import pytest

from func.src.domain.thebes_answer.model import ThebesAnswer
from func.src.domain.exceptions.exceptions import ErrorOnGetUniqueId


def test_unique_id():
    dummy = MagicMock()
    response = ThebesAnswer.unique_id.fget(dummy)
    assert response == dummy.jwt_data.get.return_value.get.return_value


def test_unique_id_raising():
    dummy = MagicMock()
    dummy.jwt_data.get.return_value.get.return_value = None
    with pytest.raises(ErrorOnGetUniqueId):
        ThebesAnswer.unique_id.fget(dummy)

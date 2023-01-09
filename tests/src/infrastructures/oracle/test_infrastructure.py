from unittest.mock import patch, AsyncMock

import cx_Oracle_async
import pytest
from decouple import AutoConfig

from func.src.infrastructures.oracle.infrastrucuture import OracleInfrastructure

dummy_env = "env"
dummy_connection = "dummy connection"


@pytest.mark.asyncio
@patch.object(
    cx_Oracle_async, "create_pool", side_effect=AsyncMock(return_value=dummy_connection)
)
@patch.object(AutoConfig, "__call__", return_value=dummy_env)
async def test_get_pool(mocked_env, mock_connection):
    new_connection_created = await OracleInfrastructure._get_pool()
    assert new_connection_created == dummy_connection
    mock_connection.assert_called_once_with(
        user=dummy_env,
        password=dummy_env,
        min=2,
        max=100,
        increment=1,
        dsn=cx_Oracle_async.makedsn(
            dummy_env,
            dummy_env,
            service_name=dummy_env,
        ),
        encoding=dummy_env,
    )
    mocked_env.assert_called()

    reused_client = await OracleInfrastructure._get_pool()
    assert reused_client == new_connection_created
    mock_connection.assert_called_once_with(
        user=dummy_env,
        password=dummy_env,
        min=2,
        max=100,
        increment=1,
        dsn=cx_Oracle_async.makedsn(
            dummy_env,
            dummy_env,
            service_name=dummy_env,
        ),
        encoding=dummy_env,
    )
    mocked_env.assert_called()
    OracleInfrastructure.client = None

from ...domain.exceptions.exceptions import FailedToGetData
from ...infrastructures.oracle.infrastrucuture import OracleInfrastructure

from typing import List, Union

from etria_logger import Gladsheim
import cx_Oracle


class OracleBaseRepository:

    infra = OracleInfrastructure

    @classmethod
    async def query(cls, sql: str, filters: List[Union[str, int]]) -> list:
        try:
            async with cls.infra.get_connection() as cursor:
                await cursor.execute(sql, filters)
                rows = await cursor.fetchall()
                return rows

        except cx_Oracle.DataError as ex:
            (error,) = ex.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {ex}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

        except cx_Oracle.ProgrammingError as ex:
            (error,) = ex.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {ex}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

        except cx_Oracle.InternalError as ex:
            (error,) = ex.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {ex}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

        except cx_Oracle.NotSupportedError as ex:
            (error,) = ex.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {ex}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

        except cx_Oracle.DatabaseError as ex:
            (error,) = ex.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {ex}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

        except cx_Oracle.Error as ex:
            (error,) = ex.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {ex}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

        except Exception as ex:
            message = f"Exception: {ex=}. Oracle-Error-Base-Exception Sql: {sql=}"
            Gladsheim.error(error=ex, message=message)
            raise FailedToGetData("common.process_issue")

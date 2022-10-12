from ....infrastructures.mongo_db.infrastructure import MongoDBInfrastructure

from etria_logger import Gladsheim
from decouple import config


class MongoDbBaseRepository:
    infra = MongoDBInfrastructure

    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_USER_COLLECTION")]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

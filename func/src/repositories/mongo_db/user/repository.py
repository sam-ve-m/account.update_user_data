from etria_logger import Gladsheim

from func.src.repositories.mongo_db.base_repository.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):
    @classmethod
    async def get_user(cls, unique_id: str) -> dict:
        collection = await cls._get_collection()
        query = {"unique_id": unique_id}
        try:
            user = await collection.find_one(query)
            return user
        except Exception as ex:
            message = f"UserRepository::get_user::with this query {query}"
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def update_user(cls, unique_id: str, new_user_registration_data: dict):
        collection = await cls._get_collection()
        try:
            user_updated = await collection.update_one(
                {"unique_id": unique_id}, {"$set": new_user_registration_data}
            )
            return user_updated
        except Exception as ex:
            message = f"UserRepository::update_user::error to update user data"
            Gladsheim.error(error=ex, message=message)
            raise ex

from functools import lru_cache

from pymongo import MongoClient

from app.config import settings


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)


def get_db():
    return get_client()[settings.mongo_db_name]


if __name__ == "__main__":
    db = get_db()
    print("ping:", get_client().admin.command("ping"))
    print("database:", db.name)
    print("collections:", db.list_collection_names())

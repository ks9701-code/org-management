from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None

db = Database()


async def get_database():
    """Get database connection."""
    if db.client is None:
        db.client = AsyncIOMotorClient(settings.mongo_uri)
    return db.client


async def get_master_db():
    """Get master database instance."""
    database = await get_database()
    return database[settings.master_db]


async def get_org_collection(organization_name: str):
    """Get organization-specific collection."""
    from app.utils.naming import slugify_org_name
    database = await get_database()
    collection_name = slugify_org_name(organization_name)
    # Collections are stored in master_db but dynamically named per organization
    master_db = database[settings.master_db]
    return master_db[collection_name]


async def close_database():
    """Close database connection."""
    if db.client:
        db.client.close()


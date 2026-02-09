"""
Database Module - MongoDB Connection Management

Motor is the async MongoDB driver for Python. It allows FastAPI to handle
database operations without blocking - while waiting for MongoDB to respond,
FastAPI can handle other requests.

This module uses the Singleton pattern - we create one database connection
that's shared across all requests.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os


class Database:
    """
    Singleton database connection holder.

    We use a class to hold the client instance so it persists
    across the application lifetime.
    """
    client: Optional[AsyncIOMotorClient] = None


# Global database instance
db = Database()


# MongoDB connection URL (can be overridden with environment variable)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "rubikscube")


async def connect_to_mongo():
    """
    Connect to MongoDB. Called when the application starts.

    This is a "lifespan" event - it runs once at startup.
    """
    print(f"Connecting to MongoDB at {MONGODB_URL}...")
    db.client = AsyncIOMotorClient(MONGODB_URL)

    # Verify connection works
    try:
        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection. Called when the application shuts down.
    """
    print("Closing MongoDB connection...")
    if db.client:
        db.client.close()
        print("MongoDB connection closed")


async def get_database():
    """
    Get the database instance.

    Use this in your route handlers to access the database:

        db = await get_database()
        result = await db.solves.find_one({"_id": some_id})
    """
    return db.client[DATABASE_NAME]


async def get_solves_collection():
    """
    Convenience function to get the solves collection directly.
    """
    database = await get_database()
    return database.solves

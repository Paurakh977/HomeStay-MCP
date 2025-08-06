import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class HomestayDatabase:
    _instance: Optional['HomestayDatabase'] = None
    _client: Optional[AsyncIOMotorClient] = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self):
        """Connect to MongoDB"""
        if self._client is None:
            # Get MongoDB URI from environment or use default
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/HomestayDB')
            self._client = AsyncIOMotorClient(mongodb_uri)
            
            # Extract database name from URI or use default
            if '/' in mongodb_uri:
                db_name = mongodb_uri.split('/')[-1]
            else:
                db_name = 'HomestayDB'
                
            self._db = self._client[db_name]
            
        return self._db
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
    
    @property
    def db(self):
        return self._db
    
    @property
    def homestays(self):
        """Get the homestays collection"""
        return self._db['Homestays Collection'] if self._db else None

# Global database instance
db_instance = HomestayDatabase()
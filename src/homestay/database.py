import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class HomestayDatabase:
    _instance: Optional['HomestayDatabase'] = None
    _client: Optional[AsyncIOMotorClient] = None
    _db = None
    _connected = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self):
        """Connect to MongoDB with persistent connection"""
        if self._client is None or not self._connected:
            try:
                # Get MongoDB URI from environment or use default
                mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/HomestayDB')
                self._client = AsyncIOMotorClient(mongodb_uri)
                
                # Extract database name from URI or use default
                if '/' in mongodb_uri:
                    db_name = mongodb_uri.split('/')[-1]
                else:
                    db_name = 'HomestayDB'
                    
                self._db = self._client[db_name]
                
                # Test the connection
                await self._client.admin.command('ping')
                self._connected = True
                
            except Exception as e:
                self._connected = False
                raise Exception(f"Failed to connect to MongoDB: {str(e)}")
                
        return self._db
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            self._connected = False
    
    @property
    def db(self):
        return self._db
    
    @property
    def homestays(self):
        """Get the homestays collection"""
        if self._db is not None:
            return self._db['Homestays Collection']
        return None
    
    @property
    def is_connected(self):
        """Check if database is connected"""
        return self._connected and self._client is not None and self._db is not None

# Global database instance
db_instance = HomestayDatabase()
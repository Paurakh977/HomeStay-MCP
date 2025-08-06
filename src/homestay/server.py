from mcp.server.fastmcp import FastMCP
from .tools import filter_homestays, get_homestay_stats
from .models import HomestayFilterRequest, HomestayFilterResponse
from .database import db_instance
from typing import Dict, Any
import os
from contextlib import asynccontextmanager

# Create lifespan manager for database connection
@asynccontextmanager
async def lifespan_manager(server: FastMCP):
    """Manage database connection lifecycle"""
    try:
        # Connect to database on startup
        await db_instance.connect()
        print("Connected to MongoDB for homestay filtering")
        yield
    finally:
        # Disconnect on shutdown
        await db_instance.disconnect()
        print("Disconnected from MongoDB")

# Create FastMCP server with lifespan management
mcp = FastMCP(
    name="Homestay_Filter_Server", 
    stateless_http=True,
    lifespan=lifespan_manager
)

@mcp.tool(name="filter_homestays")
async def filter_homestays_tool(
    filter_request: HomestayFilterRequest
) -> HomestayFilterResponse:
    """
    Filter homestays based on comprehensive criteria and return matching usernames.
    
    This tool supports filtering by:
    - Location: province, district, municipality, ward, city, village
    - Basic info: name, type, status, admin
    - Capacity: home/room/bed counts, max guests
    - Ratings: minimum/maximum ratings and review counts
    - Price: price per night ranges
    - Features: amenities, attractions, services, infrastructure
    - Verification: verified, featured, admin status
    - Registration: DHSR number, authority, business registration
    - Dates: creation and update date ranges
    - Contact: owner name, phone, email, website
    - Custom fields: any custom field values
    - Text search: search across multiple fields
    
    All filters are optional and can be combined for complex queries.
    Returns only homestay usernames (homestayId) that match the criteria.
    
    Args:
        filter_request: Comprehensive filtering criteria
    
    Returns:
        HomestayFilterResponse with matching homestay usernames and counts
    """
    return await filter_homestays(filter_request)

@mcp.tool(name="get_homestay_statistics")
async def get_homestay_statistics_tool() -> Dict[str, Any]:
    """
    Get comprehensive statistics about homestays in the database.
    
    Returns statistics including:
    - Total number of homestays
    - Count by status (approved, pending, rejected)
    - Count by type (community, private)
    - Count by verification status
    - Count of featured homestays
    - Average ratings, rooms, and beds
    
    Returns:
        Dictionary containing homestay statistics
    """
    return await get_homestay_stats()

@mcp.tool(name="quick_filter_homestays")
async def quick_filter_homestays_tool(
    province: str = None,
    district: str = None,
    municipality: str = None,
    homestay_type: str = None,
    status: str = "approved",
    min_rating: float = None,
    amenities: list = None,
    limit: int = 50
) -> HomestayFilterResponse:
    """
    Quick filter for common homestay searches with simplified parameters.
    
    This is a simplified version of the main filter tool for common use cases.
    
    Args:
        province: Province name (English or Nepali)
        district: District name (English or Nepali)
        municipality: Municipality name (English or Nepali)
        homestay_type: Type of homestay ('community' or 'private')
        status: Homestay status ('approved', 'pending', 'rejected')
        min_rating: Minimum average rating
        amenities: List of required amenities
        limit: Maximum number of results to return
    
    Returns:
        HomestayFilterResponse with matching homestay usernames
    """
    filter_request = HomestayFilterRequest(
        province=province,
        district=district,
        municipality=municipality,
        homestay_type=homestay_type,
        status=status,
        min_average_rating=min_rating,
        amenities=amenities,
        limit=limit
    )
    
    return await filter_homestays(filter_request)
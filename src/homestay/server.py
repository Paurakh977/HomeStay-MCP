from mcp.server.fastmcp import FastMCP
from .tools import enhanced_filter_homestays, get_homestay_stats
from .models import HomestayFilterRequest, HomestayFilterResponse
from .database import db_instance
from typing import Dict, Any
import os
from contextlib import asynccontextmanager
from .models import EnhancedFeatureSearchHelper

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

@mcp.tool(name="search_homestays")
async def search_homestays_tool(
    # Location filters
    province: str = None,
    district: str = None,
    municipality: str = None,
    ward: str = None,
    city: str = None,
    village_name: str = None,
    
    # Basic information filters
    homestay_name: str = None,
    homestay_type: str = None,  # "community" or "private"
    status: str = "approved",  # "pending", "approved", "rejected"
    admin_username: str = None,
    
    # Capacity filters
    min_home_count: int = None,
    max_home_count: int = None,
    min_room_count: int = None,
    max_room_count: int = None,
    min_bed_count: int = None,
    max_bed_count: int = None,
    min_max_guests: int = None,
    max_max_guests: int = None,
    
    # Rating and review filters
    min_rating: float = None,
    max_rating: float = None,
    min_average_rating: float = None,
    max_average_rating: float = None,
    min_review_count: int = None,
    
    # Price filters
    min_price_per_night: float = None,
    max_price_per_night: float = None,
    
    # Feature filters (all must match)
    amenities: list = None,
    local_attractions: list = None,
    tourism_services: list = None,
    infrastructure: list = None,
    
    # Feature filters (any can match)
    any_amenities: list = None,
    any_local_attractions: list = None,
    any_tourism_services: list = None,
    any_infrastructure: list = None,
    
    # Boolean status filters
    is_verified: bool = None,
    is_featured: bool = None,
    is_admin: bool = None,
    
    # Team and operator filters
    min_team_members: int = None,
    max_team_members: int = None,
    operator_gender: str = None,  # "male", "female", "other"
    is_committee_driven: bool = None,
    availability_status: str = None,  # "available", "unavailable", "partially_available"
    
    # Registration filters
    dhsr_no: str = None,
    registration_authority: str = None,
    business_registration_number: str = None,
    
    # Contact filters
    owner_name: str = None,
    phone: str = None,
    email: str = None,
    website: str = None,
    
    # Search and pagination
    search_query: str = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = None,
    sort_order: str = "desc",  # "asc" or "desc"
    
    # Natural language processing for complex queries
    natural_language_description: str = None
) -> HomestayFilterResponse:
    """
    Comprehensive homestay search and filtering tool with advanced natural language processing.
    
    This is the primary tool for finding homestays based on various criteria. It supports:
    
    LOCATION FILTERING:
    - province: Filter by province name (supports both English and Nepali)
    - district: Filter by district name (supports both English and Nepali)
    - municipality: Filter by municipality name (supports both English and Nepali)
    - ward: Filter by ward number or name
    - city: Filter by city name
    - village_name: Filter by village name
    
    BASIC INFORMATION:
    - homestay_name: Search by homestay name (partial matching)
    - homestay_type: Filter by type ("community" or "private")
    - status: Filter by approval status ("pending", "approved", "rejected")
    - admin_username: Filter by admin username
    
    CAPACITY AND ACCOMMODATION:
    - min/max_home_count: Filter by number of homes
    - min/max_room_count: Filter by number of rooms
    - min/max_bed_count: Filter by number of beds
    - min/max_max_guests: Filter by maximum guest capacity
    
    RATINGS AND REVIEWS:
    - min/max_rating: Filter by rating range
    - min/max_average_rating: Filter by average rating range
    - min_review_count: Filter by minimum number of reviews
    
    PRICING:
    - min/max_price_per_night: Filter by price per night range
    
    FEATURES AND AMENITIES:
    - amenities: List of amenities that ALL must be present
    - any_amenities: List of amenities where ANY can be present
    - local_attractions: List of attractions that ALL must be present
    - any_local_attractions: List of attractions where ANY can be present
    - tourism_services: List of services that ALL must be present
    - any_tourism_services: List of services where ANY can be present
    - infrastructure: List of infrastructure that ALL must be present
    - any_infrastructure: List of infrastructure where ANY can be present
    
    VERIFICATION AND STATUS:
    - is_verified: Filter by verification status
    - is_featured: Filter by featured status
    - is_admin: Filter by admin status
    
    TEAM AND MANAGEMENT:
    - min/max_team_members: Filter by team size
    - operator_gender: Filter by operator gender ("male", "female", "other")
    - is_committee_driven: Filter by committee-driven homestays
    - availability_status: Filter by availability ("available", "unavailable", "partially_available")
    
    REGISTRATION AND LEGAL:
    - dhsr_no: Filter by DHSR registration number
    - registration_authority: Filter by registration authority
    - business_registration_number: Filter by business registration number
    
    CONTACT INFORMATION:
    - owner_name: Filter by owner name
    - phone: Filter by phone number
    - email: Filter by email address
    - website: Filter by website URL
    
    SEARCH AND PAGINATION:
    - search_query: Full-text search across multiple fields
    - skip: Number of results to skip (for pagination)
    - limit: Maximum number of results to return
    - sort_by: Field to sort by
    - sort_order: Sort direction ("asc" or "desc")
    
    NATURAL LANGUAGE PROCESSING:
    - natural_language_description: Describe what you're looking for in natural language.
      The system will automatically extract relevant filters from descriptions like:
      * "homestays with hiking and fishing facilities"
      * "committee-driven homestays with female operators"
      * "homestays with good toilets and wifi"
      * "homestays with rating over 3 and traditional food"
      * "available homestays with more than 3 team members"
    
    EXAMPLE USAGE:
    1. Find homestays in Kathmandu with hiking facilities:
       province="Province 3", district="Kathmandu", any_local_attractions=["Trekking, Climbing & Hiking Routes"]
    
    2. Find private homestays with good ratings:
       homestay_type="private", min_average_rating=3.0
    
    3. Find committee-driven homestays with female operators:
       is_committee_driven=True, operator_gender="female"
    
    4. Use natural language:
       natural_language_description="homestays with hiking and trekking facilities"
    
    Returns:
        HomestayFilterResponse containing:
        - homestay_usernames: List of matching homestay IDs
        - total_count: Total homestays in database
        - filtered_count: Number of homestays matching criteria
        - applied_filters: The actual MongoDB filters applied
        - suggestions: Helpful suggestions for refining search
    """
    
    # Process natural language description if provided
    extracted_filters = {}
    if natural_language_description:
        extracted_filters = EnhancedFeatureSearchHelper.enhanced_natural_query_processing(
            natural_language_description
        )
    
    # Build filter request with all parameters
    filter_request = HomestayFilterRequest(
        # Location
        province=province,
        district=district,
        municipality=municipality,
        ward=ward,
        city=city,
        village_name=village_name,
        
        # Basic info
        homestay_name=homestay_name,
        homestay_type=homestay_type,
        status=status,
        admin_username=admin_username,
        
        # Capacity
        min_home_count=min_home_count,
        max_home_count=max_home_count,
        min_room_count=min_room_count,
        max_room_count=max_room_count,
        min_bed_count=min_bed_count,
        max_bed_count=max_bed_count,
        min_max_guests=min_max_guests,
        max_max_guests=max_max_guests,
        
        # Ratings
        min_rating=min_rating,
        max_rating=max_rating,
        min_average_rating=min_average_rating or extracted_filters.get('min_average_rating'),
        max_average_rating=max_average_rating,
        min_review_count=min_review_count,
        
        # Price
        min_price_per_night=min_price_per_night,
        max_price_per_night=max_price_per_night,
        
        # Features (all must match)
        amenities=amenities,
        local_attractions=local_attractions,
        tourism_services=tourism_services,
        infrastructure=infrastructure,
        
        # Features (any can match) - merge with extracted filters
        any_amenities=any_amenities or extracted_filters.get('any_amenities'),
        any_local_attractions=any_local_attractions or extracted_filters.get('any_local_attractions'),
        any_tourism_services=any_tourism_services or extracted_filters.get('any_tourism_services'),
        any_infrastructure=any_infrastructure or extracted_filters.get('any_infrastructure'),
        
        # Boolean status
        is_verified=is_verified if is_verified is not None else extracted_filters.get('is_verified'),
        is_featured=is_featured if is_featured is not None else extracted_filters.get('is_featured'),
        is_admin=is_admin,
        
        # Team and operator - merge with extracted filters
        min_team_members=min_team_members or extracted_filters.get('min_team_members'),
        max_team_members=max_team_members,
        operator_gender=operator_gender or extracted_filters.get('operator_gender'),
        is_committee_driven=is_committee_driven if is_committee_driven is not None else extracted_filters.get('is_committee_driven'),
        availability_status=availability_status or extracted_filters.get('availability_status'),
        
        # Registration
        dhsr_no=dhsr_no,
        registration_authority=registration_authority,
        business_registration_number=business_registration_number,
        
        # Contact
        owner_name=owner_name,
        phone=phone,
        email=email,
        website=website,
        
        # Search and pagination
        search_query=search_query,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        
        # Merge any additional extracted filters
        feature_access=extracted_filters.get('feature_access')
    )
    
    return await enhanced_filter_homestays(filter_request)

@mcp.tool(name="get_homestay_statistics")
async def get_homestay_statistics_tool() -> Dict[str, Any]:
    """
    Get comprehensive statistics about homestays in the database.
    
    Returns detailed statistics including:
    - Total number of homestays
    - Count by status (approved, pending, rejected)
    - Count by type (community, private)
    - Count by verification status
    - Count of featured homestays
    - Average ratings, rooms, and beds
    - Distribution by provinces and districts
    
    This tool is useful for understanding the overall homestay landscape
    and getting insights into the database contents.
    
    Returns:
        Dictionary containing comprehensive homestay statistics
    """
    return await get_homestay_stats()

@mcp.tool(name="test_homestay_filtering")
async def test_homestay_filtering_tool() -> Dict[str, Any]:
    """
    Run a suite of tests to validate the homestay filtering logic.
    
    This tool executes several checks:
    1. Verifies the database connection and counts total documents.
    2. Fetches a sample document to inspect its structure.
    3. Tests exact matching for a full attraction string.
    4. Tests partial matching for English and Nepali keywords.
    5. Verifies the collection structure using the new helper function.

    Returns:
        A dictionary containing the results of each test.
    """
    from .tools import test_queries, verify_collection_structure
    
    print("--- Running Collection Structure Verification ---")
    await verify_collection_structure()
    
    print("\n--- Running Test Queries ---")
    await test_queries()
    
    return {"status": "completed", "message": "Tests executed. Check server logs for details."}
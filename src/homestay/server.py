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
    status: str = None,
    
    # Feature filters - Local Attractions
    any_local_attractions: list = None,
    local_attractions: list = None,
    
    # Feature filters - Infrastructure  
    any_infrastructure: list = None,
    infrastructure: list = None,
    
    # Feature filters - Tourism Services
    any_tourism_services: list = None,
    tourism_services: list = None,
    
    # Other filters
    min_average_rating: float = None,
    skip: int = 0,
    limit: int = 100,
    sort_order: str = "desc",
    natural_language_description: str = None,
    logical_operator: str = "AND"
) -> HomestayFilterResponse:
    """Updated tool with fixed filtering logic"""
    
    # Process natural language FIRST
    extracted_filters = {}
    if natural_language_description:
        extracted_filters = EnhancedFeatureSearchHelper.enhanced_natural_query_processing(
            natural_language_description
        )
        print(f"🔍 DEBUGGING - Extracted NL filters: {extracted_filters}")

    # Override logical_operator if detected in the natural language query
    final_logical_operator = extracted_filters.get('logical_operator', logical_operator)

    # 🔧 CRITICAL PARAMETER VALIDATION - Sanitize inputs FIRST
    print(f"🔍 RAW PARAMETERS - any_local_attractions: {any_local_attractions} (type: {type(any_local_attractions)})")

    # Validate and sanitize list parameters to prevent type errors
    def sanitize_list(value):
        if value is None:
            return None
        if not isinstance(value, list):
            value = [value]
        return [str(item).strip() for item in value if item and str(item).strip()]

    any_local_attractions = sanitize_list(any_local_attractions)
    local_attractions = sanitize_list(local_attractions)
    any_infrastructure = sanitize_list(any_infrastructure)
    infrastructure = sanitize_list(infrastructure)
    any_tourism_services = sanitize_list(any_tourism_services)
    tourism_services = sanitize_list(tourism_services)

    # 🔧 ENHANCED CONSOLIDATION: Handle both must-have and optional features correctly
    # Only add NL filters if explicit parameters are empty
    if not any_local_attractions and not local_attractions:
        must_attractions_from_nl = extracted_filters.get('local_attractions') or []
        optional_attractions_from_nl = extracted_filters.get('any_local_attractions') or []
        if must_attractions_from_nl:
            local_attractions = must_attractions_from_nl
        elif optional_attractions_from_nl:
            any_local_attractions = optional_attractions_from_nl
    
    if not any_infrastructure and not infrastructure:
        must_infrastructure_from_nl = extracted_filters.get('infrastructure') or []
        optional_infrastructure_from_nl = extracted_filters.get('any_infrastructure') or []
        if must_infrastructure_from_nl:
            infrastructure = must_infrastructure_from_nl
        elif optional_infrastructure_from_nl:
            any_infrastructure = optional_infrastructure_from_nl

    # Tourism services via NL
    if not any_tourism_services and not tourism_services:
        must_services_from_nl = extracted_filters.get('tourism_services') or []
        optional_services_from_nl = extracted_filters.get('any_tourism_services') or []
        if must_services_from_nl:
            tourism_services = must_services_from_nl
        elif optional_services_from_nl:
            any_tourism_services = optional_services_from_nl

    # Location and rating via NL, if supported
    if not province:
        province = extracted_filters.get('province')
    if not district:
        district = extracted_filters.get('district')
    if not municipality:
        municipality = extracted_filters.get('municipality')
    if not min_average_rating and extracted_filters.get('min_average_rating'):
        min_average_rating = extracted_filters.get('min_average_rating')

    print(f"🔍 SANITIZED PARAMETERS - any_local_attractions: {any_local_attractions}")
    print(f"🔍 SANITIZED PARAMETERS - local_attractions: {local_attractions}")
    print(f"🔍 SANITIZED PARAMETERS - any_infrastructure: {any_infrastructure}")
    print(f"🔍 SANITIZED PARAMETERS - infrastructure: {infrastructure}")
    print(f"🔍 SANITIZED PARAMETERS - any_tourism_services: {any_tourism_services}")
    print(f"🔍 SANITIZED PARAMETERS - tourism_services: {tourism_services}")
    
    filter_request = HomestayFilterRequest(
        province=province,
        district=district,
        municipality=municipality,
        status=status or "approved",  # Default to approved

        # Features
        any_local_attractions=any_local_attractions,
        local_attractions=local_attractions,
        any_infrastructure=any_infrastructure,
        infrastructure=infrastructure,
        any_tourism_services=any_tourism_services,
        tourism_services=tourism_services,

        # Other filters
        min_average_rating=min_average_rating,
        skip=skip,
        limit=limit,
        sort_order=sort_order,
        logical_operator=final_logical_operator
    )
    
    print(f"🔍 DEBUGGING - Final filter request: {filter_request.dict(exclude_none=True)}")
    
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
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
    # ... existing parameters ...
    province: str = None,
    district: str = None,
    status: str = None,
    any_local_attractions: list = None,
    local_attractions: list = None,
    any_infrastructure: list = None,
    infrastructure: list = None,
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
    if any_local_attractions:
        if not isinstance(any_local_attractions, list):
            any_local_attractions = [str(any_local_attractions)]
        # Remove empty strings and ensure all are strings
        any_local_attractions = [str(item).strip() for item in any_local_attractions if item and str(item).strip()]

    if local_attractions:
        if not isinstance(local_attractions, list):
            local_attractions = [str(local_attractions)]
        local_attractions = [str(item).strip() for item in local_attractions if item and str(item).strip()]

    if any_infrastructure:
        if not isinstance(any_infrastructure, list):
            any_infrastructure = [str(any_infrastructure)]
        any_infrastructure = [str(item).strip() for item in any_infrastructure if item and str(item).strip()]

    if infrastructure:
        if not isinstance(infrastructure, list):
            infrastructure = [str(infrastructure)]
        infrastructure = [str(item).strip() for item in infrastructure if item and str(item).strip()]

    # Consolidate features from both explicit parameters and natural language processing
    # 🔧 FIX: Only add NL filters if explicit parameters are empty
    if not any_local_attractions and not local_attractions:
        attractions_from_nl = extracted_filters.get('any_local_attractions') or []
        any_local_attractions = attractions_from_nl if attractions_from_nl else None
    
    if not any_infrastructure and not infrastructure:
        infrastructure_from_nl = extracted_filters.get('any_infrastructure') or []
        any_infrastructure = infrastructure_from_nl if infrastructure_from_nl else None

    print(f"🔍 SANITIZED PARAMETERS - any_local_attractions: {any_local_attractions}")
    print(f"🔍 SANITIZED PARAMETERS - local_attractions: {local_attractions}")
    print(f"🔍 SANITIZED PARAMETERS - any_infrastructure: {any_infrastructure}")
    print(f"🔍 SANITIZED PARAMETERS - infrastructure: {infrastructure}")
    
    filter_request = HomestayFilterRequest(
        province=province,
        district=district,
        status=status or "approved",  # Default to approved
        
        any_local_attractions=any_local_attractions,
        local_attractions=local_attractions,
        
        any_infrastructure=any_infrastructure,
        infrastructure=infrastructure,
        
        # ... other parameters
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
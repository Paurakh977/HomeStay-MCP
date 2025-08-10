from typing import List, Dict, Any, Optional
from .models import HomestayFilterRequest, HomestayFilterResponse
from .database import db_instance
import re
from datetime import datetime
from .models import EnhancedFeatureSearchHelper

async def build_mongodb_filter(filter_request: HomestayFilterRequest) -> Dict[str, Any]:
    """Build MongoDB filter from the filter request"""
    mongo_filter = {}
    lang = filter_request.language or "en"
    
    # Location filters
    if filter_request.province:
        if lang in ['en', 'ne']:
            mongo_filter[f"address.province.{lang}"] = {"$regex": filter_request.province, "$options": "i"}
        else:
            mongo_filter["$or"] = [
                {"address.province.en": {"$regex": filter_request.province, "$options": "i"}},
                {"address.province.ne": {"$regex": filter_request.province, "$options": "i"}}
            ]
    
    if filter_request.district:
        if lang in ['en', 'ne']:
            mongo_filter[f"address.district.{lang}"] = {"$regex": filter_request.district, "$options": "i"}
        else:
            if "$or" not in mongo_filter:
                mongo_filter["$or"] = []
            mongo_filter["$or"].extend([
                {"address.district.en": {"$regex": filter_request.district, "$options": "i"}},
                {"address.district.ne": {"$regex": filter_request.district, "$options": "i"}}
            ])
    
    if filter_request.municipality:
        if lang in ['en', 'ne']:
            mongo_filter[f"address.municipality.{lang}"] = {"$regex": filter_request.municipality, "$options": "i"}
        else:
            if "$or" not in mongo_filter:
                mongo_filter["$or"] = []
            mongo_filter["$or"].extend([
                {"address.municipality.en": {"$regex": filter_request.municipality, "$options": "i"}},
                {"address.municipality.ne": {"$regex": filter_request.municipality, "$options": "i"}}
            ])
    
    if filter_request.ward:
        if lang in ['en', 'ne']:
            mongo_filter[f"address.ward.{lang}"] = {"$regex": filter_request.ward, "$options": "i"}
        else:
            if "$or" not in mongo_filter:
                mongo_filter["$or"] = []
            mongo_filter["$or"].extend([
                {"address.ward.en": {"$regex": filter_request.ward, "$options": "i"}},
                {"address.ward.ne": {"$regex": filter_request.ward, "$options": "i"}}
            ])
    
    if filter_request.city:
        mongo_filter["address.city"] = {"$regex": filter_request.city, "$options": "i"}
    
    if filter_request.village_name:
        mongo_filter["villageName"] = {"$regex": filter_request.village_name, "$options": "i"}
    
    # Basic info filters
    if filter_request.homestay_name:
        mongo_filter["homeStayName"] = {"$regex": filter_request.homestay_name, "$options": "i"}
    
    if filter_request.homestay_type:
        mongo_filter["homeStayType"] = filter_request.homestay_type
    
    if filter_request.status:
        mongo_filter["status"] = filter_request.status
    
    if filter_request.admin_username:
        mongo_filter["adminUsername"] = filter_request.admin_username
    
    # Capacity filters
    if filter_request.min_home_count is not None:
        mongo_filter["homeCount"] = {"$gte": filter_request.min_home_count}
    if filter_request.max_home_count is not None:
        if "homeCount" in mongo_filter:
            mongo_filter["homeCount"]["$lte"] = filter_request.max_home_count
        else:
            mongo_filter["homeCount"] = {"$lte": filter_request.max_home_count}
    
    if filter_request.min_room_count is not None:
        mongo_filter["roomCount"] = {"$gte": filter_request.min_room_count}
    if filter_request.max_room_count is not None:
        if "roomCount" in mongo_filter:
            mongo_filter["roomCount"]["$lte"] = filter_request.max_room_count
        else:
            mongo_filter["roomCount"] = {"$lte": filter_request.max_room_count}
    
    if filter_request.min_bed_count is not None:
        mongo_filter["bedCount"] = {"$gte": filter_request.min_bed_count}
    if filter_request.max_bed_count is not None:
        if "bedCount" in mongo_filter:
            mongo_filter["bedCount"]["$lte"] = filter_request.max_bed_count
        else:
            mongo_filter["bedCount"] = {"$lte": filter_request.max_bed_count}
    
    if filter_request.min_max_guests is not None:
        mongo_filter["maxGuests"] = {"$gte": filter_request.min_max_guests}
    if filter_request.max_max_guests is not None:
        if "maxGuests" in mongo_filter:
            mongo_filter["maxGuests"]["$lte"] = filter_request.max_max_guests
        else:
            mongo_filter["maxGuests"] = {"$lte": filter_request.max_max_guests}
    
    # Rating filters
    if filter_request.min_rating is not None:
        mongo_filter["rating"] = {"$gte": filter_request.min_rating}
    if filter_request.max_rating is not None:
        if "rating" in mongo_filter:
            mongo_filter["rating"]["$lte"] = filter_request.max_rating
        else:
            mongo_filter["rating"] = {"$lte": filter_request.max_rating}
    
    if filter_request.min_average_rating is not None:
        mongo_filter["averageRating"] = {"$gte": filter_request.min_average_rating}
    if filter_request.max_average_rating is not None:
        if "averageRating" in mongo_filter:
            mongo_filter["averageRating"]["$lte"] = filter_request.max_average_rating
        else:
            mongo_filter["averageRating"] = {"$lte": filter_request.max_average_rating}
    
    if filter_request.min_review_count is not None:
        mongo_filter["reviewCount"] = {"$gte": filter_request.min_review_count}
    
    # Price filters
    if filter_request.min_price_per_night is not None:
        mongo_filter["pricePerNight"] = {"$gte": filter_request.min_price_per_night}
    if filter_request.max_price_per_night is not None:
        if "pricePerNight" in mongo_filter:
            mongo_filter["pricePerNight"]["$lte"] = filter_request.max_price_per_night
        else:
            mongo_filter["pricePerNight"] = {"$lte": filter_request.max_price_per_night}
    
    # Feature filters
    if filter_request.amenities:
        mongo_filter["amenities"] = {"$all": filter_request.amenities}
    
    if filter_request.any_amenities:
        mongo_filter["amenities"] = {"$in": filter_request.any_amenities}
    
    #  FEATURE FILTERS MOVED TO build_enhanced_mongodb_filter() TO AVOID CONFLICTS
    # All feature filtering (local_attractions, tourism_services, infrastructure) 
    # is now handled in build_enhanced_mongodb_filter() with proper regex logic

    # if filter_request.local_attractions:
    #     mongo_filter["features.localAttractions"] = {"$all": filter_request.local_attractions}
    
    # if filter_request.tourism_services:
    #     mongo_filter["features.tourismServices"] = {"$all": filter_request.tourism_services}
    
    # if filter_request.infrastructure:
    #     mongo_filter["features.infrastructure"] = {"$all": filter_request.infrastructure}
    
    # Boolean filters
    if filter_request.is_verified is not None:
        mongo_filter["isVerified"] = filter_request.is_verified
    
    if filter_request.is_featured is not None:
        mongo_filter["isFeatured"] = filter_request.is_featured
    
    if filter_request.is_admin is not None:
        mongo_filter["isAdmin"] = filter_request.is_admin
    
    # Registration filters
    if filter_request.dhsr_no:
        mongo_filter["dhsrNo"] = {"$regex": filter_request.dhsr_no, "$options": "i"}
    
    if filter_request.registration_authority:
        mongo_filter["registrationAuthority"] = {"$regex": filter_request.registration_authority, "$options": "i"}
    
    if filter_request.business_registration_number:
        mongo_filter["businessRegistrationNumber"] = {"$regex": filter_request.business_registration_number, "$options": "i"}
    
    # Date filters
    if filter_request.created_after:
        mongo_filter["createdAt"] = {"$gte": filter_request.created_after}
    if filter_request.created_before:
        if "createdAt" in mongo_filter:
            mongo_filter["createdAt"]["$lte"] = filter_request.created_before
        else:
            mongo_filter["createdAt"] = {"$lte": filter_request.created_before}
    
    if filter_request.updated_after:
        mongo_filter["updatedAt"] = {"$gte": filter_request.updated_after}
    if filter_request.updated_before:
        if "updatedAt" in mongo_filter:
            mongo_filter["updatedAt"]["$lte"] = filter_request.updated_before
        else:
            mongo_filter["updatedAt"] = {"$lte": filter_request.updated_before}
    
    # Contact filters
    if filter_request.owner_name:
        mongo_filter["ownerName"] = {"$regex": filter_request.owner_name, "$options": "i"}
    
    if filter_request.phone:
        mongo_filter["phone"] = {"$regex": filter_request.phone, "$options": "i"}
    
    if filter_request.email:
        mongo_filter["email"] = {"$regex": filter_request.email, "$options": "i"}
    
    if filter_request.website:
        mongo_filter["website"] = {"$regex": filter_request.website, "$options": "i"}
    
    # Team member count filters
    if filter_request.min_team_members is not None:
        if "$expr" in mongo_filter:
            existing_expr = mongo_filter["$expr"]
            mongo_filter["$expr"] = {
                "$and": [
                    existing_expr,
                    {"$gte": [{"$size": {"$ifNull": ["$teamMembers", []]}}, filter_request.min_team_members]}
                ]
            }
        else:
            mongo_filter["$expr"] = {"$gte": [{"$size": {"$ifNull": ["$teamMembers", []]}}, filter_request.min_team_members]}
    
    if filter_request.max_team_members is not None:
        if "$expr" in mongo_filter:
            existing_expr = mongo_filter["$expr"]
            mongo_filter["$expr"] = {
                "$and": [
                    existing_expr,
                    {"$lte": [{"$size": {"$ifNull": ["$teamMembers", []]}}, filter_request.max_team_members]}
                ]
            }
        else:
            mongo_filter["$expr"] = {"$lte": [{"$size": {"$ifNull": ["$teamMembers", []]}}, filter_request.max_team_members]}
    
    # New field filters
    if filter_request.operator_gender is not None:
        mongo_filter["operatorGender"] = filter_request.operator_gender
    
    if filter_request.is_committee_driven is not None:
        mongo_filter["isCommitteeDriven"] = filter_request.is_committee_driven
    
    if filter_request.availability_status is not None:
        mongo_filter["availabilityStatus"] = filter_request.availability_status
    
    # Custom field filters
    if filter_request.custom_fields:
        for field_id, value in filter_request.custom_fields.items():
            mongo_filter[f"customFields.values.{field_id}"] = value
    
    # Text search
    if filter_request.search_query:
        mongo_filter["$text"] = {"$search": filter_request.search_query}
    
    return mongo_filter

async def build_enhanced_mongodb_filter(filter_request: HomestayFilterRequest) -> Dict[str, Any]:
    """🔧 COMPLETELY REWRITTEN: Builds a MongoDB filter with proper support for mixed must-have and optional features."""
    mongo_filter = await build_basic_filters(filter_request)
    
    must_have_criteria = []  # AND logic - all must match
    optional_criteria = []   # OR logic - any can match

    def add_must_have_criteria(field: str, values: List[str]):
        """Handle must-have features (ALL must match - AND logic) with smart bilingual handling"""
        if not values:
            return
        
        try:
            for val in values:
                if isinstance(val, str) and val.strip():
                    # 🔧 CRITICAL FIX: Handle bilingual labels properly
                    parts = [p.strip() for p in val.strip().split('/') if p.strip()]
                    if len(parts) > 1:
                        # Bilingual term - create OR condition for EITHER language to match
                        # This is the KEY FIX: For must-have features, each term needs OR for its parts
                        bilingual_or = []
                        for part in parts:
                            # Try both exact and partial matching for better coverage
                            bilingual_or.append({field: {"$regex": part, "$options": "i"}})
                            # For complex phrases, also try key words
                            words = part.split()
                            if len(words) > 2:
                                for word in words:
                                    if len(word.strip()) > 3:
                                        bilingual_or.append({field: {"$regex": word.strip(), "$options": "i"}})
                        # Each bilingual term gets its own OR clause, but terms are ANDed together
                        must_have_criteria.append({"$or": bilingual_or})
                    else:
                        # Single term - try both exact and partial matching
                        words = val.split()
                        if len(words) > 2:
                            # For phrases, create OR with full phrase + key words
                            phrase_or = [
                                {field: {"$regex": val.strip(), "$options": "i"}}
                            ]
                            for word in words:
                                if len(word.strip()) > 3:
                                    phrase_or.append({field: {"$regex": word.strip(), "$options": "i"}})
                            must_have_criteria.append({"$or": phrase_or})
                        else:
                            must_have_criteria.append({field: {"$regex": val.strip(), "$options": "i"}})
                
        except Exception as e:
            print(f"⚠️ Error processing must-have criteria for {field}: {e}")

    def add_optional_criteria(field: str, values: List[str]):
        """Handle optional features (ANY can match - OR logic) with smart bilingual handling"""
        if not values:
            return
        
        try:
            all_patterns = []
            for val in values:
                if isinstance(val, str) and val.strip():
                    # Handle bilingual labels
                    parts = [p.strip() for p in val.strip().split('/') if p.strip()]
                    all_patterns.extend(parts)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_patterns = []
            for p in all_patterns:
                if p.lower() not in seen:
                    unique_patterns.append(p)
                    seen.add(p.lower())
            
            if unique_patterns:
                # Create OR conditions for all patterns
                or_conditions = []
                for pattern in unique_patterns:
                    or_conditions.append({field: {"$regex": pattern, "$options": "i"}})
                
                if len(or_conditions) == 1:
                    optional_criteria.append(or_conditions[0])
                else:
                    optional_criteria.append({"$or": or_conditions})
                
        except Exception as e:
            print(f"⚠️ Error processing optional criteria for {field}: {e}")

    # 🔧 CRITICAL: Process must-have and optional features separately
    # Must-have features (ALL must match)
    add_must_have_criteria("features.localAttractions", filter_request.local_attractions)
    add_must_have_criteria("features.infrastructure", filter_request.infrastructure)
    add_must_have_criteria("features.tourismServices", filter_request.tourism_services)
    
    # Optional features (ANY can match)
    add_optional_criteria("features.localAttractions", filter_request.any_local_attractions)
    add_optional_criteria("features.infrastructure", filter_request.any_infrastructure)
    add_optional_criteria("features.tourismServices", filter_request.any_tourism_services)

    # 🔧 SMART LOGIC: Handle different logical operators intelligently
    logical_operator = filter_request.logical_operator or "AND"
    
    # Check if we have mixed feature types (attractions + infrastructure/tourism)
    has_attractions = bool(filter_request.local_attractions or filter_request.any_local_attractions)
    has_infrastructure = bool(filter_request.infrastructure or filter_request.any_infrastructure)
    has_tourism = bool(filter_request.tourism_services or filter_request.any_tourism_services)
    
    feature_type_count = sum([has_attractions, has_infrastructure, has_tourism])
    is_mixed_types = feature_type_count > 1
    
    # 🔧 ENHANCED LOGIC: Combine criteria based on logical operator
    all_criteria = []
    
    if logical_operator == "MIXED":
        # MIXED operator: Combine intelligently for mixed feature scenarios
        if must_have_criteria and optional_criteria:
            # Strategy: (must-have1 AND must-have2) OR (optional1 OR optional2)
            must_combined = {"$and": must_have_criteria} if len(must_have_criteria) > 1 else must_have_criteria[0]
            optional_combined = {"$or": optional_criteria} if len(optional_criteria) > 1 else optional_criteria[0]
            all_criteria.append({"$or": [must_combined, optional_combined]})
        elif must_have_criteria:
            # Only must-have features with MIXED operator - be more permissive
            if is_mixed_types:
                # For mixed types, use OR between categories
                category_groups = {"attractions": [], "infrastructure": [], "tourism": []}
                
                for criterion in must_have_criteria:
                    # Determine which category this criterion belongs to
                    if "features.localAttractions" in str(criterion):
                        category_groups["attractions"].append(criterion)
                    elif "features.infrastructure" in str(criterion):
                        category_groups["infrastructure"].append(criterion)
                    elif "features.tourismServices" in str(criterion):
                        category_groups["tourism"].append(criterion)
                
                # Combine within categories with AND, between categories with OR
                category_criteria = []
                for category, criteria in category_groups.items():
                    if criteria:
                        if len(criteria) == 1:
                            category_criteria.append(criteria[0])
                        else:
                            category_criteria.append({"$and": criteria})
                
                if len(category_criteria) == 1:
                    all_criteria.append(category_criteria[0])
                else:
                    all_criteria.append({"$or": category_criteria})
            else:
                # Same category features - use AND
                all_criteria.extend(must_have_criteria)
        elif optional_criteria:
            # Only optional features - use OR
            if len(optional_criteria) == 1:
                all_criteria.append(optional_criteria[0])
            else:
                all_criteria.append({"$or": optional_criteria})
    
    elif logical_operator == "OR":
        # OR operator: All features are treated as optional
        combined_criteria = must_have_criteria + optional_criteria
        if len(combined_criteria) == 1:
            all_criteria.append(combined_criteria[0])
        elif combined_criteria:
            all_criteria.append({"$or": combined_criteria})
    
    else:  # Default "AND" operator
        if must_have_criteria and optional_criteria:
            # 🔧 CRITICAL FIX: For mixed types with AND operator, be more flexible
            if is_mixed_types:
                # Mixed types with AND - use OR between categories but AND within
                category_groups = {"attractions": [], "infrastructure": [], "tourism": []}
                
                # Categorize all criteria (both must-have and optional)
                all_combined = must_have_criteria + optional_criteria
                for criterion in all_combined:
                    if "features.localAttractions" in str(criterion):
                        category_groups["attractions"].append(criterion)
                    elif "features.infrastructure" in str(criterion):
                        category_groups["infrastructure"].append(criterion)
                    elif "features.tourismServices" in str(criterion):
                        category_groups["tourism"].append(criterion)
                
                # Build category-wise criteria
                category_criteria = []
                for category, criteria in category_groups.items():
                    if criteria:
                        if len(criteria) == 1:
                            category_criteria.append(criteria[0])
                        else:
                            category_criteria.append({"$and": criteria})
                
                # Use OR between categories for better results
                if len(category_criteria) == 1:
                    all_criteria.append(category_criteria[0])
                else:
                    all_criteria.append({"$or": category_criteria})
            else:
                # Same category - standard AND logic
                all_criteria.extend(must_have_criteria)
                if len(optional_criteria) == 1:
                    all_criteria.append(optional_criteria[0])
                else:
                    all_criteria.append({"$or": optional_criteria})
        elif must_have_criteria:
            # Only must-have features
            if is_mixed_types and len(must_have_criteria) > 2:
                # For mixed types with multiple features, use OR for broader results
                all_criteria.append({"$or": must_have_criteria})
            else:
                all_criteria.extend(must_have_criteria)
        elif optional_criteria:
            # Only optional features - use OR
            if len(optional_criteria) == 1:
                all_criteria.append(optional_criteria[0])
            else:
                all_criteria.append({"$or": optional_criteria})

    # Apply the combined criteria to the filter
    if all_criteria:
        if len(all_criteria) == 1:
            # Single criterion - add directly but be careful about structure
            criterion = all_criteria[0]
            if isinstance(criterion, dict):
                # Check if it's a simple field:value or complex condition
                if any(key.startswith('$') for key in criterion.keys()):
                    # Complex condition - add to $and
                    if "$and" in mongo_filter:
                        mongo_filter["$and"].append(criterion)
                    else:
                        mongo_filter["$and"] = [criterion]
                else:
                    # Simple field condition - can merge directly if no conflicts
                    for key, value in criterion.items():
                        if key in mongo_filter:
                            # Conflict - use $and to combine
                            if "$and" in mongo_filter:
                                mongo_filter["$and"].append(criterion)
                            else:
                                mongo_filter["$and"] = [criterion]
                            break
                        else:
                            mongo_filter[key] = value
        else:
            # Multiple criteria - combine with $and
            if "$and" in mongo_filter:
                mongo_filter["$and"].extend(all_criteria)
            else:
                mongo_filter["$and"] = all_criteria
                
    return mongo_filter

async def build_basic_filters(filter_request: HomestayFilterRequest) -> Dict[str, Any]:
    """Build non-conflicting basic filters"""
    filters = {}
    lang = filter_request.language or "en"
    
    # Location filters with proper bilingual support
    if filter_request.province:
        if lang in ['en', 'ne']:
            filters[f"address.province.{lang}"] = {"$regex": filter_request.province, "$options": "i"}
        else:
            filters["$or"] = [
                {"address.province.en": {"$regex": filter_request.province, "$options": "i"}},
                {"address.province.ne": {"$regex": filter_request.province, "$options": "i"}}
            ]
    
    if filter_request.district:
        if lang in ['en', 'ne']:
            filters[f"address.district.{lang}"] = {"$regex": filter_request.district, "$options": "i"}
        else:
            if "$or" not in filters:
                filters["$or"] = []
            filters["$or"].extend([
                {"address.district.en": {"$regex": filter_request.district, "$options": "i"}},
                {"address.district.ne": {"$regex": filter_request.district, "$options": "i"}}
            ])
    
    if filter_request.municipality:
        if lang in ['en', 'ne']:
            filters[f"address.municipality.{lang}"] = {"$regex": filter_request.municipality, "$options": "i"}
        else:
            if "$or" not in filters:
                filters["$or"] = []
            filters["$or"].extend([
                {"address.municipality.en": {"$regex": filter_request.municipality, "$options": "i"}},
                {"address.municipality.ne": {"$regex": filter_request.municipality, "$options": "i"}}
            ])
    
    if filter_request.ward:
        if lang in ['en', 'ne']:
            filters[f"address.ward.{lang}"] = {"$regex": filter_request.ward, "$options": "i"}
        else:
            if "$or" not in filters:
                filters["$or"] = []
            filters["$or"].extend([
                {"address.ward.en": {"$regex": filter_request.ward, "$options": "i"}},
                {"address.ward.ne": {"$regex": filter_request.ward, "$options": "i"}}
            ])

    if filter_request.city:
        filters["address.city"] = {"$regex": filter_request.city, "$options": "i"}

    if filter_request.village_name:
        filters["villageName"] = {"$regex": filter_request.village_name, "$options": "i"}

    if filter_request.homestay_name:
        filters["homeStayName"] = {"$regex": filter_request.homestay_name, "$options": "i"}

    if filter_request.homestay_type:
        filters["homeStayType"] = filter_request.homestay_type

    if filter_request.admin_username:
        filters["adminUsername"] = filter_request.admin_username
    
    # Default to approved status
    if filter_request.status:
        filters["status"] = filter_request.status
    elif "status" not in filters:
        filters["status"] = "approved"
    
    # Add other basic filters (ratings, capacity, etc.)
    if filter_request.min_average_rating:
        filters["averageRating"] = {"$gte": filter_request.min_average_rating}
    
    if filter_request.max_average_rating:
        if "averageRating" in filters:
            filters["averageRating"]["$lte"] = filter_request.max_average_rating
        else:
            filters["averageRating"] = {"$lte": filter_request.max_average_rating}

    # Boolean filters
    if filter_request.is_verified is not None:
        filters["isVerified"] = filter_request.is_verified
    
    if filter_request.is_featured is not None:
        filters["isFeatured"] = filter_request.is_featured
    
    if filter_request.is_admin is not None:
        filters["isAdmin"] = filter_request.is_admin
    
    return filters


async def filter_homestays(filter_request: HomestayFilterRequest) -> HomestayFilterResponse:
    """Main homestay filtering function"""
    return await enhanced_filter_homestays(filter_request)

async def enhanced_filter_homestays(filter_request: HomestayFilterRequest) -> HomestayFilterResponse:
    """Enhanced homestay filtering with DETAILED DEBUGGING"""
    try:
        print(f"🔍 INPUT - Filter Request: {filter_request.dict(exclude_none=True)}")
        
        # Build MongoDB filter
        mongo_filter = await build_enhanced_mongodb_filter(filter_request)
        print(f"🔍 MONGODB - Generated Filter: {mongo_filter}")
        
        collection = db_instance.homestays

        # Test individual components
        if mongo_filter.get("$or"):
            print(f"🔍 OR CONDITIONS - Count: {len(mongo_filter['$or'])}")
            for i, condition in enumerate(mongo_filter["$or"]):
                test_count = await collection.count_documents(condition)
                print(f"🔍 OR[{i}] - {condition} → Count: {test_count}")
        
        # Execute main query
        filtered_count = await collection.count_documents(mongo_filter)
        print(f"🔍 RESULT - Filtered count: {filtered_count}")
        
        # If no results, run diagnostic queries
        if filtered_count == 0:
            await run_diagnostic_queries(filter_request, mongo_filter)
        
        # --- RELAXED FALLBACK: Broaden search if no results ---
        relaxed_applied = False
        if filtered_count == 0:
            # Prepare a relaxed version of the request
            relaxed_request = HomestayFilterRequest(**filter_request.dict())

            # Determine present categories
            has_attractions = bool(relaxed_request.local_attractions or relaxed_request.any_local_attractions)
            has_infrastructure = bool(relaxed_request.infrastructure or relaxed_request.any_infrastructure)
            has_tourism = bool(relaxed_request.tourism_services or relaxed_request.any_tourism_services)

            # Move must-have features to optional to broaden results
            def move_to_optional(any_field: str, must_field: str):
                must_vals = getattr(relaxed_request, must_field)
                if must_vals:
                    existing_any = getattr(relaxed_request, any_field) or []
                    # Merge and deduplicate while preserving order
                    merged = []
                    for v in existing_any + must_vals:
                        if v and v not in merged:
                            merged.append(v)
                    setattr(relaxed_request, any_field, merged)
                    setattr(relaxed_request, must_field, None)

            move_to_optional('any_local_attractions', 'local_attractions')
            move_to_optional('any_infrastructure', 'infrastructure')
            move_to_optional('any_tourism_services', 'tourism_services')

            # Re-evaluate categories after moving
            has_attractions = bool(relaxed_request.local_attractions or relaxed_request.any_local_attractions)
            has_infrastructure = bool(relaxed_request.infrastructure or relaxed_request.any_infrastructure)
            has_tourism = bool(relaxed_request.tourism_services or relaxed_request.any_tourism_services)
            feature_type_count = sum([has_attractions, has_infrastructure, has_tourism])

            # Choose a more permissive operator
            relaxed_request.logical_operator = "MIXED" if feature_type_count > 1 else "OR"

            # Build and test relaxed filter
            relaxed_filter = await build_enhanced_mongodb_filter(relaxed_request)
            print(f"🔍 RELAXED - Generated Filter: {relaxed_filter}")
            relaxed_count = await collection.count_documents(relaxed_filter)
            print(f"🔍 RELAXED - Filtered count: {relaxed_count}")

            if relaxed_count > 0:
                # Adopt relaxed results
                filter_request = relaxed_request
                mongo_filter = relaxed_filter
                filtered_count = relaxed_count
                relaxed_applied = True
                print("🔧 Applied relaxed search: converted must-have features to optional and switched logical operator for broader results")
        
        # Get total count
        total_count = await collection.count_documents({})

        # Execute query with sorting
        sort_criteria = []
        if filter_request.sort_by:
            sort_direction = 1 if filter_request.sort_order == "asc" else -1
            sort_criteria.append((filter_request.sort_by, sort_direction))
        else:
            # Default sorting by average rating (descending) and creation date
            sort_criteria = [("averageRating", -1), ("createdAt", -1)]
        
        cursor = collection.find(
            mongo_filter,
            {"homestayId": 1, "_id": 0}
        ).sort(sort_criteria).skip(filter_request.skip or 0).limit(filter_request.limit or 100)
        
        # Extract usernames
        homestays = await cursor.to_list(length=None)
        usernames = [homestay.get("homestayId") for homestay in homestays if homestay.get("homestayId")]
        
        # Generate suggestions for better filtering
        suggestions = await generate_filter_suggestions(filter_request, filtered_count)
        if 'relaxed_applied' in locals() and relaxed_applied:
            suggestions.insert(0, f"Applied relaxed search automatically (operator={filter_request.logical_operator}). Consider specifying fewer must-have features or using any_* lists.")
        
        return HomestayFilterResponse(
            homestayUsernames=usernames,
            totalCount=total_count,
            filteredCount=filtered_count,
            appliedFilters=mongo_filter,
            suggestions=suggestions
        )
        
    except Exception as e:
        # Add more detailed error logging
        import traceback
        print(f"💥 ERROR in enhanced_filter_homestays: {e}")
        print(traceback.format_exc())
        raise Exception(f"Error filtering homestays: {str(e)}")

async def run_diagnostic_queries(filter_request, mongo_filter):
    """Run diagnostic queries to understand why no results found"""
    collection = db_instance.homestays
    
    # Test without status filter
    no_status_filter = {k: v for k, v in mongo_filter.items() if k != 'status'}
    if no_status_filter:
        count = await collection.count_documents(no_status_filter)
        print(f"🔍 DIAGNOSTIC - Without status filter: {count}")
    
    # Test with broader regex patterns
    if filter_request.any_local_attractions:
        for attraction in filter_request.any_local_attractions:
            if isinstance(attraction, str) and attraction.strip():
                # Get the first word properly - FIXED
                words = attraction.strip().split()
                first_word = words[0] if words else attraction.strip()
                
                try:
                    broad_filter = {
                        "features.localAttractions": {
                            "$regex": re.escape(first_word),  # ✅ Now first_word is guaranteed to be a string
                            "$options": "i"
                        }
                    }
                    count = await collection.count_documents(broad_filter)
                    print(f"🔍 DIAGNOSTIC - Broad match '{first_word}': {count}")
                except Exception as e:
                    print(f"🔍 DIAGNOSTIC - Error testing '{attraction}': {e}")

async def generate_filter_suggestions(filter_request: HomestayFilterRequest, filtered_count: int) -> List[str]:
    """Generate helpful suggestions for improving filter results"""
    suggestions = []
    
    if filtered_count == 0:
        suggestions.append("No homestays found. Try relaxing some criteria or using broader keywords.")
        if filter_request.min_average_rating:
            suggestions.append(f"Consider lowering the minimum rating from {filter_request.min_average_rating}")
        if filter_request.local_attractions:
            suggestions.append("Try using 'any_local_attractions' instead of requiring all attractions")
    elif filtered_count > 100:
        suggestions.append("Many results found. Consider adding more specific criteria for better matches.")
        if not filter_request.min_average_rating:
            suggestions.append("Add a minimum rating filter to find higher quality homestays")
    
    return suggestions

async def get_homestay_stats() -> Dict[str, Any]:
    """
    Get basic statistics about homestays in the database.
    
    Returns:
        Dictionary containing homestay statistics
    """
    try:
        # Use existing database connection
        collection = db_instance.homestays
        
        # Validate collection availability
        if collection is None or not db_instance.is_connected:
            raise Exception("Database not connected. Please ensure the server is properly initialized.")
        
        # Aggregate statistics
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_homestays": {"$sum": 1},
                    "approved_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$status", "approved"]}, 1, 0]}
                    },
                    "pending_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$status", "pending"]}, 1, 0]}
                    },
                    "rejected_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$status", "rejected"]}, 1, 0]}
                    },
                    "community_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$homeStayType", "community"]}, 1, 0]}
                    },
                    "private_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$homeStayType", "private"]}, 1, 0]}
                    },
                    "verified_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$isVerified", True]}, 1, 0]}
                    },
                    "featured_homestays": {
                        "$sum": {"$cond": [{"$eq": ["$isFeatured", True]}, 1, 0]}
                    },
                    "avg_rating": {"$avg": "$averageRating"},
                    "avg_rooms": {"$avg": "$roomCount"},
                    "avg_beds": {"$avg": "$bedCount"}
                }
            }
        ]
        
        result = await collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            stats = result[0]
            stats.pop("_id", None)  # Remove the _id field
            return stats
        else:
            return {
                "total_homestays": 0,
                "approved_homestays": 0,
                "pending_homestays": 0,
                "rejected_homestays": 0,
                "community_homestays": 0,
                "private_homestays": 0,
                "verified_homestays": 0,
                "featured_homestays": 0,
                "avg_rating": 0,
                "avg_rooms": 0,
                "avg_beds": 0
            }
            
    except Exception as e:
        raise Exception(f"Error getting homestay statistics: {str(e)}")


async def validate_address_relationships(filter_request: HomestayFilterRequest) -> Dict[str, str]:
    """Validate and suggest corrections for address relationships"""
    suggestions = {}
    
    # Add logic to check if district exists in specified province
    # Add logic to check if municipality exists in specified district
    
    return suggestions

def create_fuzzy_filter(field_path: str, search_terms: List[str]) -> Dict:
    """Create fuzzy search filter for better matching"""
    conditions = []
    
    for term in search_terms:
        # Split compound terms and create individual regex patterns
        words = term.replace(',', ' ').split()
        word_conditions = []
        
        for word in words:
            if len(word.strip()) > 2:  # Only search meaningful words
                word_conditions.append({
                    field_path: {
                        "$regex": word.strip(),
                        "$options": "i"
                    }
                })
        
        if word_conditions:
            conditions.extend(word_conditions)
    
    return {"$or": conditions} if conditions else {}

async def verify_collection_structure():
    """Debug function to verify collection structure"""
    try:
        db = await db_instance.connect()
        collections = await db.list_collection_names()
        print(f"🔍 Available collections: {collections}")
        
        collection_name = 'Homestays Collection'
        if collection_name in collections:
            sample_doc = await db[collection_name].find_one()
            if sample_doc:
                print(f"🔍 Sample document structure for '{collection_name}':")
                print(f"  - Keys: {list(sample_doc.keys())}")
                if 'features' in sample_doc and isinstance(sample_doc['features'], dict):
                    print(f"  - Features keys: {list(sample_doc['features'].keys())}")
                    if 'localAttractions' in sample_doc['features']:
                        print(f"  - Sample Local Attractions: {sample_doc['features']['localAttractions'][:2]}...")
                if 'address' in sample_doc and isinstance(sample_doc['address'], dict):
                    print(f"  - Address keys: {list(sample_doc['address'].keys())}")
        else:
            print(f"⚠️ Collection '{collection_name}' not found!")
        
    except Exception as e:
        print(f"🔍 Error verifying collection: {e}")

async def test_queries():
    """Test function to validate fixes"""
    collection = db_instance.homestays
    if not collection:
        print("❌ Database not connected, cannot run tests.")
        return

    # Test 1: Basic connection and data
    total = await collection.count_documents({})
    print(f"✅ Total homestays: {total}")
    
    # Test 2: Sample documents
    sample = await collection.find_one()
    if sample:
        print(f"✅ Sample doc features keys: {sample.get('features', {}).keys()}")
    else:
        print("❌ No sample document found.")

    # Test 3: Exact attraction matching
    exact_match_count = await collection.count_documents({
        "features.localAttractions": "Trekking, Climbing & Hiking Routes/ट्रेकिङ, आरोहण तथा हाइकिङ मार्गहरू"
    })
    print(f"✅ Exact match count for 'Trekking...': {exact_match_count}")
    
    # Test 4: Partial matching
    partial_match_count = await collection.count_documents({
        "features.localAttractions": {"$regex": "Trekking", "$options": "i"}
    })
    print(f"✅ Partial match count for 'Trekking': {partial_match_count}")

    # Test 5: Partial matching for Nepali
    partial_match_nepali = await collection.count_documents({
        "features.localAttractions": {"$regex": "ट्रेकिङ", "$options": "i"}
    })
    print(f"✅ Partial match count for 'ट्रेकिङ': {partial_match_nepali}")
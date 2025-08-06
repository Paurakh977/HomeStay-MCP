from typing import List, Dict, Any, Optional
from .models import HomestayFilterRequest, HomestayFilterResponse
from .database import db_instance
import re
from datetime import datetime

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
    
    if filter_request.local_attractions:
        mongo_filter["features.localAttractions"] = {"$all": filter_request.local_attractions}
    
    if filter_request.tourism_services:
        mongo_filter["features.tourismServices"] = {"$all": filter_request.tourism_services}
    
    if filter_request.infrastructure:
        mongo_filter["features.infrastructure"] = {"$all": filter_request.infrastructure}
    
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
    
    # Custom field filters
    if filter_request.custom_fields:
        for field_id, value in filter_request.custom_fields.items():
            mongo_filter[f"customFields.values.{field_id}"] = value
    
    # Text search
    if filter_request.search_query:
        mongo_filter["$text"] = {"$search": filter_request.search_query}
    
    return mongo_filter

async def filter_homestays(
    filter_request: HomestayFilterRequest
) -> HomestayFilterResponse:
    """
    Filter homestays based on the provided criteria and return usernames.
    
    Args:
        filter_request: The filtering criteria
    
    Returns:
        HomestayFilterResponse containing filtered homestay usernames
    """
    try:
        # Connect to database
        db = await db_instance.connect()
        collection = db_instance.homestays
        
        if not collection:
            raise Exception("Failed to connect to homestays collection")
        
        # Build MongoDB filter
        mongo_filter = await build_mongodb_filter(filter_request)
        
        # Get total count of all homestays
        total_count = await collection.count_documents({})
        
        # Get count of filtered homestays
        filtered_count = await collection.count_documents(mongo_filter)
        
        # Execute query with pagination
        cursor = collection.find(
            mongo_filter,
            {"homestayId": 1, "_id": 0}  # Only return homestayId field
        ).skip(filter_request.skip or 0).limit(filter_request.limit or 100)
        
        # Extract usernames
        homestays = await cursor.to_list(length=None)
        usernames = [homestay.get("homestayId") for homestay in homestays if homestay.get("homestayId")]
        
        return HomestayFilterResponse(
            homestay_usernames=usernames,
            total_count=total_count,
            filtered_count=filtered_count
        )
        
    except Exception as e:
        raise Exception(f"Error filtering homestays: {str(e)}")

async def get_homestay_stats() -> Dict[str, Any]:
    """
    Get basic statistics about homestays in the database.
    
    Returns:
        Dictionary containing homestay statistics
    """
    try:
        db = await db_instance.connect()
        collection = db_instance.homestays
        
        if not collection:
            raise Exception("Failed to connect to homestays collection")
        
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
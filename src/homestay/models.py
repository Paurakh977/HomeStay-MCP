from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

class BilingualData(BaseModel):
    en: str
    ne: str

class AddressData(BaseModel):
    province: BilingualData
    district: BilingualData
    municipality: BilingualData
    ward: BilingualData
    city: str
    tole: str
    formatted_address: BilingualData = Field(alias="formattedAddress")
    
    class Config:
        allow_population_by_field_name = True

class FeaturesData(BaseModel):
    local_attractions: List[str] = Field(default_factory=list, alias="localAttractions")
    tourism_services: List[str] = Field(default_factory=list, alias="tourismServices")
    infrastructure: List[str] = Field(default_factory=list, alias="infrastructure")
    
    class Config:
        allow_population_by_field_name = True

class AvailabilityData(BaseModel):
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    booked_dates: List[datetime] = Field(default_factory=list, alias="bookedDates")
    
    class Config:
        allow_population_by_field_name = True

class ContactPersonData(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class HomestayFilterRequest(BaseModel):
    """Flexible filtering request for homestays"""
    
    # Location filters
    province: Optional[str] = None
    district: Optional[str] = None
    municipality: Optional[str] = None
    ward: Optional[str] = None
    city: Optional[str] = None
    village_name: Optional[str] = Field(None, alias="villageName")
    
    # Basic info filters
    homestay_name: Optional[str] = Field(None, alias="homeStayName")
    homestay_type: Optional[str] = Field(None, alias="homeStayType")  # 'community' or 'private'
    status: Optional[str] = None  # 'pending', 'approved', 'rejected'
    admin_username: Optional[str] = Field(None, alias="adminUsername")
    
    # Capacity filters
    min_home_count: Optional[int] = Field(None, alias="minHomeCount")
    max_home_count: Optional[int] = Field(None, alias="maxHomeCount")
    min_room_count: Optional[int] = Field(None, alias="minRoomCount")
    max_room_count: Optional[int] = Field(None, alias="maxRoomCount")
    min_bed_count: Optional[int] = Field(None, alias="minBedCount")
    max_bed_count: Optional[int] = Field(None, alias="maxBedCount")
    min_max_guests: Optional[int] = Field(None, alias="minMaxGuests")
    max_max_guests: Optional[int] = Field(None, alias="maxMaxGuests")
    
    # Rating filters
    min_rating: Optional[float] = Field(None, alias="minRating")
    max_rating: Optional[float] = Field(None, alias="maxRating")
    min_average_rating: Optional[float] = Field(None, alias="minAverageRating")
    max_average_rating: Optional[float] = Field(None, alias="maxAverageRating")
    min_review_count: Optional[int] = Field(None, alias="minReviewCount")
    
    # Price filters
    min_price_per_night: Optional[float] = Field(None, alias="minPricePerNight")
    max_price_per_night: Optional[float] = Field(None, alias="maxPricePerNight")
    
    # Feature filters
    amenities: Optional[List[str]] = None  # Must have ALL these amenities
    any_amenities: Optional[List[str]] = Field(None, alias="anyAmenities")  # Must have ANY of these amenities
    local_attractions: Optional[List[str]] = Field(None, alias="localAttractions")
    tourism_services: Optional[List[str]] = Field(None, alias="tourismServices")
    infrastructure: Optional[List[str]] = Field(None, alias="infrastructure")
    
    # Boolean filters
    is_verified: Optional[bool] = Field(None, alias="isVerified")
    is_featured: Optional[bool] = Field(None, alias="isFeatured")
    is_admin: Optional[bool] = Field(None, alias="isAdmin")
    
    # Registration filters
    dhsr_no: Optional[str] = Field(None, alias="dhsrNo")
    registration_authority: Optional[str] = Field(None, alias="registrationAuthority")
    business_registration_number: Optional[str] = Field(None, alias="businessRegistrationNumber")
    
    # Date filters
    created_after: Optional[datetime] = Field(None, alias="createdAfter")
    created_before: Optional[datetime] = Field(None, alias="createdBefore")
    updated_after: Optional[datetime] = Field(None, alias="updatedAfter")
    updated_before: Optional[datetime] = Field(None, alias="updatedBefore")
    
    # Contact filters
    owner_name: Optional[str] = Field(None, alias="ownerName")
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Custom field filters
    custom_fields: Optional[Dict[str, Any]] = Field(None, alias="customFields")
    
    # Search query (text search across multiple fields)
    search_query: Optional[str] = Field(None, alias="searchQuery")
    
    # Language preference for bilingual fields
    language: Optional[str] = Field("en", alias="lang")  # 'en' or 'ne'
    
    # Pagination
    limit: Optional[int] = Field(100, ge=1, le=1000)
    skip: Optional[int] = Field(0, ge=0)
    
    class Config:
        allow_population_by_field_name = True

class HomestayFilterResponse(BaseModel):
    """Response containing filtered homestay usernames"""
    homestay_usernames: List[str] = Field(alias="homestayUsernames")
    total_count: int = Field(alias="totalCount")
    filtered_count: int = Field(alias="filteredCount")
    
    class Config:
        allow_population_by_field_name = True
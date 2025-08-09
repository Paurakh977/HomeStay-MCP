from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union, Literal
from datetime import datetime
from enum import Enum

class BilingualData(BaseModel):
    en: str
    ne: str

class LocalAttractionCategories:
    """Complete list of available local attractions matching the registration form"""
    NATURAL = [
        "National Parks & Conservation Areas/राष्ट्रिय निकुञ्ज तथा संरक्षित क्षेत्र",
        "Major Rivers & Lakes/प्रमुख नदी तथा तालहरू",
        "Ponds/पोखरी",
        "Viewpoint Tower/दृश्यावलोकन स्थल (भ्यू टावर)",
        "Watchtowers, wetlands, and grasslands/मचान तथा सिमसार क्षेत्र, घासे मैदान",
    ]
    
    CULTURAL = [
        "Museums & Cultural Centers/आदिवासी संग्रहालय तथा संस्कृति केन्द्रहरू",
        "Traditional Festivals, Dances & Rituals/परम्परागत पर्व, नाच तथा विधिहरू",
        "Local Community Lifestyle & Architecture/स्थानीय जीवनशैली तथा वास्तुकला",
    ]
    
    PRODUCTS = [
        "Organic Food/Organic खाना",
        "Traditional Dishes & Recipes/परम्परागत परिकारहरू",
    ]
    
    FOREST = [
        "Community-managed Forests/सामुदायिक वन क्षेत्रहरू",
        "Nature Walks & Eco Trails/प्रकृति पदमार्ग तथा पदयात्रा",
    ]
    
    WILDLIFE = [
        "Iconic & Endangered Wildlife/प्रमुख तथा लोपोन्मुख जनावरहरू",
        "Birdwatching Hotspots/चराचुरुङ्गी हेर्ने स्थानहरू",
        "Community-led Wildlife Conservation/सामुदायिक वन्यजन्तु संरक्षण प्रयासहरू",
        "Other endangered wildlife and birds/अन्य लोपोन्मुख वन्यजन्तु तथा चराचुरुङ्गी",
    ]
    
    ADVENTURE = [
        "Trekking, Climbing & Hiking Routes/ट्रेकिङ, आरोहण तथा हाइकिङ मार्गहरू",
        "Eco-tourism based exploration/Eco-tourism based exploration",
        "Adventure Sports like: Boating, Hiking, Jungle Walk, Elephant Safari, Jeep Safari/साहसिक खेलहरू (जस्तै: बोटिङ, हाइकिङ, जंगल वाक, हात्ती सफारी, जीप सफारी)",
        "Fishing in the fish pond/माछा पोखरीमा फिसिङ",
        "Jungle Walks & Wildlife Safaris/जंगल पदयात्रा तथा सफारी",
        "Sunset/Sunrise Viewing Points/सूर्यास्त/सूर्योदय हेर्ने स्थानहरू",
        "Cultural Village Tours, Cycling & Local Mobility/गाउँ सयर, साइकल यात्रा, स्थानीय सवारी अनुभव",
    ]

class EnhancedFeatureSearchHelper:
    """Enhanced helper class for comprehensive natural language query processing"""
    
    # Comprehensive keyword mappings with synonyms and variations
    ATTRACTION_KEYWORDS = {
    # Use exact database values for better matching
        'hiking': ['Trekking, Climbing & Hiking Routes/ट्रेकिङ, आरोहण तथा हाइकिङ मार्गहरू'],
        'trekking': ['Trekking, Climbing & Hiking Routes/ट्रेकिङ, आरोहण तथा हाइकिङ मार्गहरू'],
        'climbing': ['Trekking, Climbing & Hiking Routes/ट्रेकिङ, आरोहण तथा हाइकिङ मार्गहरू'],
        'fishing': ['Fishing in the fish pond/माछा पोखरीमा फिसिङ'],
        'museum': ['Museums & Cultural Centers/आदिवासी संग्रहालय तथा संस्कृति केन्द्रहरू'],
        'cultural centers': ['Museums & Cultural Centers/आदिवासी संग्रहालय तथा संस्कृति केन्द्रहरू'],
        'local dishes': ['Traditional Dishes & Recipes/परम्परागत परिकारहरू'],
        'traditional dishes': ['Traditional Dishes & Recipes/परम्परागत परिकारहरू'],
        'organic food': ['Organic Food/Organic खाना'],
        'organic': ['Organic Food/Organic खाना'],
        'national park': ['National Parks & Conservation Areas/राष्ट्रिय निकुञ्ज तथा संरक्षित क्षेत्र'],
        'conservation': ['National Parks & Conservation Areas/राष्ट्रिय निकुञ्ज तथा संरक्षित क्षेत्र'],
        'river': ['Major Rivers & Lakes/प्रमुख नदी तथा तालहरू'],
        'lake': ['Major Rivers & Lakes/प्रमुख नदी तथा तालहरू'],
        'viewpoint': ['Viewpoint Tower/दृश्यावलोकन स्थल (भ्यू टावर)'],
        'view tower': ['Viewpoint Tower/दृश्यावलोकन स्थल (भ्यू टावर)'],
        'bird watching': ['Birdwatching Hotspots/चराचुरुङ्गी हेर्ने स्थानहरू'],
        'birdwatching': ['Birdwatching Hotspots/चराचुरुङ्गी हेर्ने स्थानहरू'],
        'wildlife': ['Iconic & Endangered Wildlife/प्रमुख तथा लोपोन्मुख जनावरहरू'],
        'safari': ['Adventure Sports like: Boating, Hiking, Jungle Walk, Elephant Safari, Jeep Safari/साहसिक खेलहरू (जस्तै: बोटिङ, हाइकिङ, जंगल वाक, हात्ती सफारी, जीप सफारी)'],
        'jungle walk': ['Adventure Sports like: Boating, Hiking, Jungle Walk, Elephant Safari, Jeep Safari/साहसिक खेलहरू (जस्तै: बोटिङ, हाइकिङ, जंगल वाक, हात्ती सफारी, जीप सफारी)'],
        'adventure sports': ['Adventure Sports like: Boating, Hiking, Jungle Walk, Elephant Safari, Jeep Safari/साहसिक खेलहरू (जस्तै: बोटिङ, हाइकिङ, जंगल वाक, हात्ती सफारी, जीप सफारी)'],
    }

    INFRASTRUCTURE_KEYWORDS = {
        'water': ['Drinking Water/खानेपानी'],
        'drinking water': ['Drinking Water/खानेपानी'],
        'clean water': ['Drinking Water/खानेपानी'],
        'clean drinking water': ['Drinking Water/खानेपानी'],
        'toilet': ['Toilet/शौचालय'],
        'bathroom': ['Toilet/शौचालय'],
        'washroom': ['Toilet/शौचालय'],
        'solar': ['Solar Panel & lighting system/सोलार प्यानल तथा बत्ती व्यवस्था'],
        'solar panel': ['Solar Panel & lighting system/सोलार प्यानल तथा बत्ती व्यवस्था'],
        'lighting': ['Solar Panel & lighting system/सोलार प्यानल तथा बत्ती व्यवस्था'],
        'communication': ['Communication & Mobile networks/सञ्चार तथा मोबाइल सञ्जाल'],
        'mobile': ['Communication & Mobile networks/सञ्चार तथा मोबाइल सञ्जाल'],
        'wifi': ['Communication & Mobile networks/सञ्चार तथा मोबाइल सञ्जाल'],
        'internet': ['Communication & Mobile networks/सञ्चार तथा मोबाइल सञ्जाल'],
        'guest room': ['Guest Room/पाहुना कोठा'],
        'room': ['Guest Room/पाहुना कोठा'],
        'community building': ['Community Building/सामुदायिक भवन'],
        'security': ['Security/सुरक्षा'],
        'health': ['Health Post/स्वास्थ्य चौकी'],
        'health post': ['Health Post/स्वास्थ्य चौकी'],
        'transport': ['Transportation/यातायात'],
        'transportation': ['Transportation/यातायात'],
    }
    
    @classmethod
    def enhanced_natural_query_processing(cls, query: str) -> Dict[str, Any]:
        """FIXED natural language processing with better keyword matching and logical operator detection"""
        import re
        query_lower = query.lower()
        filters = {}

        # Detect logical operator
        if ' or ' in query_lower or ' any of ' in query_lower:
            filters['logical_operator'] = 'OR'
        else:
            filters['logical_operator'] = 'AND'
        
        # Process attractions with PARTIAL matching keywords
        matched_attractions = set()
        for keyword, attraction_terms in cls.ATTRACTION_KEYWORDS.items():
            if keyword in query_lower:
                matched_attractions.update(attraction_terms)
        
        if matched_attractions:
            # Use any_local_attractions for broader matching
            filters['any_local_attractions'] = list(matched_attractions)
        
        # Process infrastructure
        matched_infrastructure = set()
        for keyword, infra_terms in cls.INFRASTRUCTURE_KEYWORDS.items():
            if keyword in query_lower:
                matched_infrastructure.update(infra_terms)
        
        if matched_infrastructure:
            filters['any_infrastructure'] = list(matched_infrastructure)
        
        # REMOVE conflicting local_attractions filter generation
        # Don't set local_attractions unless user explicitly wants ALL conditions
        
        # Enhanced pattern matching for ratings
        rating_patterns = [
            r'rating (?:over|above|more than|greater than) (\d+(?:\.\d+)?)',
            r'rating (\d+(?:\.\d+)?)\+',
            r'(\d+(?:\.\d+)?) star',
            r'minimum rating (\d+(?:\.\d+)?)',
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, query_lower)
            if match:
                filters['min_average_rating'] = float(match.group(1))
                break
        
        # Enhanced team member processing
        team_patterns = [
            r'team member(?:s)? (?:over|more than|greater than) (\d+)',
            r'(\d+)\+ team member',
            r'minimum (\d+) team member',
            r'at least (\d+) team member',
        ]
        
        for pattern in team_patterns:
            match = re.search(pattern, query_lower)
            if match:
                filters['min_team_members'] = int(match.group(1))
                break
        
        # Feature access processing
        feature_access = {}
        if 'dashboard' in query_lower:
            feature_access['dashboard'] = True
        if 'profile' in query_lower:
            feature_access['profile'] = True
        if 'portal' in query_lower:
            feature_access['portal'] = True
        if 'documents' in query_lower:
            feature_access['documents'] = True
        if 'image upload' in query_lower or 'upload' in query_lower:
            feature_access['image_upload'] = True
        if 'settings' in query_lower:
            feature_access['settings'] = True
        if 'chat' in query_lower:
            feature_access['chat'] = True
        
        if feature_access:
            filters['feature_access'] = feature_access
        
        # Boolean flags
        if 'verified' in query_lower:
            filters['is_verified'] = True
        if 'featured' in query_lower:
            filters['is_featured'] = True
        if 'committee-driven' in query_lower or 'committee driven' in query_lower:
            filters['is_committee_driven'] = True
        
        # Gender processing
        if 'female operator' in query_lower or 'female' in query_lower:
            filters['operator_gender'] = 'female'
        elif 'male operator' in query_lower or 'male' in query_lower:
            filters['operator_gender'] = 'male'
        
        # Availability status
        if 'available' in query_lower and 'unavailable' not in query_lower:
            if 'partially available' in query_lower:
                filters['availability_status'] = 'partially_available'
            else:
                filters['availability_status'] = 'available'
        elif 'unavailable' in query_lower:
            filters['availability_status'] = 'unavailable'
        
        return filters

class HomestayFilterRequest(BaseModel):
    """Comprehensive homestay filtering request model"""
    
    # Natural language processing
    natural_language_query: Optional[str] = None
    
    # Location filters (bilingual support)
    province: Optional[str] = None
    district: Optional[str] = None
    municipality: Optional[str] = None
    ward: Optional[str] = None
    city: Optional[str] = None
    village_name: Optional[str] = None
    language: Optional[str] = "en"  # "en" or "ne" for bilingual fields
    
    # Basic homestay information
    homestay_name: Optional[str] = None
    homestay_type: Optional[Literal["community", "private"]] = None
    status: Optional[Literal["pending", "approved", "rejected"]] = None
    admin_username: Optional[str] = None
    
    # Capacity filters
    min_home_count: Optional[int] = None
    max_home_count: Optional[int] = None
    min_room_count: Optional[int] = None
    max_room_count: Optional[int] = None
    min_bed_count: Optional[int] = None
    max_bed_count: Optional[int] = None
    min_max_guests: Optional[int] = None
    max_max_guests: Optional[int] = None
    
    # Rating filters
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    min_average_rating: Optional[float] = None
    max_average_rating: Optional[float] = None
    min_review_count: Optional[int] = None
    
    # Price filters
    min_price_per_night: Optional[float] = None
    max_price_per_night: Optional[float] = None
    
    # Feature filters
    amenities: Optional[List[str]] = None  # All must match
    any_amenities: Optional[List[str]] = None  # Any can match
    local_attractions: Optional[List[str]] = None  # All must match
    any_local_attractions: Optional[List[str]] = None  # Any can match
    tourism_services: Optional[List[str]] = None  # All must match
    any_tourism_services: Optional[List[str]] = None  # Any can match
    infrastructure: Optional[List[str]] = None  # All must match
    any_infrastructure: Optional[List[str]] = None  # Any can match
    
    # Feature access filters
    feature_access: Optional[Dict[str, bool]] = None
    
    # Boolean filters
    is_verified: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    # Registration filters
    dhsr_no: Optional[str] = None
    registration_authority: Optional[str] = None
    business_registration_number: Optional[str] = None
    
    # Date filters
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    updated_after: Optional[datetime] = None
    updated_before: Optional[datetime] = None
    
    # Contact filters
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Team member filters
    min_team_members: Optional[int] = None
    max_team_members: Optional[int] = None
    
    # Operator and management filters
    operator_gender: Optional[Literal["male", "female", "other"]] = None
    is_committee_driven: Optional[bool] = None
    availability_status: Optional[Literal["available", "unavailable", "partially_available"]] = None
    
    # Custom field filters
    custom_fields: Optional[Dict[str, Any]] = None
    
    # Text search
    search_query: Optional[str] = None
    
    # Pagination and sorting
    skip: Optional[int] = 0
    limit: Optional[int] = 100
    sort_by: Optional[str] = None
    sort_order: Optional[Literal["asc", "desc"]] = "desc"
    logical_operator: Optional[Literal["AND", "OR"]] = "AND"

class HomestayFilterResponse(BaseModel):
    """Enhanced response with additional metadata"""
    homestay_usernames: List[str] = Field(alias="homestayUsernames")
    total_count: int = Field(alias="totalCount")
    filtered_count: int = Field(alias="filteredCount")
    applied_filters: Dict[str, Any] = Field(alias="appliedFilters")
    suggestions: Optional[List[str]] = None  # Suggestions for better filtering
    
    class Config:
        allow_population_by_field_name = True

# Add to EnhancedFeatureSearchHelper
@classmethod
def fuzzy_keyword_match(cls, query: str, keywords: Dict[str, List[str]]) -> List[str]:
    """Fuzzy matching for keywords (e.g., 'hike' matches 'hiking')"""
    import difflib
    
    query_words = query.lower().split()
    matched_features = set()
    
    for word in query_words:
        for keyword, features in keywords.items():
            # Exact match
            if word in keyword or keyword in word:
                matched_features.update(features)
            # Fuzzy match
            elif difflib.SequenceMatcher(None, word, keyword).ratio() > 0.8:
                matched_features.update(features)
    
    return list(matched_features)

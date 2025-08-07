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
        # Use partial matching keywords that will work with regex
        'trekking': ['Trekking', 'Climbing', 'Hiking'],
        'hiking': ['Trekking', 'Climbing', 'Hiking'],
        'climbing': ['Trekking', 'Climbing', 'Hiking'],
        'park': ['National Parks', 'Conservation Areas'],
        'national park': ['National Parks', 'Conservation Areas'],
        'river': ['Rivers', 'Lakes'],
        'lake': ['Rivers', 'Lakes'],
        'viewpoint': ['Viewpoint Tower', 'दृश्यावलोकन'],
        'museum': ['Museums', 'Cultural Centers', 'संग्रहालय'],
        'cultural': ['Cultural', 'सांस्कृतिक'],
        'organic': ['Organic Food', 'Organic'],
        'food': ['Food', 'खाना', 'परिकारहरू'],
        'forest': ['Forest', 'वन'],
        'wildlife': ['Wildlife', 'वन्यजन्तु'],
        'bird': ['Bird', 'चराचुरुङ्गी'],
        'safari': ['Safari', 'सफारी'],
        'fishing': ['Fishing', 'फिसिङ']
    }
    
    SERVICE_KEYWORDS = {
        'welcome': ['Welcome and Farewell/स्वागत तथा विदाई'],
        'farewell': ['Welcome and Farewell/स्वागत तथा विदाई'],
        'accommodation': ['Comfortable Accommodation/आरामदायी आवास'],
        'comfortable': ['Comfortable Accommodation/आरामदायी आवास'],
        'gift': ['Gift or Souvenir/मायाको चिनो (उपहार)'],
        'souvenir': ['Gift or Souvenir/मायाको चिनो (उपहार)'],
        'token of love': ['Gift or Souvenir/मायाको चिनो (उपहार)'],
        'cultural program': ['Traditional Cultural Program/परम्परागत सांस्कृतिक कार्यक्रम'],
        'program': ['Traditional Cultural Program/परम्परागत सांस्कृतिक कार्यक्रम'],
        'local food': ['Local Dishes/स्थानीय परिकारहरू'],
        'local dish': ['Local Dishes/स्थानीय परिकारहरू'],
        'dish': ['Local Dishes/स्थानीय परिकारहरू'],
    }
    
    INFRASTRUCTURE_KEYWORDS = {
        'building': ['Community Building/सामुदायिक भवन'],
        'community building': ['Community Building/सामुदायिक भवन'],
        'room': ['Guest Room, Toilet, Bathroom/पाहुना कोठा, शौचालय, स्नानघर'],
        'guest room': ['Guest Room, Toilet, Bathroom/पाहुना कोठा, शौचालय, स्नानघर'],
        'toilet': ['Guest Room, Toilet, Bathroom/पाहुना कोठा, शौचालय, स्नानघर'],
        'bathroom': ['Guest Room, Toilet, Bathroom/पाहुना कोठा, शौचालय, स्नानघर'],
        'transportation': ['Transportation Facility/यातायात सुविधा'],
        'transport': ['Transportation Facility/यातायात सुविधा'],
        'water': ['Drinking Water and Solar Lighting/खानेपानी तथा सोलार बत्ती'],
        'drinking water': ['Drinking Water and Solar Lighting/खानेपानी तथा सोलार बत्ती'],
        'solar': ['Drinking Water and Solar Lighting/खानेपानी तथा सोलार बत्ती'],
        'lighting': ['Drinking Water and Solar Lighting/खानेपानी तथा सोलार बत्ती'],
        'security': ['Security Post (Nepaltar)/सुरक्षा चौकी (नेपालटार)'],
        'security post': ['Security Post (Nepaltar)/सुरक्षा चौकी (नेपालटार)'],
        'health': ['Health Post (Udayapurgadhi)/स्वास्थ्य चौकी (उदयपुरगढी)'],
        'health post': ['Health Post (Udayapurgadhi)/स्वास्थ्य चौकी (उदयपुरगढी)'],
        'communication': ['Communication Facility (Mobile)/सञ्चार सुविधा (मोबाइल)'],
        'mobile': ['Communication Facility (Mobile)/सञ्चार सुविधा (मोबाइल)'],
        'wifi': ['Communication Facility (Mobile)/सञ्चार सुविधा (मोबाइल)'],
        'internet': ['Communication Facility (Mobile)/सञ्चार सुविधा (मोबाइल)'],
        'good toilet': ['Guest Room, Toilet, Bathroom/पाहुना कोठा, शौचालय, स्नानघर'],
        'clean toilet': ['Guest Room, Toilet, Bathroom/पाहुना कोठा, शौचालय, स्नानघर'],
        'committee-driven': ['Community Building/सामुदायिक भवन'],
        'committee driven': ['Community Building/सामुदायिक भवन'],
    }
    
    @classmethod
    def enhanced_natural_query_processing(cls, query: str) -> Dict[str, Any]:
        """Enhanced natural language query processing with comprehensive keyword matching"""
        import re
        
        query_lower = query.lower()
        filters = {}
        
        # Process attractions with fuzzy matching
        matched_attractions = set()
        for keyword, attractions in cls.ATTRACTION_KEYWORDS.items():
            if keyword in query_lower:
                matched_attractions.update(attractions)
        
        if matched_attractions:
            filters['any_local_attractions'] = list(matched_attractions)
        
        # Process services
        matched_services = set()
        for keyword, services in cls.SERVICE_KEYWORDS.items():
            if keyword in query_lower:
                matched_services.update(services)
        
        if matched_services:
            filters['any_tourism_services'] = list(matched_services)
        
        # Process infrastructure
        matched_infrastructure = set()
        for keyword, infrastructure in cls.INFRASTRUCTURE_KEYWORDS.items():
            if keyword in query_lower:
                matched_infrastructure.update(infrastructure)
        
        if matched_infrastructure:
            filters['any_infrastructure'] = list(matched_infrastructure)
        
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

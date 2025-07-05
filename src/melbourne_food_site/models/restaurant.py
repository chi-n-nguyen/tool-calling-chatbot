"""Restaurant data models."""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class CuisineType(str, Enum):
    """Cuisine types available in Melbourne."""
    ITALIAN = "Italian"
    CHINESE = "Chinese"
    JAPANESE = "Japanese"
    THAI = "Thai"
    VIETNAMESE = "Vietnamese"
    INDIAN = "Indian"
    GREEK = "Greek"
    MEXICAN = "Mexican"
    AUSTRALIAN = "Australian"
    FRENCH = "French"
    MIDDLE_EASTERN = "Middle Eastern"
    KOREAN = "Korean"
    PIZZA = "Pizza"
    BURGERS = "Burgers"
    CAFE = "Cafe"
    BAKERY = "Bakery"
    SEAFOOD = "Seafood"
    VEGETARIAN = "Vegetarian"
    VEGAN = "Vegan"


class PriceRange(str, Enum):
    """Price range categories."""
    CHEAP = "$"          # Under $15
    MODERATE = "$$"      # $15-30
    EXPENSIVE = "$$$"    # $30-50
    VERY_EXPENSIVE = "$$$$"  # $50+


class Restaurant(BaseModel):
    """Restaurant model."""
    id: int
    name: str
    cuisine_type: CuisineType
    price_range: PriceRange
    rating: float = Field(ge=0, le=5)
    address: str
    suburb: str
    postcode: str
    phone: Optional[str] = None
    website: Optional[str] = None
    description: str
    opening_hours: dict[str, str]  # day -> hours
    is_active: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    
    # Special features
    has_delivery: bool = False
    has_takeaway: bool = False
    has_outdoor_seating: bool = False
    is_wheelchair_accessible: bool = False
    accepts_reservations: bool = False
    
    # Cheap eats specific
    has_lunch_specials: bool = False
    has_happy_hour: bool = False
    student_discount: bool = False


class PromoOffer(BaseModel):
    """Promotional offer model."""
    id: int
    restaurant_id: int
    title: str
    description: str
    discount_percentage: Optional[int] = None
    fixed_discount: Optional[float] = None
    minimum_spend: Optional[float] = None
    valid_from: str  # ISO date
    valid_until: str  # ISO date
    is_active: bool = True
    terms_conditions: str
    promo_code: Optional[str] = None


class Review(BaseModel):
    """Review model."""
    id: int
    restaurant_id: int
    rating: int = Field(ge=1, le=5)
    comment: str
    reviewer_name: str
    date_posted: str  # ISO date
    is_verified: bool = False


class RestaurantResponse(BaseModel):
    """Restaurant response with additional computed fields."""
    restaurant: Restaurant
    current_promos: List[PromoOffer] = []
    average_rating: float
    review_count: int
    distance_km: Optional[float] = None
    is_currently_open: bool
    
    
class RestaurantFilter(BaseModel):
    """Filter parameters for restaurant search."""
    cuisine_types: Optional[List[CuisineType]] = None
    price_ranges: Optional[List[PriceRange]] = None
    suburbs: Optional[List[str]] = None
    min_rating: Optional[float] = None
    max_distance_km: Optional[float] = None
    has_delivery: Optional[bool] = None
    has_takeaway: Optional[bool] = None
    has_outdoor_seating: Optional[bool] = None
    is_wheelchair_accessible: Optional[bool] = None
    accepts_reservations: Optional[bool] = None
    has_current_promos: Optional[bool] = None
    is_currently_open: Optional[bool] = None 
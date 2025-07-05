"""Restaurant API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.restaurant import (
    Restaurant, RestaurantResponse, RestaurantFilter, 
    CuisineType, PriceRange
)
from ..services.restaurant_service import RestaurantService
from ..services.recommendation_service import RecommendationService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Initialize services
restaurant_service = RestaurantService()
recommendation_service = RecommendationService(restaurant_service)


class LocationRequest(BaseModel):
    """User location for distance calculations."""
    latitude: float
    longitude: float


@router.get("/", response_model=List[RestaurantResponse])
async def get_restaurants(
    cuisine_types: Optional[List[CuisineType]] = Query(None),
    price_ranges: Optional[List[PriceRange]] = Query(None),
    suburbs: Optional[List[str]] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    max_distance_km: Optional[float] = Query(None, ge=0),
    has_delivery: Optional[bool] = Query(None),
    has_takeaway: Optional[bool] = Query(None),
    has_outdoor_seating: Optional[bool] = Query(None),
    is_wheelchair_accessible: Optional[bool] = Query(None),
    accepts_reservations: Optional[bool] = Query(None),
    has_current_promos: Optional[bool] = Query(None),
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None)
):
    """Get restaurants with optional filtering."""
    
    filters = RestaurantFilter(
        cuisine_types=cuisine_types,
        price_ranges=price_ranges,
        suburbs=suburbs,
        min_rating=min_rating,
        max_distance_km=max_distance_km,
        has_delivery=has_delivery,
        has_takeaway=has_takeaway,
        has_outdoor_seating=has_outdoor_seating,
        is_wheelchair_accessible=is_wheelchair_accessible,
        accepts_reservations=accepts_reservations,
        has_current_promos=has_current_promos
    )
    
    return restaurant_service.get_restaurants_with_details(
        filters=filters,
        user_lat=user_lat,
        user_lng=user_lng
    )


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(restaurant_id: int):
    """Get a specific restaurant by ID."""
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Get detailed response
    responses = restaurant_service.get_restaurants_with_details()
    for response in responses:
        if response.restaurant.id == restaurant_id:
            return response
    
    raise HTTPException(status_code=404, detail="Restaurant not found")


@router.get("/search/query")
async def search_restaurants(
    q: str = Query(..., description="Search query"),
    cuisine_type: Optional[str] = Query(None),
    max_distance: Optional[float] = Query(None, ge=0),
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None)
):
    """Search restaurants by name, cuisine, or description."""
    
    results = restaurant_service.search_restaurants(
        query=q,
        cuisine_type=cuisine_type,
        max_distance=max_distance,
        user_lat=user_lat,
        user_lng=user_lng
    )
    
    return results


@router.get("/cheap-eats/", response_model=List[RestaurantResponse])
async def get_cheap_eats(
    max_price: str = Query("$", description="Maximum price range: $ or $$")
):
    """Get budget-friendly restaurant recommendations."""
    return restaurant_service.get_cheap_eats(max_price=max_price)


@router.get("/promos/", response_model=List[RestaurantResponse])
async def get_restaurants_with_promos():
    """Get restaurants that currently have active promotions."""
    return restaurant_service.get_restaurants_with_promos()


@router.get("/cuisine/{cuisine_type}", response_model=List[RestaurantResponse])
async def get_restaurants_by_cuisine(
    cuisine_type: CuisineType,
    limit: int = Query(5, ge=1, le=20)
):
    """Get top restaurants for a specific cuisine type."""
    return restaurant_service.get_recommendations_by_cuisine(cuisine_type, limit) 
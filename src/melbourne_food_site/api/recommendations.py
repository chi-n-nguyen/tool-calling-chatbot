"""Recommendation API endpoints."""

from typing import List, Optional, Tuple
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.restaurant import RestaurantResponse, CuisineType, PriceRange
from ..services.restaurant_service import RestaurantService
from ..services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# Initialize services
restaurant_service = RestaurantService()
recommendation_service = RecommendationService(restaurant_service)


class PersonalizedRecommendationRequest(BaseModel):
    """Request for personalized recommendations."""
    preferred_cuisines: List[CuisineType]
    preferred_price_range: List[PriceRange]
    user_location: Optional[Tuple[float, float]] = None
    max_distance_km: float = 10.0
    num_recommendations: int = 10


@router.get("/similar/{restaurant_id}", response_model=List[RestaurantResponse])
async def get_similar_restaurants(
    restaurant_id: int,
    num_recommendations: int = Query(5, ge=1, le=20)
):
    """Get restaurants similar to the specified restaurant."""
    
    # Check if restaurant exists
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return recommendation_service.get_similar_restaurants(
        restaurant_id=restaurant_id,
        num_recommendations=num_recommendations
    )


@router.post("/personalized", response_model=List[RestaurantResponse])
async def get_personalized_recommendations(request: PersonalizedRecommendationRequest):
    """Get personalized restaurant recommendations based on user preferences."""
    
    return recommendation_service.get_personalized_recommendations(
        preferred_cuisines=request.preferred_cuisines,
        preferred_price_range=request.preferred_price_range,
        user_location=request.user_location,
        max_distance_km=request.max_distance_km,
        num_recommendations=request.num_recommendations
    )


@router.get("/budget-friendly", response_model=List[RestaurantResponse])
async def get_budget_friendly_recommendations(
    max_price: PriceRange = Query(PriceRange.MODERATE),
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None),
    num_recommendations: int = Query(8, ge=1, le=20)
):
    """Get budget-friendly restaurant recommendations."""
    
    user_location = (user_lat, user_lng) if user_lat and user_lng else None
    
    return recommendation_service.get_budget_friendly_recommendations(
        max_price=max_price,
        user_location=user_location,
        num_recommendations=num_recommendations
    )


@router.get("/trending", response_model=List[RestaurantResponse])
async def get_trending_restaurants(
    num_recommendations: int = Query(6, ge=1, le=20)
):
    """Get trending restaurants based on ratings and current promotions."""
    
    return recommendation_service.get_trending_restaurants(
        num_recommendations=num_recommendations
    )


@router.get("/cuisine/{cuisine_type}", response_model=List[RestaurantResponse])
async def get_cuisine_recommendations(
    cuisine_type: CuisineType,
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None),
    num_recommendations: int = Query(5, ge=1, le=20)
):
    """Get top recommendations for a specific cuisine type."""
    
    user_location = (user_lat, user_lng) if user_lat and user_lng else None
    
    return recommendation_service.get_cuisine_recommendations(
        cuisine_type=cuisine_type,
        user_location=user_location,
        num_recommendations=num_recommendations
    )


@router.get("/quick-lunch", response_model=List[RestaurantResponse])
async def get_quick_lunch_recommendations(
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None),
    max_distance_km: float = Query(2.0, ge=0.1, le=10.0)
):
    """Get recommendations for quick lunch options nearby."""
    
    user_location = (user_lat, user_lng) if user_lat and user_lng else None
    
    return recommendation_service.get_quick_lunch_recommendations(
        user_location=user_location,
        max_distance_km=max_distance_km
    )


@router.get("/for-students", response_model=List[RestaurantResponse])
async def get_student_friendly_recommendations(
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None)
):
    """Get student-friendly restaurants with discounts and cheap eats."""
    
    user_location = (user_lat, user_lng) if user_lat and user_lng else None
    
    # Get budget-friendly options that are student-oriented
    budget_restaurants = recommendation_service.get_budget_friendly_recommendations(
        max_price=PriceRange.MODERATE,
        user_location=user_location,
        num_recommendations=10
    )
    
    # Filter for student-friendly features
    student_friendly = []
    for restaurant_response in budget_restaurants:
        restaurant = restaurant_response.restaurant
        
        # Prioritize restaurants with student discounts or cheap prices
        if (restaurant.student_discount or 
            restaurant.price_range == PriceRange.CHEAP or
            restaurant.has_lunch_specials):
            student_friendly.append(restaurant_response)
    
    # If we don't have enough, add more budget options
    if len(student_friendly) < 8:
        remaining_spots = 8 - len(student_friendly)
        existing_ids = {r.restaurant.id for r in student_friendly}
        
        for restaurant_response in budget_restaurants:
            if restaurant_response.restaurant.id not in existing_ids:
                student_friendly.append(restaurant_response)
                remaining_spots -= 1
                if remaining_spots <= 0:
                    break
    
    return student_friendly[:8] 
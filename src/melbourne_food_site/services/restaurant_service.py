"""Restaurant service for data management and filtering."""

import json
import os
from typing import List, Optional
from datetime import datetime, time
from geopy.distance import geodesic

from ..models.restaurant import (
    Restaurant, RestaurantResponse, RestaurantFilter, 
    PromoOffer, CuisineType, PriceRange
)


class RestaurantService:
    """Service for managing restaurant data and operations."""
    
    def __init__(self):
        self.restaurants: List[Restaurant] = []
        self.promos: List[PromoOffer] = []
        self._load_data()
    
    def _load_data(self):
        """Load restaurant and promo data from JSON files."""
        # Load restaurants
        restaurant_file = os.path.join(os.path.dirname(__file__), "../../../data/melbourne_restaurants.json")
        try:
            with open(restaurant_file, 'r') as f:
                restaurant_data = json.load(f)
                self.restaurants = [Restaurant(**item) for item in restaurant_data]
        except FileNotFoundError:
            print(f"Restaurant data file not found: {restaurant_file}")
            self.restaurants = []
        
        # Load sample promos
        self._load_sample_promos()
    
    def _load_sample_promos(self):
        """Load sample promotional offers."""
        sample_promos = [
            {
                "id": 1,
                "restaurant_id": 2,  # Dumplings Plus
                "title": "Student Special",
                "description": "20% off total bill with valid student ID",
                "discount_percentage": 20,
                "valid_from": "2024-01-01",
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Valid with student ID. Cannot be combined with other offers.",
                "promo_code": "STUDENT20"
            },
            {
                "id": 2,
                "restaurant_id": 1,  # Chin Chin
                "title": "Lunch Special",
                "description": "Set lunch menu for $25",
                "fixed_discount": 10.0,
                "minimum_spend": 25.0,
                "valid_from": "2024-01-01",
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Available Monday to Friday 11:30 AM - 3:00 PM",
                "promo_code": "LUNCH25"
            },
            {
                "id": 3,
                "restaurant_id": 5,  # Gazi
                "title": "Happy Hour",
                "description": "50% off drinks Tuesday to Thursday 5-7 PM",
                "discount_percentage": 50,
                "valid_from": "2024-01-01",
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Valid Tuesday to Thursday 5:00 PM - 7:00 PM. Drinks only.",
                "promo_code": None
            }
        ]
        self.promos = [PromoOffer(**promo) for promo in sample_promos]
    
    def get_all_restaurants(self) -> List[Restaurant]:
        """Get all active restaurants."""
        return [r for r in self.restaurants if r.is_active]
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by ID."""
        for restaurant in self.restaurants:
            if restaurant.id == restaurant_id and restaurant.is_active:
                return restaurant
        return None
    
    def get_restaurants_with_details(self, 
                                   filters: Optional[RestaurantFilter] = None,
                                   user_lat: Optional[float] = None,
                                   user_lng: Optional[float] = None) -> List[RestaurantResponse]:
        """Get restaurants with full details including promos and distance."""
        restaurants = self.get_all_restaurants()
        
        # Apply filters
        if filters:
            restaurants = self._apply_filters(restaurants, filters)
        
        # Build detailed responses
        responses = []
        for restaurant in restaurants:
            # Get current promos
            current_promos = [p for p in self.promos 
                            if p.restaurant_id == restaurant.id and p.is_active]
            
            # Calculate distance if user location provided
            distance_km = None
            if (user_lat is not None and user_lng is not None and 
                restaurant.latitude is not None and restaurant.longitude is not None):
                distance_km = geodesic(
                    (user_lat, user_lng),
                    (restaurant.latitude, restaurant.longitude)
                ).kilometers
            
            # Mock review data (in real app, this would come from database)
            average_rating = restaurant.rating
            review_count = 150 + (restaurant.id * 23)  # Mock review count
            
            # Check if currently open (simplified logic)
            is_currently_open = self._is_currently_open(restaurant)
            
            response = RestaurantResponse(
                restaurant=restaurant,
                current_promos=current_promos,
                average_rating=average_rating,
                review_count=review_count,
                distance_km=distance_km,
                is_currently_open=is_currently_open
            )
            responses.append(response)
        
        return responses
    
    def _apply_filters(self, restaurants: List[Restaurant], filters: RestaurantFilter) -> List[Restaurant]:
        """Apply filters to restaurant list."""
        filtered = restaurants
        
        if filters.cuisine_types:
            filtered = [r for r in filtered if r.cuisine_type in filters.cuisine_types]
        
        if filters.price_ranges:
            filtered = [r for r in filtered if r.price_range in filters.price_ranges]
        
        if filters.suburbs:
            filtered = [r for r in filtered if r.suburb in filters.suburbs]
        
        if filters.min_rating:
            filtered = [r for r in filtered if r.rating >= filters.min_rating]
        
        if filters.has_delivery is not None:
            filtered = [r for r in filtered if r.has_delivery == filters.has_delivery]
        
        if filters.has_takeaway is not None:
            filtered = [r for r in filtered if r.has_takeaway == filters.has_takeaway]
        
        if filters.has_outdoor_seating is not None:
            filtered = [r for r in filtered if r.has_outdoor_seating == filters.has_outdoor_seating]
        
        if filters.is_wheelchair_accessible is not None:
            filtered = [r for r in filtered if r.is_wheelchair_accessible == filters.is_wheelchair_accessible]
        
        if filters.accepts_reservations is not None:
            filtered = [r for r in filtered if r.accepts_reservations == filters.accepts_reservations]
        
        if filters.has_current_promos:
            restaurant_ids_with_promos = {p.restaurant_id for p in self.promos if p.is_active}
            filtered = [r for r in filtered if r.id in restaurant_ids_with_promos]
        
        return filtered
    
    def _is_currently_open(self, restaurant: Restaurant) -> bool:
        """Check if restaurant is currently open (simplified logic)."""
        now = datetime.now()
        day_name = now.strftime("%A").lower()
        
        if day_name not in restaurant.opening_hours:
            return False
        
        hours = restaurant.opening_hours[day_name]
        if hours == "Closed":
            return False
        
        # Simplified parsing - in real app you'd want more robust time parsing
        try:
            if " - " in hours:
                open_time, close_time = hours.split(" - ")
                # For now, just return True if it has opening hours
                return True
        except:
            return False
        
        return True
    
    def get_cheap_eats(self, max_price: str = "$") -> List[RestaurantResponse]:
        """Get restaurants in the cheap eats category."""
        filters = RestaurantFilter(
            price_ranges=[PriceRange.CHEAP] if max_price == "$" else [PriceRange.CHEAP, PriceRange.MODERATE]
        )
        return self.get_restaurants_with_details(filters)
    
    def get_restaurants_with_promos(self) -> List[RestaurantResponse]:
        """Get restaurants that currently have active promotions."""
        filters = RestaurantFilter(has_current_promos=True)
        return self.get_restaurants_with_details(filters)
    
    def search_restaurants(self, 
                         query: str,
                         cuisine_type: Optional[str] = None,
                         max_distance: Optional[float] = None,
                         user_lat: Optional[float] = None,
                         user_lng: Optional[float] = None) -> List[RestaurantResponse]:
        """Search restaurants by name, cuisine, or description."""
        all_restaurants = self.get_restaurants_with_details(user_lat=user_lat, user_lng=user_lng)
        
        # Filter by search query
        results = []
        query_lower = query.lower()
        
        for restaurant_response in all_restaurants:
            restaurant = restaurant_response.restaurant
            
            # Search in name, description, and cuisine
            if (query_lower in restaurant.name.lower() or 
                query_lower in restaurant.description.lower() or
                query_lower in restaurant.cuisine_type.value.lower() or
                query_lower in restaurant.suburb.lower()):
                
                # Apply additional filters
                if cuisine_type and restaurant.cuisine_type.value != cuisine_type:
                    continue
                
                if (max_distance and restaurant_response.distance_km and 
                    restaurant_response.distance_km > max_distance):
                    continue
                
                results.append(restaurant_response)
        
        return results
    
    def get_recommendations_by_cuisine(self, cuisine_type: CuisineType, limit: int = 5) -> List[RestaurantResponse]:
        """Get top-rated restaurants for a specific cuisine type."""
        filters = RestaurantFilter(cuisine_types=[cuisine_type])
        restaurants = self.get_restaurants_with_details(filters)
        
        # Sort by rating and return top results
        sorted_restaurants = sorted(restaurants, 
                                  key=lambda x: x.restaurant.rating, 
                                  reverse=True)
        return sorted_restaurants[:limit] 
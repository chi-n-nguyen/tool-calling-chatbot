"""Recommendation service using ML for personalized restaurant suggestions."""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from ..models.restaurant import Restaurant, RestaurantResponse, CuisineType, PriceRange
from .restaurant_service import RestaurantService


class RecommendationService:
    """Service for generating personalized restaurant recommendations."""
    
    def __init__(self, restaurant_service: RestaurantService):
        self.restaurant_service = restaurant_service
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.scaler = StandardScaler()
        self._setup_recommendation_engine()
    
    def _setup_recommendation_engine(self):
        """Set up the recommendation engine with restaurant features."""
        restaurants = self.restaurant_service.get_all_restaurants()
        if not restaurants:
            return
        
        # Create feature matrix
        self.restaurant_df = self._create_restaurant_dataframe(restaurants)
        self.similarity_matrix = self._calculate_similarity_matrix()
    
    def _create_restaurant_dataframe(self, restaurants: List[Restaurant]) -> pd.DataFrame:
        """Create a DataFrame with restaurant features for ML."""
        data = []
        
        for restaurant in restaurants:
            # Create text features for content-based filtering
            text_features = f"{restaurant.cuisine_type.value} {restaurant.description} {restaurant.suburb}"
            
            # Numerical features
            price_numeric = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}.get(restaurant.price_range.value, 2)
            
            data.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'cuisine_type': restaurant.cuisine_type.value,
                'price_range': restaurant.price_range.value,
                'price_numeric': price_numeric,
                'rating': restaurant.rating,
                'text_features': text_features,
                'has_delivery': int(restaurant.has_delivery),
                'has_takeaway': int(restaurant.has_takeaway),
                'has_outdoor_seating': int(restaurant.has_outdoor_seating),
                'is_wheelchair_accessible': int(restaurant.is_wheelchair_accessible),
                'accepts_reservations': int(restaurant.accepts_reservations),
                'has_lunch_specials': int(restaurant.has_lunch_specials),
                'has_happy_hour': int(restaurant.has_happy_hour),
                'student_discount': int(restaurant.student_discount),
                'latitude': restaurant.latitude or -37.8136,  # Default to Melbourne CBD
                'longitude': restaurant.longitude or 144.9631
            })
        
        return pd.DataFrame(data)
    
    def _calculate_similarity_matrix(self) -> np.ndarray:
        """Calculate similarity matrix based on restaurant features."""
        if self.restaurant_df.empty:
            return np.array([])
        
        # Text similarity (content-based)
        text_matrix = self.vectorizer.fit_transform(self.restaurant_df['text_features'])
        text_similarity = cosine_similarity(text_matrix)
        
        # Numerical features similarity
        numerical_features = [
            'price_numeric', 'rating', 'has_delivery', 'has_takeaway',
            'has_outdoor_seating', 'is_wheelchair_accessible', 'accepts_reservations',
            'has_lunch_specials', 'has_happy_hour', 'student_discount'
        ]
        
        numerical_matrix = self.scaler.fit_transform(self.restaurant_df[numerical_features])
        numerical_similarity = cosine_similarity(numerical_matrix)
        
        # Combine similarities (weighted)
        combined_similarity = (0.6 * text_similarity + 0.4 * numerical_similarity)
        
        return combined_similarity
    
    def get_similar_restaurants(self, restaurant_id: int, num_recommendations: int = 5) -> List[RestaurantResponse]:
        """Get restaurants similar to the given restaurant."""
        if self.restaurant_df.empty or self.similarity_matrix.size == 0:
            return []
        
        try:
            # Find restaurant index
            restaurant_idx = self.restaurant_df[self.restaurant_df['id'] == restaurant_id].index[0]
            
            # Get similarity scores
            similarity_scores = list(enumerate(self.similarity_matrix[restaurant_idx]))
            
            # Sort by similarity (excluding the restaurant itself)
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            similar_restaurants = similarity_scores[1:num_recommendations+1]  # Exclude self
            
            # Get restaurant IDs
            similar_ids = [self.restaurant_df.iloc[idx]['id'] for idx, _ in similar_restaurants]
            
            # Return detailed responses
            responses = []
            for restaurant_id in similar_ids:
                restaurant = self.restaurant_service.get_restaurant_by_id(restaurant_id)
                if restaurant:
                    restaurant_responses = self.restaurant_service.get_restaurants_with_details()
                    for response in restaurant_responses:
                        if response.restaurant.id == restaurant_id:
                            responses.append(response)
                            break
            
            return responses
            
        except (IndexError, KeyError):
            return []
    
    def get_personalized_recommendations(self,
                                       preferred_cuisines: List[CuisineType],
                                       preferred_price_range: List[PriceRange],
                                       user_location: Optional[Tuple[float, float]] = None,
                                       max_distance_km: float = 10.0,
                                       num_recommendations: int = 10) -> List[RestaurantResponse]:
        """Get personalized recommendations based on user preferences."""
        
        # Get all restaurants with details
        all_restaurants = self.restaurant_service.get_restaurants_with_details(
            user_lat=user_location[0] if user_location else None,
            user_lng=user_location[1] if user_location else None
        )
        
        # Score restaurants based on preferences
        scored_restaurants = []
        
        for restaurant_response in all_restaurants:
            restaurant = restaurant_response.restaurant
            score = 0.0
            
            # Cuisine preference score (40% weight)
            if restaurant.cuisine_type in preferred_cuisines:
                score += 0.4
            
            # Price preference score (20% weight)
            if restaurant.price_range in preferred_price_range:
                score += 0.2
            
            # Rating score (20% weight)
            score += (restaurant.rating / 5.0) * 0.2
            
            # Distance score (10% weight) - closer is better
            if restaurant_response.distance_km is not None:
                if restaurant_response.distance_km <= max_distance_km:
                    distance_score = max(0, 1 - (restaurant_response.distance_km / max_distance_km))
                    score += distance_score * 0.1
            else:
                score += 0.05  # Neutral score if no distance data
            
            # Promo bonus (10% weight)
            if restaurant_response.current_promos:
                score += 0.1
            
            scored_restaurants.append((restaurant_response, score))
        
        # Sort by score and return top recommendations
        scored_restaurants.sort(key=lambda x: x[1], reverse=True)
        return [restaurant for restaurant, _ in scored_restaurants[:num_recommendations]]
    
    def get_budget_friendly_recommendations(self, 
                                          max_price: PriceRange = PriceRange.MODERATE,
                                          user_location: Optional[Tuple[float, float]] = None,
                                          num_recommendations: int = 8) -> List[RestaurantResponse]:
        """Get budget-friendly restaurant recommendations."""
        
        budget_ranges = [PriceRange.CHEAP]
        if max_price in [PriceRange.MODERATE, PriceRange.EXPENSIVE, PriceRange.VERY_EXPENSIVE]:
            budget_ranges.append(PriceRange.MODERATE)
        
        return self.get_personalized_recommendations(
            preferred_cuisines=list(CuisineType),  # All cuisines
            preferred_price_range=budget_ranges,
            user_location=user_location,
            num_recommendations=num_recommendations
        )
    
    def get_trending_restaurants(self, num_recommendations: int = 6) -> List[RestaurantResponse]:
        """Get trending restaurants based on ratings and promos."""
        all_restaurants = self.restaurant_service.get_restaurants_with_details()
        
        # Score based on rating and current promotions
        scored_restaurants = []
        for restaurant_response in all_restaurants:
            restaurant = restaurant_response.restaurant
            
            # Base score from rating
            score = restaurant.rating
            
            # Bonus for having promotions
            if restaurant_response.current_promos:
                score += 0.5
            
            # Bonus for student discounts and lunch specials
            if restaurant.student_discount:
                score += 0.3
            if restaurant.has_lunch_specials:
                score += 0.2
            
            scored_restaurants.append((restaurant_response, score))
        
        # Sort and return top trending
        scored_restaurants.sort(key=lambda x: x[1], reverse=True)
        return [restaurant for restaurant, _ in scored_restaurants[:num_recommendations]]
    
    def get_cuisine_recommendations(self, 
                                  cuisine_type: CuisineType,
                                  user_location: Optional[Tuple[float, float]] = None,
                                  num_recommendations: int = 5) -> List[RestaurantResponse]:
        """Get top recommendations for a specific cuisine type."""
        return self.get_personalized_recommendations(
            preferred_cuisines=[cuisine_type],
            preferred_price_range=list(PriceRange),  # All price ranges
            user_location=user_location,
            num_recommendations=num_recommendations
        )
    
    def get_quick_lunch_recommendations(self,
                                      user_location: Optional[Tuple[float, float]] = None,
                                      max_distance_km: float = 2.0) -> List[RestaurantResponse]:
        """Get recommendations for quick lunch options nearby."""
        all_restaurants = self.restaurant_service.get_restaurants_with_details(
            user_lat=user_location[0] if user_location else None,
            user_lng=user_location[1] if user_location else None
        )
        
        # Filter for lunch-friendly options
        lunch_restaurants = []
        for restaurant_response in all_restaurants:
            restaurant = restaurant_response.restaurant
            
            # Check if suitable for lunch
            is_lunch_friendly = (
                restaurant.has_takeaway or 
                restaurant.has_lunch_specials or
                restaurant.price_range in [PriceRange.CHEAP, PriceRange.MODERATE]
            )
            
            # Check distance
            if (restaurant_response.distance_km is not None and 
                restaurant_response.distance_km <= max_distance_km and 
                is_lunch_friendly):
                lunch_restaurants.append(restaurant_response)
            elif restaurant_response.distance_km is None and is_lunch_friendly:
                lunch_restaurants.append(restaurant_response)
        
        # Sort by rating and return top options
        lunch_restaurants.sort(key=lambda x: x.restaurant.rating, reverse=True)
        return lunch_restaurants[:8] 
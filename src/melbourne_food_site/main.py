"""Main FastAPI application for Melbourne Food Site."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List

from .api.restaurants import router as restaurants_router
from .api.recommendations import router as recommendations_router
from .models.restaurant import CuisineType, PriceRange
from .services.restaurant_service import RestaurantService

# Create FastAPI app
app = FastAPI(
    title="Melbourne Food Site API",
    description="API for restaurant recommendations, promos, and cheap eats in Melbourne",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(restaurants_router)
app.include_router(recommendations_router)

# Initialize services
restaurant_service = RestaurantService()


@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with API overview."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Melbourne Food Site API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #e74c3c; text-align: center; }
            h2 { color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }
            .endpoint { background: #ecf0f1; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { background: #3498db; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }
            .method.get { background: #27ae60; }
            .method.post { background: #e67e22; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍽️ Melbourne Food Site API</h1>
            <p>Welcome to the Melbourne Food Site API! This API provides restaurant recommendations, promotional offers, and cheap eats across Melbourne, Australia.</p>
            
            <h2>🔗 Quick Links</h2>
            <ul>
                <li><a href="/docs">📚 Interactive API Documentation (Swagger)</a></li>
                <li><a href="/redoc">📖 Alternative API Documentation (ReDoc)</a></li>
            </ul>
            
            <h2>🚀 Key Features</h2>
            <ul>
                <li><strong>Restaurant Discovery:</strong> Find restaurants by cuisine, location, price range</li>
                <li><strong>Smart Recommendations:</strong> ML-powered personalized suggestions</li>
                <li><strong>Cheap Eats:</strong> Budget-friendly dining options</li>
                <li><strong>Promotional Offers:</strong> Current deals and student discounts</li>
                <li><strong>Location-Based:</strong> Distance calculations and nearby recommendations</li>
            </ul>
            
            <h2>📍 Popular Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/restaurants/</strong><br>
                Get all restaurants with optional filtering
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/restaurants/cheap-eats/</strong><br>
                Find budget-friendly dining options
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/restaurants/promos/</strong><br>
                Restaurants with current promotional offers
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/recommendations/trending</strong><br>
                Get trending restaurants based on ratings and promos
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/recommendations/budget-friendly</strong><br>
                ML-powered budget-friendly recommendations
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/recommendations/for-students</strong><br>
                Student-friendly restaurants with discounts
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <strong>/recommendations/personalized</strong><br>
                Get personalized recommendations based on preferences
            </div>
            
            <h2>💡 Example Usage</h2>
            <p>Try these example requests:</p>
            <ul>
                <li><a href="/restaurants/?cuisine_types=Thai&price_ranges=$">Thai restaurants under $15</a></li>
                <li><a href="/restaurants/cheap-eats/">All cheap eats</a></li>
                <li><a href="/recommendations/trending">Trending restaurants</a></li>
                <li><a href="/recommendations/for-students">Student-friendly options</a></li>
            </ul>
            
            <h2>🏗️ Built With</h2>
            <ul>
                <li><strong>FastAPI:</strong> Modern, fast web framework</li>
                <li><strong>Pydantic:</strong> Data validation and settings</li>
                <li><strong>scikit-learn:</strong> Machine learning recommendations</li>
                <li><strong>Pandas & NumPy:</strong> Data analysis and processing</li>
                <li><strong>Geopy:</strong> Location distance calculations</li>
            </ul>
            
            <p style="text-align: center; margin-top: 30px; color: #7f8c8d;">
                Made with ❤️ for Melbourne food lovers
            </p>
        </div>
    </body>
    </html>
    """
    return html_content


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    total_restaurants = len(restaurant_service.get_all_restaurants())
    return {
        "status": "healthy",
        "service": "Melbourne Food Site API",
        "version": "1.0.0",
        "total_restaurants": total_restaurants
    }


@app.get("/cuisines", response_model=List[str])
async def get_available_cuisines():
    """Get list of available cuisine types."""
    return [cuisine.value for cuisine in CuisineType]


@app.get("/price-ranges", response_model=List[str])
async def get_available_price_ranges():
    """Get list of available price ranges."""
    return [price.value for price in PriceRange]


@app.get("/stats")
async def get_stats():
    """Get site statistics."""
    restaurants = restaurant_service.get_all_restaurants()
    
    # Count by cuisine type
    cuisine_counts = {}
    price_counts = {}
    
    for restaurant in restaurants:
        cuisine = restaurant.cuisine_type.value
        price = restaurant.price_range.value
        
        cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
        price_counts[price] = price_counts.get(price, 0) + 1
    
    # Calculate averages
    total_restaurants = len(restaurants)
    average_rating = sum(r.rating for r in restaurants) / total_restaurants if total_restaurants > 0 else 0
    
    # Count features
    delivery_count = sum(1 for r in restaurants if r.has_delivery)
    takeaway_count = sum(1 for r in restaurants if r.has_takeaway)
    student_discount_count = sum(1 for r in restaurants if r.student_discount)
    lunch_specials_count = sum(1 for r in restaurants if r.has_lunch_specials)
    
    return {
        "total_restaurants": total_restaurants,
        "average_rating": round(average_rating, 2),
        "cuisine_distribution": cuisine_counts,
        "price_distribution": price_counts,
        "features": {
            "delivery_available": delivery_count,
            "takeaway_available": takeaway_count,
            "student_discounts": student_discount_count,
            "lunch_specials": lunch_specials_count
        }
    }


def main():
    """Main entry point for running the application."""
    import uvicorn
    uvicorn.run(
        "melbourne_food_site.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main() 
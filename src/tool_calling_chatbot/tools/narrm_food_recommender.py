"""narrm food recommendation tool."""

import random
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult


class NarrmFoodRecommender(BaseTool):
    """narrm food recommendation tool for local dining."""
    
    CHEAP_EATS = [
        {
            "name": "dumplings plus",
            "cuisine": "chinese",
            "location": "bourke street",
            "price": "$8-12",
            "specialty": "handmade dumplings and noodles",
            "student_discount": True
        },
        {
            "name": "pellegrini's espresso bar",
            "cuisine": "italian",
            "location": "bourke street", 
            "price": "$6-15",
            "specialty": "authentic italian coffee and pasta since 1954",
            "student_discount": False
        },
        {
            "name": "pho dzung",
            "cuisine": "vietnamese",
            "location": "swanston street",
            "price": "$12-18",
            "specialty": "traditional pho and vietnamese dishes",
            "student_discount": True
        },
        {
            "name": "stalactites",
            "cuisine": "greek",
            "location": "lonsdale street",
            "price": "$10-20",
            "specialty": "24/7 greek food and souvlaki",
            "student_discount": False
        },
        {
            "name": "hwaro korean bbq",
            "cuisine": "korean",
            "location": "little collins street",
            "price": "$15-25",
            "specialty": "all you can eat korean bbq",
            "student_discount": True
        },
        {
            "name": "hanoi hannah",
            "cuisine": "vietnamese",
            "location": "smith street collingwood",
            "price": "$14-22",
            "specialty": "modern vietnamese street food",
            "student_discount": True
        },
        {
            "name": "momo grill",
            "cuisine": "nepalese",
            "location": "russell street",
            "price": "$10-16",
            "specialty": "authentic momos and dal bhat",
            "student_discount": True
        },
        {
            "name": "rumi",
            "cuisine": "middle eastern",
            "location": "brunswick street",
            "price": "$12-20",
            "specialty": "lebanese mezze and charcoal grills",
            "student_discount": False
        },
        {
            "name": "laksa king",
            "cuisine": "malaysian",
            "location": "flemington",
            "price": "$9-15",
            "specialty": "legendary curry laksa",
            "student_discount": False
        },
        {
            "name": "ghost donkey",
            "cuisine": "mexican",
            "location": "collins street",
            "price": "$8-14",
            "specialty": "tacos and mezcal bar vibes",
            "student_discount": True
        },
        {
            "name": "crossways food for life",
            "cuisine": "vegetarian",
            "location": "swanston street",
            "price": "$5-10",
            "specialty": "hare krishna vegetarian buffet",
            "student_discount": True
        },
        {
            "name": "miznon",
            "cuisine": "israeli",
            "location": "fitzroy",
            "price": "$12-18",
            "specialty": "cauliflower and pita perfection",
            "student_discount": False
        }
    ]
    
    TRENDY_SPOTS = [
        {
            "name": "chin chin",
            "cuisine": "thai",
            "location": "flinders lane",
            "price": "$25-40",
            "specialty": "modern thai with buzzing atmosphere",
            "student_discount": False
        },
        {
            "name": "cumulus inc",
            "cuisine": "modern australian",
            "location": "flinders lane",
            "price": "$30-50",
            "specialty": "contemporary dining and wine bar",
            "student_discount": False
        },
        {
            "name": "gazi",
            "cuisine": "greek",
            "location": "exhibition street",
            "price": "$35-55",
            "specialty": "modern greek with creative cocktails",
            "student_discount": False
        },
        {
            "name": "tipo 00",
            "cuisine": "italian",
            "location": "little bourke street",
            "price": "$28-45",
            "specialty": "fresh pasta and natural wines",
            "student_discount": False
        },
        {
            "name": "mr miyagi",
            "cuisine": "japanese",
            "location": "fawkner",
            "price": "$30-50",
            "specialty": "izakaya vibes with killer cocktails",
            "student_discount": False
        },
        {
            "name": "huxtaburger",
            "cuisine": "american",
            "location": "smith street",
            "price": "$18-28",
            "specialty": "gourmet burgers and loaded fries",
            "student_discount": False
        },
        {
            "name": "transformer",
            "cuisine": "fusion",
            "location": "fitzroy",
            "price": "$25-38",
            "specialty": "robot-themed asian fusion",
            "student_discount": False
        },
        {
            "name": "dealer de cafe",
            "cuisine": "european",
            "location": "collins street",
            "price": "$22-35",
            "specialty": "all day brunch and natural wines",
            "student_discount": False
        }
    ]
    
    COFFEE_CULTURE = [
        {
            "name": "brother baba budan",
            "cuisine": "coffee",
            "location": "little bourke street",
            "price": "$4-8",
            "specialty": "specialty coffee and small bites",
            "student_discount": False
        },
        {
            "name": "degraves espresso bar",
            "cuisine": "coffee",
            "location": "degraves street",
            "price": "$4-10",
            "specialty": "iconic laneway coffee culture",
            "student_discount": False
        },
        {
            "name": "patricia coffee brewers",
            "cuisine": "coffee",
            "location": "little bourke street",
            "price": "$5-12",
            "specialty": "third wave coffee roastery",
            "student_discount": False
        },
        {
            "name": "seven seeds",
            "cuisine": "coffee",
            "location": "carlton",
            "price": "$4-9",
            "specialty": "warehouse coffee roasting",
            "student_discount": False
        },
        {
            "name": "st ali",
            "cuisine": "coffee",
            "location": "south melbourne",
            "price": "$5-11",
            "specialty": "industrial coffee culture pioneer",
            "student_discount": False
        },
        {
            "name": "auction rooms",
            "cuisine": "coffee",
            "location": "north melbourne",
            "price": "$4-10",
            "specialty": "converted warehouse coffee vibes",
            "student_discount": False
        }
    ]
    
    @property
    def name(self) -> str:
        return "narrm_food_recommender"
    
    @property
    def description(self) -> str:
        return "recommends narrm restaurants based on budget, cuisine, and student status"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="budget",
                type="string",
                description="budget preference for dining",
                required=False,
                enum=["cheap", "moderate", "expensive"]
            ),
            ToolParameter(
                name="cuisine",
                type="string",
                description="preferred cuisine type",
                required=False,
                enum=["any", "asian", "italian", "greek", "australian", "coffee"]
            ),
            ToolParameter(
                name="student",
                type="boolean",
                description="whether user is a student seeking discounts",
                required=False
            )
        ]
    
    def _filter_restaurants(self, restaurants: List[dict], cuisine: str, student: bool) -> List[dict]:
        """filter restaurants based on criteria."""
        filtered = restaurants
        
        if cuisine != "any":
            if cuisine == "asian":
                filtered = [r for r in filtered if r["cuisine"] in ["chinese", "vietnamese", "korean", "thai", "japanese", "malaysian", "nepalese"]]
            else:
                filtered = [r for r in filtered if r["cuisine"] == cuisine]
        
        if student:
            # prioritize places with student discounts but don't exclude others
            student_places = [r for r in filtered if r["student_discount"]]
            if student_places:
                return student_places
        
        return filtered
    
    def _add_creative_variation(self, recommendation: dict) -> str:
        """add creative variations to make recommendations feel more dynamic."""
        variations = [
            f"hidden gem alert: {recommendation['name']} on {recommendation['location']}",
            f"local favorite: {recommendation['name']} - {recommendation['specialty']}",
            f"narrm classic: {recommendation['name']} ({recommendation['cuisine']} vibes)",
            f"worth the trek: {recommendation['name']} in {recommendation['location']}",
            f"insider pick: {recommendation['name']} - {recommendation['specialty']}"
        ]
        
        return random.choice(variations)
    
    async def execute(self, budget: str = "cheap", cuisine: str = "any", student: bool = False) -> ToolResult:
        """execute the narrm food recommender tool."""
        try:
            # select restaurant pool based on budget
            if budget == "cheap":
                restaurant_pool = self.CHEAP_EATS
            elif budget == "moderate":
                restaurant_pool = self.CHEAP_EATS + self.TRENDY_SPOTS
            elif budget == "expensive":
                restaurant_pool = self.TRENDY_SPOTS
            else:
                restaurant_pool = self.CHEAP_EATS
            
            # add coffee culture for coffee requests
            if cuisine == "coffee":
                restaurant_pool = self.COFFEE_CULTURE
            
            # filter restaurants
            filtered_restaurants = self._filter_restaurants(restaurant_pool, cuisine, student)
            
            if not filtered_restaurants:
                # fallback to cheap eats if no matches
                filtered_restaurants = self.CHEAP_EATS
            
            # select random recommendation
            recommendation = random.choice(filtered_restaurants)
            
            # create creative intro
            creative_intro = self._add_creative_variation(recommendation)
            
            # create recommendation text
            student_note = ""
            if student and recommendation["student_discount"]:
                student_note = "\n\nstudent tip: this place offers student discounts with valid id"
            elif student and not recommendation["student_discount"]:
                student_note = "\n\nno student discount here, but great value for money"
            
            recommendation_text = f"""
{creative_intro}

{recommendation['name']}
cuisine: {recommendation['cuisine']}
location: {recommendation['location']} 
price range: {recommendation['price']}
specialty: {recommendation['specialty']}{student_note}

narrm food tip: explore the laneways around this area for more hidden gems, 
and remember narrm's dining scene is best experienced by walking between spots.
            """.strip()
            
            return ToolResult(
                success=True,
                data={
                    "restaurant_name": recommendation["name"],
                    "cuisine": recommendation["cuisine"],
                    "location": recommendation["location"],
                    "price_range": recommendation["price"],
                    "specialty": recommendation["specialty"],
                    "student_discount": recommendation["student_discount"],
                    "budget_category": budget,
                    "recommendation_text": recommendation_text
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"error getting food recommendation: {str(e)}"
            ) 
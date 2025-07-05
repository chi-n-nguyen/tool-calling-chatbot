"""vintage narrm core outfit generator tool."""

import random
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult


class VintageOutfitGenerator(BaseTool):
    """vintage narrm core outfit generator tool."""
    
    VINTAGE_TOPS = [
        "oversized band tee (nirvana, pearl jam, or local narrm bands)",
        "striped long sleeve shirt layered under vintage slip dress",
        "cropped vintage denim jacket over basic black tee",
        "oversized blazer from savers or chapel street vintage store",
        "vintage graphic sweater with retro patterns",
        "black turtleneck with statement vintage accessories",
        "band merch hoodie from local venues like corner hotel",
        "vintage band tee tied at the waist over slip dress"
    ]
    
    VINTAGE_BOTTOMS = [
        "high waisted black jeans cuffed to show vintage boots",
        "vintage levi's 501s with natural distressing",
        "black mini skirt with opaque tights",
        "wide leg vintage trousers from camberwell market",
        "leather or faux leather mini skirt",
        "vintage slip dress worn as a skirt",
        "high waisted vintage shorts with tights",
        "corduroy wide leg pants from chapel street"
    ]
    
    VINTAGE_ACCESSORIES = [
        "chunky vintage belt from greville street vintage stores",
        "black doc martens or vintage band tee tied around waist",
        "vintage leather jacket (essential narrm piece)",
        "oversized vintage sunglasses",
        "vintage band pins on denim jacket",
        "layered silver jewelry from vintage markets",
        "vintage scarf worn around neck or as headband",
        "canvas tote bag from local record stores"
    ]
    
    NARRM_VINTAGE_SPOTS = [
        "chapel street vintage stores",
        "camberwell sunday market",
        "greville street vintage shopping",
        "savers stores across narrm",
        "vintage clothing warehouse richmond",
        "lost and found market",
        "vintage depot brunswick",
        "retro star vintage stores"
    ]
    
    @property
    def name(self) -> str:
        return "vintage_outfit_generator"
    
    @property
    def description(self) -> str:
        return "generates vintage narrm core outfit recommendations with local shopping spots"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="occasion",
                type="string",
                description="occasion for the outfit",
                required=False,
                enum=["casual", "concert", "date", "uni", "work", "weekend"]
            ),
            ToolParameter(
                name="season",
                type="string", 
                description="narrm season for appropriate layering",
                required=False,
                enum=["summer", "autumn", "winter", "spring"]
            )
        ]
    
    def _get_seasonal_modifications(self, season: str) -> dict:
        """get seasonal modifications for narrm weather."""
        modifications = {
            "summer": {
                "extra_items": ["vintage band tee", "denim shorts", "canvas sneakers"],
                "note": "narrm summer can be unpredictable, always carry a light jacket"
            },
            "autumn": {
                "extra_items": ["vintage cardigan", "ankle boots", "light scarf"],
                "note": "perfect vintage layering season in narrm"
            },
            "winter": {
                "extra_items": ["vintage wool coat", "chunky knit sweater", "warm boots"],
                "note": "narrm winter calls for serious vintage layering"
            },
            "spring": {
                "extra_items": ["light vintage jacket", "transitional boots", "colorful accessories"],
                "note": "classic narrm 'four seasons in one day' weather prep"
            }
        }
        return modifications.get(season, modifications["autumn"])
    
    async def execute(self, occasion: str = "casual", season: str = "autumn") -> ToolResult:
        """execute the vintage outfit generator tool."""
        try:
            # select random pieces for the outfit
            top = random.choice(self.VINTAGE_TOPS)
            bottom = random.choice(self.VINTAGE_BOTTOMS)
            accessories = random.sample(self.VINTAGE_ACCESSORIES, 2)
            shopping_spot = random.choice(self.NARRM_VINTAGE_SPOTS)
            
            # get seasonal modifications
            seasonal_mods = self._get_seasonal_modifications(season)
            
            # create outfit description
            outfit_description = f"""
vintage narrm core outfit for {occasion} in {season}:

top: {top}
bottom: {bottom}
accessories: {', '.join(accessories)}
seasonal addition: {random.choice(seasonal_mods['extra_items'])}

where to shop: {shopping_spot}

styling note: {seasonal_mods['note']}

narrm vintage tip: hit up multiple chapel street stores in one trip, 
and always check camberwell market on sundays for unique finds.
            """.strip()
            
            return ToolResult(
                success=True,
                data={
                    "occasion": occasion,
                    "season": season,
                    "top": top,
                    "bottom": bottom,
                    "accessories": accessories,
                    "shopping_spot": shopping_spot,
                    "outfit_description": outfit_description,
                    "seasonal_note": seasonal_mods['note']
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"error generating vintage outfit: {str(e)}"
            ) 
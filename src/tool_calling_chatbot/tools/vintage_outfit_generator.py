"""vintage narrm core outfit generator tool."""

import random
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult


class VintageOutfitGenerator(BaseTool):
    """vintage narrm core grunge outfit generator tool."""
    
    GRUNGE_TOPS = [
        "oversized carhartt flannel layered over band tee",
        "vintage stussy hoodie in earth tones",
        "thrifted nirvana or soundgarden band tee (oversized)",
        "carhartt detroit jacket in brown or olive",
        "vintage champion crewneck sweatshirt",
        "oversized flannel shirt tied around waist",
        "stussy basic tee in muted colours",
        "carhartt workwear shirt unbuttoned over tank",
        "vintage dickies work shirt in navy or khaki",
        "oversized graphic tee from local narrm venues",
        "grunge-style cropped cardigan over slip dress",
        "vintage patagonia fleece in earth tones"
    ]
    
    GRUNGE_BOTTOMS = [
        "baggy carhartt carpenter pants cuffed at ankles",
        "vintage levi's 501s with natural distressing and loose fit",
        "wide leg dickies work pants in khaki or black",
        "oversized cargo pants from surplus stores",
        "loose fitting corduroy pants in brown or olive",
        "baggy jeans with frayed hems",
        "vintage parachute pants in muted tones",
        "wide leg trousers from thrift stores",
        "carpenter jeans with tool loops",
        "loose fitting chinos in earth tones",
        "vintage ski pants for that 90s grunge vibe",
        "baggy shorts with long socks for warmer days"
    ]
    
    GRUNGE_ACCESSORIES = [
        "chunky doc martens 1460s in black or brown",
        "vintage carhartt beanie in brown or olive",
        "oversized silver chain or choker",
        "thrifted leather jacket (essential grunge piece)",
        "canvas messenger bag or jansport backpack",
        "vintage band pins on jacket or bag",
        "chunky silver rings and layered bracelets",
        "stussy bucket hat or dad cap",
        "vintage sunglasses with thick frames",
        "layered vintage band tees as accessories",
        "oversized flannel tied around waist",
        "vintage work gloves as styling piece"
    ]
    
    NARRM_GRUNGE_SPOTS = [
        "beyond retro chapel street (for authentic vintage)",
        "savers stores across narrm (best for carhartt finds)",
        "chapel street vintage stores (stussy and streetwear)",
        "camberwell sunday market (rare vintage workwear)",
        "vintage clothing warehouse richmond (bulk grunge pieces)",
        "lost and found market (curated grunge selections)",
        "vintage depot brunswick (90s streetwear focus)",
        "retro star vintage stores (band tees and flannels)",
        "greville street thrift stores (carhartt and dickies)",
        "smith street vintage shops (authentic 90s pieces)"
    ]
    
    @property
    def name(self) -> str:
        return "vintage_outfit_generator"
    
    @property
    def description(self) -> str:
        return "generates grunge core vintage narrm outfits with carhartt, stussy, and authentic 90s streetwear vibes"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="occasion",
                type="string",
                description="occasion for the grunge outfit",
                required=False,
                enum=["casual", "concert", "date", "uni", "work", "weekend"]
            ),
            ToolParameter(
                name="season",
                type="string", 
                description="narrm season for appropriate grunge layering",
                required=False,
                enum=["summer", "autumn", "winter", "spring"]
            )
        ]
    
    def _get_seasonal_grunge_mods(self, season: str) -> dict:
        """get seasonal modifications for narrm grunge weather."""
        modifications = {
            "summer": {
                "extra_items": ["vintage band tee", "baggy cargo shorts", "canvas sneakers or docs"],
                "note": "narrm summer grunge: oversized tees and baggy shorts, but keep that carhartt beanie for the vibe"
            },
            "autumn": {
                "extra_items": ["carhartt flannel", "chunky doc martens", "vintage windbreaker"],
                "note": "perfect grunge layering season in narrm - flannel over band tee is essential"
            },
            "winter": {
                "extra_items": ["carhartt detroit jacket", "chunky knit beanie", "heavyweight docs"],
                "note": "narrm winter grunge: serious layering with carhartt workwear and vintage flannels"
            },
            "spring": {
                "extra_items": ["light vintage hoodie", "stussy long sleeve", "canvas high tops"],
                "note": "classic narrm unpredictable weather - layer that stussy piece under a flannel"
            }
        }
        return modifications.get(season, modifications["autumn"])
    
    async def execute(self, occasion: str = "casual", season: str = "autumn") -> ToolResult:
        """execute the grunge outfit generator tool."""
        try:
            # select random grunge pieces for the outfit
            top = random.choice(self.GRUNGE_TOPS)
            bottom = random.choice(self.GRUNGE_BOTTOMS)
            accessories = random.sample(self.GRUNGE_ACCESSORIES, 2)
            shopping_spot = random.choice(self.NARRM_GRUNGE_SPOTS)
            
            # get seasonal modifications
            seasonal_mods = self._get_seasonal_grunge_mods(season)
            
            # create grunge outfit description
            outfit_description = f"""
grunge core narrm outfit for {occasion} in {season}:

top: {top}
bottom: {bottom}
accessories: {', '.join(accessories)}
seasonal addition: {random.choice(seasonal_mods['extra_items'])}

where to shop: {shopping_spot}

styling note: {seasonal_mods['note']}

grunge tip: authentic carhartt and stussy pieces at savers are gems - 
check multiple locations and don't sleep on dickies workwear for that proper 90s vibe.
the key is oversized silhouettes and earth tones, mate.
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
                error=f"error generating grunge outfit: {str(e)}"
            ) 
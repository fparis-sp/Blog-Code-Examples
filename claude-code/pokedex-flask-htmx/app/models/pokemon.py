from dataclasses import dataclass
from typing import List, Dict, Optional


# Tailwind color classes for pokemon types
TYPE_COLORS = {
    "normal": "bg-gray-400",
    "fire": "bg-red-500",
    "water": "bg-blue-500",
    "electric": "bg-yellow-400",
    "grass": "bg-green-500",
    "ice": "bg-cyan-300",
    "fighting": "bg-orange-700",
    "poison": "bg-purple-500",
    "ground": "bg-yellow-600",
    "flying": "bg-indigo-300",
    "psychic": "bg-pink-500",
    "bug": "bg-lime-500",
    "rock": "bg-yellow-700",
    "ghost": "bg-purple-700",
    "dragon": "bg-indigo-600",
    "dark": "bg-gray-700",
    "steel": "bg-gray-500",
    "fairy": "bg-pink-300",
}


@dataclass
class PokemonListItem:
    """Simplified Pokemon data for list view."""

    id: int
    name: str
    display_name: str

    @classmethod
    def from_api(cls, data: Dict) -> "PokemonListItem":
        """Create from PokeAPI response."""
        # Extract ID from URL: https://pokeapi.co/api/v2/pokemon/1/
        url = data["url"]
        pokemon_id = int(url.rstrip("/").split("/")[-1])

        return cls(id=pokemon_id, name=data["name"], display_name=data["name"].capitalize())


@dataclass
class Pokemon:
    """Complete Pokemon data for detail view."""

    id: int
    name: str
    display_name: str
    height_m: float
    weight_kg: float
    types: List[str]
    stats: Dict[str, int]
    abilities: List[str]
    sprite_url: Optional[str]
    artwork_url: Optional[str]

    @classmethod
    def from_api(cls, data: Dict) -> "Pokemon":
        """Create from PokeAPI response."""
        # Convert height from decimeters to meters
        height_m = data["height"] / 10

        # Convert weight from hectograms to kilograms
        weight_kg = data["weight"] / 10

        # Extract types and capitalize
        types = [t["type"]["name"].capitalize() for t in data["types"]]

        # Extract stats into a clean dict
        stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}

        # Extract abilities and capitalize
        abilities = [a["ability"]["name"].capitalize().replace("-", " ") for a in data["abilities"]]

        # Get sprite URLs
        sprites = data.get("sprites", {})
        sprite_url = sprites.get("front_default")
        artwork_url = sprites.get("other", {}).get("official-artwork", {}).get("front_default")

        return cls(
            id=data["id"],
            name=data["name"],
            display_name=data["name"].capitalize(),
            height_m=height_m,
            weight_kg=weight_kg,
            types=types,
            stats=stats,
            abilities=abilities,
            sprite_url=sprite_url,
            artwork_url=artwork_url,
        )

    def get_type_color(self, type_name: str) -> str:
        """Get Tailwind color class for a pokemon type."""
        return TYPE_COLORS.get(type_name.lower(), "bg-gray-400")

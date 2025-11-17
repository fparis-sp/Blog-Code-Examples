import requests
from typing import Optional, Dict, List


class PokeAPIService:
    """Service for interacting with PokeAPI."""

    def __init__(self, base_url: str):
        """Initialize the service with base URL."""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def get_pokemon_list(self, limit: int = 151, offset: int = 0) -> Optional[Dict]:
        """
        Fetch a list of pokemon.

        Args:
            limit: Number of pokemon to fetch (default 151 for Gen 1)
            offset: Offset for pagination

        Returns:
            Dictionary with pokemon list or None on error
        """
        try:
            url = f"{self.base_url}/pokemon"
            params = {'limit': limit, 'offset': offset}
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def get_pokemon_detail(self, name_or_id: str) -> Optional[Dict]:
        """
        Fetch detailed information for a specific pokemon.

        Args:
            name_or_id: Pokemon name or ID

        Returns:
            Dictionary with pokemon details or None if not found
        """
        try:
            url = f"{self.base_url}/pokemon/{name_or_id.lower()}"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

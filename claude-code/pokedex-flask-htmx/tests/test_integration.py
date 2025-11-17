import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client with real API calls."""
    app = create_app({"TESTING": True, "POKEAPI_BASE_URL": "https://pokeapi.co/api/v2"})
    with app.test_client() as client:
        yield client


def test_full_user_journey(client, mocker):
    """Test complete user flow from index to detail."""
    # Mock the API service to avoid relying on external API
    mock_service = mocker.patch("app.routes.main.get_pokeapi_service")

    # 1. Visit homepage
    mock_service.return_value.get_pokemon_list.return_value = {
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
        ]
    }
    response = client.get("/")
    assert response.status_code == 200
    assert b"Pok" in response.data  # Pokédex

    # 2. Click to view all pokemon
    mock_service.return_value.get_pokemon_list.return_value = {
        "results": [{"name": f"pokemon{i}", "url": f"https://pokeapi.co/api/v2/pokemon/{i}/"} for i in range(1, 152)]
    }
    response = client.get("/pokemon")
    assert response.status_code == 200
    assert b"All Pok" in response.data

    # 3. Search for a specific pokemon
    mock_service.return_value.get_pokemon_list.return_value = {
        "results": [
            {"name": "pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
        ]
    }
    response = client.get("/search?q=pikachu")
    assert response.status_code == 200
    assert b"pikachu" in response.data or b"Pikachu" in response.data

    # 4. View pokemon detail
    mock_service.return_value.get_pokemon_detail.return_value = {
        "id": 25,
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "types": [{"type": {"name": "electric"}}],
        "stats": [
            {"base_stat": 35, "stat": {"name": "hp"}},
            {"base_stat": 55, "stat": {"name": "attack"}},
            {"base_stat": 40, "stat": {"name": "defense"}},
            {"base_stat": 50, "stat": {"name": "special-attack"}},
            {"base_stat": 50, "stat": {"name": "special-defense"}},
            {"base_stat": 90, "stat": {"name": "speed"}},
        ],
        "abilities": [{"ability": {"name": "static"}}, {"ability": {"name": "lightning-rod"}}],
        "sprites": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
            "other": {
                "official-artwork": {
                    "front_default": (
                        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites"
                        "/pokemon/other/official-artwork/25.png"
                    )
                }
            },
        },
    }
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert b"pikachu" in response.data or b"Pikachu" in response.data
    assert b"Electric" in response.data or b"electric" in response.data


def test_error_handling(client, mocker):
    """Test that 404 errors are handled gracefully."""
    # Mock service to return None for non-existent pokemon
    mock_service = mocker.patch("app.routes.main.get_pokeapi_service")
    mock_service.return_value.get_pokemon_detail.return_value = None

    # Test 404 for non-existent pokemon
    response = client.get("/pokemon/notarealmon")
    assert response.status_code == 404
    assert b"404" in response.data or b"Not Found" in response.data

    # Test 404 for invalid route
    response = client.get("/invalid/route/that/does/not/exist")
    assert response.status_code == 404

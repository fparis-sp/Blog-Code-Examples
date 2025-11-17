import pytest
from app.services.pokeapi import PokeAPIService


@pytest.fixture
def pokeapi_service():
    """Create a PokeAPI service instance."""
    return PokeAPIService(base_url="https://pokeapi.co/api/v2")


def test_get_pokemon_list(pokeapi_service, mocker):
    """Test fetching list of pokemon."""
    mock_response = {
        "count": 151,
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
        ],
    }

    mock_get = mocker.patch.object(pokeapi_service.session, "get")
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = pokeapi_service.get_pokemon_list(limit=151)

    assert result is not None
    assert len(result["results"]) == 2
    assert result["results"][0]["name"] == "bulbasaur"
    mock_get.assert_called_once()


def test_get_pokemon_detail(pokeapi_service, mocker):
    """Test fetching pokemon detail by name."""
    mock_response = {
        "id": 1,
        "name": "bulbasaur",
        "height": 7,
        "weight": 69,
        "types": [{"type": {"name": "grass"}}, {"type": {"name": "poison"}}],
        "stats": [{"base_stat": 45, "stat": {"name": "hp"}}, {"base_stat": 49, "stat": {"name": "attack"}}],
        "abilities": [{"ability": {"name": "overgrow"}}],
        "sprites": {"front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"},
    }

    mock_get = mocker.patch.object(pokeapi_service.session, "get")
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = pokeapi_service.get_pokemon_detail("bulbasaur")

    assert result is not None
    assert result["id"] == 1
    assert result["name"] == "bulbasaur"
    assert len(result["types"]) == 2
    mock_get.assert_called_once()


def test_get_pokemon_detail_not_found(pokeapi_service, mocker):
    """Test handling of pokemon not found."""
    mock_get = mocker.patch.object(pokeapi_service.session, "get")
    mock_get.return_value.status_code = 404

    result = pokeapi_service.get_pokemon_detail("notapokemon")

    assert result is None

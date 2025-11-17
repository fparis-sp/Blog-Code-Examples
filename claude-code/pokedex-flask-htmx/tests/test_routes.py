import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app({
        'TESTING': True,
        'POKEAPI_BASE_URL': 'https://pokeapi.co/api/v2'
    })
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Pok' in response.data  # Unicode é might vary


def test_pokemon_list_route(client, mocker):
    """Test pokemon list page loads."""
    # Mock the PokeAPI service
    mock_service = mocker.patch('app.routes.main.get_pokeapi_service')
    mock_service.return_value.get_pokemon_list.return_value = {
        'results': [
            {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'},
            {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'}
        ]
    }

    response = client.get('/pokemon')
    assert response.status_code == 200
    assert b'bulbasaur' in response.data or b'Bulbasaur' in response.data

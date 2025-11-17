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


def test_pokemon_detail_route(client, mocker):
    """Test pokemon detail page loads."""
    mock_service = mocker.patch('app.routes.main.get_pokeapi_service')
    mock_service.return_value.get_pokemon_detail.return_value = {
        'id': 1,
        'name': 'bulbasaur',
        'height': 7,
        'weight': 69,
        'types': [{'type': {'name': 'grass'}}, {'type': {'name': 'poison'}}],
        'stats': [
            {'base_stat': 45, 'stat': {'name': 'hp'}},
            {'base_stat': 49, 'stat': {'name': 'attack'}},
            {'base_stat': 49, 'stat': {'name': 'defense'}},
            {'base_stat': 65, 'stat': {'name': 'special-attack'}},
            {'base_stat': 65, 'stat': {'name': 'special-defense'}},
            {'base_stat': 45, 'stat': {'name': 'speed'}}
        ],
        'abilities': [{'ability': {'name': 'overgrow'}}],
        'sprites': {
            'front_default': 'https://example.com/1.png',
            'other': {'official-artwork': {'front_default': 'https://example.com/official/1.png'}}
        }
    }

    response = client.get('/pokemon/bulbasaur')
    assert response.status_code == 200
    assert b'bulbasaur' in response.data or b'Bulbasaur' in response.data
    assert b'Grass' in response.data or b'grass' in response.data


def test_pokemon_detail_not_found(client, mocker):
    """Test 404 for non-existent pokemon."""
    mock_service = mocker.patch('app.routes.main.get_pokeapi_service')
    mock_service.return_value.get_pokemon_detail.return_value = None

    response = client.get('/pokemon/notapokemon')
    assert response.status_code == 404

import pytest
from app.models.pokemon import Pokemon, PokemonListItem


def test_pokemon_list_item_from_api():
    """Test creating PokemonListItem from API response."""
    api_data = {
        'name': 'bulbasaur',
        'url': 'https://pokeapi.co/api/v2/pokemon/1/'
    }

    item = PokemonListItem.from_api(api_data)

    assert item.name == 'bulbasaur'
    assert item.id == 1
    assert item.display_name == 'Bulbasaur'


def test_pokemon_from_api():
    """Test creating Pokemon from API response."""
    api_data = {
        'id': 1,
        'name': 'bulbasaur',
        'height': 7,
        'weight': 69,
        'types': [
            {'slot': 1, 'type': {'name': 'grass'}},
            {'slot': 2, 'type': {'name': 'poison'}}
        ],
        'stats': [
            {'base_stat': 45, 'stat': {'name': 'hp'}},
            {'base_stat': 49, 'stat': {'name': 'attack'}},
            {'base_stat': 49, 'stat': {'name': 'defense'}},
            {'base_stat': 65, 'stat': {'name': 'special-attack'}},
            {'base_stat': 65, 'stat': {'name': 'special-defense'}},
            {'base_stat': 45, 'stat': {'name': 'speed'}}
        ],
        'abilities': [
            {'ability': {'name': 'overgrow'}},
            {'ability': {'name': 'chlorophyll'}}
        ],
        'sprites': {
            'front_default': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
            'other': {
                'official-artwork': {
                    'front_default': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png'
                }
            }
        }
    }

    pokemon = Pokemon.from_api(api_data)

    assert pokemon.id == 1
    assert pokemon.name == 'bulbasaur'
    assert pokemon.display_name == 'Bulbasaur'
    assert pokemon.height_m == 0.7
    assert pokemon.weight_kg == 6.9
    assert len(pokemon.types) == 2
    assert 'Grass' in pokemon.types
    assert 'Poison' in pokemon.types
    assert pokemon.stats['hp'] == 45
    assert pokemon.stats['attack'] == 49
    assert len(pokemon.abilities) == 2
    assert 'Overgrow' in pokemon.abilities
    assert pokemon.sprite_url is not None
    assert pokemon.artwork_url is not None


def test_pokemon_type_colors():
    """Test that type colors are defined."""
    from app.models.pokemon import TYPE_COLORS

    assert 'fire' in TYPE_COLORS
    assert 'water' in TYPE_COLORS
    assert 'grass' in TYPE_COLORS
    assert TYPE_COLORS['fire'] == 'bg-red-500'

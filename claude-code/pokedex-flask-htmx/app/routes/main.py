from flask import Blueprint, render_template, current_app
from app.services.pokeapi import PokeAPIService
from app.models.pokemon import PokemonListItem

bp = Blueprint('main', __name__)


def get_pokeapi_service():
    """Get PokeAPI service instance."""
    return PokeAPIService(current_app.config['POKEAPI_BASE_URL'])


@bp.route('/')
def index():
    """Home page with featured pokemon."""
    service = get_pokeapi_service()

    # Fetch first 9 pokemon for featured section
    response = service.get_pokemon_list(limit=9)

    featured = []
    if response and 'results' in response:
        featured = [PokemonListItem.from_api(p) for p in response['results']]

    return render_template('index.html', featured=featured)


@bp.route('/pokemon')
def pokemon_list():
    """Full pokemon list page (Gen 1)."""
    service = get_pokeapi_service()

    # Fetch all 151 Gen 1 pokemon
    response = service.get_pokemon_list(limit=151)

    pokemon_list = []
    if response and 'results' in response:
        pokemon_list = [PokemonListItem.from_api(p) for p in response['results']]

    return render_template('pokemon_list.html', pokemon_list=pokemon_list)

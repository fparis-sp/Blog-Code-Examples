from flask import Blueprint, render_template, current_app, abort, request
from app.services.pokeapi import PokeAPIService
from app.models.pokemon import PokemonListItem, Pokemon

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


@bp.route('/pokemon/<string:name>')
def pokemon_detail(name):
    """Pokemon detail page."""
    service = get_pokeapi_service()

    # Fetch pokemon details
    response = service.get_pokemon_detail(name)

    if not response:
        abort(404)

    pokemon = Pokemon.from_api(response)

    return render_template('pokemon_detail.html', pokemon=pokemon)


@bp.route('/search')
def search():
    """Search pokemon by name or number."""
    query = request.args.get('q', '').strip()
    service = get_pokeapi_service()

    results = []

    if not query:
        # Empty query - return no results
        return render_template('components/search_results.html', results=results)

    # Check if query is a number (search by ID)
    if query.isdigit():
        pokemon_id = int(query)
        # Only search for Gen 1 pokemon (1-151)
        if 1 <= pokemon_id <= 151:
            response = service.get_pokemon_detail(pokemon_id)
            if response:
                pokemon = PokemonListItem(
                    id=response['id'],
                    name=response['name'],
                    display_name=response['name'].capitalize()
                )
                results.append(pokemon)
    else:
        # Search by name - filter Gen 1 list
        response = service.get_pokemon_list(limit=151)
        if response and 'results' in response:
            # Filter pokemon that contain the query string
            query_lower = query.lower()
            filtered = [
                PokemonListItem.from_api(p)
                for p in response['results']
                if query_lower in p['name'].lower()
            ]
            # Limit to 10 results
            results = filtered[:10]

    return render_template('components/search_results.html', results=results)

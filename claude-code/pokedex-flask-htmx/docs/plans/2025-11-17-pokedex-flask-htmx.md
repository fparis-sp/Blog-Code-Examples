# Pokédex Flask + HTMX Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Build a web-based Pokédex with Flask backend, HTMX frontend, consuming PokeAPI to display Gen 1 Pokémon with search, list, and detail views.

**Architecture:** Flask serves HTML templates enhanced with HTMX for dynamic interactions. Backend fetches data from PokeAPI, caches responses, and renders templates. No JavaScript required - HTMX handles all interactivity via HTML attributes.

**Tech Stack:** Flask 3.x, HTMX 1.9.x, Tailwind CSS 3.x, PokeAPI, pytest, Docker

---

## Task 1: Project Setup and Dependencies

**Files:**
- Create: `claude-code/pokedex-flask-htmx/.gitignore`
- Create: `claude-code/pokedex-flask-htmx/requirements.txt`
- Create: `claude-code/pokedex-flask-htmx/requirements-dev.txt`
- Create: `claude-code/pokedex-flask-htmx/.python-version`
- Create: `claude-code/pokedex-flask-htmx/pytest.ini`

**Step 1: Create .gitignore**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local

# Flask
instance/
.webassets-cache

# OS
.DS_Store
Thumbs.db
```

**Step 2: Create requirements.txt**

```
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
```

**Step 3: Create requirements-dev.txt**

```
-r requirements.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.0
flake8==6.1.0
```

**Step 4: Create .python-version**

```
3.12
```

**Step 5: Create pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=app --cov-report=html --cov-report=term
```

**Step 6: Commit project setup**

```bash
cd claude-code/pokedex-flask-htmx
git add .gitignore requirements.txt requirements-dev.txt .python-version pytest.ini
git commit -m "chore: initial project setup with dependencies"
```

---

## Task 2: Flask Application Structure

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/__init__.py`
- Create: `claude-code/pokedex-flask-htmx/app/config.py`
- Create: `claude-code/pokedex-flask-htmx/run.py`
- Create: `claude-code/pokedex-flask-htmx/.env.example`

**Step 1: Write test for Flask app creation**

Create: `claude-code/pokedex-flask-htmx/tests/test_app.py`

```python
import pytest
from app import create_app


def test_app_creation():
    """Test that Flask app can be created."""
    app = create_app()
    assert app is not None
    assert app.config['TESTING'] is False


def test_app_test_config():
    """Test that app can be created with test config."""
    app = create_app({'TESTING': True})
    assert app.config['TESTING'] is True
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_app.py -v
```

Expected: FAIL with "cannot import name 'create_app'"

**Step 3: Create config.py**

Create: `claude-code/pokedex-flask-htmx/app/config.py`

```python
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    POKEAPI_BASE_URL = 'https://pokeapi.co/api/v2'
    CACHE_TIMEOUT = 3600  # 1 hour in seconds


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

**Step 4: Create app factory**

Create: `claude-code/pokedex-flask-htmx/app/__init__.py`

```python
from flask import Flask
from app.config import config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default config
        env = os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config.get(env, config['default']))
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
```

Wait, we need to import os. Let me fix that:

```python
import os
from flask import Flask
from app.config import config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default config
        env = os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config.get(env, config['default']))
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
```

**Step 5: Run test to verify it passes**

```bash
pytest tests/test_app.py -v
```

Expected: PASS (2 tests)

**Step 6: Create run.py**

Create: `claude-code/pokedex-flask-htmx/run.py`

```python
#!/usr/bin/env python3
"""Run the Flask application."""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**Step 7: Create .env.example**

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000
```

**Step 8: Commit Flask structure**

```bash
git add app/ tests/test_app.py run.py .env.example
git commit -m "feat: create Flask app factory and configuration"
```

---

## Task 3: PokeAPI Service Layer

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/services/__init__.py`
- Create: `claude-code/pokedex-flask-htmx/app/services/pokeapi.py`
- Create: `claude-code/pokedex-flask-htmx/tests/test_pokeapi_service.py`

**Step 1: Write failing test for fetching pokemon list**

Create: `claude-code/pokedex-flask-htmx/tests/test_pokeapi_service.py`

```python
import pytest
from app.services.pokeapi import PokeAPIService


@pytest.fixture
def pokeapi_service():
    """Create a PokeAPI service instance."""
    return PokeAPIService(base_url='https://pokeapi.co/api/v2')


def test_get_pokemon_list(pokeapi_service, mocker):
    """Test fetching list of pokemon."""
    mock_response = {
        'count': 151,
        'results': [
            {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'},
            {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'}
        ]
    }

    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = pokeapi_service.get_pokemon_list(limit=151)

    assert result is not None
    assert len(result['results']) == 2
    assert result['results'][0]['name'] == 'bulbasaur'
    mock_get.assert_called_once()


def test_get_pokemon_detail(pokeapi_service, mocker):
    """Test fetching pokemon detail by name."""
    mock_response = {
        'id': 1,
        'name': 'bulbasaur',
        'height': 7,
        'weight': 69,
        'types': [
            {'type': {'name': 'grass'}},
            {'type': {'name': 'poison'}}
        ],
        'stats': [
            {'base_stat': 45, 'stat': {'name': 'hp'}},
            {'base_stat': 49, 'stat': {'name': 'attack'}}
        ],
        'abilities': [
            {'ability': {'name': 'overgrow'}}
        ],
        'sprites': {
            'front_default': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
        }
    }

    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = pokeapi_service.get_pokemon_detail('bulbasaur')

    assert result is not None
    assert result['id'] == 1
    assert result['name'] == 'bulbasaur'
    assert len(result['types']) == 2
    mock_get.assert_called_once()


def test_get_pokemon_detail_not_found(pokeapi_service, mocker):
    """Test handling of pokemon not found."""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 404

    result = pokeapi_service.get_pokemon_detail('notapokemon')

    assert result is None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_pokeapi_service.py -v
```

Expected: FAIL with "cannot import name 'PokeAPIService'"

**Step 3: Create PokeAPI service implementation**

Create: `claude-code/pokedex-flask-htmx/app/services/__init__.py` (empty file)

Create: `claude-code/pokedex-flask-htmx/app/services/pokeapi.py`

```python
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
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_pokeapi_service.py -v
```

Expected: PASS (3 tests)

**Step 5: Commit PokeAPI service**

```bash
git add app/services/ tests/test_pokeapi_service.py
git commit -m "feat: add PokeAPI service layer with tests"
```

---

## Task 4: Data Transformation Layer

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/models/__init__.py`
- Create: `claude-code/pokedex-flask-htmx/app/models/pokemon.py`
- Create: `claude-code/pokedex-flask-htmx/tests/test_pokemon_model.py`

**Step 1: Write failing test for Pokemon model**

Create: `claude-code/pokedex-flask-htmx/tests/test_pokemon_model.py`

```python
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
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_pokemon_model.py -v
```

Expected: FAIL with "cannot import name 'Pokemon'"

**Step 3: Create Pokemon model**

Create: `claude-code/pokedex-flask-htmx/app/models/__init__.py` (empty file)

Create: `claude-code/pokedex-flask-htmx/app/models/pokemon.py`

```python
from dataclasses import dataclass
from typing import List, Dict, Optional


# Tailwind color classes for pokemon types
TYPE_COLORS = {
    'normal': 'bg-gray-400',
    'fire': 'bg-red-500',
    'water': 'bg-blue-500',
    'electric': 'bg-yellow-400',
    'grass': 'bg-green-500',
    'ice': 'bg-cyan-300',
    'fighting': 'bg-orange-700',
    'poison': 'bg-purple-500',
    'ground': 'bg-yellow-600',
    'flying': 'bg-indigo-300',
    'psychic': 'bg-pink-500',
    'bug': 'bg-lime-500',
    'rock': 'bg-yellow-700',
    'ghost': 'bg-purple-700',
    'dragon': 'bg-indigo-600',
    'dark': 'bg-gray-700',
    'steel': 'bg-gray-500',
    'fairy': 'bg-pink-300',
}


@dataclass
class PokemonListItem:
    """Simplified Pokemon data for list view."""
    id: int
    name: str
    display_name: str

    @classmethod
    def from_api(cls, data: Dict) -> 'PokemonListItem':
        """Create from PokeAPI response."""
        # Extract ID from URL: https://pokeapi.co/api/v2/pokemon/1/
        url = data['url']
        pokemon_id = int(url.rstrip('/').split('/')[-1])

        return cls(
            id=pokemon_id,
            name=data['name'],
            display_name=data['name'].capitalize()
        )


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
    def from_api(cls, data: Dict) -> 'Pokemon':
        """Create from PokeAPI response."""
        # Convert height from decimeters to meters
        height_m = data['height'] / 10

        # Convert weight from hectograms to kilograms
        weight_kg = data['weight'] / 10

        # Extract types and capitalize
        types = [t['type']['name'].capitalize() for t in data['types']]

        # Extract stats into a clean dict
        stats = {
            stat['stat']['name']: stat['base_stat']
            for stat in data['stats']
        }

        # Extract abilities and capitalize
        abilities = [a['ability']['name'].capitalize().replace('-', ' ') for a in data['abilities']]

        # Get sprite URLs
        sprites = data.get('sprites', {})
        sprite_url = sprites.get('front_default')
        artwork_url = sprites.get('other', {}).get('official-artwork', {}).get('front_default')

        return cls(
            id=data['id'],
            name=data['name'],
            display_name=data['name'].capitalize(),
            height_m=height_m,
            weight_kg=weight_kg,
            types=types,
            stats=stats,
            abilities=abilities,
            sprite_url=sprite_url,
            artwork_url=artwork_url
        )

    def get_type_color(self, type_name: str) -> str:
        """Get Tailwind color class for a pokemon type."""
        return TYPE_COLORS.get(type_name.lower(), 'bg-gray-400')
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_pokemon_model.py -v
```

Expected: PASS (3 tests)

**Step 5: Commit Pokemon model**

```bash
git add app/models/ tests/test_pokemon_model.py
git commit -m "feat: add Pokemon data models with transformation logic"
```

---

## Task 5: Base Templates and Static Files

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/templates/base.html`
- Create: `claude-code/pokedex-flask-htmx/app/templates/components/navbar.html`
- Create: `claude-code/pokedex-flask-htmx/app/static/css/styles.css`

**Step 1: Create base template with HTMX and Tailwind**

Create: `claude-code/pokedex-flask-htmx/app/templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Pokédex{% endblock %}</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>

    <!-- Custom styles -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">

    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    {% include 'components/navbar.html' %}

    <!-- Main content -->
    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-auto py-6">
        <div class="container mx-auto px-4 text-center">
            <p>Built with Flask + HTMX | Data from <a href="https://pokeapi.co" class="text-blue-400 hover:underline">PokeAPI</a></p>
        </div>
    </footer>

    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

**Step 2: Create navbar component**

Create: `claude-code/pokedex-flask-htmx/app/templates/components/navbar.html`

```html
<nav class="bg-red-600 text-white shadow-lg">
    <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
            <!-- Logo -->
            <div class="flex items-center">
                <a href="{{ url_for('main.index') }}" class="text-2xl font-bold">
                    🔴 Pokédex
                </a>
            </div>

            <!-- Search bar -->
            <div class="flex-1 max-w-lg mx-8">
                <form hx-get="{{ url_for('main.search') }}"
                      hx-target="#search-results"
                      hx-trigger="input changed delay:300ms, search"
                      class="relative">
                    <input
                        type="search"
                        name="q"
                        placeholder="Search Pokémon by name or number..."
                        class="w-full px-4 py-2 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                    >
                </form>
            </div>

            <!-- Navigation links -->
            <div class="flex space-x-4">
                <a href="{{ url_for('main.index') }}" class="hover:text-yellow-300 transition">Home</a>
                <a href="{{ url_for('main.pokemon_list') }}" class="hover:text-yellow-300 transition">All Pokémon</a>
            </div>
        </div>
    </div>
</nav>

<!-- Search results container (hidden by default) -->
<div id="search-results" class="container mx-auto px-4 mt-4"></div>
```

**Step 3: Create custom CSS**

Create: `claude-code/pokedex-flask-htmx/app/static/css/styles.css`

```css
/* Custom animations and utilities */

.pokemon-card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.pokemon-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.stat-bar {
    transition: width 0.3s ease-in-out;
}

/* HTMX loading states */
.htmx-request .htmx-indicator {
    display: inline-block;
}

.htmx-indicator {
    display: none;
}

/* Type badge animations */
.type-badge {
    transition: transform 0.2s ease;
}

.type-badge:hover {
    transform: scale(1.05);
}

/* Search result highlighting */
.search-result-item {
    transition: background-color 0.2s ease;
}

.search-result-item:hover {
    background-color: rgba(254, 243, 199, 0.5);
}

/* Loading spinner */
.spinner {
    border: 3px solid rgba(0, 0, 0, 0.1);
    border-left-color: #ef4444;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
```

**Step 4: Commit templates and static files**

```bash
git add app/templates/ app/static/
git commit -m "feat: add base templates and static files with Tailwind and HTMX"
```

---

## Task 6: Main Routes - Index and List

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/routes/__init__.py`
- Create: `claude-code/pokedex-flask-htmx/app/routes/main.py`
- Create: `claude-code/pokedex-flask-htmx/app/templates/index.html`
- Create: `claude-code/pokedex-flask-htmx/app/templates/pokemon_list.html`
- Create: `claude-code/pokedex-flask-htmx/app/templates/components/pokemon_card.html`
- Modify: `claude-code/pokedex-flask-htmx/app/__init__.py`

**Step 1: Write failing test for index route**

Create: `claude-code/pokedex-flask-htmx/tests/test_routes.py`

```python
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app({'TESTING': True})
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
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_routes.py -v
```

Expected: FAIL with "404 Not Found"

**Step 3: Create routes module**

Create: `claude-code/pokedex-flask-htmx/app/routes/__init__.py` (empty file)

Create: `claude-code/pokedex-flask-htmx/app/routes/main.py`

```python
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
```

**Step 4: Update app factory to register blueprint**

Modify: `claude-code/pokedex-flask-htmx/app/__init__.py`

```python
import os
from flask import Flask
from app.config import config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default config
        env = os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config.get(env, config['default']))
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)

    return app
```

**Step 5: Create index template**

Create: `claude-code/pokedex-flask-htmx/app/templates/index.html`

```html
{% extends "base.html" %}

{% block title %}Pokédex - Gotta Catch 'Em All!{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="text-center mb-12">
    <h1 class="text-5xl font-bold text-gray-800 mb-4">
        Welcome to the Pokédex!
    </h1>
    <p class="text-xl text-gray-600">
        Explore the first generation of Pokémon
    </p>
</div>

<!-- Featured Pokemon -->
<section class="mb-12">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Featured Pokémon</h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {% for pokemon in featured %}
            {% include 'components/pokemon_card.html' %}
        {% endfor %}
    </div>
</section>

<!-- CTA Section -->
<div class="text-center bg-red-600 text-white rounded-lg p-8">
    <h2 class="text-3xl font-bold mb-4">Ready to Explore?</h2>
    <p class="text-lg mb-6">Browse all 151 Generation 1 Pokémon</p>
    <a href="{{ url_for('main.pokemon_list') }}"
       class="inline-block bg-yellow-400 text-gray-800 font-bold px-8 py-3 rounded-lg hover:bg-yellow-300 transition">
        View All Pokémon
    </a>
</div>
{% endblock %}
```

**Step 6: Create pokemon list template**

Create: `claude-code/pokedex-flask-htmx/app/templates/pokemon_list.html`

```html
{% extends "base.html" %}

{% block title %}All Pokémon - Pokédex{% endblock %}

{% block content %}
<div class="mb-8">
    <h1 class="text-4xl font-bold text-gray-800 mb-2">All Pokémon</h1>
    <p class="text-gray-600">Generation 1 - {{ pokemon_list|length }} Pokémon</p>
</div>

<!-- Pokemon Grid -->
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
    {% for pokemon in pokemon_list %}
        {% include 'components/pokemon_card.html' %}
    {% endfor %}
</div>
{% endblock %}
```

**Step 7: Create pokemon card component**

Create: `claude-code/pokedex-flask-htmx/app/templates/components/pokemon_card.html`

```html
<a href="{{ url_for('main.pokemon_detail', name=pokemon.name) }}"
   class="pokemon-card block bg-white rounded-lg shadow-md p-4 hover:shadow-xl">
    <div class="text-center">
        <!-- Pokemon Image -->
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{{ pokemon.id }}.png"
             alt="{{ pokemon.display_name }}"
             class="mx-auto w-24 h-24 object-contain"
             loading="lazy">

        <!-- Pokemon Number -->
        <p class="text-gray-500 text-sm font-mono">
            #{{ '%03d'|format(pokemon.id) }}
        </p>

        <!-- Pokemon Name -->
        <h3 class="text-lg font-bold text-gray-800 capitalize">
            {{ pokemon.display_name }}
        </h3>
    </div>
</a>
```

**Step 8: Run test to verify it passes**

```bash
pytest tests/test_routes.py -v
```

Expected: PASS (2 tests)

**Step 9: Commit routes and templates**

```bash
git add app/routes/ app/__init__.py app/templates/index.html app/templates/pokemon_list.html app/templates/components/pokemon_card.html tests/test_routes.py
git commit -m "feat: add index and pokemon list routes with templates"
```

---

## Task 7: Pokemon Detail View

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/templates/pokemon_detail.html`
- Create: `claude-code/pokedex-flask-htmx/app/templates/components/stat_bar.html`
- Modify: `claude-code/pokedex-flask-htmx/app/routes/main.py`
- Modify: `claude-code/pokedex-flask-htmx/tests/test_routes.py`

**Step 1: Write failing test for pokemon detail route**

Modify: `claude-code/pokedex-flask-htmx/tests/test_routes.py` (add test)

```python
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
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_routes.py::test_pokemon_detail_route -v
```

Expected: FAIL with "404 Not Found"

**Step 3: Add detail route to main.py**

Modify: `claude-code/pokedex-flask-htmx/app/routes/main.py` (add route)

```python
from flask import Blueprint, render_template, current_app, abort
from app.services.pokeapi import PokeAPIService
from app.models.pokemon import PokemonListItem, Pokemon

# ... existing code ...

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
```

**Step 4: Create stat bar component**

Create: `claude-code/pokedex-flask-htmx/app/templates/components/stat_bar.html`

```html
{% macro render_stat(name, value, max_value=255) %}
<div class="mb-3">
    <div class="flex justify-between mb-1">
        <span class="text-sm font-medium text-gray-700 capitalize">{{ name }}</span>
        <span class="text-sm font-bold text-gray-900">{{ value }}</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div class="stat-bar bg-blue-600 h-2.5 rounded-full"
             style="width: {{ (value / max_value * 100)|round|int }}%">
        </div>
    </div>
</div>
{% endmacro %}
```

**Step 5: Create pokemon detail template**

Create: `claude-code/pokedex-flask-htmx/app/templates/pokemon_detail.html`

```html
{% extends "base.html" %}
{% from "components/stat_bar.html" import render_stat %}

{% block title %}{{ pokemon.display_name }} - Pokédex{% endblock %}

{% block content %}
<!-- Back button -->
<div class="mb-6">
    <a href="{{ url_for('main.pokemon_list') }}"
       class="inline-flex items-center text-blue-600 hover:text-blue-800">
        ← Back to List
    </a>
</div>

<div class="bg-white rounded-lg shadow-lg overflow-hidden">
    <div class="md:flex">
        <!-- Left side - Image -->
        <div class="md:w-1/2 bg-gradient-to-br from-gray-100 to-gray-200 p-8">
            <div class="text-center">
                <p class="text-gray-500 text-xl font-mono mb-2">
                    #{{ '%03d'|format(pokemon.id) }}
                </p>
                <h1 class="text-4xl font-bold text-gray-800 mb-8 capitalize">
                    {{ pokemon.display_name }}
                </h1>

                <!-- Official Artwork -->
                {% if pokemon.artwork_url %}
                <img src="{{ pokemon.artwork_url }}"
                     alt="{{ pokemon.display_name }}"
                     class="mx-auto w-64 h-64 object-contain drop-shadow-2xl">
                {% elif pokemon.sprite_url %}
                <img src="{{ pokemon.sprite_url }}"
                     alt="{{ pokemon.display_name }}"
                     class="mx-auto w-48 h-48 object-contain">
                {% endif %}

                <!-- Types -->
                <div class="flex justify-center gap-2 mt-6">
                    {% for type in pokemon.types %}
                    <span class="{{ pokemon.get_type_color(type) }} text-white px-4 py-2 rounded-full font-semibold type-badge">
                        {{ type }}
                    </span>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Right side - Details -->
        <div class="md:w-1/2 p-8">
            <!-- Physical Info -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Physical Info</h2>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-gray-600 text-sm">Height</p>
                        <p class="text-2xl font-bold text-gray-800">{{ "%.1f"|format(pokemon.height_m) }} m</p>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <p class="text-gray-600 text-sm">Weight</p>
                        <p class="text-2xl font-bold text-gray-800">{{ "%.1f"|format(pokemon.weight_kg) }} kg</p>
                    </div>
                </div>
            </div>

            <!-- Abilities -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Abilities</h2>
                <div class="flex flex-wrap gap-2">
                    {% for ability in pokemon.abilities %}
                    <span class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                        {{ ability }}
                    </span>
                    {% endfor %}
                </div>
            </div>

            <!-- Base Stats -->
            <div>
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Base Stats</h2>
                {{ render_stat('HP', pokemon.stats.hp) }}
                {{ render_stat('Attack', pokemon.stats.attack) }}
                {{ render_stat('Defense', pokemon.stats.defense) }}
                {{ render_stat('Sp. Attack', pokemon.stats['special-attack']) }}
                {{ render_stat('Sp. Defense', pokemon.stats['special-defense']) }}
                {{ render_stat('Speed', pokemon.stats.speed) }}
            </div>
        </div>
    </div>
</div>

<!-- Navigation to previous/next pokemon -->
<div class="mt-8 flex justify-between">
    {% if pokemon.id > 1 %}
    <a href="{{ url_for('main.pokemon_detail', name=pokemon.id - 1) }}"
       class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
        ← Previous
    </a>
    {% else %}
    <div></div>
    {% endif %}

    {% if pokemon.id < 151 %}
    <a href="{{ url_for('main.pokemon_detail', name=pokemon.id + 1) }}"
       class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
        Next →
    </a>
    {% endif %}
</div>
{% endblock %}
```

**Step 6: Run test to verify it passes**

```bash
pytest tests/test_routes.py -v
```

Expected: PASS (4 tests)

**Step 7: Commit detail view**

```bash
git add app/templates/pokemon_detail.html app/templates/components/stat_bar.html app/routes/main.py tests/test_routes.py
git commit -m "feat: add pokemon detail view with stats and navigation"
```

---

## Task 8: Search Functionality with HTMX

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/templates/components/search_results.html`
- Modify: `claude-code/pokedex-flask-htmx/app/routes/main.py`
- Modify: `claude-code/pokedex-flask-htmx/tests/test_routes.py`

**Step 1: Write failing test for search route**

Modify: `claude-code/pokedex-flask-htmx/tests/test_routes.py` (add test)

```python
def test_search_route(client, mocker):
    """Test search endpoint returns filtered results."""
    mock_service = mocker.patch('app.routes.main.get_pokeapi_service')
    mock_service.return_value.get_pokemon_list.return_value = {
        'results': [
            {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'},
            {'name': 'charmander', 'url': 'https://pokeapi.co/api/v2/pokemon/4/'},
            {'name': 'squirtle', 'url': 'https://pokeapi.co/api/v2/pokemon/7/'}
        ]
    }

    response = client.get('/search?q=char')
    assert response.status_code == 200
    assert b'charmander' in response.data or b'Charmander' in response.data
    assert b'bulbasaur' not in response.data


def test_search_by_number(client, mocker):
    """Test search by pokemon number."""
    mock_service = mocker.patch('app.routes.main.get_pokeapi_service')
    mock_service.return_value.get_pokemon_detail.return_value = {
        'id': 25,
        'name': 'pikachu',
        'height': 4,
        'weight': 60,
        'types': [{'type': {'name': 'electric'}}],
        'stats': [
            {'base_stat': 35, 'stat': {'name': 'hp'}},
            {'base_stat': 55, 'stat': {'name': 'attack'}},
            {'base_stat': 40, 'stat': {'name': 'defense'}},
            {'base_stat': 50, 'stat': {'name': 'special-attack'}},
            {'base_stat': 50, 'stat': {'name': 'special-defense'}},
            {'base_stat': 90, 'stat': {'name': 'speed'}}
        ],
        'abilities': [{'ability': {'name': 'static'}}],
        'sprites': {
            'front_default': 'https://example.com/25.png',
            'other': {'official-artwork': {'front_default': 'https://example.com/official/25.png'}}
        }
    }

    response = client.get('/search?q=25')
    assert response.status_code == 200
    assert b'pikachu' in response.data or b'Pikachu' in response.data


def test_search_empty_query(client):
    """Test search with empty query."""
    response = client.get('/search?q=')
    assert response.status_code == 200
    assert b'Enter a search term' in response.data or len(response.data) < 100
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_routes.py::test_search_route -v
```

Expected: FAIL with "404 Not Found"

**Step 3: Add search route**

Modify: `claude-code/pokedex-flask-htmx/app/routes/main.py` (add route)

```python
from flask import Blueprint, render_template, current_app, abort, request
from app.services.pokeapi import PokeAPIService
from app.models.pokemon import PokemonListItem, Pokemon

# ... existing code ...

@bp.route('/search')
def search():
    """Search pokemon by name or number (HTMX endpoint)."""
    query = request.args.get('q', '').strip().lower()

    if not query:
        return render_template('components/search_results.html', results=[])

    service = get_pokeapi_service()
    results = []

    # Check if query is a number
    if query.isdigit():
        pokemon_id = int(query)
        if 1 <= pokemon_id <= 151:
            # Try to get specific pokemon by ID
            response = service.get_pokemon_detail(pokemon_id)
            if response:
                results.append(PokemonListItem(
                    id=response['id'],
                    name=response['name'],
                    display_name=response['name'].capitalize()
                ))
    else:
        # Search by name - fetch all Gen 1 and filter
        response = service.get_pokemon_list(limit=151)
        if response and 'results' in response:
            all_pokemon = [PokemonListItem.from_api(p) for p in response['results']]
            # Filter by name match
            results = [p for p in all_pokemon if query in p.name.lower()]

    return render_template('components/search_results.html', results=results[:10])  # Limit to 10 results
```

**Step 4: Create search results component**

Create: `claude-code/pokedex-flask-htmx/app/templates/components/search_results.html`

```html
{% if results %}
<div class="bg-white rounded-lg shadow-lg mt-2 max-w-lg mx-auto">
    <div class="p-4">
        <p class="text-sm text-gray-600 mb-3">Found {{ results|length }} result(s)</p>
        <div class="space-y-2">
            {% for pokemon in results %}
            <a href="{{ url_for('main.pokemon_detail', name=pokemon.name) }}"
               class="search-result-item flex items-center p-3 rounded-lg hover:bg-yellow-50 transition">
                <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{{ pokemon.id }}.png"
                     alt="{{ pokemon.display_name }}"
                     class="w-12 h-12 object-contain mr-3">
                <div>
                    <p class="text-sm text-gray-500 font-mono">#{{ '%03d'|format(pokemon.id) }}</p>
                    <p class="font-semibold text-gray-800">{{ pokemon.display_name }}</p>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</div>
{% elif request.args.get('q') %}
<div class="bg-white rounded-lg shadow-lg mt-2 max-w-lg mx-auto p-4">
    <p class="text-gray-600 text-center">No Pokémon found matching "{{ request.args.get('q') }}"</p>
</div>
{% endif %}
```

**Step 5: Run test to verify it passes**

```bash
pytest tests/test_routes.py -v
```

Expected: PASS (7 tests)

**Step 6: Commit search functionality**

```bash
git add app/routes/main.py app/templates/components/search_results.html tests/test_routes.py
git commit -m "feat: add HTMX-powered search functionality"
```

---

## Task 9: Error Handling and 404 Page

**Files:**
- Create: `claude-code/pokedex-flask-htmx/app/templates/errors/404.html`
- Create: `claude-code/pokedex-flask-htmx/app/templates/errors/500.html`
- Modify: `claude-code/pokedex-flask-htmx/app/__init__.py`

**Step 1: Create 404 error template**

Create: `claude-code/pokedex-flask-htmx/app/templates/errors/404.html`

```html
{% extends "base.html" %}

{% block title %}404 - Pokémon Not Found{% endblock %}

{% block content %}
<div class="text-center py-16">
    <div class="mb-8">
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/54.png"
             alt="Psyduck"
             class="mx-auto w-48 h-48 object-contain opacity-50">
    </div>

    <h1 class="text-6xl font-bold text-gray-800 mb-4">404</h1>
    <h2 class="text-3xl font-bold text-gray-700 mb-4">Pokémon Not Found!</h2>
    <p class="text-xl text-gray-600 mb-8">
        This Pokémon seems to have fled!
    </p>

    <div class="space-x-4">
        <a href="{{ url_for('main.index') }}"
           class="inline-block bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition">
            Go Home
        </a>
        <a href="{{ url_for('main.pokemon_list') }}"
           class="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
            View All Pokémon
        </a>
    </div>
</div>
{% endblock %}
```

**Step 2: Create 500 error template**

Create: `claude-code/pokedex-flask-htmx/app/templates/errors/500.html`

```html
{% extends "base.html" %}

{% block title %}500 - Server Error{% endblock %}

{% block content %}
<div class="text-center py-16">
    <div class="mb-8">
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/79.png"
             alt="Slowpoke"
             class="mx-auto w-48 h-48 object-contain opacity-50">
    </div>

    <h1 class="text-6xl font-bold text-gray-800 mb-4">500</h1>
    <h2 class="text-3xl font-bold text-gray-700 mb-4">Oops! Something Went Wrong</h2>
    <p class="text-xl text-gray-600 mb-8">
        Our server is feeling a bit slow... like Slowpoke!
    </p>

    <a href="{{ url_for('main.index') }}"
       class="inline-block bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition">
        Go Home
    </a>
</div>
{% endblock %}
```

**Step 3: Register error handlers**

Modify: `claude-code/pokedex-flask-htmx/app/__init__.py`

```python
import os
from flask import Flask, render_template
from app.config import config


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default config
        env = os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config.get(env, config['default']))
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    return app
```

**Step 4: Test error pages manually**

```bash
# Start the dev server
python run.py
# Visit http://localhost:5000/pokemon/notapokemon to see 404 page
```

**Step 5: Commit error handling**

```bash
git add app/templates/errors/ app/__init__.py
git commit -m "feat: add custom 404 and 500 error pages"
```

---

## Task 10: Docker Configuration

**Files:**
- Create: `claude-code/pokedex-flask-htmx/Dockerfile`
- Create: `claude-code/pokedex-flask-htmx/docker-compose.yml`
- Create: `claude-code/pokedex-flask-htmx/.dockerignore`

**Step 1: Create Dockerfile**

```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "run.py"]
```

**Step 2: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY:-change-this-secret-key}
    restart: unless-stopped
```

**Step 3: Create .dockerignore**

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.pytest_cache/
.coverage
htmlcov/
.git/
.gitignore
.vscode/
.idea/
*.swp
*.swo
*~
.env
.env.local
instance/
docs/
tests/
README.md
BUILD_LOG.md
PROJECT_IDEA.md
requirements-dev.txt
pytest.ini
```

**Step 4: Test Docker build**

```bash
docker-compose build
```

Expected: Build completes successfully

**Step 5: Test Docker run**

```bash
docker-compose up
# Visit http://localhost:5000 to verify app works
# Ctrl+C to stop
docker-compose down
```

**Step 6: Commit Docker configuration**

```bash
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "feat: add Docker configuration for deployment"
```

---

## Task 11: Documentation and README

**Files:**
- Create: `claude-code/pokedex-flask-htmx/DEPLOYMENT.md`
- Modify: `claude-code/pokedex-flask-htmx/README.md`

**Step 1: Update README with complete project info**

Modify: `claude-code/pokedex-flask-htmx/README.md`

```markdown
# Pokédex Web App

A modern web-based Pokédex application built with Flask, HTMX, and Tailwind CSS. Browse and search through all 151 Generation 1 Pokémon with detailed information including stats, types, abilities, and more.

## Features

- 🔍 **Search**: Find Pokémon by name or number
- 📋 **Browse**: View all 151 Gen 1 Pokémon in a grid layout
- 📊 **Details**: See comprehensive stats, types, abilities, height, and weight
- 📱 **Responsive**: Works seamlessly on mobile and desktop
- ⚡ **HTMX**: Dynamic search without writing JavaScript
- 🎨 **Tailwind CSS**: Modern, clean design
- 🐳 **Docker**: Easy deployment with Docker Compose

## Tech Stack

- **Backend**: Flask 3.0
- **Frontend**: HTMX 1.9 + Tailwind CSS 3.x
- **API**: [PokeAPI](https://pokeapi.co)
- **Testing**: pytest with coverage
- **Deployment**: Docker + Docker Compose

## Quick Start

### Prerequisites

- Python 3.12+
- pip

### Local Development

1. Clone the repository:
```bash
git clone <repo-url>
cd pokedex-flask-htmx
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Run the application:
```bash
python run.py
```

5. Open browser to `http://localhost:5000`

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Open browser to `http://localhost:5000`

## Testing

Run tests with coverage:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Check coverage report:
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Project Structure

```
pokedex-flask-htmx/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models/              # Data models
│   │   └── pokemon.py
│   ├── routes/              # Flask routes
│   │   └── main.py
│   ├── services/            # External API services
│   │   └── pokeapi.py
│   ├── static/              # Static files
│   │   └── css/
│   │       └── styles.css
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── pokemon_list.html
│       ├── pokemon_detail.html
│       ├── components/
│       └── errors/
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── run.py                  # Application entry point
```

## Development

### Code Quality

Format code with black:
```bash
black app/ tests/
```

Lint with flake8:
```bash
flake8 app/ tests/
```

### Environment Variables

Create a `.env` file for local development:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
PORT=5000
```

## License

MIT License - feel free to use this project for learning and development.

## Acknowledgments

- Pokémon data from [PokeAPI](https://pokeapi.co)
- Sprites from [PokeAPI/sprites](https://github.com/PokeAPI/sprites)
- Built as a learning project for Flask + HTMX
```

**Step 2: Create deployment guide**

Create: `claude-code/pokedex-flask-htmx/DEPLOYMENT.md`

```markdown
# Deployment Guide

This guide covers deploying the Pokédex application to production.

## Docker Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+

### Steps

1. Clone the repository:
```bash
git clone <repo-url>
cd pokedex-flask-htmx
```

2. Set environment variables:
```bash
# Create .env file
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" > .env
echo "FLASK_ENV=production" >> .env
```

3. Build and start:
```bash
docker-compose up -d --build
```

4. Verify deployment:
```bash
docker-compose ps
curl http://localhost:5000
```

5. View logs:
```bash
docker-compose logs -f
```

6. Stop application:
```bash
docker-compose down
```

## Production Considerations

### Security

1. **Secret Key**: Always use a strong, random secret key:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

2. **HTTPS**: Use a reverse proxy (nginx, Caddy) for HTTPS

3. **Environment Variables**: Never commit `.env` files

### Performance

1. **Caching**: Consider adding Redis for API response caching

2. **CDN**: Serve static assets via CDN in production

3. **Gunicorn**: Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Monitoring

1. **Logging**: Configure structured logging

2. **Health Checks**: Add `/health` endpoint

3. **Metrics**: Consider Prometheus + Grafana

## Cloud Platforms

### Deploy to Railway

1. Install Railway CLI
2. Run `railway init`
3. Run `railway up`

### Deploy to Render

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python run.py`

### Deploy to Heroku

1. Create `Procfile`:
```
web: gunicorn "app:create_app()"
```

2. Deploy:
```bash
heroku create
git push heroku main
```

## Environment Variables for Production

```
FLASK_ENV=production
SECRET_KEY=<your-secret-key>
PORT=5000
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs web
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8080:5000"
```

### API rate limiting
PokeAPI has rate limits. Consider implementing caching for production use.
```

**Step 3: Commit documentation**

```bash
git add README.md DEPLOYMENT.md
git commit -m "docs: add comprehensive README and deployment guide"
```

---

## Task 12: Final Testing and Quality Assurance

**Files:**
- Create: `claude-code/pokedex-flask-htmx/tests/test_integration.py`

**Step 1: Create integration tests**

Create: `claude-code/pokedex-flask-htmx/tests/test_integration.py`

```python
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client with real API calls."""
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_full_user_journey(client):
    """Test complete user flow from index to detail."""
    # 1. Visit homepage
    response = client.get('/')
    assert response.status_code == 200

    # 2. Click to view all pokemon
    response = client.get('/pokemon')
    assert response.status_code == 200

    # 3. Search for a specific pokemon
    response = client.get('/search?q=pikachu')
    assert response.status_code == 200

    # 4. View pokemon detail (if API is available)
    # Note: This test requires actual API connectivity
    # In CI/CD, you might want to mock this
    try:
        response = client.get('/pokemon/pikachu')
        assert response.status_code in [200, 404]  # 404 if API is down
    except Exception:
        pytest.skip("API not available for integration test")


def test_error_handling(client):
    """Test that errors are handled gracefully."""
    # Test 404
    response = client.get('/pokemon/notarealmon')
    assert response.status_code == 404

    # Test invalid route
    response = client.get('/invalid/route')
    assert response.status_code == 404
```

**Step 2: Run full test suite**

```bash
pytest -v --cov=app --cov-report=term --cov-report=html
```

Expected: All tests pass with >80% coverage

**Step 3: Run linting**

```bash
flake8 app/ tests/ --max-line-length=120 --extend-ignore=E203
```

Expected: No critical errors

**Step 4: Format code**

```bash
black app/ tests/ --line-length=120
```

**Step 5: Manual testing checklist**

Test the following manually:
- [ ] Homepage loads with featured pokemon
- [ ] All pokemon list displays 151 pokemon
- [ ] Search by name works (try "pikachu")
- [ ] Search by number works (try "25")
- [ ] Pokemon detail page shows all info
- [ ] Navigation between pokemon works
- [ ] Error pages display correctly
- [ ] Mobile responsive design works
- [ ] Docker build and run successful

**Step 6: Commit integration tests**

```bash
git add tests/test_integration.py
git commit -m "test: add integration tests and QA checklist"
```

---

## Summary

This plan creates a complete, production-ready Pokédex application with:

✅ **12 Tasks** - Bite-sized, test-driven implementation
✅ **Flask Backend** - Clean architecture with services and models
✅ **HTMX Frontend** - No JavaScript required for interactivity
✅ **Tailwind CSS** - Modern, responsive design
✅ **PokeAPI Integration** - Full Gen 1 Pokemon data
✅ **Test Coverage** - Unit, integration, and manual tests
✅ **Docker Ready** - Easy deployment
✅ **Documentation** - README and deployment guide

**Total Estimated Time**: 2-3 hours for an engineer following this plan

**Execution Strategy**: Use `executing-plans` skill to implement tasks in batches with review checkpoints.
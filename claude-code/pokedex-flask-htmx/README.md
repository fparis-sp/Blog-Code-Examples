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

- Python 3.11+
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

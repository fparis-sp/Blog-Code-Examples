# Pokédex Web - Especificaciones del Proyecto

> **Documento de Requisitos** para construcción con Claude Code
> **Fecha:** 2025-11-17
> **Tutorial:** Post 3 - Serie Claude Code (franciscoparis.com)

---

## 📋 Descripción del Proyecto

Construir una **aplicación web de Pokédex** que permita buscar y explorar información de Pokémon usando la API pública de PokeAPI.

**Objetivo educativo:** Aprender a usar Claude Code's `writing-plans` y `executing-plans` skills para construir un proyecto completo desde cero.

---

## 🎯 Features Requeridas

### Funcionalidades Core (MVP)

#### 1. Búsqueda de Pokémon
- Input de búsqueda por nombre o número
- Búsqueda en tiempo real sin recargar la página
- Mostrar resultados mientras el usuario escribe

#### 2. Lista de Pokémon
- Mostrar los primeros 151 Pokémon (Generación 1)
- Cards visuales con:
  - Sprite/imagen del Pokémon
  - Nombre
  - Número de Pokédex
  - Tipos (ej: Fire, Water, Grass)

#### 3. Vista de Detalle
- Al hacer click en un Pokémon, mostrar página de detalle con:
  - **Stats principales:** HP, Attack, Defense, Speed
  - **Tipos:** Badges con colores (Fire=rojo, Water=azul, etc.)
  - **Habilidades:** Lista de abilities
  - **Sprites:** Front y back view
  - **Información básica:** Altura, peso

#### 4. Diseño Responsive
- Funcional en móvil, tablet y desktop
- Grid adaptativo (1 columna en móvil, 3+ en desktop)

---

## 🛠️ Stack Tecnológico Requerido

### Backend
- **Framework:** Flask 3.0+ (Python web framework)
- **API Client:** `requests` library para consumir PokeAPI

### Frontend
- **HTML Engine:** Jinja2 (templating de Flask)
- **Interactividad:** HTMX 1.9+ (búsqueda sin JavaScript)
- **Styling:** Tailwind CSS 3 (vía CDN, sin build step)

### Testing
- **Framework:** pytest
- **Coverage:** pytest-cov
- **Mínimo:** 80% coverage en código crítico

### API Externa
- **Servicio:** PokeAPI v2 (https://pokeapi.co/api/v2/)
- **Autenticación:** No requerida (API pública)
- **Endpoints a usar:**
  - `GET /pokemon/{id or name}` - Detalles de un Pokémon
  - `GET /pokemon?limit=151` - Lista de Pokémon Gen 1

### Deployment
- **Containerización:** Dockerfile (multi-stage build)
- **Platform:** Railway o Render (free tier)
- **Production server:** Gunicorn

---

## 📁 Estructura de Proyecto Esperada

```
pokedex-flask-htmx/
├── app/
│   ├── __init__.py           # Flask application factory
│   ├── routes.py             # Route handlers
│   ├── services.py           # PokeAPI client
│   ├── templates/
│   │   ├── base.html         # Base template con Tailwind + HTMX
│   │   ├── index.html        # Homepage con lista y búsqueda
│   │   ├── pokemon.html      # Página de detalle
│   │   └── partials/
│   │       └── search_results.html  # Partial para HTMX
│   └── static/
│       └── (opcional: favicon, images)
│
├── tests/
│   ├── conftest.py           # Pytest fixtures
│   ├── test_services.py      # Tests del API client
│   └── test_routes.py        # Tests de rutas/integration
│
├── requirements.txt          # Python dependencies
├── Dockerfile                # Multi-stage build
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # Setup y deployment instructions
```

---

## 🎨 Especificaciones de Diseño

### Paleta de Colores
- **Background:** Dark theme (gris oscuro #1a1a1a o similar)
- **Cards:** Gris medio (#2d2d2d) con hover effect
- **Accent:** Amarillo Pokémon (#ffcb05) para títulos/highlights
- **Text:** Blanco/gris claro para legibilidad

### Type Badges (colores por tipo)
```
Fire:     #F08030 (naranja-rojo)
Water:    #6890F0 (azul)
Grass:    #78C850 (verde)
Electric: #F8D030 (amarillo)
Normal:   #A8A878 (beige)
Fighting: #C03028 (rojo oscuro)
Flying:   #A890F0 (lavanda)
Poison:   #A040A0 (púrpura)
Ground:   #E0C068 (marrón claro)
Rock:     #B8A038 (marrón)
Bug:      #A8B820 (verde oliva)
Ghost:    #705898 (morado)
Steel:    #B8B8D0 (gris)
Psychic:  #F85888 (rosa)
Ice:      #98D8D8 (cyan)
Dragon:   #7038F8 (azul-púrpura)
Dark:     #705848 (marrón oscuro)
Fairy:    #EE99AC (rosa pastel)
```

### Tipografía
- **Headings:** Font bold, tamaño grande
- **Body:** Font regular, tamaño legible (16px+)
- **Fuente:** System fonts (sin custom fonts para simplicidad)

---

## 🔧 Requisitos Técnicos

### Python
- **Versión:** Python 3.11+
- **Virtual environment:** Recomendado (venv)

### Dependencias Principales
```txt
Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0
pytest==7.4.3
pytest-cov==4.1.0
python-dotenv==1.0.0  # Para manejar .env files
```

### Environment Variables
```bash
# .env.example
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

---

## 📡 Integración con PokeAPI

### Endpoints a consumir

#### 1. Obtener detalles de un Pokémon
```http
GET https://pokeapi.co/api/v2/pokemon/{id or name}
```

**Respuesta relevante:**
```json
{
  "id": 25,
  "name": "pikachu",
  "height": 4,
  "weight": 60,
  "types": [
    {
      "slot": 1,
      "type": {
        "name": "electric"
      }
    }
  ],
  "abilities": [
    {
      "ability": {
        "name": "static"
      }
    }
  ],
  "stats": [
    {
      "base_stat": 35,
      "stat": {
        "name": "hp"
      }
    },
    // ... más stats
  ],
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/.../pikachu.png"
  }
}
```

#### 2. Obtener lista de Pokémon
```http
GET https://pokeapi.co/api/v2/pokemon?limit=151&offset=0
```

**Respuesta:**
```json
{
  "count": 1302,
  "results": [
    {
      "name": "bulbasaur",
      "url": "https://pokeapi.co/api/v2/pokemon/1/"
    },
    // ... más pokémon
  ]
}
```

### Manejo de Errores
- **Timeout:** 10 segundos máximo por request
- **404 Not Found:** Mostrar mensaje amigable "Pokémon no encontrado"
- **500 Server Error:** Mensaje "Error conectando con PokeAPI, intenta de nuevo"
- **Network Error:** Mensaje "Sin conexión a internet"

### Performance
- **Cache opcional:** Considerar cachear resultados en memoria para mejorar velocidad
- **Rate limiting:** PokeAPI no tiene límite estricto, pero ser respetuoso (no spam)

---

## 🧪 Especificaciones de Testing

### Cobertura Mínima
- **Services (PokeAPI client):** 90%+ coverage
- **Routes:** 80%+ coverage
- **Overall:** 80%+ coverage

### Tipos de Tests

#### Unit Tests (test_services.py)
```python
def test_get_pokemon_by_name():
    """Should fetch Pikachu by name"""
    client = PokeAPIClient()
    pokemon = client.get_pokemon("pikachu")
    assert pokemon is not None
    assert pokemon["name"] == "pikachu"
    assert pokemon["id"] == 25

def test_get_pokemon_not_found():
    """Should return None for invalid pokemon"""
    client = PokeAPIClient()
    pokemon = client.get_pokemon("fakemon12345")
    assert pokemon is None
```

#### Integration Tests (test_routes.py)
```python
def test_homepage_loads(client):
    """Should load homepage with pokemon list"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Pok" in response.data  # "Pokédex" en título

def test_search_endpoint(client):
    """Should return search results via HTMX"""
    response = client.get("/search?q=pikachu")
    assert response.status_code == 200
    assert b"pikachu" in response.data.lower()
```

---

## 🚀 Deployment Requirements

### Dockerfile Specs
- **Base image:** python:3.11-slim
- **Build type:** Multi-stage (builder + runtime)
- **Port:** 5000
- **Server:** Gunicorn con 4 workers
- **Health check:** Endpoint `/` debe responder 200

### Railway/Render Configuration
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn --bind 0.0.0.0:5000 'app:create_app()'`
- **Environment variables:** Configurar `SECRET_KEY` en platform

---

## ✅ Criterios de Éxito

### Funcional
- [ ] Búsqueda funciona sin recargar página (HTMX)
- [ ] Muestra primeros 151 Pokémon en homepage
- [ ] Click en card abre página de detalle correcta
- [ ] Type badges tienen colores correctos
- [ ] Responsive en mobile (breakpoint 768px)

### Técnico
- [ ] Tests pasan con 80%+ coverage
- [ ] Flask app inicia sin errores
- [ ] Dockerfile build exitoso
- [ ] Deploy funciona en Railway/Render
- [ ] No hay errores en browser console

### UX
- [ ] Loading states visibles (spinner o mensaje)
- [ ] Error messages claros y amigables
- [ ] Navegación intuitiva (back to home, etc.)
- [ ] Imágenes cargan correctamente

---

## 🎓 Notas para el Desarrollador

### Nivel de Dificultad
**Intermedio** - Requiere conocimientos básicos de:
- Python y Flask
- HTML/CSS
- HTTP requests
- Git básico

### Tiempo Estimado
- **Con Claude Code:** 30-60 minutos
- **Manual (sin AI):** 4-6 horas

### Extensiones Futuras (fuera de MVP)
- Filtros por tipo (Fire, Water, etc.)
- Ordenamiento (por nombre, número, stats)
- Sistema de favoritos (localStorage)
- Comparación de 2 Pokémon
- Gráficos de stats (Chart.js)
- Autenticación y equipos personalizados
- Base de datos propia (PostgreSQL)

---

## 📚 Referencias Útiles

### Documentación
- [PokeAPI Docs](https://pokeapi.co/docs/v2)
- [Flask Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [HTMX Docs](https://htmx.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Ejemplos
- [PokeAPI Examples](https://github.com/PokeAPI/pokeapi#wrapper-libraries)
- [Flask + HTMX Tutorial](https://htmx.org/examples/)

---

## 🎯 Prompt para Claude Code

Copia este prompt y úsalo con `writing-plans` skill:

```
Usa writing-plans para crear un plan de implementación completo para una Pokédex web con Flask + HTMX.

Requisitos:
- Backend: Flask 3.0 con application factory pattern
- Frontend: HTMX para búsqueda dinámica + Tailwind CSS
- API: Integración con PokeAPI v2 (obtener Pokémon por nombre/ID y lista Gen 1)
- Features: Búsqueda en tiempo real, lista de 151 Pokémon, vista de detalle con stats/tipos/habilidades
- Testing: pytest con 80%+ coverage
- Deploy: Dockerfile multi-stage + Railway/Render ready

El proyecto debe seguir la estructura definida en REQUIREMENTS.md y cumplir todos los criterios de éxito.
```

---

**Este documento es el punto de partida oficial del tutorial. Todo lo que necesitas está aquí. ¡Manos a la obra!** 🚀

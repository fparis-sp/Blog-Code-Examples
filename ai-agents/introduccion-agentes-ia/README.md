# Introducción a Agentes de IA: Del Concepto a la Práctica

Código completo del post: **[Introducción a Agentes de IA](https://franciscoparis.com/es/blog/introduccion-agentes-ia)**

## 📖 Descripción

Este directorio contiene todos los ejemplos de código del post, desde agentes simples con OpenAI hasta agentes escalables con LangGraph. Aprenderás a construir agentes que razonan, deciden y actúan de forma autónoma usando el patrón ReAct.

## 🎯 Qué aprenderás

1. **Agente Simple** - Razonamiento básico + herramientas (calculadora, reloj)
2. **Agente con API Real** - Integración con PokeAPI para consultar datos de Pokémon
3. **Escalado con LangGraph** - Framework de producción para agentes complejos
4. **Chat Interactivo** - Interfaz de terminal con historial conversacional

## 📁 Archivos

| Archivo | Descripción | Complejidad |
|---------|-------------|-------------|
| `01_simple_agent.py` | Agente básico con OpenAI function calling | ⭐ Beginner |
| `02_pokemon_agent.py` | Agente con PokeAPI + razonamiento multi-paso | ⭐⭐ Intermediate |
| `03_langgraph_agent.py` | Agente con LangGraph (grafo de estados) | ⭐⭐⭐ Advanced |
| `04_interactive_chat.py` | Chat interactivo en terminal con historial | ⭐⭐ Intermediate |
| `requirements.txt` | Dependencias Python | - |
| `.env.example` | Template de variables de entorno | - |

## 🚀 Quick Start

### 1. Instala dependencias

```bash
# Crea entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instala paquetes
pip install -r requirements.txt
```

### 2. Configura tu API key de OpenAI

```bash
# Copia el template
cp .env.example .env

# Edita .env y añade tu API key
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### 3. Ejecuta los ejemplos

```bash
# Agente simple (ejemplos predefinidos)
python 01_simple_agent.py

# Agente con Pokemon (ejemplos predefinidos)
python 02_pokemon_agent.py

# Agente con LangGraph (ejemplos predefinidos)
python 03_langgraph_agent.py

# Chat interactivo (¡pruébalo tú mismo!)
python 04_interactive_chat.py
```

## 💡 Ejemplos de Uso

### Agente Simple (`01_simple_agent.py`)

```python
from simple_agent import run_agent

# El agente puede usar calculadora y reloj
result = run_agent("¿Cuánto es 25 * 4 + 10?")
print(result)  # "El resultado es 110"

result = run_agent("¿Qué hora es?")
print(result)  # "Son las 14:30:00 UTC"
```

### Agente Pokemon (`02_pokemon_agent.py`)

```python
from pokemon_agent import run_agent

# El agente consulta PokeAPI y hace cálculos
result = run_agent("¿Cuánto pesan juntos Pikachu y Charizard?")
print(result)
# Output: "Juntos pesan 96.5 kg"
# (Agente ejecutó: get_pokemon_info("pikachu") + get_pokemon_info("charizard") + calculate)
```

### Agente LangGraph (`03_langgraph_agent.py`)

```python
from langgraph_agent import create_agent_graph

app = create_agent_graph()

# Streaming de resultados
inputs = {"messages": [("user", "¿Cuánto pesa Pikachu en kg?")]}
for output in app.stream(inputs):
    print(output)
```

### Chat Interactivo (`04_interactive_chat.py`)

```bash
# Ejecuta el chat
python 04_interactive_chat.py

# Ejemplo de sesión:
Tú: ¿Cuánto pesa Pikachu?
  🔧 Ejecutando: get_pokemon_info({'pokemon_name': 'pikachu'})

🤖 Agente: Pikachu pesa 6.0 kilogramos.

Tú: ¿Y cuánto pesa Charizard?
  🔧 Ejecutando: get_pokemon_info({'pokemon_name': 'charizard'})

🤖 Agente: Charizard pesa 90.5 kilogramos.

Tú: ¿Cuánto pesan juntos?
  🔧 Ejecutando: calculate({'expression': '6.0 + 90.5'})

🤖 Agente: Juntos pesan 96.5 kilogramos.

Tú: /salir
👋 ¡Hasta luego!
```

**Comandos disponibles:**
- `/ayuda` - Muestra ejemplos de preguntas
- `/limpiar` - Limpia el historial de conversación
- `/salir` - Salir del chat

## 🔑 Variables de Entorno

Crea un archivo `.env` en este directorio:

```bash
# OpenAI API Key (obligatoria)
OPENAI_API_KEY=sk-tu-api-key

# Opcional: Modelo a usar (por defecto: gpt-4)
OPENAI_MODEL=gpt-4

# Opcional: Temperatura (por defecto: 0)
OPENAI_TEMPERATURE=0
```

**⚠️ Nota:** Los ejemplos generan costos reales en la API de OpenAI.

Costos estimados (con gpt-4):
- Agente simple: ~$0.01 por ejecución
- Agente Pokemon: ~$0.02 por ejecución
- Agente LangGraph: ~$0.03 por ejecución

## 📦 Dependencias

- `openai>=1.0.0` - Cliente oficial de OpenAI
- `requests>=2.31.0` - Para llamadas HTTP (PokeAPI)
- `python-dotenv>=1.0.0` - Manejo de variables de entorno
- `langchain>=0.1.0` - Framework para LLM apps
- `langgraph>=0.0.20` - Orchestration para agentes
- `langchain-openai>=0.0.5` - Integración OpenAI + LangChain

**Versión de Python:** 3.12 o superior

## 🎓 Conceptos Clave

### Patrón ReAct (Reasoning + Acting)

```
1. Thought (Razonamiento): ¿Qué necesito hacer?
2. Action (Acción): Ejecutar herramienta X
3. Observation (Observación): Resultado = Y
4. Repeat: Volver al paso 1 hasta completar
```

### Componentes de un Agente

- **LLM (Brain):** Toma decisiones y razona
- **Tools (Hands):** Ejecutan acciones (API calls, cálculos, DB queries)
- **Loop (Coordinator):** Ciclo que conecta razonamiento → acción → razonamiento

### OpenAI Function Calling

Permite que el LLM:
1. Decida qué función llamar
2. Genere los parámetros correctos
3. Procese el resultado

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calcula expresiones matemáticas",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                }
            }
        }
    }
]
```

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'openai'`
```bash
pip install -r requirements.txt
```

### Error: `openai.error.AuthenticationError`
```bash
# Verifica que .env tenga tu API key
cat .env  # Linux/Mac
type .env  # Windows
```

### Error: `rate_limit_exceeded`
```bash
# Espera 20 segundos y reintenta
# O usa un modelo más barato: gpt-3.5-turbo
```

## 📚 Recursos Adicionales

- **Post del Blog:** [Introducción a Agentes de IA](https://franciscoparis.com/es/blog/introduccion-agentes-ia)
- **OpenAI Function Calling:** [Docs oficiales](https://platform.openai.com/docs/guides/function-calling)
- **LangGraph:** [Documentación](https://langchain-ai.github.io/langgraph/)
- **PokeAPI:** [API Reference](https://pokeapi.co/docs/v2)
- **Paper ReAct:** [Arxiv](https://arxiv.org/abs/2210.03629)

## 🤝 Contribuciones

¿Encontraste un bug o tienes una mejora?
1. Abre un issue en el repo principal
2. Envía un pull request con la solución

## 📄 Licencia

MIT License - Código libre para usar en tus proyectos.

---

**Última actualización:** Noviembre 2025

"""
Agente con PokeAPI - Consultas sobre Pokémon

Este ejemplo muestra un agente más avanzado que puede:
1. Consultar información de Pokémon desde PokeAPI
2. Comparar Pokémon
3. Hacer cálculos con datos obtenidos

El agente demuestra razonamiento multi-paso y uso de APIs externas.
"""

import json
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ========== HERRAMIENTAS (TOOLS) ==========

def get_pokemon_info(pokemon_name: str) -> str:
    """
    Obtiene información de un Pokémon desde PokeAPI.

    Args:
        pokemon_name: Nombre del Pokémon en inglés (ej: "pikachu", "charizard")

    Returns:
        JSON string con información del Pokémon o mensaje de error
    """
    try:
        pokemon_name = pokemon_name.lower().strip()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extraer información relevante
        pokemon_info = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "height": data["height"] / 10,  # Convertir decímetros a metros
            "weight": data["weight"] / 10,  # Convertir hectogramos a kilogramos
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"][:3]],  # Top 3
            "base_experience": data.get("base_experience", "Unknown")
        }

        return json.dumps(pokemon_info, ensure_ascii=False)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: Pokémon '{pokemon_name}' no encontrado. Verifica el nombre."
        return f"Error HTTP: {str(e)}"
    except Exception as e:
        return f"Error al consultar PokeAPI: {str(e)}"


def compare_pokemon(pokemon1: str, pokemon2: str) -> str:
    """
    Compara dos Pokémon.

    Args:
        pokemon1: Nombre del primer Pokémon
        pokemon2: Nombre del segundo Pokémon

    Returns:
        Comparación estructurada de ambos Pokémon
    """
    info1 = get_pokemon_info(pokemon1)
    info2 = get_pokemon_info(pokemon2)

    # Verificar si hubo errores
    if "Error" in info1 or "Error" in info2:
        return f"No se pudo comparar. {info1} {info2}"

    data1 = json.loads(info1)
    data2 = json.loads(info2)

    comparison = {
        "pokemon_1": data1,
        "pokemon_2": data2,
        "weight_difference_kg": abs(data1["weight"] - data2["weight"]),
        "height_difference_m": abs(data1["height"] - data2["height"]),
        "heavier": data1["name"] if data1["weight"] > data2["weight"] else data2["name"],
        "taller": data1["name"] if data1["height"] > data2["height"] else data2["name"]
    }

    return json.dumps(comparison, ensure_ascii=False, indent=2)


def calculate(expression: str) -> str:
    """Calcula expresiones matemáticas simples."""
    try:
        result = eval(expression)
        return str(float(result))
    except Exception as e:
        return f"Error: {str(e)}"


# ========== DEFINICIÓN DE HERRAMIENTAS PARA OPENAI ==========

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_pokemon_info",
            "description": "Obtiene información detallada de un Pokémon desde PokeAPI. Incluye: nombre, ID, altura, peso, tipos y habilidades.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pokemon_name": {
                        "type": "string",
                        "description": "Nombre del Pokémon en inglés (ej: 'pikachu', 'charizard', 'bulbasaur')"
                    }
                },
                "required": ["pokemon_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_pokemon",
            "description": "Compara dos Pokémon mostrando diferencias en peso, altura y otros atributos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pokemon1": {
                        "type": "string",
                        "description": "Nombre del primer Pokémon"
                    },
                    "pokemon2": {
                        "type": "string",
                        "description": "Nombre del segundo Pokémon"
                    }
                },
                "required": ["pokemon1", "pokemon2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calcula expresiones matemáticas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Expresión matemática (ej: '6 + 90.5')"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


available_functions = {
    "get_pokemon_info": get_pokemon_info,
    "compare_pokemon": compare_pokemon,
    "calculate": calculate
}


# ========== LÓGICA DEL AGENTE ==========

def run_agent(user_message: str, max_iterations: int = 15, model: str = "gpt-4") -> str:
    """
    Ejecuta el agente Pokemon con un mensaje del usuario.

    Args:
        user_message: Pregunta sobre Pokémon
        max_iterations: Máximo de iteraciones
        model: Modelo de OpenAI

    Returns:
        Respuesta final del agente
    """
    messages = [{"role": "user", "content": user_message}]

    print(f"\n{'='*70}")
    print(f"USUARIO: {user_message}")
    print(f"{'='*70}\n")

    for iteration in range(max_iterations):
        print(f"--- Iteración {iteration + 1} ---")

        # REASONING: LLM decide qué hacer
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Si no hay tool calls, terminamos
        if not tool_calls:
            final_response = response_message.content
            print(f"\n✅ RESPUESTA FINAL: {final_response}\n")
            return final_response

        messages.append(response_message)

        # ACTION + OBSERVATION: Ejecutar herramientas
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"🔧 ACTION: {function_name}({function_args})")

            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)

            print(f"👁️ OBSERVATION: {function_response[:200]}...")

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response)
            })

    return "⚠️ El agente excedió el número máximo de iteraciones."


# ========== EJEMPLOS DE USO ==========

if __name__ == "__main__":
    # Ejemplo 1: Información de un Pokémon
    print("\n" + "🎯 EJEMPLO 1: Información de Pikachu " + "\n")
    result = run_agent("¿Cuánto pesa Pikachu en kilogramos?")

    # Ejemplo 2: Comparación de Pokémon
    print("\n" + "🎯 EJEMPLO 2: Comparación " + "\n")
    result = run_agent("¿Quién es más alto, Charizard o Blastoise?")

    # Ejemplo 3: Razonamiento multi-paso (consulta + cálculo)
    print("\n" + "🎯 EJEMPLO 3: Multi-paso con cálculo " + "\n")
    result = run_agent("¿Cuánto pesan juntos Pikachu y Charizard?")

    # Ejemplo 4: Consulta compleja
    print("\n" + "🎯 EJEMPLO 4: Consulta compleja " + "\n")
    result = run_agent("Dame las habilidades de Pikachu y compara su peso con Raichu")

    print("\n✅ Todos los ejemplos completados!")
    print("\n💡 Tip: Prueba tus propias preguntas sobre Pokémon!")

"""
Chat Interactivo con Agente de IA

Este ejemplo muestra un chat interactivo en terminal donde:
1. El usuario puede hacer preguntas en tiempo real
2. El agente mantiene historial de conversación
3. Se pueden usar todas las herramientas (Pokemon + calculadora)
4. Comandos especiales: /ayuda, /limpiar, /salir

Perfecto para experimentar y entender cómo funciona un agente conversacional.
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
    "calculate": calculate
}


# ========== SISTEMA DE CHAT INTERACTIVO ==========

class InteractiveAgent:
    """Agente conversacional con historial de mensajes"""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente útil especializado en Pokémon y cálculos matemáticos. "
                    "Responde de forma amigable y concisa. Usa las herramientas cuando sea necesario. "
                    "Si el usuario pregunta sobre un Pokémon, usa get_pokemon_info. "
                    "Si necesitas hacer cálculos, usa calculate."
                )
            }
        ]

    def chat(self, user_message: str, max_iterations: int = 10) -> str:
        """
        Procesa un mensaje del usuario y retorna la respuesta del agente.

        Args:
            user_message: Pregunta o comentario del usuario
            max_iterations: Máximo de iteraciones para evitar loops infinitos

        Returns:
            Respuesta del agente
        """
        # Agregar mensaje del usuario al historial
        self.messages.append({"role": "user", "content": user_message})

        for iteration in range(max_iterations):
            # REASONING: LLM decide qué hacer
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Si no hay tool calls, terminamos
            if not tool_calls:
                final_response = response_message.content
                # Agregar respuesta al historial
                self.messages.append({"role": "assistant", "content": final_response})
                return final_response

            # Agregar respuesta del LLM al historial
            self.messages.append(response_message)

            # ACTION + OBSERVATION: Ejecutar herramientas
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Mostrar acción ejecutada (para que el usuario vea qué hace el agente)
                print(f"  🔧 Ejecutando: {function_name}({function_args})")

                function_to_call = available_functions[function_name]
                function_response = function_to_call(**function_args)

                # Agregar resultado al historial
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response)
                })

        return "⚠️ El agente excedió el número máximo de iteraciones."

    def clear_history(self):
        """Limpia el historial de conversación (excepto el system message)"""
        self.messages = [self.messages[0]]  # Mantener solo el system message
        print("🗑️  Historial limpiado\n")


# ========== INTERFAZ DE TERMINAL ==========

def print_banner():
    """Muestra el banner de bienvenida"""
    print("\n" + "="*70)
    print("🤖 CHAT INTERACTIVO CON AGENTE DE IA")
    print("="*70)
    print("\n💬 Pregúntame sobre Pokémon o pídeme que haga cálculos")
    print("\n📋 Comandos disponibles:")
    print("   /ayuda   - Muestra esta ayuda")
    print("   /limpiar - Limpia el historial de conversación")
    print("   /salir   - Salir del chat")
    print("\n" + "="*70 + "\n")


def print_help():
    """Muestra la ayuda"""
    print("\n📚 AYUDA - ¿Qué puedes hacer?")
    print("="*70)
    print("\n🔹 Consultar Pokémon:")
    print("   • ¿Cuánto pesa Pikachu?")
    print("   • Dame información sobre Charizard")
    print("   • ¿Qué habilidades tiene Bulbasaur?")
    print("\n🔹 Hacer cálculos:")
    print("   • ¿Cuánto es 25 * 4 + 10?")
    print("   • Calcula la raíz cuadrada de 144")
    print("\n🔹 Combinar ambas:")
    print("   • ¿Cuánto pesan juntos Pikachu y Raichu?")
    print("   • Compara el peso de Charizard y Blastoise")
    print("\n" + "="*70 + "\n")


def run_interactive_chat():
    """Ejecuta el chat interactivo en terminal"""
    print_banner()

    # Crear agente
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    agent = InteractiveAgent(model=model)

    print(f"✅ Agente inicializado con modelo: {model}\n")

    # Loop principal
    while True:
        try:
            # Leer input del usuario
            user_input = input("Tú: ").strip()

            # Comandos especiales
            if user_input.lower() in ["/salir", "/exit", "/quit"]:
                print("\n👋 ¡Hasta luego! Gracias por usar el chat.\n")
                break

            elif user_input.lower() == "/ayuda":
                print_help()
                continue

            elif user_input.lower() == "/limpiar":
                agent.clear_history()
                continue

            elif not user_input:
                continue  # Ignorar input vacío

            # Procesar mensaje con el agente
            print()  # Línea en blanco
            response = agent.chat(user_input)
            print(f"\n🤖 Agente: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrumpido. ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


# ========== PUNTO DE ENTRADA ==========

if __name__ == "__main__":
    run_interactive_chat()

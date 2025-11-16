"""
Agente Simple con OpenAI Function Calling

Este ejemplo muestra un agente básico que puede:
1. Calcular expresiones matemáticas
2. Obtener la hora actual en UTC

El agente usa el patrón ReAct: Reasoning → Action → Observation
"""

import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ========== HERRAMIENTAS (TOOLS) ==========

def calculate(expression: str) -> str:
    """
    Calcula expresiones matemáticas simples.

    Args:
        expression: Expresión matemática como string (ej: "25 * 4 + 10")

    Returns:
        Resultado del cálculo como string
    """
    try:
        # ADVERTENCIA: eval() solo para ejemplos educativos
        # En producción usar ast.literal_eval() o una librería segura
        result = eval(expression)
        return str(float(result))
    except Exception as e:
        return f"Error en el cálculo: {str(e)}"


def get_current_time() -> str:
    """
    Retorna la fecha y hora actual en UTC.

    Returns:
        Timestamp en formato ISO
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


# ========== DEFINICIÓN DE HERRAMIENTAS PARA OPENAI ==========

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calcula expresiones matemáticas. Útil para sumas, restas, multiplicaciones, divisiones, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "La expresión matemática a calcular (ej: '25 * 4 + 10')"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Obtiene la hora y fecha actual en UTC. No requiere parámetros.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# Mapeo de nombres de funciones a funciones Python
available_functions = {
    "calculate": calculate,
    "get_current_time": get_current_time
}


# ========== LÓGICA DEL AGENTE ==========

def run_agent(user_message: str, max_iterations: int = 10, model: str = "gpt-4") -> str:
    """
    Ejecuta el agente con un mensaje del usuario.

    El agente entra en un loop ReAct:
    1. THOUGHT: LLM decide qué hacer
    2. ACTION: Ejecuta una herramienta
    3. OBSERVATION: Recibe el resultado
    4. REPEAT: Hasta completar la tarea

    Args:
        user_message: Pregunta o tarea del usuario
        max_iterations: Número máximo de iteraciones (evita loops infinitos)
        model: Modelo de OpenAI a usar

    Returns:
        Respuesta final del agente
    """
    # Inicializar historial de mensajes
    messages = [{"role": "user", "content": user_message}]

    print(f"\n{'='*60}")
    print(f"USUARIO: {user_message}")
    print(f"{'='*60}\n")

    for iteration in range(max_iterations):
        print(f"--- Iteración {iteration + 1} ---")

        # PASO 1: LLM decide qué hacer (REASONING)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"  # El LLM decide si usar herramientas o responder directamente
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Si no hay tool calls, el agente terminó
        if not tool_calls:
            final_response = response_message.content
            print(f"\n✅ RESPUESTA FINAL: {final_response}\n")
            return final_response

        # Agregar respuesta del LLM al historial
        messages.append(response_message)

        # PASO 2 y 3: Ejecutar herramientas (ACTION + OBSERVATION)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"🔧 ACTION: {function_name}({function_args})")

            # Ejecutar la función
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)

            print(f"👁️ OBSERVATION: {function_response}")

            # Agregar resultado al historial
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response)
            })

    # Si llegamos aquí, excedimos max_iterations
    return "⚠️ El agente excedió el número máximo de iteraciones sin llegar a una respuesta final."


# ========== EJEMPLOS DE USO ==========

if __name__ == "__main__":
    # Ejemplo 1: Cálculo matemático
    print("\n" + "🎯 EJEMPLO 1: Cálculo Matemático " + "\n")
    result = run_agent("¿Cuánto es 25 * 4 + 10?")

    # Ejemplo 2: Hora actual
    print("\n" + "🎯 EJEMPLO 2: Hora Actual " + "\n")
    result = run_agent("¿Qué hora es?")

    # Ejemplo 3: Combinación (razonamiento multi-paso)
    print("\n" + "🎯 EJEMPLO 3: Multi-paso " + "\n")
    result = run_agent("¿Qué hora es y cuántas horas faltan para medianoche UTC?")

    print("\n✅ Todos los ejemplos completados!")

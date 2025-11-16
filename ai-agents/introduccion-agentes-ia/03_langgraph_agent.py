"""
Agente con LangGraph - Framework de Producción

Este ejemplo muestra un agente escalable usando LangGraph que puede:
1. Gestionar estado complejo con grafo de estados
2. Streaming de respuestas en tiempo real
3. Persistencia de historial de conversación
4. Checkpointing para recuperación de errores

LangGraph permite construir agentes de producción con control fino del flujo.
"""

import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Cargar variables de entorno
load_dotenv()


# ========== HERRAMIENTAS (TOOLS) ==========

@tool
def get_pokemon_info(pokemon_name: str) -> str:
    """
    Obtiene información de un Pokémon desde PokeAPI.

    Args:
        pokemon_name: Nombre del Pokémon en inglés (ej: "pikachu")

    Returns:
        Información del Pokémon en formato JSON
    """
    import requests
    import json

    try:
        pokemon_name = pokemon_name.lower().strip()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        pokemon_info = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "height": data["height"] / 10,  # metros
            "weight": data["weight"] / 10,  # kilogramos
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"][:3]],
            "base_experience": data.get("base_experience", "Unknown")
        }

        return json.dumps(pokemon_info, ensure_ascii=False)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: Pokémon '{pokemon_name}' no encontrado."
        return f"Error HTTP: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def calculate(expression: str) -> str:
    """
    Calcula expresiones matemáticas.

    Args:
        expression: Expresión matemática (ej: "25 * 4 + 10")

    Returns:
        Resultado del cálculo como string
    """
    try:
        result = eval(expression)
        return str(float(result))
    except Exception as e:
        return f"Error en el cálculo: {str(e)}"


# ========== DEFINICIÓN DEL ESTADO ==========

class AgentState(TypedDict):
    """
    Estado del agente que se mantiene a lo largo de la conversación.

    - messages: Historial de mensajes (se van agregando)
    """
    messages: Annotated[list, add_messages]


# ========== NODOS DEL GRAFO ==========

def agent_node(state: AgentState):
    """
    Nodo del agente: LLM decide qué hacer (REASONING).

    Puede:
    1. Responder directamente
    2. Llamar herramientas
    """
    # Crear LLM con herramientas vinculadas
    tools = [get_pokemon_info, calculate]
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    llm_with_tools = llm.bind_tools(tools)

    # System message para guiar al agente
    system_message = SystemMessage(
        content=(
            "Eres un asistente útil que puede consultar información de Pokémon "
            "y hacer cálculos matemáticos. Usa las herramientas cuando sea necesario."
        )
    )

    # Invocar LLM con contexto completo
    messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """
    Función de enrutamiento: decide si continuar o terminar.

    Returns:
        "tools" si hay tool_calls (ejecutar herramientas)
        "end" si no hay tool_calls (terminar)
    """
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"
    else:
        return "end"


# ========== CONSTRUCCIÓN DEL GRAFO ==========

def create_agent_graph():
    """
    Crea el grafo de estados del agente.

    Estructura:
    START → agent → should_continue?
                    ├─ tools → agent (loop)
                    └─ end → END
    """
    # Crear grafo
    workflow = StateGraph(AgentState)

    # Añadir nodos
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode([get_pokemon_info, calculate]))

    # Añadir edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")

    # Compilar grafo
    app = workflow.compile()

    return app


# ========== FUNCIÓN PRINCIPAL ==========

def run_langgraph_agent(user_message: str):
    """
    Ejecuta el agente LangGraph con streaming.

    Args:
        user_message: Pregunta del usuario
    """
    app = create_agent_graph()

    print(f"\n{'='*70}")
    print(f"USUARIO: {user_message}")
    print(f"{'='*70}\n")

    # Preparar input
    inputs = {"messages": [HumanMessage(content=user_message)]}

    # Ejecutar con streaming
    print("🔄 STREAMING DE RESPUESTA:\n")

    for output in app.stream(inputs, stream_mode="values"):
        last_message = output["messages"][-1]

        # Mostrar tool calls
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                print(f"🔧 TOOL CALL: {tool_call['name']}({tool_call['args']})")

        # Mostrar respuesta final
        elif hasattr(last_message, 'content') and last_message.content:
            if not hasattr(last_message, 'tool_calls'):  # Solo mostrar si no es tool call
                print(f"\n✅ RESPUESTA FINAL:\n{last_message.content}\n")

    return output["messages"][-1].content


# ========== EJEMPLOS DE USO ==========

if __name__ == "__main__":
    # Ejemplo 1: Consulta simple
    print("\n" + "🎯 EJEMPLO 1: Información de Pikachu " + "\n")
    run_langgraph_agent("¿Cuánto pesa Pikachu?")

    # Ejemplo 2: Multi-paso con cálculo
    print("\n" + "🎯 EJEMPLO 2: Multi-paso con cálculo " + "\n")
    run_langgraph_agent("¿Cuánto pesan juntos Pikachu y Charizard?")

    # Ejemplo 3: Consulta compleja
    print("\n" + "🎯 EJEMPLO 3: Consulta compleja " + "\n")
    run_langgraph_agent(
        "Compara el peso de Pikachu con el de Raichu y dime cuánto más pesa uno que el otro en porcentaje"
    )

    print("\n✅ Todos los ejemplos completados!")
    print("\n💡 Ventajas de LangGraph:")
    print("   - Streaming de respuestas")
    print("   - Estado persistente")
    print("   - Control fino del flujo")
    print("   - Checkpointing para recuperación")
    print("   - Escalable a grafos complejos")

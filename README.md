# Blog Code Examples

Código fuente completo de todos los ejemplos publicados en [franciscoparis.com/blog](https://franciscoparis.com/blog).

## 📚 Estructura

Este repositorio está organizado por categoría y post del blog. Cada carpeta contiene código funcional, listo para ejecutar, con instrucciones detalladas.

```
blog-code-examples/
├── ai-agents/                    # Agentes de IA
│   ├── introduccion-agentes-ia/  # Post: Introducción a Agentes de IA
│   ├── sistemas-multiagentes/    # (próximamente)
│   └── agentes-produccion/       # (próximamente)
├── rag-systems/                  # Sistemas RAG
│   └── building-rag-systems/     # (próximamente)
└── ...                           # Más categorías próximamente
```

## 🚀 Posts Disponibles

### AI Agents

#### [Introducción a Agentes de IA: Del Concepto a la Práctica](https://franciscoparis.com/es/blog/introduccion-agentes-ia)
**Carpeta:** [`ai-agents/introduccion-agentes-ia/`](./ai-agents/introduccion-agentes-ia/)

Aprende a construir agentes de IA desde cero usando OpenAI function calling, PokeAPI y LangGraph. Incluye:
- ✅ Agente simple con herramientas (calculadora, tiempo)
- ✅ Agente con API real (PokeAPI)
- ✅ Escalado con LangGraph para producción

**Tecnologías:** Python 3.12+, OpenAI API, LangGraph, PokeAPI

---

## 🛠️ Uso General

Cada carpeta de post contiene:
- `README.md` - Instrucciones específicas del post
- `requirements.txt` - Dependencias Python
- `*.py` - Código fuente de los ejemplos
- `.env.example` - Variables de entorno necesarias (si aplica)

### Instalación típica

```bash
# 1. Navega a la carpeta del post
cd ai-agents/introduccion-agentes-ia/

# 2. Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura variables de entorno (si aplica)
cp .env.example .env
# Edita .env con tus API keys

# 5. Ejecuta el ejemplo
python nombre_archivo.py
```

## 📝 Convenciones

- **Python 3.12+** requerido para todos los ejemplos
- **Type hints** en todo el código
- **Comentarios en español** para alinearse con el blog
- **Código production-simplified**: completo y funcional, pero no exhaustivo
- **Error handling básico**: suficiente para ejemplos educativos

## 🔗 Enlaces

- **Blog:** [franciscoparis.com/blog](https://franciscoparis.com/blog)
- **LinkedIn:** [linkedin.com/in/fparis1987](https://linkedin.com/in/fparis1987)
- **GitHub:** [github.com/fparis_sp](https://github.com/fparis_sp)

## 📄 Licencia

MIT License - Siéntete libre de usar estos ejemplos en tus propios proyectos.

## 🤝 Contribuciones

¿Encontraste un bug o tienes una mejora?
1. Abre un issue describiendo el problema
2. O mejor aún, envía un pull request con la solución

## ⚠️ Notas Importantes

- Los ejemplos usan APIs externas (OpenAI, PokeAPI, etc.) que pueden requerir API keys
- Algunos ejemplos generan costos reales (ej. OpenAI API)
- Los ejemplos son educativos, no están optimizados para producción sin modificaciones
- Siempre revisa el `README.md` específico de cada post antes de ejecutar

---

**Última actualización:** Noviembre 2025
**Posts totales:** 1
**Categorías:** 1 (AI Agents)
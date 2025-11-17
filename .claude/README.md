# Claude Code: Skills, Commands & Templates

Herramientas de productividad para personalizar tu workspace de Claude Code en PyCharm.

Este repositorio contiene skills reutilizables, slash commands y templates que transforman Claude Code de asistente genérico a copiloto personalizado.

## 📦 Contenido

### Skills (Agentes Especializados)

- **code-reviewer** - Review automático con checklist de calidad, seguridad y performance
- **test-writer** - Genera tests unitarios completos (pytest por defecto, personalizable)
- **doc-generator** - Documenta código automáticamente (Google style por defecto)

### Slash Commands (Atajos Rápidos)

- **/commit** - Genera commit messages siguiendo Conventional Commits
- **/review** - Quick code review antes de commit

### Templates

- **CLAUDE.md.template** - Template para documentar tu proyecto y darle contexto a Claude Code

## 🚀 Instalación Rápida

### Opción 1: Copiar todo

```bash
# Clona este repo
git clone https://github.com/fparis-sp/Blog-Code-Examples.git

# Ve a tu proyecto
cd tu-proyecto

# Copia skills y commands
cp -r Blog-Code-Examples/.claude/.claude .

# Copia template de CLAUDE.md
cp Blog-Code-Examples/.claude/templates/CLAUDE.md.template ./CLAUDE.md

# Edita CLAUDE.md con la info de tu proyecto
code CLAUDE.md  # o usa tu editor favorito
```

### Opción 2: Copiar selectivamente

Solo copia los skills/commands que necesites:

```bash
# Solo code-reviewer skill
cp -r Blog-Code-Examples/.claude/skills/code-reviewer .claude/skills/

# Solo /commit command
cp Blog-Code-Examples/.claude/commands/commit.md .claude/commands/
```

## 📖 Uso

### Skills

Los skills se invocan con el Task tool de Claude Code:

```
Tú: "Usa code-reviewer para revisar src/api/users.py"

Claude Code:
[Analiza archivo con checklist completo]
[Genera review con severidades y sugerencias]
```

### Slash Commands

Los comandos se invocan con `/nombre`:

```
Tú: "/commit"

Claude Code:
[Genera commit message conventional]
```

### CLAUDE.md

Simplemente edita `CLAUDE.md` en la raíz de tu proyecto. Claude Code lo lee automáticamente.

```markdown
# Project: Mi API

## Tech Stack
- Python 3.12 + FastAPI
- PostgreSQL
- pytest

## Structure
src/
├── api/      # Endpoints
└── services/ # Business logic
```

Claude ahora conoce tu proyecto sin preguntar.

## 🎯 Para Qué Sirve Cada Uno

### Code Reviewer Skill

**Cuándo usarlo:**
- Antes de hacer commit (validación completa)
- Después de refactorizar
- Al terminar una feature

**Qué hace:**
- Busca bugs, code smells, security issues
- Revisa mejores prácticas de Python
- Detecta problemas de performance
- Da feedback constructivo con código

**Ejemplo de output:**
```markdown
## 🔴 Críticos
- SQL Injection en línea 23
- Missing None check en línea 45

## 🟡 Mejorables
- Type hints faltantes
- Función muy larga (>80 líneas)

## ✅ Aspectos Positivos
- Buena separación de concerns
- Tests comprehensivos
```

### Test Writer Skill

**Cuándo usarlo:**
- Acabas de escribir una función
- Necesitas tests para código legacy
- Quieres validar edge cases

**Qué hace:**
- Genera suite completa de tests
- Happy path + edge cases + error cases
- Mocks para dependencias externas
- Coverage analysis

**Personalizable para:**
- pytest (default)
- unittest
- Django TestCase
- FastAPI TestClient
- Async tests (pytest-asyncio)

### Doc Generator Skill

**Cuándo usarlo:**
- Función sin docstring
- Necesitas README para módulo
- Documentación desactualizada

**Qué hace:**
- Genera docstrings completos
- Incluye ejemplos de uso
- Documenta parámetros, retorno, excepciones
- Crea READMEs para módulos

**Personalizable para:**
- Google style (default)
- NumPy style
- Sphinx/reStructuredText

### /commit Command

**Cuándo usarlo:**
- Antes de cada commit
- Quieres mensajes profesionales sin pensar

**Qué hace:**
- Analiza tus cambios (git diff)
- Genera mensaje Conventional Commits
- Tipo correcto (feat/fix/docs/etc)
- Descripción clara y concisa

### /review Command

**Cuándo usarlo:**
- Quick check antes de commit
- Sanity check de cambios

**Diferencia con code-reviewer skill:**
- `/review` = 2 segundos, problemas obvios
- `code-reviewer` = 30 segundos, análisis exhaustivo

### CLAUDE.md Template

**Cuándo usarlo:**
- Cada proyecto nuevo
- Claude pregunta lo mismo repetidamente

**Qué hace:**
- Claude lee tu proyecto automáticamente
- No más explicar framework/estructura/convenciones
- Contexto persistente en todas las conversaciones

## 🔧 Personalización

Todos los skills son templates base. Adáptalos a tu stack:

### Ejemplo: Django

En `code-reviewer/skill.md`, agrega:

```markdown
**Django-specific checks:**
- QuerySet N+1 problems
- Missing select_related/prefetch_related
- Signals vs model methods
```

En `test-writer/skill.md`, cambia:

```python
from django.test import TestCase

class TestMyModel(TestCase):
    # Django test structure
```

### Ejemplo: FastAPI

En `CLAUDE.md.template`:

```markdown
## Framework
FastAPI 0.104

## Testing
- TestClient for endpoints
- Pytest fixtures for DB
- Mock external APIs
```

## 📝 Blog Post

Estos ejemplos acompañan el post:

**[Personalizando tu Workspace con Claude Code: Skills, Comandos y Workflow](https://franciscoparis.com/blog/claude-code-personalizacion-workspace)**

Serie completa:
1. [Claude Code 101: Setup y Fundamentos](https://franciscoparis.com/blog/claude-code-setup-fundamentos)
2. Personalizando tu Workspace (este código)
3. Tu Primer Proyecto Completo (próximamente)

## 🤝 Contribuciones

¿Creaste un skill útil? ¡Compártelo!

1. Fork este repo
2. Agrega tu skill en `skills/tu-skill/`
3. Documenta qué hace y cuándo usarlo
4. Pull request

## 📄 Licencia

MIT License - Úsalo libremente en tus proyectos

## ✉️ Contacto

**Francisco París**
- Blog: [franciscoparis.com](https://franciscoparis.com)
- LinkedIn: [fparis1987](https://linkedin.com/in/fparis1987)

---

**¿Preguntas? ¿Sugerencias?** Abre un issue o conecta conmigo en LinkedIn.

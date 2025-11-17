Haz una revisión rápida del código staged (o modificado si no hay staged).

Usa `git diff --staged` (o `git diff` si no hay staged changes) para ver qué cambió.

## Qué revisar

Busca **problemas obvios**:

### 🔴 Críticos (detén el commit)
- Secrets/API keys hardcoded
- SQL injection evidente
- Código comentado que debería eliminarse
- `console.log` / `print()` de debugging olvidados
- Imports no usados obviamente

### 🟡 Mejorables (avisa pero no bloquees)
- Funciones muy largas (>80 líneas)
- Type hints faltantes en funciones nuevas
- Nombres de variables poco claros
- Duplicación de código evidente

### 💡 Sugerencias (nice-to-have)
- Comentarios que podrían ser docstrings
- Oportunidades de refactoring obvias

## Output format

```
Revisión rápida de cambios:

✅ No veo problemas críticos

🟡 Sugerencias:
- Línea 23: Considera agregar type hint a parámetro 'data'
- Línea 45: Nombre de variable 'x' poco descriptivo

💡 Nice-to-have:
- Función process_data() podría tener docstring
```

O si hay problemas críticos:

```
⚠️  DETÉN - Problemas encontrados:

🔴 Línea 15: API key hardcoded (OPENAI_API_KEY = "sk-...")
🔴 Línea 34: console.log de debugging olvidado

Arregla estos issues antes de commitear.
```

## Diferencia con code-reviewer skill

Este comando es para **quick check antes de commit**.

El skill `code-reviewer` es para **análisis exhaustivo** después de terminar feature.

Usa este comando: rápido, pre-commit
Usa el skill: profundo, post-feature

## Tono

- Rápido y al punto
- No redundante (el usuario ya sabe qué cambió)
- Constructivo, no crítico
- Si todo está bien, di que está bien (no inventes problemas)

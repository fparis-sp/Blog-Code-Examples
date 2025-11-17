Haz una revisión rápida pre-commit del código staged (o modificado si no hay staged).

**Pasos:**
1. Ejecuta `git diff --staged` (o `git diff` si no hay staged)
2. Revisa el código buscando problemas obvios
3. Reporta hallazgos en formato estructurado

**Busca problemas obvios:**

🔴 **Críticos** (detener commit):
- Secrets/API keys hardcoded
- SQL injection evidente
- Código comentado a eliminar
- `console.log`/`print()` de debugging
- Imports no usados

🟡 **Mejorables** (avisar):
- Funciones muy largas (>80 líneas)
- Type hints faltantes
- Nombres poco claros
- Duplicación de código

💡 **Sugerencias** (nice-to-have):
- Comentarios → docstrings
- Oportunidades de refactoring

**Output:**
```
Revisión rápida:

✅ No veo problemas críticos

🟡 Sugerencias:
- archivo.py:23: Agregar type hint a 'data'
- archivo.py:45: Variable 'x' poco descriptiva
```

O si hay críticos:
```
⚠️ DETÉN:

🔴 archivo.py:15: API key hardcoded
🔴 archivo.py:34: console.log olvidado
```

**Nota:** Este es un quick check pre-commit. Para análisis exhaustivo usa el skill `code-reviewer`.

Tono: rápido, constructivo, honesto (si está bien, di que está bien).

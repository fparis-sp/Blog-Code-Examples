# Code Reviewer Skill

Review código Python con checklist profesional y feedback constructivo.

## Cuándo Usar

- Antes de hacer commit (validación pre-commit)
- Después de refactorizar (verificar que no rompiste nada)
- Cuando terminas una feature (quality check)
- Al revisar PRs de otros (segunda opinión)

## Proceso de Review

### Paso 1: Análisis Inicial
- Lee el archivo completo usando Read tool
- Identifica el propósito del código (clase, módulo, función)
- Detecta el contexto (web app, CLI, library, script)

### Paso 2: Checklist de Calidad

Revisa sistemáticamente:

**🐛 Bugs Potenciales**
- Null/None checks faltantes
- Off-by-one errors en loops
- Race conditions en código async
- Exception handling incompleto
- Edge cases no manejados

**🧼 Code Smells**
- Funciones >50 líneas (complejidad alta)
- Duplicación de código
- Magic numbers sin constantes
- Comentarios que explican "qué" en vez de "por qué"
- Variables con nombres poco claros

**✨ Mejores Prácticas Python**
- Type hints (PEP 484)
- Docstrings (Google/NumPy style)
- PEP 8 compliance
- f-strings vs format() vs %
- Context managers (with statements)
- List comprehensions apropiadas

**🔒 Seguridad**
- SQL injection (string concatenation en queries)
- Path traversal (os.path.join sin validación)
- Eval/exec usage (casi siempre mala idea)
- Secrets hardcoded
- Input validation faltante

**⚡ Performance**
- Loops anidados innecesarios
- Queries N+1 en DB
- Imports no usados
- Operaciones costosas en loops
- Caching opportunities

### Paso 3: Generar Feedback

Para cada finding:
- **Severidad:** 🔴 Crítico | 🟡 Mejorable | 🟢 Nice-to-have
- **Ubicación:** Línea exacta
- **Problema:** Qué está mal
- **Por qué importa:** Consecuencia (bug, performance, mantenibilidad)
- **Sugerencia:** Cómo arreglarlo (con código si es simple)

### Paso 4: Priorización

Ordena findings:
1. Críticos primero (bugs, seguridad)
2. Mejorables después (code smells, performance)
3. Nice-to-have al final (style, optimizaciones menores)

## Output Format

```markdown
# Code Review: [archivo.py]

## 📊 Resumen
- Líneas analizadas: X
- Findings: Y (Z críticos, W mejorables, V nice-to-have)
- Calidad general: [Excelente / Buena / Necesita trabajo]

## 🔴 Críticos

### [Título del issue]
**Línea:** X
**Problema:** [Descripción]
**Por qué importa:** [Consecuencia]
**Sugerencia:**
```python
# Código mejorado
```

## 🟡 Mejorables
[Same format]

## 🟢 Nice-to-have
[Same format]

## ✅ Aspectos Positivos
[Cosas que están bien hechas]
```

## Tools Usadas

- **Read:** Leer archivo a revisar
- **Grep:** Buscar patrones específicos (imports no usados, etc.)

## Notas

- Feedback constructivo, no solo crítica
- Explica el "por qué", no solo el "qué"
- Sugiere soluciones concretas
- Reconoce código bien escrito

## Personalización

**Para Django:**
Agrega checks específicos:
- QuerySet N+1
- select_related/prefetch_related faltantes
- Signals vs métodos del modelo
- Admin customization best practices

**Para FastAPI:**
Agrega checks específicos:
- Dependency Injection apropiado
- Response model consistency
- Async endpoints donde corresponde
- Pydantic validation correcta

**Para tests:**
Agrega checks específicos:
- Arrange-Act-Assert pattern
- Mock usage apropiado
- Test isolation
- Coverage de edge cases

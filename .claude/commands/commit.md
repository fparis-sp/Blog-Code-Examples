Analiza los cambios en git (usa `git diff --staged` si hay staged changes, o `git diff` si no hay nada staged).

Genera un commit message siguiendo **Conventional Commits**:

## Formato

```
<tipo>(<scope>): <descripción>

<body opcional>

<footer opcional>
```

## Tipos válidos
- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **docs**: Cambios en documentación
- **style**: Formato, punto y coma, etc (no afecta código)
- **refactor**: Refactorización (no es feat ni fix)
- **perf**: Mejora de performance
- **test**: Agregar o corregir tests
- **chore**: Cambios en build, herramientas, dependencias

## Reglas

1. **Tipo:** Obligatorio, lowercase
2. **Scope:** Opcional, módulo/componente afectado
3. **Descripción:**
   - Presente imperativo ("add" no "added")
   - Lowercase
   - Sin punto final
   - Máximo 50 caracteres
4. **Body:**
   - Opcional
   - Explica QUÉ y POR QUÉ (no el cómo)
   - Wrap a 72 caracteres
5. **Footer:**
   - Opcional
   - Breaking changes: `BREAKING CHANGE: description`
   - Issues: `Closes #123` o `Fixes #456`

## Ejemplos

### Simple
```
feat(auth): add JWT token refresh endpoint
```

### Con body
```
fix(api): prevent SQL injection in user lookup

Replace string concatenation with parameterized queries
in get_user() function. Add input validation for user_id.
```

### Con breaking change
```
feat(api)!: change response format to JSON:API spec

BREAKING CHANGE: All API responses now follow JSON:API
specification. Clients need to update their parsers.

Closes #234
```

### Multiple changes
Si hay cambios en múltiples áreas, enfócate en el cambio principal.
Si son cambios no relacionados, sugiere hacer commits separados.

## Tono

- Profesional pero conciso
- Claro y descriptivo
- Sin jerga innecesaria
- En inglés (convención estándar en desarrollo)

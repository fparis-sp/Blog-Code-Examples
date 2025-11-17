Analiza los cambios en git y genera un commit message siguiendo Conventional Commits.

**Formato:** `<tipo>(<scope>): <descripción>`

**Tipos válidos:**
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Cambios en documentación
- style: Formato (no afecta código)
- refactor: Refactorización
- perf: Mejora de performance
- test: Tests
- chore: Build, herramientas, dependencias

**Reglas:**
- Tipo obligatorio, lowercase
- Scope opcional (módulo/componente)
- Descripción: imperativo, lowercase, sin punto, max 50 chars
- Body opcional: explica QUÉ y POR QUÉ, wrap 72 chars
- Footer opcional: `BREAKING CHANGE:` o `Closes #123`

**Pasos:**
1. Ejecuta `git diff --staged` (o `git diff` si no hay staged)
2. Analiza los cambios
3. Genera commit message apropiado
4. Si hay múltiples cambios no relacionados, sugiere commits separados

**Ejemplos:**
```
feat(auth): add JWT token refresh endpoint

fix(api): prevent SQL injection in user lookup

feat(api)!: change response format to JSON:API spec

BREAKING CHANGE: All API responses now follow JSON:API spec
```

Mensaje en inglés, profesional y conciso.

# Doc Generator Skill

Genera documentación clara y completa para código Python.

## Cuándo Usar

- Función sin docstring
- Clase nueva que necesita documentación
- README para proyecto/módulo
- Actualizar documentación obsoleta

## Proceso

### Paso 1: Analizar Código
- Lee función/clase/módulo con Read tool
- Identifica: propósito, parámetros, retorno, exceptions, ejemplos

### Paso 2: Generar Docstring

Estilo: **Google**
(Personaliza aquí para NumPy, reStructuredText, etc.)

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """Breve descripción (una línea).

    Descripción más detallada si es necesario. Explica qué hace
    la función, casos de uso, consideraciones importantes.

    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2. Defaults to 0.

    Returns:
        bool: Descripción del valor de retorno

    Raises:
        ValueError: Cuándo se lanza esta exception
        TypeError: Cuándo se lanza esta otra

    Examples:
        >>> function_name("hello", 5)
        True

        >>> function_name("", 0)
        False
    """
```

### Paso 3: README para Módulos

Si se pide README, genera:
- Título y descripción
- Instalación
- Uso básico (ejemplos)
- API reference (funciones principales)
- Contribución (si es open source)

## Output Format

**Para funciones/clases:**
Docstring completo insertado en código

**Para módulos:**
```markdown
# Module Name

Brief description.

## Installation

```bash
pip install module-name
```

## Usage

```python
from module import function_name

result = function_name("example")
```

## API Reference

### function_name(param1, param2)
Description...

**Parameters:**
- `param1` (str): Description
- `param2` (int, optional): Description. Defaults to 0.

**Returns:**
- bool: Description

**Raises:**
- ValueError: When...

### ClassName

Description of class...

**Attributes:**
- `attribute1`: Description
- `attribute2`: Description

**Methods:**
- `method1()`: Description

## Examples

```python
# Example 1
result = function_name("hello")

# Example 2
obj = ClassName()
obj.method1()
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
```

## Tools Usadas

- **Read:** Leer código a documentar
- **Write:** Insertar docstrings o crear README

## Personalización

### Para NumPy style

```python
"""
Brief description.

Parameters
----------
param1 : str
    Description
param2 : int, optional
    Description (default is 0)

Returns
-------
bool
    Description

Raises
------
ValueError
    When...

Examples
--------
>>> function_name("hello", 5)
True
"""
```

### Para Sphinx/reStructuredText

```python
"""
Brief description.

:param param1: Description
:type param1: str
:param param2: Description
:type param2: int
:returns: Description
:rtype: bool
:raises ValueError: When...

Example::

    result = function_name("hello")
"""
```

### Para clases

```python
class ClassName:
    """One-line class description.

    Longer description explaining what this class does,
    when to use it, and any important considerations.

    Attributes:
        attribute1 (str): Description of attribute1
        attribute2 (int): Description of attribute2

    Examples:
        >>> obj = ClassName("value")
        >>> obj.method1()
        'result'
    """

    def __init__(self, param1: str):
        """Initialize the class.

        Args:
            param1: Description
        """
        self.attribute1 = param1
```

### Para módulos enteros

Si se pide documentar un módulo Python completo:

```python
"""
Module: mymodule
================

Brief module description.

This module provides functionality for X, Y, and Z.
It is designed to be used in contexts where...

Functions:
    - function1(): Description
    - function2(): Description

Classes:
    - ClassName: Description

Constants:
    - CONSTANT1: Description

Examples:
    >>> import mymodule
    >>> result = mymodule.function1()

Author: Your Name
License: MIT
"""
```

## Notas

- Siempre incluye ejemplos cuando sea posible
- Usa lenguaje claro y conciso
- Documenta el "por qué" además del "qué"
- Actualiza docs cuando cambia código
- Para APIs públicas, documenta exhaustivamente
- Para código interno, docstring breve suele ser suficiente

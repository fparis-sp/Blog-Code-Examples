# Test Writer Skill

Genera tests unitarios completos para código Python.

## Cuándo Usar

- Acabas de escribir una función y necesitas tests
- Refactorizaste código y quieres validar comportamiento
- Código legacy sin tests (test de caracterización)

## Proceso

### Paso 1: Analizar Código
- Lee función/clase con Read tool
- Identifica: inputs, outputs, edge cases, dependencias externas

### Paso 2: Diseñar Test Cases

Genera tests para:
- **Happy path:** Caso normal de uso
- **Edge cases:** Valores límite (0, None, empty string, max int)
- **Error cases:** Inputs inválidos, exceptions esperadas
- **Dependencies:** Mock de APIs, DB, file system

### Paso 3: Generar Tests

Framework: **pytest**
(Personaliza aquí si usas unittest, nose, etc.)

Estructura:
```python
import pytest
from unittest.mock import Mock, patch

def test_<function>_happy_path():
    """Test caso normal"""
    # Arrange
    # Act
    # Assert

def test_<function>_edge_case_empty_input():
    """Test con input vacío"""

def test_<function>_raises_exception():
    """Test que verifica exception esperada"""
    with pytest.raises(ValueError):
        ...
```

### Paso 4: Coverage Analysis

Sugiere tests adicionales si coverage <80%

## Output Format

```python
# tests/test_<module>.py

import pytest
from unittest.mock import Mock, patch
from mymodule import function_to_test

class Test<FunctionName>:
    """Tests for <function_name>"""

    def test_happy_path(self):
        # Arrange
        input_data = ...
        expected = ...

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == expected

    def test_edge_case_none_input(self):
        # Test None handling
        with pytest.raises(ValueError):
            function_to_test(None)

    def test_edge_case_empty_string(self):
        # Test empty string
        result = function_to_test("")
        assert result == expected_for_empty

    @patch('mymodule.external_api')
    def test_with_mocked_dependency(self, mock_api):
        # Mock external dependency
        mock_api.return_value = {"status": "ok"}

        result = function_to_test()

        assert result is not None
        mock_api.assert_called_once()
```

## Tools Usadas

- **Read:** Leer código a testear
- **Grep:** Buscar imports, dependencias

## Personalización

### Para unittest en vez de pytest

Cambios necesarios:

```python
import unittest
from mymodule import function_to_test

class TestFunctionName(unittest.TestCase):
    """Tests for function_name"""

    def test_happy_path(self):
        """Test caso normal"""
        result = function_to_test(valid_input)
        self.assertEqual(result, expected)

    def test_raises_exception(self):
        """Test exception"""
        with self.assertRaises(ValueError):
            function_to_test(invalid_input)
```

### Para Django

Agrega imports y setup:

```python
from django.test import TestCase
from myapp.models import MyModel

class TestMyModel(TestCase):
    """Tests for MyModel"""

    def setUp(self):
        # Setup test database
        self.instance = MyModel.objects.create(name="test")

    def test_model_creation(self):
        self.assertEqual(self.instance.name, "test")
```

### Para FastAPI

Usa TestClient:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Para tests async

Usa pytest-asyncio:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

## Notas

- Siempre incluye docstrings en tests
- Usa nombres descriptivos (no test_1, test_2)
- Un assert por test cuando sea posible
- Fixture en conftest.py si se reusan

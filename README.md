# 📋 Sistema de Gestión de Tareas

Un sistema completo de gestión de tareas desarrollado en Python que permite crear, modificar y gestionar tareas asignadas a diferentes usuarios.

## 🚀 Características

- ✅ **Gestión de Usuarios**: Crear y administrar usuarios del sistema
- ✅ **Gestión de Tareas**: CRUD completo de tareas con estados (pendiente, en progreso, completada)
- ✅ **Persistencia**: Guardado en archivos JSON y binarios
- ✅ **Reportes**: Generación de informes y estadísticas
- ✅ **Interfaz CLI**: Menú interactivo en línea de comandos
- ✅ **Validaciones**: Sistema robusto de validación de datos

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Configuración del Proyecto

1. **Clonar/Descargar el proyecto**

   ```bash
   # Si tienes el código, navega al directorio
   cd sistema_tareas
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**

   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Ejecutar Pruebas

```bash
# Activar el entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas
python -m pytest tests/ -v

# Ejecutar pruebas específicas
python -m pytest tests/test_usuario.py -v
python -m pytest tests/test_tarea.py -v
```

## 📦 Dependencias

- `tabulate>=0.9.0` - Formateo de tablas para reportes
- `colorama>=0.4.6` - Colores en terminal
- `pytest>=7.0.0` - Framework de pruebas

## 🏗️ Estructura del Proyecto

```
sistema_tareas/
├── src/
│   ├── models/          # Clases principales (Usuario, Tarea)
│   ├── services/        # Lógica de negocio
│   ├── utils/           # Utilidades y helpers
│   └── main.py         # Punto de entrada
├── data/
│   ├── json/           # Archivos JSON
│   ├── binarios/       # Archivos binarios (pickle)
│   └── backups/        # Respaldos
├── tests/              # Pruebas unitarias
├── docs/               # Documentación
├── requirements.txt    # Dependencias
├── .gitignore         # Archivos a ignorar en git
└── README.md          # Este archivo
```

## 💻 Uso Básico

### Importar las clases principales

```python
from src.models.usuario import Usuario
from src.models.tarea import Tarea, EstadoTarea
from datetime import datetime, timedelta

# Crear un usuario
usuario = Usuario("Juan Pérez", "juan@email.com")

# Crear una tarea
fecha_limite = datetime.now() + timedelta(days=7)
tarea = Tarea("Desarrollar API", "Crear endpoints REST", fecha_limite, usuario.id)

# Cambiar estado de tarea
tarea.cambiar_estado(EstadoTarea.EN_PROGRESO)

# Asignar tarea al usuario
usuario.agregar_tarea(tarea.id)
```

### Ejecutar el sistema completo

```python
# Una vez implementado el main.py
python src/main.py
```

### 🆕 Usar el Sistema de Logging

```python
from src.utils.logger import obtener_logger, log_inicio_operacion, log_exito_operacion, log_error

# Obtener logger
logger = obtener_logger("mi_modulo")

# Usar helpers de logging
log_inicio_operacion("Crear Usuario", "Juan Pérez")
log_exito_operacion("Usuario creado", "ID: 12345")
log_error("Error de validación", "Email inválido")

# Los logs se guardan automáticamente en: logs/sistema_tareas.log
```

### 📝 Demo del Sistema de Logging

```bash
# Ejecutar demostración completa de logging
python demo_logging.py

# Ver archivo de logs generado
cat logs/sistema_tareas.log
```

## 🧪 Conceptos de Python Implementados

Este proyecto demuestra el uso de:

- **Programación Orientada a Objetos (POO)**

  - Clases y objetos
  - Métodos de instancia y de clase
  - Properties y métodos especiales (`__str__`, `__repr__`, `__eq__`)

- **Métodos de Cadenas y Listas**

  - Formateo con `.strip()`, `.title()`, `.lower()`
  - Manipulación de listas con `.append()`, `.remove()`, `in`
  - Join de listas y comprehensions

- **Manejo de Archivos**

  - JSON para datos legibles
  - Pickle para serialización binaria
  - Gestión automática de directorios

- **🆕 Sistema de Logging Profesional**

  - Logging con niveles (INFO, WARNING, ERROR)
  - Archivos de log con timestamp automático
  - Helpers para operaciones comunes
  - Manejo de errores con contexto
  - **Sistema profesional y robusto**

- **Módulos Estándar**

  - `datetime`: Cálculo de fechas y diferencias
  - `uuid`: Generación de identificadores únicos
  - `os`: Manipulación de directorios
  - `enum`: Enumeraciones para estados
  - `logging`: Sistema de logging profesional

- **Paquetes Externos**
  - `tabulate`: Formateo profesional de tablas
  - `colorama`: Colores en terminal
  - `pytest`: Testing profesional

## 🤝 Desarrollo

### Agregar nuevas funcionalidades

1. Crear nuevas clases en `src/models/` o `src/services/`
2. Añadir pruebas correspondientes en `tests/`
3. Ejecutar las pruebas para validar
4. Actualizar documentación si es necesario

### Estructura de desarrollo recomendada

- Cada módulo debe tener sus pruebas correspondientes
- Usar docstrings en español para documentar funciones
- Seguir PEP 8 para el estilo de código
- Mantener cobertura de pruebas alta

## 📄 Licencia

Este proyecto implementa un sistema completo de gestión de tareas desarrollado en Python.

## 🎯 Características Técnicas

- ✅ Estructura profesional de proyectos Python
- ✅ Uso de entornos virtuales
- ✅ Programación orientada a objetos
- ✅ Manejo de archivos y persistencia
- ✅ Testing con pytest
- ✅ Documentación de código
- ✅ Gestión de dependencias

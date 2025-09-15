# 👥 Manual de Usuario - Sistema de Gestión de Tareas

## 📋 Guía Completa para Usuarios

### 🎯 **¿Qué es este Sistema?**

El **Sistema de Gestión de Tareas** es una aplicación profesional que permite organizar y hacer seguimiento de proyectos personales. El sistema permite crear tareas, asignar responsabilidades, cambiar estados y generar informes detallados.

### 🌟 **Características Principales**

- ✅ **Gestión de Tareas**: Crear, modificar y eliminar tareas
- 👥 **Gestión de Usuarios**: Agregar usuarios del sistema
- 📊 **Reportes Visuales**: Dashboards e informes detallados
- 💾 **Almacenamiento Seguro**: Tus datos se guardan automáticamente
- 🔍 **Búsqueda Avanzada**: Encuentra tareas rápidamente
- 📅 **Vista de Calendario**: Visualiza fechas límite

---

## 🚀 Instalación y Configuración

### 📋 **Requisitos del Sistema**

| **Requisito**     | **Versión Mínima** | **Recomendada** |
| ----------------- | ------------------ | --------------- |
| **Python**        | 3.8                | 3.11+           |
| **Sistema**       | Windows/Mac/Linux  | Cualquiera      |
| **Memoria RAM**   | 512 MB             | 1 GB            |
| **Espacio Disco** | 50 MB              | 100 MB          |

### 🔧 **Pasos de Instalación**

#### **Paso 1: Descargar el Proyecto**

```bash
# Opción A: Si tienes git
git clone <repositorio>
cd sistema_tareas

# Opción B: Descargar ZIP y extraer
# Navegar al directorio extraído
```

#### **Paso 2: Crear Entorno Virtual**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

#### **Paso 3: Instalar Dependencias**

```bash
# Instalar paquetes necesarios
pip install -r requirements.txt
```

#### **Paso 4: Verificar Instalación**

```bash
# Ejecutar demostración
python demo_simple.py
```

Si ves el mensaje "🎉 EJECUCIÓN COMPLETADA", ¡la instalación fue exitosa!

---

## 🎮 Primeros Pasos

### 🌟 **Tu Primera Experiencia**

#### **Ejecutar el Sistema**

```bash
python demo_simple.py
```

Esta ejecución mostrará:

- ✅ Cómo se crean usuarios automáticamente
- ✅ Cómo se formatean los nombres
- ✅ Cómo se crean y asignan tareas
- ✅ Cómo se generan reportes profesionales

#### **Explorar los Datos Generados**

Después de la ejecución, encontrarás:

```
data_demo/
├── json/           # Archivos legibles
│   ├── usuarios.json
│   └── tareas.json
├── binarios/       # Archivos de respaldo
└── backups/        # Copias de seguridad
```

### 📖 **Conceptos Básicos**

#### **👤 Usuario**

Un usuario del sistema con:

- **Nombre completo** (ej: "María García")
- **Email único** (ej: "maria@empresa.com")
- **Lista de tareas** asignadas

#### **📋 Tarea**

Una actividad de trabajo con:

- **Título descriptivo** (ej: "Desarrollar API de usuarios")
- **Descripción detallada**
- **Fecha límite**
- **Estado actual**: Pendiente → En Progreso → Completada
- **Usuario asignado**

#### **📊 Estados de Tareas**

| **Estado**      | **Significado**        | **Emoji** |
| --------------- | ---------------------- | --------- |
| **Pendiente**   | Aún no iniciada        | 📋        |
| **En Progreso** | Siendo trabajada       | ⚙️        |
| **Completada**  | Terminada exitosamente | ✅        |

---

## 💻 Guías de Uso Práctico

### 👥 **Gestión de Usuarios**

#### **Crear Nuevo Usuario**

```python
from src.services.gestor_sistema import GestorSistema

# Inicializar sistema
gestor = GestorSistema()

# Crear usuario (el sistema formatea automáticamente)
usuario = gestor.crear_usuario(
    nombre="  juan carlos pérez  ",  # Se formatea a "Juan Carlos Pérez"
    email="JUAN@EMPRESA.COM"        # Se normaliza a "juan@empresa.com"
)

print(f"✅ Usuario creado: {usuario}")
```

**💡 Tips para Usuarios:**

- Los nombres se formatean automáticamente
- Los emails deben ser únicos en el sistema
- Espacios extra se eliminan automáticamente

#### **Buscar Usuarios**

```python
# Por email
usuario = gestor.obtener_usuario_por_email("juan@empresa.com")

# Listar usuarios activos (con tareas)
for usuario in gestor.listar_usuarios_activos():
    print(f"👤 {usuario.nombre}: {len(usuario.tareas_asignadas)} tareas")
```

### 📋 **Gestión de Tareas**

#### **Crear Nueva Tarea**

```python
from datetime import datetime, timedelta

# Crear tarea con fecha límite en 2 semanas
fecha_limite = datetime.now() + timedelta(days=14)

tarea = gestor.crear_tarea(
    titulo="Desarrollar sistema de login",
    descripcion="Implementar autenticación con JWT y validación de usuarios",
    fecha_limite=fecha_limite,
    usuario_email="juan@empresa.com"  # Asignar inmediatamente
)

print(f"✅ Tarea creada: {tarea.titulo}")
```

#### **Cambiar Estado de Tarea**

```python
# Obtener ID de la tarea (puedes verlo en los reportes)
tarea_id = "tarea-123"

# Cambiar a "en progreso"
gestor.cambiar_estado_tarea(tarea_id, "en_progreso")

# Marcar como completada
gestor.cambiar_estado_tarea(tarea_id, "completada")
```

#### **Reasignar Tarea**

```python
# Cambiar asignación a otro usuario
gestor.asignar_tarea("tarea-123", "maria@empresa.com")
```

### 🔍 **Búsqueda de Tareas**

#### **Buscar por Texto**

```python
# Buscar en títulos y descripciones
tareas = gestor.buscar_tareas("login")

for tarea in tareas:
    print(f"🔍 Encontrada: {tarea.titulo}")
```

#### **Filtrar por Estado**

```python
# Obtener solo tareas pendientes
for tarea in gestor.listar_tareas_por_estado("pendiente"):
    dias = tarea.calcular_dias_restantes()
    print(f"📋 {tarea.titulo} - {dias} días restantes")
```

#### **Tareas Próximas a Vencer**

```python
# Tareas que vencen en los próximos 3 días
for tarea in gestor.obtener_tareas_proximas_vencer(3):
    print(f"🔥 URGENTE: {tarea.titulo}")
```

---

## 📊 Generación de Reportes

### 🌟 **Dashboard Ejecutivo**

**El reporte más completo** con métricas clave:

```python
# Generar dashboard completo
dashboard = gestor.generar_dashboard_ejecutivo()
print(dashboard)
```

**Incluye:**

- 📊 **Métricas generales**: Total usuarios, tareas, progreso
- 📈 **Distribución por estados**: Con porcentajes
- 👥 **Top usuarios más activos**: Ranking por asignaciones
- 🔥 **Tareas críticas**: Vencidas o próximas a vencer

### 👥 **Reporte de Usuarios**

```python
# Reporte detallado de usuarios
reporte = gestor.generar_reporte_usuarios()
print(reporte)
```

**Información por usuario:**

- Total de tareas asignadas
- Distribución por estados
- Fecha de registro
- Estadísticas de productividad

### 📋 **Reporte de Tareas**

```python
# Todas las tareas
reporte = gestor.generar_reporte_tareas()

# Solo tareas pendientes
reporte = gestor.generar_reporte_tareas(filtrar_estado="pendiente")

print(reporte)
```

### 📅 **Vista de Calendario**

```python
from datetime import datetime

# Calendario de enero 2025
calendario = gestor.generar_reporte_calendario(2025, 1)
print(calendario)
```

**Características:**

- Días con tareas marcados con \*
- Lista detallada de tareas por día
- Resumen mensual

### 📈 **Análisis de Productividad**

```python
# Análisis de los últimos 30 días
productividad = gestor.generar_reporte_productividad(30)
print(productividad)
```

**Incluye:**

- Tasa de completitud por usuario
- Tiempo promedio de tareas
- Tendencias semanales
- Recomendaciones automáticas

---

## 💾 Gestión de Datos

### 🔒 **Guardar Datos**

#### **Guardado Manual**

```python
# Guardar en formato JSON (legible)
gestor.guardar_datos_sistema("json")

# Guardar en formato binario (eficiente)
gestor.guardar_datos_sistema("binario")
```

#### **Crear Backup**

```python
# Backup completo del sistema
gestor.crear_backup_completo()
```

**Los backups incluyen:**

- Timestamp automático
- Ambos formatos (JSON + binario)
- Limpieza automática de backups antiguos

### 📁 **Estructura de Archivos**

**Después de usar el sistema:**

```
data/
├── json/                    # 📄 Archivos legibles
│   ├── usuarios.json        # Lista de usuarios
│   └── tareas.json          # Lista de tareas
├── binarios/               # 🔧 Archivos optimizados
│   ├── usuarios.pkl        # Usuarios en formato binario
│   └── tareas.pkl          # Tareas en formato binario
└── backups/                # 🔒 Copias de seguridad
    ├── usuarios_20250115_143022.json
    ├── usuarios_20250115_143022.pkl
    ├── tareas_20250115_143022.json
    └── tareas_20250115_143022.pkl
```

### 📈 **Estadísticas del Sistema**

```python
# Obtener estadísticas generales
stats = gestor.obtener_estadisticas_sistema()

print(f"👥 Usuarios: {stats['total_usuarios']}")
print(f"📋 Tareas: {stats['total_tareas']}")
print(f"✅ Completadas: {stats['tareas_completadas']}")
print(f"🎯 Progreso: {stats['porcentaje_completadas']}%")
```

---

## 🛠️ Casos de Uso Comunes

### 🚀 **Scenario 1: Nuevo Proyecto**

**Situación:** Iniciar un nuevo proyecto de desarrollo.

```python
# 1. Inicializar sistema
gestor = GestorSistema()

# 2. Agregar usuarios del sistema
gestor.crear_usuario("Ana López", "ana@empresa.com")
gestor.crear_usuario("Carlos Ruiz", "carlos@empresa.com")
gestor.crear_usuario("María García", "maria@empresa.com")

# 3. Crear tareas del proyecto
from datetime import datetime, timedelta

# Tarea de diseño
gestor.crear_tarea(
    "Diseñar interfaz de usuario",
    "Crear mockups y prototipos de la aplicación",
    datetime.now() + timedelta(days=7),
    "ana@empresa.com"
)

# Tarea de desarrollo
gestor.crear_tarea(
    "Desarrollar API REST",
    "Implementar endpoints para usuarios y autenticación",
    datetime.now() + timedelta(days=14),
    "carlos@empresa.com"
)

# 4. Generar reporte inicial
print(gestor.generar_dashboard_ejecutivo())

# 5. Guardar datos
gestor.guardar_datos_sistema()
```

### 📊 **Scenario 2: Seguimiento Semanal**

**Situación:** Revisión semanal del progreso del proyecto.

```python
# 1. Cargar sistema existente
gestor = GestorSistema()  # Carga datos automáticamente

# 2. Revisar tareas urgentes
print("🔥 TAREAS URGENTES (próximas 3 días):")
for tarea in gestor.obtener_tareas_proximas_vencer(3):
    print(f"  • {tarea.titulo} - Asignada a: {tarea.usuario_id}")

# 3. Actualizar estados de tareas
# (IDs obtenidos de reportes anteriores)
gestor.cambiar_estado_tarea("tarea-123", "completada")
gestor.cambiar_estado_tarea("tarea-456", "en_progreso")

# 4. Generar reporte de productividad
print("\n📈 ANÁLISIS DE PRODUCTIVIDAD:")
print(gestor.generar_reporte_productividad(7))  # Última semana

# 5. Guardar cambios
gestor.guardar_datos_sistema()
```

### 🔄 **Scenario 3: Reasignación de Tareas**

**Situación:** Un usuario del sistema tiene demasiadas tareas asignadas.

```python
# 1. Revisar cargas de trabajo
reporte = gestor.generar_reporte_usuarios()
print(reporte)

# 2. Buscar tareas del usuario sobrecargado
tareas_usuario = []
for tarea in gestor.tareas:
    if tarea.usuario_id == "usuario-sobrecargado-123":
        tareas_usuario.append(tarea)

# 3. Reasignar tareas pendientes
for tarea in tareas_usuario:
    if tarea.estado.value == "pendiente":
        gestor.asignar_tarea(tarea.id, "maria@empresa.com")
        print(f"✅ Reasignada: {tarea.titulo}")

# 4. Verificar nueva distribución
print("\n👥 NUEVA DISTRIBUCIÓN:")
print(gestor.generar_reporte_usuarios())
```

### 📅 **Scenario 4: Planificación Mensual**

**Situación:** Planificar el trabajo del próximo mes.

```python
from datetime import datetime

# 1. Ver calendario del mes actual
mes_actual = datetime.now().month
año_actual = datetime.now().year

calendario = gestor.generar_reporte_calendario(año_actual, mes_actual)
print(calendario)

# 2. Crear tareas para el próximo mes
proximas_tareas = [
    ("Refactorizar código base", "Mejorar arquitectura del sistema"),
    ("Implementar tests unitarios", "Aumentar cobertura de pruebas"),
    ("Optimizar base de datos", "Mejorar consultas lentas")
]

for titulo, descripcion in proximas_tareas:
    gestor.crear_tarea(
        titulo,
        descripcion,
        datetime.now() + timedelta(days=30),
        "carlos@empresa.com"  # Asignar por defecto
    )

# 3. Generar plan mensual
print("\n📋 PLAN MENSUAL:")
print(gestor.generar_reporte_tareas(filtrar_estado="pendiente"))
```

---

## 🔧 Personalización y Configuración

### 🎨 **Formatos de Reportes**

Puedes cambiar el estilo visual de los reportes:

```python
# Diferentes estilos disponibles
estilos = [
    "plain",        # Texto simple
    "simple",       # Líneas simples
    "github",       # Estilo GitHub
    "grid",         # Con bordes (predeterminado)
    "fancy_grid",   # Bordes decorativos
    "pipe",         # Estilo pipeline
    "html",         # Para páginas web
    "latex"         # Para documentos PDF
]

# Usar estilo específico
reporte = gestor.generar_reporte_usuarios("fancy_grid")
print(reporte)
```

### 📁 **Configurar Directorio de Datos**

```python
# Usar directorio personalizado
gestor = GestorSistema("mi_proyecto_datos")

# Esto creará:
# mi_proyecto_datos/
# ├── json/
# ├── binarios/
# └── backups/
```

### 🔄 **Automatización de Backups**

```python
import schedule
import time

def backup_automatico():
    gestor = GestorSistema()
    gestor.crear_backup_completo()
    print("🔒 Backup automático completado")

# Programar backup diario a las 2:00 AM
schedule.every().day.at("02:00").do(backup_automatico)

# Mantener el programa corriendo
while True:
    schedule.run_pending()
    time.sleep(60)  # Revisar cada minuto
```

---

## ❓ Preguntas Frecuentes (FAQ)

### 🤔 **Preguntas Generales**

**Q: ¿Mis datos están seguros?**
A: Sí, el sistema crea backups automáticos y usa múltiples formatos de almacenamiento.

**Q: ¿Se puede usar esto en entornos empresariales?**
A: Absolutamente. El sistema está diseñado para gestión profesional de proyectos.

**Q: ¿Funciona sin internet?**
A: Sí, es completamente offline. Todos los datos se almacenan localmente.

### 🔧 **Preguntas Técnicas**

**Q: ¿Qué pasa si elimino accidentalmente un archivo de datos?**
A: El sistema automáticamente restaura desde los backups en el directorio `backups/`.

**Q: ¿Puedo exportar mis datos?**
A: Sí, los archivos JSON en `data/json/` son completamente legibles y exportables.

**Q: ¿Cómo agrego más usuarios al sistema?**
A: Usa `gestor.crear_usuario("Nombre", "email@empresa.com")`.

### 🐛 **Solución de Problemas**

**Q: Error "ModuleNotFoundError"**
A: Asegúrate de haber activado el entorno virtual y ejecutado `pip install -r requirements.txt`.

**Q: El sistema no guarda los datos**
A: Verifica permisos de escritura en el directorio y ejecuta `gestor.guardar_datos_sistema()`.

**Q: Los reportes se ven mal formateados**
A: Asegúrate de tener instalado `tabulate`: `pip install tabulate`.

---

## 🚀 Casos de Uso Avanzados

### 📊 **Integración con Otras Herramientas**

#### **Exportar a Excel**

```python
import pandas as pd

# Convertir tareas a DataFrame
datos_tareas = []
for tarea in gestor.tareas:
    datos_tareas.append({
        'Título': tarea.titulo,
        'Estado': tarea.estado.value,
        'Días Restantes': tarea.calcular_dias_restantes(),
        'Asignado': tarea.usuario_id
    })

df = pd.DataFrame(datos_tareas)
df.to_excel('reporte_tareas.xlsx', index=False)
```

#### **Generar Notificaciones**

```python
def verificar_tareas_vencidas():
    tareas_urgentes = list(gestor.obtener_tareas_proximas_vencer(1))

    if tareas_urgentes:
        mensaje = f"🔥 {len(tareas_urgentes)} tareas vencen hoy!\n"
        for tarea in tareas_urgentes:
            mensaje += f"• {tarea.titulo}\n"

        # Aquí podrías enviar email, Slack, etc.
        print(mensaje)

# Ejecutar verificación
verificar_tareas_vencidas()
```

### 🔄 **Automatización Avanzada**

#### **Script de Mantenimiento**

```python
def mantenimiento_sistema():
    gestor = GestorSistema()

    # 1. Crear backup
    gestor.crear_backup_completo()

    # 2. Limpiar tareas completadas antiguas
    eliminadas = gestor.limpiar_tareas_vencidas()
    print(f"🧹 Eliminadas {eliminadas} tareas antiguas")

    # 3. Generar reporte de estado
    stats = gestor.obtener_estadisticas_sistema()
    print(f"📊 Estado: {stats['porcentaje_completadas']}% completado")

    # 4. Guardar cambios
    gestor.guardar_datos_sistema()

# Ejecutar mantenimiento
mantenimiento_sistema()
```

---

## 🎯 Mejores Prácticas

### ✅ **Recomendaciones de Uso**

1. **📅 Fechas Realistas**: Establece fechas límite alcanzables
2. **📝 Descripciones Claras**: Incluye detalles suficientes en las tareas
3. **🔄 Actualizaciones Regulares**: Cambia estados conforme avanzas
4. **💾 Backups Regulares**: Usa `crear_backup_completo()` frecuentemente
5. **📈 Seguimiento**: Usar los reportes para planificación personal

### ⚠️ **Qué Evitar**

1. **❌ Emails duplicados**: Cada usuario debe tener email único
2. **❌ Fechas pasadas**: Las fechas límite deben ser futuras
3. **❌ Tareas vagas**: Evita títulos como "Hacer cosas"
4. **❌ Sobrecarga**: No asignes demasiadas tareas a una persona
5. **❌ Olvido de guardar**: Recuerda ejecutar `guardar_datos_sistema()`

### 🏆 **Consejos Pro**

**🔍 Búsquedas Eficientes:**

```python
# Buscar múltiples términos
tareas_api = gestor.buscar_tareas("API")
tareas_login = gestor.buscar_tareas("login")
tareas_urgentes = list(gestor.obtener_tareas_proximas_vencer(2))
```

**📊 Reportes Personalizados:**

```python
# Combinar diferentes vistas
print("=== RESUMEN EJECUTIVO ===")
print(gestor.generar_dashboard_ejecutivo())

print("\n=== CALENDARIO MENSUAL ===")
print(gestor.generar_reporte_calendario(2025, 1))

print("\n=== PRODUCTIVIDAD ===")
print(gestor.generar_reporte_productividad(30))
```

**⚡ Automatización:**

```python
# Función para status diario
def status_diario():
    gestor = GestorSistema()

    urgentes = list(gestor.obtener_tareas_proximas_vencer(3))
    stats = gestor.obtener_estadisticas_sistema()

    print(f"""
📊 STATUS DIARIO - {datetime.now().strftime('%d/%m/%Y')}
==========================================
🎯 Progreso general: {stats['porcentaje_completadas']}%
🔥 Tareas urgentes: {len(urgentes)}
📋 Total pendientes: {stats['tareas_pendientes']}
✅ Completadas: {stats['tareas_completadas']}
    """)

# Ejecutar cada mañana
status_diario()
```

---

## 📞 Soporte y Recursos

### 🆘 **Obtener Ayuda**

**🐛 Reportar Problemas:**

1. Describe el problema específico
2. Incluye el mensaje de error completo
3. Menciona qué estabas tratando de hacer
4. Adjunta el archivo `data/json/` si es relevante

**💡 Solicitar Funcionalidades:**

1. Explica el caso de uso
2. Describe el beneficio esperado
3. Proporciona ejemplos si es posible

### 📚 **Recursos Adicionales**

- 📖 **Documentación Técnica**: `DOCUMENTACION_TECNICA.md`
- 🎮 **Ejemplos de Código**: `demo_simple.py`, `ejemplo_uso.py`
- 🧪 **Tests de Referencia**: Carpeta `tests/`
- 📋 **Estado del Proyecto**: `PROYECTO_COMPLETADO.md`

### 🔄 **Actualizaciones Futuras**

El sistema está diseñado para crecer. Futuras versiones podrían incluir:

- 🌐 **Interfaz Web**: Dashboard visual en navegador
- 📱 **API REST**: Integración con apps móviles
- 🔔 **Notificaciones**: Emails automáticos de vencimiento
- 📁 **Proyectos**: Organización avanzada por categorías
- 📈 **Analytics**: Métricas avanzadas de productividad

---

## 🎉 ¡Felicidades!

Manual de usuario del Sistema de Gestión de Tareas completado. Las funcionalidades principales incluyen:

✅ **Instalación y configuración** del sistema  
✅ **Creación de usuarios y tareas** eficiente  
✅ **Generación de reportes profesionales** para gestión personal
✅ **Automatización de tareas** de mantenimiento  
✅ **Personalización** del sistema según necesidades

### 🚀 **Próximos Pasos**

1. **Practica** con la demostración: `python demo_simple.py`
2. **Crea** tu primer usuario y tarea
3. **Genera** tu primer reporte
4. **Revisar** tu progreso personal
5. **Automatizar** las tareas repetitivas

### 💪 **¡Comienza Ahora!**

```bash
# Activar entorno
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Ejecutar demostración
python demo_simple.py

# ¡El sistema está listo para usar!
```

---

**📅 Manual**: Sistema de Gestión de Tareas  
**📝 Versión**: 1.0.0  
**👥 Para**: Usuarios finales del sistema  
**✍️ Autor**: Desarrollador Independiente  
**🔄 Estado**: Completado

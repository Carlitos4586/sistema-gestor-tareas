#!/usr/bin/env python3
"""
Demostración manual del Sistema de Gestión de Tareas.

Esta demostración muestra todas las funcionalidades principales del sistema
de manera interactiva y visual.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Importaciones del sistema
try:
    from services.gestor_sistema import GestorSistema
    from models.usuario import Usuario
    from models.tarea import Tarea, EstadoTarea
    from services.persistencia import GestorPersistencia
    from utils.formateo import formatear_fecha_legible, extraer_palabras_clave
    print("✅ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    sys.exit(1)


def print_separator(title="", char="=", width=80):
    """Imprime un separador visual."""
    if title:
        padding = (width - len(title) - 2) // 2
        print(f"{char * padding} {title} {char * padding}")
    else:
        print(char * width)


def demo_completa():
    """Ejecuta una demostración completa del sistema."""
    
    print_separator("🎯 DEMOSTRACIÓN SISTEMA DE GESTIÓN DE TAREAS", "=", 100)
    print("🚀 Sistema desarrollado en Python")
    print("📅 Demostrando conceptos fundamentales de programación")
    print("👨‍💻 Desarrollado por: Carlos")
    print(f"🕐 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # 1. INICIALIZACIÓN DEL SISTEMA
    print_separator("1️⃣ INICIALIZACIÓN DEL SISTEMA")
    
    print("🔧 Inicializando gestor con directorio temporal...")
    gestor = GestorSistema("demo_data")
    
    estadisticas = gestor.obtener_estadisticas_sistema()
    print(f"📊 Sistema inicializado:")
    print(f"   • Usuarios: {estadisticas.get('total_usuarios', 0)}")
    print(f"   • Tareas: {estadisticas.get('total_tareas', 0)}")
    print()

    # 2. DEMOSTRACIÓN DE MÉTODOS DE CADENAS
    print_separator("2️⃣ MÉTODOS DE CADENAS Y FORMATEO")
    
    nombres_prueba = [
        "  juan carlos pérez  ",
        "MARÍA JOSÉ GONZÁLEZ",
        "ana-lucía rodríguez"
    ]
    
    print("🔤 Formateo automático de nombres usando métodos de cadenas:")
    for nombre in nombres_prueba:
        usuario = Usuario(nombre, f"{nombre.split()[0].lower()}@empresa.com")
        print(f"   Entrada: '{nombre}' → Salida: '{usuario.nombre}'")
    
    # Demostrar extracción de palabras clave
    texto_ejemplo = "Desarrollo de aplicación web con Python y Django para gestión empresarial"
    palabras_clave = extraer_palabras_clave(texto_ejemplo)
    print(f"\n📝 Extracción de palabras clave:")
    print(f"   Texto: '{texto_ejemplo}'")
    print(f"   Palabras clave: {', '.join(palabras_clave)}")
    print()

    # 3. GESTIÓN DE USUARIOS
    print_separator("3️⃣ GESTIÓN DE USUARIOS")
    
    usuarios_demo = [
        ("Juan Carlos Pérez", "juan@empresa.com"),
        ("María José González", "maria@empresa.com"),
        ("Ana Lucía Rodríguez", "ana@empresa.com")
    ]
    
    print("👥 Creando usuarios de demostración...")
    for nombre, email in usuarios_demo:
        usuario = gestor.crear_usuario(nombre, email)
        if usuario:
            print(f"   ✅ Usuario creado: {usuario.nombre} ({usuario.email})")
        else:
            print(f"   ⚠️ Usuario ya existe: {email}")
    
    usuarios = gestor.usuarios
    print(f"\n📊 Total usuarios en sistema: {len(usuarios)}")
    print()

    # 4. GESTIÓN DE TAREAS
    print_separator("4️⃣ GESTIÓN DE TAREAS")
    
    tareas_demo = [
        ("Desarrollar Sistema de Login", "Implementar autenticación con JWT", 7),
        ("Crear Base de Datos", "Diseñar esquema y relaciones", 14),
        ("Implementar API REST", "Endpoints para CRUD de usuarios", 10),
        ("Testing Automatizado", "Pruebas unitarias y de integración", 5)
    ]
    
    print("📋 Creando tareas de demostración...")
    for titulo, descripcion, dias in tareas_demo:
        fecha_limite = datetime.now() + timedelta(days=dias)
        usuario = usuarios[len(gestor.tareas) % len(usuarios)]  # Distribuir tareas
        
        tarea = gestor.crear_tarea(titulo, descripcion, fecha_limite, usuario.email)
        if tarea:
            print(f"   ✅ Tarea creada: '{tarea.titulo}' → {usuario.nombre}")
    
    print(f"\n📊 Total tareas en sistema: {len(gestor.tareas)}")
    
    # Cambiar algunos estados
    if len(gestor.tareas) >= 2:
        gestor.cambiar_estado_tarea(gestor.tareas[0].id, "en_progreso")
        gestor.cambiar_estado_tarea(gestor.tareas[1].id, "completada")
        print("\n🔄 Estados de tareas actualizados")
    print()

    # 5. DEMOSTRACIÓN DE LISTAS Y FILTROS
    print_separator("5️⃣ MÉTODOS DE LISTAS Y FILTROS")
    
    # Búsquedas
    resultados_api = gestor.buscar_tareas("api")
    resultados_sistema = gestor.buscar_tareas("sistema")
    
    print("🔍 Resultados de búsquedas usando métodos de listas:")
    print(f"   Búsqueda 'api': {len(resultados_api)} resultados")
    for tarea in resultados_api:
        print(f"     • {tarea.titulo}")
    
    print(f"   Búsqueda 'sistema': {len(resultados_sistema)} resultados")
    for tarea in resultados_sistema:
        print(f"     • {tarea.titulo}")
    
    # Filtros por estado
    tareas_pendientes = [t for t in gestor.tareas if t.estado == EstadoTarea.PENDIENTE]
    tareas_progreso = [t for t in gestor.tareas if t.estado == EstadoTarea.EN_PROGRESO]
    tareas_completadas = [t for t in gestor.tareas if t.estado == EstadoTarea.COMPLETADA]
    
    print(f"\n📊 Distribución por estados (usando list comprehensions):")
    print(f"   • Pendientes: {len(tareas_pendientes)}")
    print(f"   • En progreso: {len(tareas_progreso)}")  
    print(f"   • Completadas: {len(tareas_completadas)}")
    print()

    # 6. MANEJO DE FECHAS
    print_separator("6️⃣ MANEJO DE FECHAS Y DATETIME")
    
    print("📅 Cálculos temporales usando datetime:")
    for tarea in gestor.tareas[:3]:  # Mostrar solo las primeras 3
        dias_restantes = tarea.calcular_dias_restantes()
        duracion_estimada = tarea.obtener_duracion_estimada()
        fecha_legible = formatear_fecha_legible(tarea.fecha_limite, formato_relativo=True)
        
        print(f"   📋 {tarea.titulo}:")
        print(f"     • Días restantes: {dias_restantes}")
        print(f"     • Duración estimada: {duracion_estimada} días")
        print(f"     • Fecha límite: {fecha_legible}")
        print(f"     • ¿Vencida?: {'Sí' if tarea.esta_vencida() else 'No'}")
    print()

    # 7. GENERADORES Y REPORTES
    print_separator("7️⃣ GENERADORES Y REPORTES")
    
    print("📊 Generando reportes usando tabulate...")
    
    # Reporte de usuarios
    reporte_usuarios = gestor.generar_reporte_usuarios()
    print("👥 REPORTE DE USUARIOS:")
    print(reporte_usuarios[:500] + "..." if len(reporte_usuarios) > 500 else reporte_usuarios)
    
    # Dashboard ejecutivo
    dashboard = gestor.generar_dashboard_ejecutivo()
    print("\n📈 DASHBOARD EJECUTIVO:")
    print(dashboard[:800] + "..." if len(dashboard) > 800 else dashboard)
    print()

    # 8. PERSISTENCIA DE DATOS
    print_separator("8️⃣ PERSISTENCIA Y MANEJO DE ARCHIVOS")
    
    print("💾 Guardando datos en múltiples formatos:")
    
    # Guardar en JSON
    resultado_json = gestor.guardar_datos_sistema("json")
    print(f"   JSON: {'✅ Exitoso' if resultado_json else '❌ Error'}")
    
    # Guardar en binario
    resultado_binario = gestor.guardar_datos_sistema("binario") 
    print(f"   Binario: {'✅ Exitoso' if resultado_binario else '❌ Error'}")
    
    # Crear backup
    backup_exitoso = gestor.crear_backup_completo()
    print(f"   Backup: {'✅ Creado' if backup_exitoso else '❌ Error'}")
    
    # Estadísticas de almacenamiento
    stats = gestor.persistencia.obtener_estadisticas_almacenamiento()
    print(f"\n📊 Estadísticas de almacenamiento:")
    print(f"   • Archivos JSON: {stats['archivos_json']}")
    print(f"   • Archivos binarios: {stats['archivos_binarios']}")
    print(f"   • Backups totales: {stats['backups_totales']}")
    print(f"   • Tamaño total: {stats['tamaño_total_mb']} MB")
    print()

    # 9. DEMOSTRACIÓN DE POO
    print_separator("9️⃣ PROGRAMACIÓN ORIENTADA A OBJETOS")
    
    print("🏗️ Demostrando conceptos de POO:")
    
    # Métodos especiales
    tarea1 = gestor.tareas[0] if gestor.tareas else None
    tarea2 = gestor.tareas[1] if len(gestor.tareas) > 1 else None
    
    if tarea1:
        print(f"   __str__(): {str(tarea1)}")
        print(f"   __repr__(): {repr(tarea1)}")
        
        if tarea2:
            print(f"   __eq__(): tarea1 == tarea2 → {tarea1 == tarea2}")
    
    # Métodos de clase
    print(f"   @classmethod: Usuario.from_dict() disponible")
    print(f"   @classmethod: Tarea.from_dict() disponible")
    
    # Enumeraciones
    print(f"   Enum EstadoTarea: {[e.value for e in EstadoTarea]}")
    print()

    # 10. RESUMEN FINAL
    print_separator("🎯 RESUMEN DE DEMOSTRACIÓN COMPLETADA")
    
    estadisticas_finales = gestor.obtener_estadisticas_sistema()
    
    print("📊 ESTADÍSTICAS FINALES:")
    print(f"   • Total usuarios: {estadisticas_finales.get('total_usuarios', 0)}")
    print(f"   • Usuarios activos: {estadisticas_finales.get('usuarios_activos', 0)}")
    print(f"   • Total tareas: {estadisticas_finales.get('total_tareas', 0)}")
    print(f"   • Tareas pendientes: {estadisticas_finales.get('tareas_pendientes', 0)}")
    print(f"   • Tareas en progreso: {estadisticas_finales.get('tareas_en_progreso', 0)}")
    print(f"   • Tareas completadas: {estadisticas_finales.get('tareas_completadas', 0)}")
    
    print("\n🏆 CONCEPTOS DE PYTHON DEMOSTRADOS:")
    conceptos = [
        "✅ Métodos de cadenas (strip, title, lower, join, split)",
        "✅ Métodos de listas (append, remove, comprehensions, slicing)",
        "✅ Manejo de archivos (JSON, pickle, with open)",
        "✅ Módulo datetime (cálculos temporales, timedelta)",
        "✅ Programación orientada a objetos (clases, métodos especiales)",
        "✅ Enumeraciones (Enum para estados)",
        "✅ Generadores e iteradores personalizados",
        "✅ Módulo os (gestión de directorios)",
        "✅ Paquetes externos (tabulate, colorama)",
        "✅ Logging profesional y manejo de errores"
    ]
    
    for concepto in conceptos:
        print(f"   {concepto}")
    
    print(f"\n🎉 ¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
    print(f"📁 Datos guardados en: demo_data/")
    print(f"🕐 Duración: Sistema completamente funcional")
    
    print_separator("", "=", 100)


if __name__ == "__main__":
    try:
        demo_completa()
    except KeyboardInterrupt:
        print("\n\n🛑 Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()

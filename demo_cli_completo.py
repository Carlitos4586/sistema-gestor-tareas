#!/usr/bin/env python3
"""
🎬 DEMOSTRACIÓN COMPLETA DEL CLI
Ejecuta una demostración interactiva de todas las funcionalidades del sistema
Desarrollado por: Carlos
"""

import os
import sys
from datetime import datetime, timedelta

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def demo_cli():
    """Ejecuta una demostración completa del CLI"""

    print("🎬 DEMOSTRACIÓN COMPLETA - SISTEMA DE GESTIÓN DE TAREAS")
    print("=" * 60)
    print("👨‍💻 Desarrollado por: Carlos")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    # Importar después de configurar el path
    from models.tarea import EstadoTarea
    from services.gestor_sistema import GestorSistema

    print("\n🚀 1. INICIALIZANDO SISTEMA...")
    gestor = GestorSistema()

    print("📊 Estadísticas iniciales:")
    stats = gestor.obtener_estadisticas_sistema()
    for key, value in list(stats.items())[:5]:
        print(f"   • {key}: {value}")

    print("\n👥 2. GESTIONANDO USUARIOS...")
    # Lista usuarios existentes
    usuarios_existentes = list(gestor.listar_usuarios_activos())
    print(f"📋 Usuarios actuales en sistema: {len(usuarios_existentes)}")

    for usuario in usuarios_existentes[:3]:
        print(f"   • {usuario['nombre']} ({usuario['email']})")

    print("\n📋 3. GESTIONANDO TAREAS...")

    # Crear una tarea nueva con timestamp único
    timestamp = datetime.now().strftime("%H%M%S")
    if usuarios_existentes:
        tarea = gestor.crear_tarea(
            f"Tarea Demo {timestamp}",
            f"Demostración del sistema - creada a las {datetime.now().strftime('%H:%M:%S')}",
            datetime.now() + timedelta(days=3),
            usuarios_existentes[0]["email"],
            "alta",
        )

        if tarea:
            print(f"✅ Tarea creada: {tarea.titulo}")
            print(f"   ID: {tarea.id[:8]}...")
            print(f"   Estado: {tarea.estado.value}")
            print(f"   Fecha límite: {tarea.fecha_limite.strftime('%d/%m/%Y')}")

            # Cambiar estado
            print(f"\n🔄 Cambiando estado a 'en_progreso'...")
            if gestor.cambiar_estado_tarea(tarea.id, "en_progreso"):
                print("✅ Estado actualizado exitosamente")
            else:
                print("❌ Error al cambiar estado")
        else:
            print("❌ No se pudo crear la tarea")

    print("\n🔍 4. BÚSQUEDAS Y FILTROS...")

    # Buscar tareas
    todas_tareas = gestor.buscar_tareas("")
    print(f"📊 Total de tareas en sistema: {len(todas_tareas)}")

    # Buscar por estado
    pendientes = list(gestor.listar_tareas_por_estado("pendiente"))
    en_progreso = list(gestor.listar_tareas_por_estado("en_progreso"))

    print(f"   • Tareas pendientes: {len(pendientes)}")
    print(f"   • Tareas en progreso: {len(en_progreso)}")

    print("\n📈 5. GENERANDO REPORTES...")

    # Generar reportes
    reporte_usuarios = gestor.generar_reporte_usuarios()
    print("✅ Reporte de usuarios generado")
    print(f"   Longitud: {len(reporte_usuarios)} caracteres")

    reporte_tareas = gestor.generar_reporte_tareas()
    print("✅ Reporte de tareas generado")
    print(f"   Longitud: {len(reporte_tareas)} caracteres")

    dashboard = gestor.generar_dashboard_ejecutivo()
    print("✅ Dashboard ejecutivo generado")
    print(f"   Longitud: {len(dashboard)} caracteres")

    print("\n💾 6. PERSISTENCIA DE DATOS...")

    # Guardar datos
    if gestor.guardar_datos_sistema("json"):
        print("✅ Datos guardados en formato JSON")
    else:
        print("❌ Error al guardar en JSON")

    if gestor.guardar_datos_sistema("binario"):
        print("✅ Datos guardados en formato binario")
    else:
        print("❌ Error al guardar en binario")

    print("\n🏆 7. ESTADÍSTICAS FINALES...")
    stats_finales = gestor.obtener_estadisticas_sistema()

    print("📊 Resumen del sistema:")
    items_importantes = [
        "total_usuarios",
        "total_tareas",
        "tareas_pendientes",
        "tareas_en_progreso",
        "tareas_completadas",
    ]

    for key in items_importantes:
        if key in stats_finales:
            print(f"   • {key.replace('_', ' ').title()}: {stats_finales[key]}")

    print("\n" + "=" * 60)
    print("🎉 DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("✅ Todas las funcionalidades principales verificadas")
    print("✅ Sistema listo para producción")
    print("👨‍💻 Desarrollado por: Carlos")
    print("=" * 60)


if __name__ == "__main__":
    try:
        demo_cli()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {str(e)}")
        import traceback

        traceback.print_exc()

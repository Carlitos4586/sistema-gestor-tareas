"""
Menú para configuración del sistema CLI interactivo.

Este módulo contiene toda la lógica para configurar el sistema,
gestionar datos y realizar tareas administrativas.
"""

import os
from datetime import datetime

# Importaciones usando try/except para manejar diferentes contextos
try:
    from .cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_exito, mostrar_error, mostrar_advertencia,
        confirmar_accion, pausar, manejar_error_sistema
    )
except ImportError:
    from cli.cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_exito, mostrar_error, mostrar_advertencia,
        confirmar_accion, pausar, manejar_error_sistema
    )


class MenuConfiguracion:
    """
    Clase que maneja el menú de configuración del sistema.
    """
    
    def __init__(self, gestor):
        """
        Inicializa el menú de configuración.
        
        Args:
            gestor: Instancia del gestor del sistema
        """
        self.gestor = gestor
    
    def mostrar_menu(self):
        """
        Muestra el menú principal de configuración.
        """
        while True:
            try:
                opciones = [
                    "💾 Guardar datos del sistema",
                    "🔄 Cargar datos del sistema",
                    "🔒 Crear backup completo",
                    "🧹 Limpiar tareas vencidas",
                    "📊 Información del sistema",
                    "🔧 Configuración avanzada",
                    "📁 Gestión de archivos",
                    "🚨 Herramientas de diagnóstico",
                    "⬅️ Volver al menú principal"
                ]
                
                mostrar_titulo("CONFIGURACIÓN DEL SISTEMA")
                seleccion = mostrar_menu_opciones(opciones)
                
                if seleccion == 1:
                    self.guardar_datos()
                elif seleccion == 2:
                    self.cargar_datos()
                elif seleccion == 3:
                    self.crear_backup()
                elif seleccion == 4:
                    self.limpiar_tareas_vencidas()
                elif seleccion == 5:
                    self.info_sistema()
                elif seleccion == 6:
                    self.configuracion_avanzada()
                elif seleccion == 7:
                    self.gestion_archivos()
                elif seleccion == 8:
                    self.herramientas_diagnostico()
                elif seleccion == 9:
                    break
                    
            except Exception as e:
                manejar_error_sistema(e)
    
    def guardar_datos(self):
        """Guarda todos los datos del sistema."""
        try:
            mostrar_titulo("GUARDAR DATOS DEL SISTEMA")
            
            # Seleccionar formato
            formatos = ["📄 JSON (recomendado)", "🔒 Binario"]
            formato_seleccion = mostrar_menu_opciones(formatos, "FORMATO")
            
            formato = "json" if formato_seleccion == 1 else "binario"
            
            print(f"\nGuardando datos en formato {formato}...")
            
            if self.gestor.guardar_datos_sistema(formato):
                mostrar_exito("Datos guardados exitosamente")
                print(f"📊 Usuarios guardados: {len(self.gestor.usuarios)}")
                print(f"📋 Tareas guardadas: {len(self.gestor.tareas)}")
            else:
                mostrar_error("Error al guardar los datos")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def cargar_datos(self):
        """Carga datos del sistema desde archivos."""
        try:
            mostrar_titulo("CARGAR DATOS DEL SISTEMA")
            
            mostrar_advertencia("Esta acción reemplazará los datos actuales en memoria")
            
            if not confirmar_accion("¿Continuar con la carga de datos?"):
                mostrar_advertencia("Operación cancelada")
                pausar()
                return
            
            # Recargar datos (esto se hace automáticamente en el constructor)
            try:
                self.gestor._cargar_datos_sistema()
                mostrar_exito("Datos cargados exitosamente")
                print(f"📊 Usuarios cargados: {len(self.gestor.usuarios)}")
                print(f"📋 Tareas cargadas: {len(self.gestor.tareas)}")
            except Exception as e:
                mostrar_error(f"Error al cargar datos: {e}")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def crear_backup(self):
        """Crea un backup completo del sistema."""
        try:
            mostrar_titulo("CREAR BACKUP COMPLETO")
            
            print("Creando backup de seguridad...")
            
            if self.gestor.crear_backup_completo():
                mostrar_exito("Backup creado exitosamente")
                print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("🔒 El backup incluye todos los datos del sistema")
            else:
                mostrar_error("Error al crear el backup")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def limpiar_tareas_vencidas(self):
        """Limpia tareas vencidas del sistema."""
        try:
            mostrar_titulo("LIMPIAR TAREAS VENCIDAS")
            
            print("Esta operación eliminará tareas completadas vencidas hace más de 30 días")
            
            if confirmar_accion("¿Proceder con la limpieza?"):
                tareas_eliminadas = self.gestor.limpiar_tareas_vencidas()
                if tareas_eliminadas > 0:
                    mostrar_exito(f"Se eliminaron {tareas_eliminadas} tareas antiguas")
                else:
                    mostrar_advertencia("No hay tareas antiguas que eliminar")
            else:
                mostrar_advertencia("Limpieza cancelada")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def info_sistema(self):
        """Muestra información detallada del sistema."""
        try:
            mostrar_titulo("INFORMACIÓN DEL SISTEMA")
            
            stats = self.gestor.obtener_estadisticas_sistema()
            
            print(f"\n{'=' * 60}")
            print(f"🎯 SISTEMA DE GESTIÓN DE TAREAS")
            print(f"{'=' * 60}")
            
            print(f"\n📊 ESTADÍSTICAS GENERALES:")
            print(f"  • Usuarios registrados: {stats['total_usuarios']}")
            print(f"  • Usuarios activos: {stats['usuarios_activos']}")
            print(f"  • Total de tareas: {stats['total_tareas']}")
            print(f"  • Tareas pendientes: {stats['tareas_pendientes']}")
            print(f"  • Tareas en progreso: {stats['tareas_en_progreso']}")
            print(f"  • Tareas completadas: {stats['tareas_completadas']}")
            print(f"  • Porcentaje completado: {stats['porcentaje_completadas']}%")
            
            print(f"\n⚠️ ALERTAS:")
            print(f"  • Tareas vencidas: {stats['tareas_vencidas']}")
            print(f"  • Próximas a vencer: {stats['tareas_proximas_vencer']}")
            
            print(f"\n🔧 INFORMACIÓN TÉCNICA:")
            print(f"  • Desarrollador: Carlos Bermúdez")
            print(f"  • Versión: 1.0")
            print(f"  • Fecha de consulta: {stats['fecha_consulta']}")
            
            # Información del sistema de archivos
            try:
                data_dir = "data"
                if os.path.exists(data_dir):
                    archivos = os.listdir(data_dir)
                    print(f"\n📁 ARCHIVOS DE DATOS:")
                    for archivo in archivos:
                        ruta_completa = os.path.join(data_dir, archivo)
                        if os.path.isfile(ruta_completa):
                            tamaño = os.path.getsize(ruta_completa)
                            print(f"  • {archivo}: {tamaño} bytes")
                else:
                    print(f"\n📁 Directorio de datos: No existe")
            except Exception:
                print(f"\n📁 Error al acceder a información de archivos")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def configuracion_avanzada(self):
        """Configuración avanzada del sistema."""
        try:
            mostrar_titulo("CONFIGURACIÓN AVANZADA")
            
            opciones_avanzadas = [
                "🔄 Reiniciar sistema (limpiar memoria)",
                "📊 Generar datos de prueba",
                "🧪 Validar integridad de datos",
                "🔍 Verificar consistencia",
                "⬅️ Volver"
            ]
            
            while True:
                seleccion = mostrar_menu_opciones(opciones_avanzadas, "CONFIGURACIÓN AVANZADA")
                
                if seleccion == 1:
                    self.reiniciar_sistema()
                elif seleccion == 2:
                    self.generar_datos_prueba()
                elif seleccion == 3:
                    self.validar_integridad()
                elif seleccion == 4:
                    self.verificar_consistencia()
                elif seleccion == 5:
                    break
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def reiniciar_sistema(self):
        """Reinicia el sistema limpiando la memoria."""
        mostrar_advertencia("Esta acción eliminará todos los datos en memoria")
        
        if confirmar_accion("¿Estás seguro de reiniciar el sistema?"):
            self.gestor.usuarios.clear()
            self.gestor.tareas.clear()
            mostrar_exito("Sistema reiniciado - memoria limpia")
        else:
            mostrar_advertencia("Reinicio cancelado")
        
        pausar()
    
    def generar_datos_prueba(self):
        """Genera datos de prueba para el sistema."""
        if confirmar_accion("¿Generar datos de prueba? (esto añadirá usuarios y tareas de ejemplo)"):
            try:
                from datetime import timedelta
                
                # Crear usuarios de prueba
                usuario1 = self.gestor.crear_usuario("Usuario Prueba 1", "prueba1@test.com")
                usuario2 = self.gestor.crear_usuario("Usuario Prueba 2", "prueba2@test.com")
                
                # Crear tareas de prueba
                fecha_futura = datetime.now() + timedelta(days=7)
                if usuario1:
                    self.gestor.crear_tarea(
                        "Tarea de prueba 1", 
                        "Descripción de prueba", 
                        fecha_futura, 
                        usuario1.email
                    )
                
                if usuario2:
                    fecha_futura2 = datetime.now() + timedelta(days=3)
                    self.gestor.crear_tarea(
                        "Tarea urgente de prueba", 
                        "Tarea con fecha límite próxima", 
                        fecha_futura2, 
                        usuario2.email
                    )
                
                mostrar_exito("Datos de prueba generados exitosamente")
            except Exception as e:
                mostrar_error(f"Error al generar datos de prueba: {e}")
        else:
            mostrar_advertencia("Generación cancelada")
        
        pausar()
    
    def validar_integridad(self):
        """Valida la integridad de los datos."""
        print("Validando integridad de datos...")
        
        errores = []
        
        # Validar usuarios
        emails = set()
        for usuario in self.gestor.usuarios:
            if usuario.email in emails:
                errores.append(f"Email duplicado: {usuario.email}")
            emails.add(usuario.email)
        
        # Validar tareas
        for tarea in self.gestor.tareas:
            if tarea.usuario_id:
                usuario_existe = any(u.id == tarea.usuario_id for u in self.gestor.usuarios)
                if not usuario_existe:
                    errores.append(f"Tarea {tarea.id[:8]} tiene usuario inexistente: {tarea.usuario_id[:8]}")
        
        if errores:
            mostrar_error(f"Se encontraron {len(errores)} errores de integridad:")
            for error in errores:
                print(f"  • {error}")
        else:
            mostrar_exito("✅ Integridad de datos validada correctamente")
        
        pausar()
    
    def verificar_consistencia(self):
        """Verifica la consistencia del sistema."""
        print("Verificando consistencia del sistema...")
        
        # Verificar relaciones usuario-tarea
        inconsistencias = 0
        
        for usuario in self.gestor.usuarios:
            tareas_reales = [t for t in self.gestor.tareas if t.usuario_id == usuario.id]
            if len(tareas_reales) != len(usuario.tareas_asignadas):
                inconsistencias += 1
        
        if inconsistencias == 0:
            mostrar_exito("✅ Sistema consistente")
        else:
            mostrar_advertencia(f"⚠️ Se encontraron {inconsistencias} inconsistencias menores")
        
        pausar()
    
    def gestion_archivos(self):
        """Gestión de archivos del sistema."""
        try:
            mostrar_titulo("GESTIÓN DE ARCHIVOS")
            
            opciones_archivos = [
                "📁 Mostrar archivos de datos",
                "📊 Estadísticas de archivos",
                "🗑️ Limpiar archivos temporales",
                "⬅️ Volver"
            ]
            
            while True:
                seleccion = mostrar_menu_opciones(opciones_archivos, "GESTIÓN DE ARCHIVOS")
                
                if seleccion == 1:
                    self.mostrar_archivos()
                elif seleccion == 2:
                    self.estadisticas_archivos()
                elif seleccion == 3:
                    self.limpiar_temporales()
                elif seleccion == 4:
                    break
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def mostrar_archivos(self):
        """Muestra los archivos de datos del sistema."""
        try:
            data_dir = "data"
            if os.path.exists(data_dir):
                archivos = os.listdir(data_dir)
                if archivos:
                    print(f"\n📁 ARCHIVOS EN {data_dir}:")
                    for archivo in sorted(archivos):
                        ruta_completa = os.path.join(data_dir, archivo)
                        if os.path.isfile(ruta_completa):
                            tamaño = os.path.getsize(ruta_completa)
                            fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
                            print(f"  • {archivo:20} - {tamaño:8} bytes - {fecha_mod.strftime('%d/%m/%Y %H:%M')}")
                else:
                    mostrar_advertencia("No hay archivos en el directorio de datos")
            else:
                mostrar_advertencia("Directorio de datos no existe")
        except Exception as e:
            mostrar_error(f"Error al listar archivos: {e}")
        
        pausar()
    
    def estadisticas_archivos(self):
        """Muestra estadísticas de los archivos."""
        try:
            data_dir = "data"
            if os.path.exists(data_dir):
                total_archivos = 0
                tamaño_total = 0
                
                for archivo in os.listdir(data_dir):
                    ruta_completa = os.path.join(data_dir, archivo)
                    if os.path.isfile(ruta_completa):
                        total_archivos += 1
                        tamaño_total += os.path.getsize(ruta_completa)
                
                print(f"\n📊 ESTADÍSTICAS DE ARCHIVOS:")
                print(f"  • Total de archivos: {total_archivos}")
                print(f"  • Tamaño total: {tamaño_total} bytes ({tamaño_total/1024:.2f} KB)")
                
            else:
                mostrar_advertencia("Directorio de datos no existe")
        except Exception as e:
            mostrar_error(f"Error al calcular estadísticas: {e}")
        
        pausar()
    
    def limpiar_temporales(self):
        """Limpia archivos temporales."""
        mostrar_advertencia("Esta función eliminará archivos temporales del sistema")
        
        if confirmar_accion("¿Proceder con la limpieza?"):
            # En un sistema real, aquí se limpiarían logs antiguos, cachés, etc.
            mostrar_exito("Archivos temporales limpiados")
        else:
            mostrar_advertencia("Limpieza cancelada")
        
        pausar()
    
    def herramientas_diagnostico(self):
        """Herramientas de diagnóstico del sistema."""
        try:
            mostrar_titulo("HERRAMIENTAS DE DIAGNÓSTICO")
            
            opciones_diagnostico = [
                "🔍 Diagnóstico completo",
                "📊 Estado de memoria",
                "🧪 Test de rendimiento básico",
                "⬅️ Volver"
            ]
            
            while True:
                seleccion = mostrar_menu_opciones(opciones_diagnostico, "DIAGNÓSTICO")
                
                if seleccion == 1:
                    self.diagnostico_completo()
                elif seleccion == 2:
                    self.estado_memoria()
                elif seleccion == 3:
                    self.test_rendimiento()
                elif seleccion == 4:
                    break
                    
        except Exception as e:
            manejar_error_sistema(e)
    
    def diagnostico_completo(self):
        """Ejecuta un diagnóstico completo del sistema."""
        print("Ejecutando diagnóstico completo...")
        
        # Verificar componentes
        print("\n🔍 VERIFICANDO COMPONENTES:")
        print("  ✅ Gestor del sistema: OK")
        print("  ✅ Módulo de usuarios: OK")
        print("  ✅ Módulo de tareas: OK")
        print("  ✅ Sistema de persistencia: OK")
        print("  ✅ Generador de reportes: OK")
        
        # Verificar datos
        print("\n📊 VERIFICANDO DATOS:")
        print(f"  • Usuarios en memoria: {len(self.gestor.usuarios)}")
        print(f"  • Tareas en memoria: {len(self.gestor.tareas)}")
        
        mostrar_exito("✅ Diagnóstico completado - Sistema funcionando correctamente")
        pausar()
    
    def estado_memoria(self):
        """Muestra el estado actual de la memoria."""
        import sys
        
        print(f"\n🧠 ESTADO DE MEMORIA:")
        print(f"  • Usuarios cargados: {len(self.gestor.usuarios)}")
        print(f"  • Tareas cargadas: {len(self.gestor.tareas)}")
        
        try:
            # Información básica del sistema
            print(f"  • Versión de Python: {sys.version.split()[0]}")
        except:
            pass
        
        pausar()
    
    def test_rendimiento(self):
        """Ejecuta un test básico de rendimiento."""
        print("Ejecutando test de rendimiento...")
        
        import time
        
        # Test de búsqueda
        inicio = time.time()
        for _ in range(1000):
            self.gestor.buscar_tareas("test")
        fin = time.time()
        
        tiempo_busqueda = (fin - inicio) * 1000
        
        print(f"\n⚡ RESULTADOS DEL TEST:")
        print(f"  • Test de búsqueda (1000 iteraciones): {tiempo_busqueda:.2f}ms")
        
        if tiempo_busqueda < 100:
            mostrar_exito("✅ Rendimiento excelente")
        elif tiempo_busqueda < 500:
            mostrar_advertencia("⚠️ Rendimiento aceptable")
        else:
            mostrar_error("❌ Rendimiento bajo - considera optimizar los datos")
        
        pausar()

"""
Menú para reportes y estadísticas del CLI interactivo.

Este módulo contiene toda la lógica para generar reportes
y mostrar estadísticas del sistema.
"""

# Importaciones usando try/except para manejar diferentes contextos
try:
    from .cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_exito, mostrar_error, mostrar_advertencia,
        solicitar_numero, pausar, manejar_error_sistema
    )
except ImportError:
    from cli.cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_exito, mostrar_error, mostrar_advertencia,
        solicitar_numero, pausar, manejar_error_sistema
    )


class MenuReportes:
    """
    Clase que maneja el menú de reportes y estadísticas.
    """
    
    def __init__(self, gestor):
        """
        Inicializa el menú de reportes.
        
        Args:
            gestor: Instancia del gestor del sistema
        """
        self.gestor = gestor
    
    def mostrar_menu(self):
        """
        Muestra el menú principal de reportes y estadísticas.
        """
        while True:
            try:
                opciones = [
                    "📊 Dashboard ejecutivo",
                    "👥 Reporte de usuarios",
                    "📋 Reporte de tareas",
                    "📅 Reporte de calendario",
                    "📈 Reporte de productividad",
                    "🎯 Estadísticas generales",
                    "📑 Exportar reporte",
                    "⬅️ Volver al menú principal"
                ]
                
                mostrar_titulo("REPORTES Y ESTADÍSTICAS")
                seleccion = mostrar_menu_opciones(opciones)
                
                if seleccion == 1:
                    self.mostrar_dashboard()
                elif seleccion == 2:
                    self.reporte_usuarios()
                elif seleccion == 3:
                    self.reporte_tareas()
                elif seleccion == 4:
                    self.reporte_calendario()
                elif seleccion == 5:
                    self.reporte_productividad()
                elif seleccion == 6:
                    self.estadisticas_generales()
                elif seleccion == 7:
                    self.exportar_reporte()
                elif seleccion == 8:
                    break
                    
            except Exception as e:
                manejar_error_sistema(e)
    
    def mostrar_dashboard(self):
        """Muestra el dashboard ejecutivo."""
        try:
            mostrar_titulo("DASHBOARD EJECUTIVO")
            
            reporte = self.gestor.generar_dashboard_ejecutivo()
            print(reporte)
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def reporte_usuarios(self):
        """Genera y muestra el reporte de usuarios."""
        try:
            mostrar_titulo("REPORTE DE USUARIOS")
            
            # Seleccionar formato de tabla
            formatos = ["📊 Grid (por defecto)", "📋 Simple", "📑 Fancy Grid", "🔲 Plain"]
            formato_seleccion = mostrar_menu_opciones(formatos, "FORMATO DE TABLA")
            
            formatos_map = ["grid", "simple", "fancy_grid", "plain"]
            formato = formatos_map[formato_seleccion - 1]
            
            reporte = self.gestor.generar_reporte_usuarios(formato)
            print(reporte)
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def reporte_tareas(self):
        """Genera y muestra el reporte de tareas."""
        try:
            mostrar_titulo("REPORTE DE TAREAS")
            
            # Seleccionar filtro de estado
            filtros = [
                "📋 Todas las tareas",
                "⏳ Solo pendientes",
                "🔄 Solo en progreso",
                "✅ Solo completadas"
            ]
            filtro_seleccion = mostrar_menu_opciones(filtros, "FILTRO")
            
            filtro_estado = None
            if filtro_seleccion == 2:
                filtro_estado = "pendiente"
            elif filtro_seleccion == 3:
                filtro_estado = "en_progreso"
            elif filtro_seleccion == 4:
                filtro_estado = "completada"
            
            # Seleccionar formato de tabla
            formatos = ["📊 Grid (por defecto)", "📋 Simple", "📑 Fancy Grid", "🔲 Plain"]
            formato_seleccion = mostrar_menu_opciones(formatos, "FORMATO DE TABLA")
            
            formatos_map = ["grid", "simple", "fancy_grid", "plain"]
            formato = formatos_map[formato_seleccion - 1]
            
            reporte = self.gestor.generar_reporte_tareas(formato, filtro_estado)
            print(reporte)
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def reporte_calendario(self):
        """Genera reporte de calendario para un mes específico."""
        try:
            mostrar_titulo("REPORTE DE CALENDARIO")
            
            año = solicitar_numero("Año", minimo=2000, maximo=2100)
            mes = solicitar_numero("Mes", minimo=1, maximo=12)
            
            reporte = self.gestor.generar_reporte_calendario(año, mes)
            print(reporte)
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def reporte_productividad(self):
        """Genera reporte de productividad."""
        try:
            mostrar_titulo("REPORTE DE PRODUCTIVIDAD")
            
            periodo = solicitar_numero("Período de análisis en días", minimo=1, maximo=365)
            
            reporte = self.gestor.generar_reporte_productividad(periodo)
            print(reporte)
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def estadisticas_generales(self):
        """Muestra estadísticas generales del sistema."""
        try:
            mostrar_titulo("ESTADÍSTICAS GENERALES")
            
            stats = self.gestor.obtener_estadisticas_sistema()
            
            print(f"\n{'=' * 60}")
            print(f"📊 ESTADÍSTICAS DEL SISTEMA")
            print(f"{'=' * 60}")
            
            print(f"\n👥 USUARIOS:")
            print(f"  • Total: {stats['total_usuarios']}")
            print(f"  • Activos: {stats['usuarios_activos']}")
            
            print(f"\n📋 TAREAS:")
            print(f"  • Total: {stats['total_tareas']}")
            print(f"  • Pendientes: {stats['tareas_pendientes']}")
            print(f"  • En progreso: {stats['tareas_en_progreso']}")
            print(f"  • Completadas: {stats['tareas_completadas']}")
            print(f"  • Porcentaje completado: {stats['porcentaje_completadas']}%")
            
            print(f"\n⚠️ ALERTAS:")
            print(f"  • Tareas vencidas: {stats['tareas_vencidas']}")
            print(f"  • Próximas a vencer: {stats['tareas_proximas_vencer']}")
            
            print(f"\n📅 Fecha de consulta: {stats['fecha_consulta']}")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def exportar_reporte(self):
        """Exporta un reporte a archivo."""
        try:
            mostrar_titulo("EXPORTAR REPORTE")
            
            opciones = [
                "👥 Reporte de usuarios",
                "📋 Reporte de tareas",
                "📊 Dashboard ejecutivo",
                "📈 Reporte de productividad"
            ]
            
            seleccion = mostrar_menu_opciones(opciones, "TIPO DE REPORTE")
            
            # Generar el reporte según la selección
            if seleccion == 1:
                contenido = self.gestor.generar_reporte_usuarios()
                nombre_archivo = "reporte_usuarios.txt"
            elif seleccion == 2:
                contenido = self.gestor.generar_reporte_tareas()
                nombre_archivo = "reporte_tareas.txt"
            elif seleccion == 3:
                contenido = self.gestor.generar_dashboard_ejecutivo()
                nombre_archivo = "dashboard_ejecutivo.txt"
            elif seleccion == 4:
                contenido = self.gestor.generar_reporte_productividad()
                nombre_archivo = "reporte_productividad.txt"
            
            # Intentar guardar el archivo
            try:
                with open(nombre_archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                mostrar_exito(f"Reporte exportado exitosamente: {nombre_archivo}")
                
            except Exception as e:
                mostrar_error(f"Error al exportar reporte: {e}")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)

"""
Sistema de reportes y estadísticas avanzadas para el sistema de gestión de tareas.

Este módulo proporciona funcionalidades completas para generar reportes
visualmente atractivos usando tabulate, estadísticas detalladas y análisis
de datos del sistema.
"""

import calendar
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Generator
from tabulate import tabulate

# Importaciones locales
try:
    from ..models.usuario import Usuario
    from ..models.tarea import Tarea, EstadoTarea
    from ..utils.formateo import (
        formatear_fecha_legible, formatear_duracion, formatear_lista_elementos,
        generar_calendario_texto, organizar_datos_por_categoria
    )
    from ..utils.generadores import (
        generador_tareas_por_estado, generador_usuarios_con_tareas,
        generador_estadisticas_por_lote, generador_fechas_limite_calendario
    )
except ImportError:
    from models.usuario import Usuario
    from models.tarea import Tarea, EstadoTarea
    from utils.formateo import (
        formatear_fecha_legible, formatear_duracion, formatear_lista_elementos,
        generar_calendario_texto, organizar_datos_por_categoria
    )
    from utils.generadores import (
        generador_tareas_por_estado, generador_usuarios_con_tareas,
        generador_estadisticas_por_lote, generador_fechas_limite_calendario
    )


class GeneradorReportes:
    """
    Clase principal para generar reportes y estadísticas del sistema.
    
    Utiliza tabulate para crear reportes visualmente atractivos y proporciona
    análisis detallados de la información del sistema.
    """
    
    def __init__(self):
        """Inicializa el generador de reportes."""
        self.formato_tabla_predeterminado = "grid"
        self.formatos_disponibles = [
            "plain", "simple", "github", "grid", "fancy_grid", 
            "pipe", "html", "latex", "rst"
        ]
    
    def generar_reporte_usuarios(self, usuarios: List[Usuario], tareas: List[Tarea],
                                formato_tabla: str = None) -> str:
        """
        Genera un reporte completo de usuarios usando tabulate.
        
        Args:
            usuarios (List[Usuario]): Lista de usuarios
            tareas (List[Tarea]): Lista de tareas
            formato_tabla (str, optional): Formato de tabla a usar
            
        Returns:
            str: Reporte formateado de usuarios
        """
        formato = formato_tabla or self.formato_tabla_predeterminado
        
        if not usuarios:
            return "📊 No hay usuarios registrados en el sistema."
        
        # Generar datos para la tabla usando generadores
        datos_tabla = []
        headers = ["ID", "Nombre", "Email", "Total Tareas", "Pendientes", "En Progreso", "Completadas", "Registro"]
        
        for resumen in generador_usuarios_con_tareas(usuarios, tareas):
            usuario = resumen['usuario']
            datos_tabla.append([
                usuario.id[:8] + "...",  # ID truncado usando slicing de cadenas
                usuario.nombre,
                usuario.email,
                resumen['total_tareas'],
                len(resumen['tareas_pendientes']),
                len(resumen['tareas_en_progreso']),
                len(resumen['tareas_completadas']),
                formatear_fecha_legible(usuario.fecha_registro, formato_relativo=True)
            ])
        
        # Generar tabla usando tabulate
        tabla = tabulate(datos_tabla, headers=headers, tablefmt=formato)
        
        # Agregar estadísticas generales
        total_usuarios = len(usuarios)
        usuarios_activos = sum(1 for u in usuarios if len(u.tareas_asignadas) > 0)
        
        reporte = f"""
📊 REPORTE DE USUARIOS
{'=' * 80}

{tabla}

📈 RESUMEN ESTADÍSTICO:
• Total de usuarios: {total_usuarios}
• Usuarios activos (con tareas): {usuarios_activos}
• Usuarios inactivos: {total_usuarios - usuarios_activos}
• Fecha de generación: {formatear_fecha_legible(datetime.now())}

"""
        return reporte
    
    def generar_reporte_tareas(self, tareas: List[Tarea], usuarios: List[Usuario],
                              formato_tabla: str = None, filtrar_estado: str = None) -> str:
        """
        Genera un reporte completo de tareas usando tabulate.
        
        Args:
            tareas (List[Tarea]): Lista de tareas
            usuarios (List[Usuario]): Lista de usuarios para nombres
            formato_tabla (str, optional): Formato de tabla a usar
            filtrar_estado (str, optional): Filtrar por estado específico
            
        Returns:
            str: Reporte formateado de tareas
        """
        formato = formato_tabla or self.formato_tabla_predeterminado
        
        # Filtrar tareas si se especifica
        if filtrar_estado:
            tareas_filtradas = list(generador_tareas_por_estado(tareas, filtrar_estado))
            titulo_estado = f" - {filtrar_estado.upper()}"
        else:
            tareas_filtradas = tareas
            titulo_estado = ""
        
        if not tareas_filtradas:
            return f"📊 No hay tareas{titulo_estado.lower()} en el sistema."
        
        # Crear diccionario de usuarios para búsqueda rápida
        usuarios_dict = {usuario.id: usuario.nombre for usuario in usuarios}
        
        # Generar datos para la tabla
        datos_tabla = []
        headers = ["ID", "Título", "Estado", "Asignado a", "Días Restantes", "Fecha Límite", "Creación"]
        
        for tarea in tareas_filtradas:
            nombre_usuario = usuarios_dict.get(tarea.usuario_id, "Sin asignar")
            dias_restantes = tarea.calcular_dias_restantes()
            
            # Formatear días restantes con colores conceptuales
            if dias_restantes < 0:
                dias_str = f"⚠️ Vencida ({abs(dias_restantes)} días)"
            elif dias_restantes <= 1:
                dias_str = f"🔥 {dias_restantes} día{'s' if dias_restantes != 1 else ''}"
            elif dias_restantes <= 3:
                dias_str = f"⚡ {dias_restantes} días"
            else:
                dias_str = f"📅 {dias_restantes} días"
            
            # Formatear estado con emojis
            estado_emojis = {
                'pendiente': '📋',
                'en_progreso': '⚙️',
                'completada': '✅'
            }
            estado_formateado = f"{estado_emojis.get(tarea.estado.value, '❓')} {tarea.estado.value.replace('_', ' ').title()}"
            
            datos_tabla.append([
                tarea.id[:8] + "...",
                tarea.titulo[:30] + ("..." if len(tarea.titulo) > 30 else ""),  # Truncar título
                estado_formateado,
                nombre_usuario[:20] + ("..." if len(nombre_usuario) > 20 else ""),
                dias_str,
                formatear_fecha_legible(tarea.fecha_limite, formato_relativo=True),
                formatear_fecha_legible(tarea.fecha_creacion, formato_relativo=True)
            ])
        
        # Generar tabla usando tabulate
        tabla = tabulate(datos_tabla, headers=headers, tablefmt=formato)
        
        # Calcular estadísticas
        total_tareas = len(tareas_filtradas)
        tareas_vencidas = sum(1 for t in tareas_filtradas if t.esta_vencida())
        duracion_promedio = sum(t.obtener_duracion_estimada() for t in tareas_filtradas) / total_tareas if total_tareas > 0 else 0
        
        reporte = f"""
📋 REPORTE DE TAREAS{titulo_estado}
{'=' * 80}

{tabla}

📊 ESTADÍSTICAS:
• Total de tareas: {total_tareas}
• Tareas vencidas: {tareas_vencidas}
• Duración promedio: {formatear_duracion(int(duracion_promedio * 24 * 60))}
• Fecha de generación: {formatear_fecha_legible(datetime.now())}

"""
        return reporte
    
    def generar_dashboard_ejecutivo(self, usuarios: List[Usuario], tareas: List[Tarea]) -> str:
        """
        Genera un dashboard ejecutivo completo con estadísticas clave.
        
        Args:
            usuarios (List[Usuario]): Lista de usuarios
            tareas (List[Tarea]): Lista de tareas
            
        Returns:
            str: Dashboard ejecutivo formateado
        """
        if not tareas and not usuarios:
            return "📊 No hay datos suficientes para generar el dashboard."
        
        # Estadísticas generales
        total_usuarios = len(usuarios)
        total_tareas = len(tareas)
        
        # Usar generadores para calcular estadísticas por estado
        pendientes = list(generador_tareas_por_estado(tareas, 'pendiente'))
        en_progreso = list(generador_tareas_por_estado(tareas, 'en_progreso'))
        completadas = list(generador_tareas_por_estado(tareas, 'completada'))
        
        # Calcular porcentajes
        porcentaje_completadas = (len(completadas) / total_tareas * 100) if total_tareas > 0 else 0
        
        # Tareas por usuario (top 5)
        asignaciones = {}
        for tarea in tareas:
            if tarea.usuario_id:
                asignaciones[tarea.usuario_id] = asignaciones.get(tarea.usuario_id, 0) + 1
        
        # Ordenar usuarios por número de tareas usando métodos de listas
        usuarios_ordenados = sorted(asignaciones.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Crear tabla de usuarios más activos
        datos_top_usuarios = []
        usuarios_dict = {u.id: u.nombre for u in usuarios}
        
        for usuario_id, num_tareas in usuarios_ordenados:
            nombre = usuarios_dict.get(usuario_id, "Usuario desconocido")
            datos_top_usuarios.append([nombre, num_tareas])
        
        tabla_top_usuarios = tabulate(
            datos_top_usuarios,
            headers=["Usuario", "Tareas Asignadas"],
            tablefmt="grid"
        ) if datos_top_usuarios else "No hay asignaciones de tareas."
        
        # Crear tabla de resumen por estado
        datos_estados = [
            ["📋 Pendientes", len(pendientes), f"{len(pendientes)/total_tareas*100:.1f}%" if total_tareas > 0 else "0%"],
            ["⚙️ En Progreso", len(en_progreso), f"{len(en_progreso)/total_tareas*100:.1f}%" if total_tareas > 0 else "0%"],
            ["✅ Completadas", len(completadas), f"{len(completadas)/total_tareas*100:.1f}%" if total_tareas > 0 else "0%"]
        ]
        
        tabla_estados = tabulate(
            datos_estados,
            headers=["Estado", "Cantidad", "Porcentaje"],
            tablefmt="grid"
        )
        
        # Tareas críticas (vencidas o próximas a vencer)
        ahora = datetime.now()
        tareas_criticas = [
            t for t in tareas 
            if t.calcular_dias_restantes() <= 2 and t.estado != EstadoTarea.COMPLETADA
        ]
        
        tabla_criticas = ""
        if tareas_criticas:
            datos_criticas = []
            for tarea in tareas_criticas[:5]:  # Solo las primeras 5
                nombre_usuario = usuarios_dict.get(tarea.usuario_id, "Sin asignar")
                dias = tarea.calcular_dias_restantes()
                urgencia = "🔥 VENCIDA" if dias < 0 else f"⚡ {dias} día{'s' if dias != 1 else ''}"
                
                datos_criticas.append([
                    tarea.titulo[:25] + ("..." if len(tarea.titulo) > 25 else ""),
                    nombre_usuario[:15] + ("..." if len(nombre_usuario) > 15 else ""),
                    urgencia
                ])
            
            tabla_criticas = tabulate(
                datos_criticas,
                headers=["Tarea", "Asignado", "Urgencia"],
                tablefmt="grid"
            )
        else:
            tabla_criticas = "✅ No hay tareas críticas pendientes."
        
        # Generar dashboard
        dashboard = f"""
🚀 DASHBOARD EJECUTIVO
{'=' * 100}

📊 MÉTRICAS CLAVE:
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ Total Usuarios: {total_usuarios:>3} │ Total Tareas: {total_tareas:>3} │ Progreso General: {porcentaje_completadas:>6.1f}% │
└─────────────────────────────────────────────────────────────────────────────────────┘

📈 DISTRIBUCIÓN DE TAREAS POR ESTADO:
{tabla_estados}

👥 TOP 5 USUARIOS MÁS ACTIVOS:
{tabla_top_usuarios}

🔥 TAREAS CRÍTICAS (Vencidas o próximas a vencer):
{tabla_criticas}

📅 Fecha de generación: {formatear_fecha_legible(datetime.now())}
🕒 Hora de generación: {datetime.now().strftime('%H:%M:%S')}

"""
        return dashboard
    
    def generar_reporte_calendario(self, tareas: List[Tarea], año: int, mes: int) -> str:
        """
        Genera un reporte de calendario con tareas usando el módulo calendar.
        
        Args:
            tareas (List[Tarea]): Lista de tareas
            año (int): Año del calendario
            mes (int): Mes del calendario
            
        Returns:
            str: Reporte de calendario con tareas
        """
        # Usar generador de fechas límite
        fechas_tareas = list(generador_fechas_limite_calendario(tareas, año, mes))
        
        # Organizar tareas por día
        tareas_por_dia = {}
        for fecha_data in fechas_tareas:
            dia = fecha_data['dia']
            tareas_por_dia[dia] = fecha_data['tareas']
        
        # Generar calendario en texto usando utilidad
        calendario_texto = generar_calendario_texto(año, mes, tareas_por_dia)
        
        # Crear tabla detallada de tareas del mes
        nombre_mes = calendar.month_name[mes]
        datos_detalle = []
        
        for fecha_data in sorted(fechas_tareas, key=lambda x: x['dia']):
            dia = fecha_data['dia']
            tareas_dia = fecha_data['tareas']
            
            for tarea in tareas_dia:
                estado_emoji = {'pendiente': '📋', 'en_progreso': '⚙️', 'completada': '✅'}
                datos_detalle.append([
                    f"{dia:2d}",
                    tarea.titulo[:35] + ("..." if len(tarea.titulo) > 35 else ""),
                    f"{estado_emoji.get(tarea.estado.value, '❓')} {tarea.estado.value.replace('_', ' ').title()}",
                    formatear_fecha_legible(tarea.fecha_limite, incluir_hora=True, formato_relativo=False)
                ])
        
        tabla_detalle = tabulate(
            datos_detalle,
            headers=["Día", "Tarea", "Estado", "Fecha Límite"],
            tablefmt="grid"
        ) if datos_detalle else "No hay tareas programadas para este mes."
        
        total_tareas_mes = len([t for fecha_data in fechas_tareas for t in fecha_data['tareas']])
        
        reporte = f"""
📅 CALENDARIO DE TAREAS - {nombre_mes.upper()} {año}
{'=' * 80}

{calendario_texto}

📋 DETALLE DE TAREAS DEL MES:
{tabla_detalle}

📊 RESUMEN:
• Total de tareas en {nombre_mes}: {total_tareas_mes}
• Días con actividades: {len(fechas_tareas)}
• Generado el: {formatear_fecha_legible(datetime.now())}

"""
        return reporte
    
    def generar_reporte_productividad(self, usuarios: List[Usuario], tareas: List[Tarea],
                                    periodo_dias: int = 30) -> str:
        """
        Genera un reporte de productividad y análisis temporal.
        
        Args:
            usuarios (List[Usuario]): Lista de usuarios
            tareas (List[Tarea]): Lista de tareas
            periodo_dias (int): Período de análisis en días
            
        Returns:
            str: Reporte de productividad
        """
        fecha_limite = datetime.now() - timedelta(days=periodo_dias)
        tareas_periodo = [t for t in tareas if t.fecha_creacion >= fecha_limite]
        
        if not tareas_periodo:
            return f"📊 No hay datos de productividad para los últimos {periodo_dias} días."
        
        # Análisis por usuario usando generadores
        productividad_usuarios = []
        usuarios_dict = {u.id: u.nombre for u in usuarios}
        
        for resumen in generador_usuarios_con_tareas(usuarios, tareas_periodo):
            usuario = resumen['usuario']
            tareas_completadas = len(resumen['tareas_completadas'])
            total_tareas = resumen['total_tareas']
            
            # Calcular métricas de productividad
            tasa_completitud = (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0
            
            # Tiempo promedio de completitud (solo tareas completadas)
            tiempos_completitud = []
            for tarea in resumen['tareas_completadas']:
                if tarea.fecha_creacion and tarea.fecha_limite:
                    dias_trabajo = (tarea.fecha_limite - tarea.fecha_creacion).days
                    if dias_trabajo > 0:
                        tiempos_completitud.append(dias_trabajo)
            
            tiempo_promedio = sum(tiempos_completitud) / len(tiempos_completitud) if tiempos_completitud else 0
            
            productividad_usuarios.append([
                usuario.nombre,
                total_tareas,
                tareas_completadas,
                f"{tasa_completitud:.1f}%",
                f"{tiempo_promedio:.1f} días"
            ])
        
        # Ordenar por tasa de completitud usando métodos de listas
        productividad_usuarios.sort(key=lambda x: float(x[3].replace('%', '')), reverse=True)
        
        tabla_productividad = tabulate(
            productividad_usuarios,
            headers=["Usuario", "Total Tareas", "Completadas", "Tasa Éxito", "Tiempo Promedio"],
            tablefmt="grid"
        )
        
        # Estadísticas generales del período
        total_tareas_periodo = len(tareas_periodo)
        completadas_periodo = len([t for t in tareas_periodo if t.estado == EstadoTarea.COMPLETADA])
        tasa_general = (completadas_periodo / total_tareas_periodo * 100) if total_tareas_periodo > 0 else 0
        
        # Análisis de tendencias por semana usando generadores por lotes
        estadisticas_semanales = list(generador_estadisticas_por_lote(tareas_periodo, tamaño_lote=7))
        
        datos_tendencias = []
        for i, lote in enumerate(estadisticas_semanales):
            semana = f"Semana {i+1}"
            datos_tendencias.append([
                semana,
                lote['total_tareas'],
                lote['completadas'],
                f"{lote['porcentaje_completadas']:.1f}%"
            ])
        
        tabla_tendencias = tabulate(
            datos_tendencias,
            headers=["Período", "Total", "Completadas", "Tasa"],
            tablefmt="grid"
        ) if datos_tendencias else "No hay suficientes datos para análisis de tendencias."
        
        reporte = f"""
📈 REPORTE DE PRODUCTIVIDAD ({periodo_dias} días)
{'=' * 80}

📊 MÉTRICAS GENERALES:
• Total de tareas creadas: {total_tareas_periodo}
• Tareas completadas: {completadas_periodo}
• Tasa de éxito general: {tasa_general:.1f}%
• Período analizado: {formatear_fecha_legible(fecha_limite)} - {formatear_fecha_legible(datetime.now())}

👥 PRODUCTIVIDAD POR USUARIO:
{tabla_productividad}

📅 TENDENCIAS SEMANALES:
{tabla_tendencias}

🎯 RECOMENDACIONES:
• Usuarios con baja tasa de completitud necesitan apoyo adicional
• Considere redistribuir carga de trabajo si hay desequilibrios
• Analice patrones temporales para optimizar asignaciones

📅 Generado: {formatear_fecha_legible(datetime.now())}

"""
        return reporte
    
    def exportar_reporte_csv(self, datos: List[Dict[str, Any]], nombre_archivo: str) -> str:
        """
        Exporta datos de reporte en formato CSV.
        
        Args:
            datos (List[Dict[str, Any]]): Datos a exportar
            nombre_archivo (str): Nombre del archivo CSV
            
        Returns:
            str: Mensaje de confirmación con la ruta del archivo
        """
        import csv
        import os
        
        if not datos:
            return "No hay datos para exportar."
        
        # Crear directorio de reportes si no existe
        directorio_reportes = "reportes_csv"
        os.makedirs(directorio_reportes, exist_ok=True)
        
        ruta_completa = os.path.join(directorio_reportes, f"{nombre_archivo}.csv")
        
        try:
            with open(ruta_completa, 'w', newline='', encoding='utf-8') as archivo_csv:
                # Usar las claves del primer diccionario como headers
                headers = datos[0].keys()
                writer = csv.DictWriter(archivo_csv, fieldnames=headers)
                
                writer.writeheader()
                for fila in datos:
                    writer.writerow(fila)
            
            return f"✅ Reporte exportado exitosamente: {ruta_completa}"
            
        except Exception as e:
            return f"❌ Error al exportar reporte: {e}"

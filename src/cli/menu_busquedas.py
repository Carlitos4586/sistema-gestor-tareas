"""
Menú para búsquedas y filtros del CLI interactivo.

Este módulo contiene toda la lógica para realizar búsquedas
avanzadas y aplicar filtros en el sistema.
"""

from typing import List

# Importaciones usando try/except para manejar diferentes contextos
try:
    from .cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_tabla_tareas, mostrar_tabla_usuarios, mostrar_exito,
        mostrar_error, mostrar_advertencia, solicitar_entrada_requerida,
        solicitar_entrada, pausar, manejar_error_sistema, formatear_fecha_legible
    )
except ImportError:
    from cli.cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_tabla_tareas, mostrar_tabla_usuarios, mostrar_exito,
        mostrar_error, mostrar_advertencia, solicitar_entrada_requerida,
        solicitar_entrada, pausar, manejar_error_sistema, formatear_fecha_legible
    )


class MenuBusquedas:
    """
    Clase que maneja el menú de búsquedas y filtros.
    """
    
    def __init__(self, gestor):
        """
        Inicializa el menú de búsquedas.
        
        Args:
            gestor: Instancia del gestor del sistema
        """
        self.gestor = gestor
    
    def mostrar_menu(self):
        """
        Muestra el menú principal de búsquedas y filtros.
        """
        while True:
            try:
                opciones = [
                    "🔍 Búsqueda general",
                    "📋 Buscar tareas por criterio",
                    "👥 Buscar usuarios",
                    "⏰ Tareas próximas a vencer",
                    "🚫 Tareas vencidas",
                    "📊 Filtros por estado",
                    "🎯 Filtros por prioridad",
                    "👤 Tareas por usuario específico",
                    "⬅️ Volver al menú principal"
                ]
                
                mostrar_titulo("BÚSQUEDAS Y FILTROS")
                seleccion = mostrar_menu_opciones(opciones)
                
                if seleccion == 1:
                    self.busqueda_general()
                elif seleccion == 2:
                    self.buscar_tareas_por_criterio()
                elif seleccion == 3:
                    self.buscar_usuarios()
                elif seleccion == 4:
                    self.tareas_proximas_vencer()
                elif seleccion == 5:
                    self.tareas_vencidas()
                elif seleccion == 6:
                    self.filtrar_por_estado()
                elif seleccion == 7:
                    self.filtrar_por_prioridad()
                elif seleccion == 8:
                    self.tareas_por_usuario()
                elif seleccion == 9:
                    break
                    
            except Exception as e:
                manejar_error_sistema(e)
    
    def busqueda_general(self):
        """Realiza búsqueda general en el sistema."""
        try:
            mostrar_titulo("BÚSQUEDA GENERAL")
            
            termino = solicitar_entrada_requerida("Término de búsqueda")
            
            # Buscar en tareas
            tareas_encontradas = self.gestor.buscar_tareas(termino)
            
            # Buscar en usuarios
            usuarios_encontrados = []
            for usuario in self.gestor.usuarios:
                if (termino.lower() in usuario.nombre.lower() or 
                    termino.lower() in usuario.email.lower()):
                    usuarios_encontrados.append(usuario)
            
            # Mostrar resultados
            total_resultados = len(tareas_encontradas) + len(usuarios_encontrados)
            
            if total_resultados == 0:
                mostrar_advertencia(f"No se encontraron resultados para: '{termino}'")
            else:
                mostrar_subtitulo(f"Resultados de búsqueda ({total_resultados} encontrados)")
                
                if tareas_encontradas:
                    print(f"\n📋 TAREAS ENCONTRADAS ({len(tareas_encontradas)}):")
                    mostrar_tabla_tareas(tareas_encontradas)
                
                if usuarios_encontrados:
                    print(f"\n👥 USUARIOS ENCONTRADOS ({len(usuarios_encontrados)}):")
                    mostrar_tabla_usuarios(usuarios_encontrados)
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def buscar_tareas_por_criterio(self):
        """Busca tareas usando diferentes criterios."""
        try:
            mostrar_titulo("BUSCAR TAREAS POR CRITERIO")
            
            criterios = [
                "📝 Por título",
                "📄 Por descripción",
                "📅 Por fecha de creación",
                "⏰ Por fecha límite",
                "🔍 Búsqueda combinada"
            ]
            
            criterio_seleccion = mostrar_menu_opciones(criterios, "CRITERIO DE BÚSQUEDA")
            
            resultados = []
            
            if criterio_seleccion == 1:
                # Búsqueda por título
                termino = solicitar_entrada_requerida("Término en el título")
                resultados = [t for t in self.gestor.tareas if termino.lower() in t.titulo.lower()]
                
            elif criterio_seleccion == 2:
                # Búsqueda por descripción
                termino = solicitar_entrada_requerida("Término en la descripción")
                resultados = [t for t in self.gestor.tareas 
                            if t.descripcion and termino.lower() in t.descripcion.lower()]
                
            elif criterio_seleccion == 3:
                # Por fecha de creación (hoy, ayer, esta semana)
                opciones_fecha = ["📅 Hoy", "📆 Ayer", "📊 Esta semana"]
                fecha_seleccion = mostrar_menu_opciones(opciones_fecha, "PERÍODO")
                
                from datetime import datetime, timedelta
                hoy = datetime.now().date()
                
                if fecha_seleccion == 1:  # Hoy
                    resultados = [t for t in self.gestor.tareas if t.fecha_creacion.date() == hoy]
                elif fecha_seleccion == 2:  # Ayer
                    ayer = hoy - timedelta(days=1)
                    resultados = [t for t in self.gestor.tareas if t.fecha_creacion.date() == ayer]
                elif fecha_seleccion == 3:  # Esta semana
                    inicio_semana = hoy - timedelta(days=hoy.weekday())
                    resultados = [t for t in self.gestor.tareas 
                                if t.fecha_creacion.date() >= inicio_semana]
                
            elif criterio_seleccion == 4:
                # Por fecha límite próxima
                from datetime import datetime, timedelta
                dias_adelante = 7  # Por defecto 7 días
                fecha_limite = datetime.now() + timedelta(days=dias_adelante)
                resultados = [t for t in self.gestor.tareas 
                            if t.fecha_limite and t.fecha_limite <= fecha_limite]
                
            elif criterio_seleccion == 5:
                # Búsqueda combinada
                termino = solicitar_entrada_requerida("Término general")
                resultados = self.gestor.buscar_tareas(termino)
            
            if resultados:
                mostrar_subtitulo(f"Resultados encontrados ({len(resultados)} tareas)")
                mostrar_tabla_tareas(resultados)
            else:
                mostrar_advertencia("No se encontraron tareas que coincidan con el criterio")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def buscar_usuarios(self):
        """Busca usuarios específicos."""
        try:
            mostrar_titulo("BUSCAR USUARIOS")
            
            termino = solicitar_entrada_requerida("Término de búsqueda (nombre o email)")
            
            resultados = []
            for usuario in self.gestor.usuarios:
                if (termino.lower() in usuario.nombre.lower() or 
                    termino.lower() in usuario.email.lower()):
                    resultados.append(usuario)
            
            if resultados:
                mostrar_subtitulo(f"Usuarios encontrados ({len(resultados)})")
                mostrar_tabla_usuarios(resultados)
                
                # Mostrar tareas de cada usuario encontrado
                for usuario in resultados:
                    tareas_usuario = [t for t in self.gestor.tareas if t.usuario_id == usuario.id]
                    print(f"\n📋 Tareas de {usuario.nombre}: {len(tareas_usuario)}")
                    if tareas_usuario:
                        pendientes = len([t for t in tareas_usuario if t.estado.value == 'pendiente'])
                        en_progreso = len([t for t in tareas_usuario if t.estado.value == 'en_progreso'])
                        completadas = len([t for t in tareas_usuario if t.estado.value == 'completada'])
                        print(f"  • Pendientes: {pendientes} | En progreso: {en_progreso} | Completadas: {completadas}")
            else:
                mostrar_advertencia("No se encontraron usuarios que coincidan con la búsqueda")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def tareas_proximas_vencer(self):
        """Muestra tareas próximas a vencer."""
        try:
            mostrar_titulo("TAREAS PRÓXIMAS A VENCER")
            
            # Obtener tareas próximas a vencer (próximos 7 días por defecto)
            tareas_proximas = list(self.gestor.obtener_tareas_proximas_vencer(7))
            
            if tareas_proximas:
                mostrar_subtitulo(f"Tareas que vencen en los próximos 7 días ({len(tareas_proximas)})")
                mostrar_tabla_tareas(tareas_proximas)
                
                # Mostrar detalles adicionales
                print(f"\n📊 ANÁLISIS:")
                criticas = [t for t in tareas_proximas 
                          if t.fecha_limite and (t.fecha_limite - self.gestor.obtener_estadisticas_sistema()['fecha_consulta']).days <= 3]
                print(f"  • Tareas críticas (≤3 días): {len(criticas)}")
                
            else:
                mostrar_advertencia("No hay tareas próximas a vencer en los próximos 7 días")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def tareas_vencidas(self):
        """Muestra tareas vencidas."""
        try:
            mostrar_titulo("TAREAS VENCIDAS")
            
            from datetime import datetime
            ahora = datetime.now()
            
            tareas_vencidas = [t for t in self.gestor.tareas 
                             if t.fecha_limite and t.fecha_limite < ahora and t.estado.value != 'completada']
            
            if tareas_vencidas:
                mostrar_subtitulo(f"Tareas vencidas ({len(tareas_vencidas)})")
                mostrar_tabla_tareas(tareas_vencidas)
                
                # Mostrar análisis de días vencidos
                print(f"\n📊 ANÁLISIS DE VENCIMIENTOS:")
                for tarea in tareas_vencidas:
                    dias_vencida = (ahora - tarea.fecha_limite).days
                    print(f"  • {tarea.titulo[:30]:30} - Vencida hace {dias_vencida} días")
                
            else:
                mostrar_exito("¡No hay tareas vencidas! 🎉")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def filtrar_por_estado(self):
        """Filtra tareas por estado."""
        try:
            mostrar_titulo("FILTRAR POR ESTADO")
            
            estados = ["📋 Pendientes", "⏳ En progreso", "✅ Completadas"]
            estado_seleccion = mostrar_menu_opciones(estados, "ESTADO")
            
            estados_map = ["pendiente", "en_progreso", "completada"]
            estado_filtro = estados_map[estado_seleccion - 1]
            
            tareas_filtradas = list(self.gestor.listar_tareas_por_estado(estado_filtro))
            
            if tareas_filtradas:
                mostrar_subtitulo(f"Tareas {estado_filtro.replace('_', ' ')} ({len(tareas_filtradas)})")
                mostrar_tabla_tareas(tareas_filtradas)
            else:
                mostrar_advertencia(f"No hay tareas en estado: {estado_filtro.replace('_', ' ')}")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def filtrar_por_prioridad(self):
        """Filtra tareas por prioridad."""
        try:
            mostrar_titulo("FILTRAR POR PRIORIDAD")
            
            prioridades = ["🔴 Alta", "🟡 Media", "🟢 Baja"]
            prioridad_seleccion = mostrar_menu_opciones(prioridades, "PRIORIDAD")
            
            prioridades_map = ["alta", "media", "baja"]
            prioridad_filtro = prioridades_map[prioridad_seleccion - 1]
            
            tareas_filtradas = [t for t in self.gestor.tareas 
                              if hasattr(t, 'prioridad') and t.prioridad == prioridad_filtro]
            
            if tareas_filtradas:
                mostrar_subtitulo(f"Tareas de prioridad {prioridad_filtro} ({len(tareas_filtradas)})")
                mostrar_tabla_tareas(tareas_filtradas)
            else:
                mostrar_advertencia(f"No hay tareas de prioridad: {prioridad_filtro}")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def tareas_por_usuario(self):
        """Muestra tareas de un usuario específico."""
        try:
            mostrar_titulo("TAREAS POR USUARIO")
            
            if not self.gestor.usuarios:
                mostrar_error("No hay usuarios registrados")
                pausar()
                return
            
            print("Selecciona un usuario:")
            mostrar_tabla_usuarios(self.gestor.usuarios)
            
            while True:
                try:
                    indice_usuario = int(solicitar_entrada_requerida("Número de usuario")) - 1
                    if 0 <= indice_usuario < len(self.gestor.usuarios):
                        usuario_seleccionado = self.gestor.usuarios[indice_usuario]
                        break
                    else:
                        mostrar_error("Número de usuario inválido")
                except ValueError:
                    mostrar_error("Por favor ingresa un número válido")
            
            # Obtener tareas del usuario
            tareas_usuario = [t for t in self.gestor.tareas if t.usuario_id == usuario_seleccionado.id]
            
            if tareas_usuario:
                mostrar_subtitulo(f"Tareas de {usuario_seleccionado.nombre} ({len(tareas_usuario)})")
                mostrar_tabla_tareas(tareas_usuario)
                
                # Estadísticas del usuario
                pendientes = len([t for t in tareas_usuario if t.estado.value == 'pendiente'])
                en_progreso = len([t for t in tareas_usuario if t.estado.value == 'en_progreso'])
                completadas = len([t for t in tareas_usuario if t.estado.value == 'completada'])
                
                print(f"\n📊 ESTADÍSTICAS DEL USUARIO:")
                print(f"  • Pendientes: {pendientes}")
                print(f"  • En progreso: {en_progreso}")
                print(f"  • Completadas: {completadas}")
                
                if tareas_usuario:
                    porcentaje_completado = (completadas / len(tareas_usuario)) * 100
                    print(f"  • Porcentaje de completado: {porcentaje_completado:.1f}%")
                
            else:
                mostrar_advertencia(f"{usuario_seleccionado.nombre} no tiene tareas asignadas")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)

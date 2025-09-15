"""
Menú para gestión de tareas del CLI interactivo.

Este módulo contiene toda la lógica para el manejo de tareas
a través del CLI interactivo.
"""

from typing import Optional, List
from datetime import datetime

# Importaciones usando try/except para manejar diferentes contextos
try:
    from ..models.tarea import Tarea
    from ..models.usuario import Usuario
    from .cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_tabla_tareas, mostrar_tabla_usuarios, mostrar_exito, 
        mostrar_error, mostrar_advertencia, solicitar_entrada_requerida, 
        solicitar_entrada, solicitar_fecha, confirmar_accion, pausar, 
        manejar_error_sistema, formatear_fecha_legible
    )
except ImportError:
    from models.tarea import Tarea
    from models.usuario import Usuario
    from cli.cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_tabla_tareas, mostrar_tabla_usuarios, mostrar_exito, 
        mostrar_error, mostrar_advertencia, solicitar_entrada_requerida, 
        solicitar_entrada, solicitar_fecha, confirmar_accion, pausar, 
        manejar_error_sistema, formatear_fecha_legible
    )


class MenuTareas:
    """
    Clase que maneja el menú de gestión de tareas.
    """
    
    def __init__(self, gestor):
        """
        Inicializa el menú de tareas.
        
        Args:
            gestor: Instancia del gestor del sistema
        """
        self.gestor = gestor
    
    def mostrar_menu(self):
        """
        Muestra el menú principal de gestión de tareas.
        """
        while True:
            try:
                opciones = [
                    "📝 Crear nueva tarea",
                    "👀 Ver todas las tareas",
                    "🔍 Buscar tareas",
                    "✏️ Editar tarea",
                    "🔄 Cambiar estado de tarea",
                    "🗑️ Eliminar tarea",
                    "📋 Ver detalles de tarea",
                    "👤 Ver tareas por usuario",
                    "⬅️ Volver al menú principal"
                ]
                
                mostrar_titulo("GESTIÓN DE TAREAS")
                seleccion = mostrar_menu_opciones(opciones)
                
                if seleccion == 1:
                    self.crear_tarea()
                elif seleccion == 2:
                    self.listar_tareas()
                elif seleccion == 3:
                    self.buscar_tareas()
                elif seleccion == 4:
                    self.editar_tarea()
                elif seleccion == 5:
                    self.cambiar_estado_tarea()
                elif seleccion == 6:
                    self.eliminar_tarea()
                elif seleccion == 7:
                    self.ver_detalles_tarea()
                elif seleccion == 8:
                    self.ver_tareas_por_usuario()
                elif seleccion == 9:
                    break
                    
            except Exception as e:
                manejar_error_sistema(e)
    
    def crear_tarea(self):
        """Crea una nueva tarea."""
        try:
            mostrar_titulo("CREAR NUEVA TAREA")
            
            # Verificar que hay usuarios
            usuarios = self.gestor.usuarios
            if not usuarios:
                mostrar_error("No hay usuarios registrados. Crea un usuario primero.")
                pausar()
                return
            
            # Datos básicos de la tarea
            titulo = solicitar_entrada_requerida("Título de la tarea")
            descripcion = solicitar_entrada("Descripción (opcional)")
            
            # Fecha límite (requerida para el gestor)
            fecha_limite = solicitar_fecha("Fecha límite", permitir_vacia=False)
            
            # Seleccionar usuario asignado
            print("\nSelecciona el usuario asignado:")
            mostrar_tabla_usuarios(usuarios)
            
            while True:
                try:
                    indice_usuario = int(solicitar_entrada_requerida("Número de usuario")) - 1
                    if 0 <= indice_usuario < len(usuarios):
                        usuario_asignado = usuarios[indice_usuario]
                        break
                    else:
                        mostrar_error("Número de usuario inválido")
                except ValueError:
                    mostrar_error("Por favor ingresa un número válido")
            
            # Crear la tarea usando el método del gestor
            tarea_creada = self.gestor.crear_tarea(
                titulo=titulo,
                descripcion=descripcion if descripcion else "",
                fecha_limite=fecha_limite,
                usuario_email=usuario_asignado.email
            )
            
            if tarea_creada:
                mostrar_exito(f"Tarea '{titulo}' creada exitosamente")
                print(f"Asignada a: {usuario_asignado.nombre}")
            else:
                mostrar_error("No se pudo crear la tarea")
                
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def listar_tareas(self):
        """Lista todas las tareas."""
        try:
            mostrar_titulo("LISTA DE TAREAS")
            
            # Opción de filtrado
            opciones_filtro = [
                "📋 Todas las tareas",
                "⏳ Solo pendientes",
                "🔄 Solo en progreso", 
                "✅ Solo completadas"
            ]
            
            filtro_seleccion = mostrar_menu_opciones(opciones_filtro, "FILTRO")
            
            tareas = self.gestor.tareas
            
            if filtro_seleccion == 2:
                tareas = [t for t in tareas if t.estado.value == "pendiente"]
            elif filtro_seleccion == 3:
                tareas = [t for t in tareas if t.estado.value == "en_progreso"]
            elif filtro_seleccion == 4:
                tareas = [t for t in tareas if t.estado.value == "completada"]
            
            mostrar_tabla_tareas(tareas)
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def buscar_tareas(self):
        """Busca tareas específicas."""
        try:
            mostrar_titulo("BUSCAR TAREAS")
            termino = solicitar_entrada_requerida("Término de búsqueda (título o descripción)")
            
            resultados = self.gestor.buscar_tareas(termino)
            
            if resultados:
                mostrar_subtitulo(f"Resultados de búsqueda ({len(resultados)} encontradas)")
                mostrar_tabla_tareas(resultados)
            else:
                mostrar_advertencia("No se encontraron tareas con ese término de búsqueda")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def seleccionar_tarea(self) -> Optional[Tarea]:
        """
        Permite seleccionar una tarea de la lista.
        
        Returns:
            Tarea: Tarea seleccionada o None si no hay tareas
        """
        tareas = self.gestor.tareas
        if not tareas:
            mostrar_advertencia("No hay tareas registradas")
            return None
        
        mostrar_tabla_tareas(tareas)
        
        while True:
            try:
                indice = int(solicitar_entrada_requerida("Número de tarea")) - 1
                if 0 <= indice < len(tareas):
                    return tareas[indice]
                else:
                    mostrar_error("Número de tarea inválido")
            except ValueError:
                mostrar_error("Por favor ingresa un número válido")
    
    def editar_tarea(self):
        """Edita una tarea existente."""
        try:
            mostrar_titulo("EDITAR TAREA")
            
            tarea = self.seleccionar_tarea()
            if not tarea:
                pausar()
                return
            
            mostrar_subtitulo(f"Editando tarea: {tarea.titulo}")
            print(f"Deja vacío para mantener el valor actual")
            
            # Solicitar nuevos valores
            nuevo_titulo = solicitar_entrada("Título", tarea.titulo)
            nueva_descripcion = solicitar_entrada("Descripción", tarea.descripcion or "")
            
            # Prioridad
            print(f"\nPrioridad actual: {tarea.prioridad}")
            if confirmar_accion("¿Cambiar prioridad?"):
                opciones_prioridad = ["🟢 Baja", "🟡 Media", "🔴 Alta"]
                prioridad_seleccion = mostrar_menu_opciones(opciones_prioridad, "NUEVA PRIORIDAD")
                prioridades = ["baja", "media", "alta"]
                nueva_prioridad = prioridades[prioridad_seleccion - 1]
            else:
                nueva_prioridad = tarea.prioridad
            
            # Fecha límite
            if tarea.fecha_limite:
                fecha_actual = formatear_fecha_legible(tarea.fecha_limite)
                print(f"\nFecha límite actual: {fecha_actual}")
            else:
                print("\nNo tiene fecha límite establecida")
                
            if confirmar_accion("¿Cambiar fecha límite?"):
                nueva_fecha_limite = solicitar_fecha("Nueva fecha límite", permitir_vacia=True)
            else:
                nueva_fecha_limite = tarea.fecha_limite
            
            # Actualizar tarea
            tarea.titulo = nuevo_titulo
            tarea.descripcion = nueva_descripcion if nueva_descripcion else None
            tarea.prioridad = nueva_prioridad
            tarea.fecha_limite = nueva_fecha_limite
            
            if self.gestor.actualizar_tarea(tarea):
                mostrar_exito("Tarea actualizada exitosamente")
            else:
                mostrar_error("No se pudo actualizar la tarea")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def cambiar_estado_tarea(self):
        """Cambia el estado de una tarea."""
        try:
            mostrar_titulo("CAMBIAR ESTADO DE TAREA")
            
            tarea = self.seleccionar_tarea()
            if not tarea:
                pausar()
                return
            
            print(f"\nTarea: {tarea.titulo}")
            print(f"Estado actual: {tarea.estado}")
            
            # Opciones de estado
            estados_opciones = ["📋 Pendiente", "⏳ En progreso", "✅ Completada"]
            nueva_seleccion = mostrar_menu_opciones(estados_opciones, "NUEVO ESTADO")
            
            estados = ["pendiente", "en_progreso", "completada"]
            nuevo_estado = estados[nueva_seleccion - 1]
            
            # Mapear estado string a Enum
            try:
                from ..models.tarea import EstadoTarea
            except ImportError:
                from models.tarea import EstadoTarea
            
            estados_map = {
                "pendiente": EstadoTarea.PENDIENTE,
                "en_progreso": EstadoTarea.EN_PROGRESO,
                "completada": EstadoTarea.COMPLETADA
            }
            
            nuevo_estado_enum = estados_map[nuevo_estado]
            
            if nuevo_estado_enum != tarea.estado:
                tarea.estado = nuevo_estado_enum
                
                # Si se marca como completada, establecer fecha de finalización
                if nuevo_estado == "completada":
                    tarea.fecha_finalizacion = datetime.now()
                else:
                    tarea.fecha_finalizacion = None
                
                if self.gestor.actualizar_tarea(tarea):
                    mostrar_exito(f"Estado cambiado a: {nuevo_estado}")
                    if nuevo_estado == "completada":
                        print("🎉 ¡Tarea completada!")
                else:
                    mostrar_error("No se pudo cambiar el estado")
            else:
                mostrar_advertencia("El estado seleccionado es el mismo actual")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def eliminar_tarea(self):
        """Elimina una tarea."""
        try:
            mostrar_titulo("ELIMINAR TAREA")
            
            tarea = self.seleccionar_tarea()
            if not tarea:
                pausar()
                return
            
            # Confirmar eliminación
            mostrar_advertencia(f"Estás a punto de eliminar la tarea: {tarea.titulo}")
            print(f"Estado: {tarea.estado}")
            print(f"Prioridad: {tarea.prioridad}")
            
            if confirmar_accion("¿Estás seguro de eliminar esta tarea?"):
                if self.gestor.eliminar_tarea(tarea.id):
                    mostrar_exito("Tarea eliminada exitosamente")
                else:
                    mostrar_error("No se pudo eliminar la tarea")
            else:
                mostrar_advertencia("Eliminación cancelada")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def ver_detalles_tarea(self):
        """Muestra los detalles completos de una tarea."""
        try:
            mostrar_titulo("DETALLES DE TAREA")
            
            tarea = self.seleccionar_tarea()
            if not tarea:
                pausar()
                return
            
            print(f"\n{'=' * 60}")
            print(f"📋 INFORMACIÓN DE LA TAREA")
            print(f"{'=' * 60}")
            print(f"ID: {tarea.id}")
            print(f"Título: {tarea.titulo}")
            print(f"Descripción: {tarea.descripcion or 'Sin descripción'}")
            print(f"Estado: {tarea.estado}")
            print(f"Prioridad: {tarea.prioridad}")
            print(f"Fecha de creación: {tarea.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")
            
            if tarea.fecha_limite:
                print(f"Fecha límite: {formatear_fecha_legible(tarea.fecha_limite)}")
            else:
                print("Fecha límite: No establecida")
            
            if tarea.fecha_finalizacion:
                print(f"Fecha de finalización: {tarea.fecha_finalizacion.strftime('%d/%m/%Y %H:%M')}")
            
            # Información del usuario asignado
            try:
                usuario = self.gestor.obtener_usuario_por_id(tarea.usuario_id)
                if usuario:
                    print(f"\n👤 USUARIO ASIGNADO:")
                    print(f"Nombre: {usuario.nombre}")
                    print(f"Email: {usuario.email}")
            except Exception:
                print("\nNo se pudo obtener información del usuario asignado")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def ver_tareas_por_usuario(self):
        """Muestra las tareas filtradas por usuario."""
        try:
            mostrar_titulo("TAREAS POR USUARIO")
            
            usuarios = self.gestor.obtener_todos_los_usuarios()
            if not usuarios:
                mostrar_error("No hay usuarios registrados")
                pausar()
                return
            
            print("Selecciona un usuario:")
            mostrar_tabla_usuarios(usuarios)
            
            while True:
                try:
                    indice_usuario = int(solicitar_entrada_requerida("Número de usuario")) - 1
                    if 0 <= indice_usuario < len(usuarios):
                        usuario_seleccionado = usuarios[indice_usuario]
                        break
                    else:
                        mostrar_error("Número de usuario inválido")
                except ValueError:
                    mostrar_error("Por favor ingresa un número válido")
            
            tareas_usuario = self.gestor.obtener_tareas_por_usuario(usuario_seleccionado.id)
            
            if tareas_usuario:
                mostrar_subtitulo(f"Tareas de {usuario_seleccionado.nombre} ({len(tareas_usuario)} tareas)")
                mostrar_tabla_tareas(tareas_usuario)
            else:
                mostrar_advertencia(f"{usuario_seleccionado.nombre} no tiene tareas asignadas")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)

"""
Gestor principal del sistema de gestión de tareas.

Esta clase coordina todas las funcionalidades del sistema: usuarios, tareas,
persistencia y utilidades. Proporciona una interfaz unificada para el manejo
completo del sistema usando todos los módulos implementados.
"""

import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple, Generator
import sys

# Importar nuestros módulos
try:
    # Importaciones relativas (cuando se usa como módulo)
    from ..models.usuario import Usuario
    from ..models.tarea import Tarea, EstadoTarea
    from .persistencia import GestorPersistencia
    from ..utils.generadores import (
        IteradorTareas, generador_tareas_por_estado, generador_tareas_por_usuario,
        generador_tareas_vencidas, generador_tareas_proximas_vencer,
        generador_estadisticas_por_lote, generador_usuarios_con_tareas,
        crear_filtro_fecha_rango, crear_filtro_titulo_contiene, filtro_compuesto
    )
    from ..utils.formateo import (
        formatear_titulo, formatear_nombre_completo, validar_y_formatear_email,
        formatear_lista_elementos, formatear_fecha_legible, formatear_duracion
    )
except ImportError:
    # Importaciones absolutas (cuando se ejecuta directamente)
    from models.usuario import Usuario
    from models.tarea import Tarea, EstadoTarea
    from services.persistencia import GestorPersistencia
    from utils.generadores import (
        IteradorTareas, generador_tareas_por_estado, generador_tareas_por_usuario,
        generador_tareas_vencidas, generador_tareas_proximas_vencer,
        generador_estadisticas_por_lote, generador_usuarios_con_tareas,
        crear_filtro_fecha_rango, crear_filtro_titulo_contiene, filtro_compuesto
    )
    from utils.formateo import (
        formatear_titulo, formatear_nombre_completo, validar_y_formatear_email,
        formatear_lista_elementos, formatear_fecha_legible, formatear_duracion
    )


class GestorTareas:
    """
    Clase principal que gestiona todo el sistema de tareas.
    
    Coordina usuarios, tareas, persistencia y proporciona funcionalidades
    avanzadas como filtrado, búsqueda y generación de reportes.
    """
    
    def __init__(self, directorio_datos: str = "data"):
        """
        Inicializa el gestor de tareas.
        
        Args:
            directorio_datos (str): Directorio base para almacenar datos
        """
        self.directorio_datos = directorio_datos
        self.persistencia = GestorPersistencia(directorio_datos)
        
        # Almacenamiento en memoria
        self.usuarios: List[Usuario] = []
        self.tareas: List[Tarea] = []
        
        # Configuración del sistema
        self.auto_guardar = True
        self.formato_preferido = "json"
        self.crear_backups = True
        
        # Cargar datos existentes al inicializar
        self._cargar_datos_iniciales()
        
        print(f"🚀 GestorTareas inicializado con {len(self.usuarios)} usuarios y {len(self.tareas)} tareas")
    
    # ===============================
    # GESTIÓN DE USUARIOS
    # ===============================
    
    def crear_usuario(self, nombre: str, email: str) -> Usuario:
        """
        Crea un nuevo usuario en el sistema.
        
        Args:
            nombre (str): Nombre del usuario
            email (str): Email del usuario
            
        Returns:
            Usuario: Usuario creado
            
        Raises:
            ValueError: Si el email ya existe o los datos son inválidos
        """
        # Formatear datos usando utilidades
        nombre_formateado = formatear_nombre_completo(nombre)
        valido, email_formateado = validar_y_formatear_email(email)
        
        if not valido:
            raise ValueError(f"Email inválido: {email}")
        
        # Verificar que el email no exista
        if self._buscar_usuario_por_email(email_formateado):
            raise ValueError(f"Ya existe un usuario con el email: {email_formateado}")
        
        # Crear usuario
        usuario = Usuario(nombre_formateado, email_formateado)
        self.usuarios.append(usuario)
        
        # Auto-guardar si está habilitado
        if self.auto_guardar:
            self._guardar_usuarios()
        
        print(f"👤 Usuario creado: {usuario.nombre} ({usuario.email})")
        return usuario
    
    def obtener_usuario(self, usuario_id: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            usuario_id (str): ID del usuario
            
        Returns:
            Optional[Usuario]: Usuario encontrado o None
        """
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None
    
    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email (str): Email del usuario
            
        Returns:
            Optional[Usuario]: Usuario encontrado o None
        """
        email_normalizado = email.strip().lower()
        return self._buscar_usuario_por_email(email_normalizado)
    
    def listar_usuarios(self) -> List[Usuario]:
        """
        Obtiene la lista completa de usuarios.
        
        Returns:
            List[Usuario]: Lista de todos los usuarios
        """
        return self.usuarios.copy()
    
    def actualizar_usuario(self, usuario_id: str, nuevo_nombre: str = None, 
                          nuevo_email: str = None) -> bool:
        """
        Actualiza los datos de un usuario.
        
        Args:
            usuario_id (str): ID del usuario a actualizar
            nuevo_nombre (str, optional): Nuevo nombre
            nuevo_email (str, optional): Nuevo email
            
        Returns:
            bool: True si se actualizó correctamente
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False
        
        # Actualizar nombre si se proporciona
        if nuevo_nombre:
            usuario.nombre = formatear_nombre_completo(nuevo_nombre)
        
        # Actualizar email si se proporciona
        if nuevo_email:
            valido, email_formateado = validar_y_formatear_email(nuevo_email)
            if not valido:
                raise ValueError(f"Email inválido: {nuevo_email}")
            
            # Verificar que el nuevo email no exista en otro usuario
            usuario_existente = self._buscar_usuario_por_email(email_formateado)
            if usuario_existente and usuario_existente.id != usuario_id:
                raise ValueError(f"El email {email_formateado} ya está en uso")
            
            usuario.email = email_formateado
        
        # Auto-guardar si está habilitado
        if self.auto_guardar:
            self._guardar_usuarios()
        
        print(f"👤 Usuario actualizado: {usuario.nombre}")
        return True
    
    # ===============================
    # GESTIÓN DE TAREAS
    # ===============================
    
    def crear_tarea(self, titulo: str, descripcion: str, fecha_limite: datetime,
                   usuario_id: Optional[str] = None) -> Tarea:
        """
        Crea una nueva tarea en el sistema.
        
        Args:
            titulo (str): Título de la tarea
            descripcion (str): Descripción de la tarea
            fecha_limite (datetime): Fecha límite
            usuario_id (Optional[str]): ID del usuario asignado
            
        Returns:
            Tarea: Tarea creada
            
        Raises:
            ValueError: Si los datos son inválidos o el usuario no existe
        """
        # Formatear título usando utilidades
        titulo_formateado = formatear_titulo(titulo)
        
        # Verificar que el usuario existe si se proporciona
        if usuario_id:
            usuario = self.obtener_usuario(usuario_id)
            if not usuario:
                raise ValueError(f"Usuario no encontrado: {usuario_id}")
        
        # Crear tarea
        tarea = Tarea(titulo_formateado, descripcion, fecha_limite, usuario_id)
        self.tareas.append(tarea)
        
        # Asignar tarea al usuario si se especifica
        if usuario_id:
            usuario = self.obtener_usuario(usuario_id)
            if usuario:
                usuario.agregar_tarea(tarea.id)
        
        # Auto-guardar si está habilitado
        if self.auto_guardar:
            self._guardar_tareas()
            if usuario_id:
                self._guardar_usuarios()
        
        print(f"📋 Tarea creada: {tarea.titulo}")
        return tarea
    
    def obtener_tarea(self, tarea_id: str) -> Optional[Tarea]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            tarea_id (str): ID de la tarea
            
        Returns:
            Optional[Tarea]: Tarea encontrada o None
        """
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                return tarea
        return None
    
    def listar_tareas(self) -> List[Tarea]:
        """
        Obtiene la lista completa de tareas.
        
        Returns:
            List[Tarea]: Lista de todas las tareas
        """
        return self.tareas.copy()
    
    def actualizar_estado_tarea(self, tarea_id: str, nuevo_estado: EstadoTarea) -> bool:
        """
        Actualiza el estado de una tarea.
        
        Args:
            tarea_id (str): ID de la tarea
            nuevo_estado (EstadoTarea): Nuevo estado
            
        Returns:
            bool: True si se actualizó correctamente
        """
        tarea = self.obtener_tarea(tarea_id)
        if not tarea:
            return False
        
        tarea.cambiar_estado(nuevo_estado)
        
        # Auto-guardar si está habilitado
        if self.auto_guardar:
            self._guardar_tareas()
        
        return True
    
    def reasignar_tarea(self, tarea_id: str, nuevo_usuario_id: Optional[str]) -> bool:
        """
        Reasigna una tarea a un usuario diferente.
        
        Args:
            tarea_id (str): ID de la tarea
            nuevo_usuario_id (Optional[str]): ID del nuevo usuario
            
        Returns:
            bool: True si se reasignó correctamente
        """
        tarea = self.obtener_tarea(tarea_id)
        if not tarea:
            return False
        
        # Verificar que el nuevo usuario existe
        if nuevo_usuario_id:
            nuevo_usuario = self.obtener_usuario(nuevo_usuario_id)
            if not nuevo_usuario:
                raise ValueError(f"Usuario no encontrado: {nuevo_usuario_id}")
        
        # Remover tarea del usuario anterior
        if tarea.usuario_id:
            usuario_anterior = self.obtener_usuario(tarea.usuario_id)
            if usuario_anterior:
                usuario_anterior.remover_tarea(tarea_id)
        
        # Asignar a nuevo usuario
        tarea.reasignar(nuevo_usuario_id)
        if nuevo_usuario_id:
            nuevo_usuario = self.obtener_usuario(nuevo_usuario_id)
            if nuevo_usuario:
                nuevo_usuario.agregar_tarea(tarea_id)
        
        # Auto-guardar si está habilitado
        if self.auto_guardar:
            self._guardar_tareas()
            self._guardar_usuarios()
        
        return True
    
    # ===============================
    # FILTRADO Y BÚSQUEDA USANDO GENERADORES
    # ===============================
    
    def obtener_tareas_por_estado(self, estado: str) -> Generator[Tarea, None, None]:
        """
        Obtiene tareas filtradas por estado usando generadores.
        
        Args:
            estado (str): Estado a filtrar
            
        Yields:
            Tarea: Tareas que coinciden con el estado
        """
        return generador_tareas_por_estado(self.tareas, estado)
    
    def obtener_tareas_usuario(self, usuario_id: str) -> Generator[Tarea, None, None]:
        """
        Obtiene tareas asignadas a un usuario usando generadores.
        
        Args:
            usuario_id (str): ID del usuario
            
        Yields:
            Tarea: Tareas asignadas al usuario
        """
        return generador_tareas_por_usuario(self.tareas, usuario_id)
    
    def obtener_tareas_vencidas(self) -> Generator[Tarea, None, None]:
        """
        Obtiene tareas vencidas usando generadores.
        
        Yields:
            Tarea: Tareas vencidas
        """
        return generador_tareas_vencidas(self.tareas)
    
    def obtener_tareas_proximas_vencer(self, dias: int = 3) -> Generator[Tarea, None, None]:
        """
        Obtiene tareas próximas a vencer usando generadores.
        
        Args:
            dias (int): Días para considerar "próximo a vencer"
            
        Yields:
            Tarea: Tareas próximas a vencer
        """
        return generador_tareas_proximas_vencer(self.tareas, dias)
    
    def buscar_tareas_por_titulo(self, texto_busqueda: str) -> List[Tarea]:
        """
        Busca tareas por título usando filtros de cadenas.
        
        Args:
            texto_busqueda (str): Texto a buscar en el título
            
        Returns:
            List[Tarea]: Lista de tareas que coinciden
        """
        filtro = crear_filtro_titulo_contiene(texto_busqueda)
        return [tarea for tarea in self.tareas if filtro(tarea)]
    
    def buscar_tareas_por_fecha_rango(self, fecha_inicio: datetime, 
                                    fecha_fin: datetime) -> List[Tarea]:
        """
        Busca tareas en un rango de fechas usando filtros.
        
        Args:
            fecha_inicio (datetime): Fecha de inicio del rango
            fecha_fin (datetime): Fecha de fin del rango
            
        Returns:
            List[Tarea]: Lista de tareas en el rango
        """
        filtro = crear_filtro_fecha_rango(fecha_inicio, fecha_fin)
        return [tarea for tarea in self.tareas if filtro(tarea)]
    
    def buscar_tareas_compuesto(self, titulo: str = None, estado: str = None,
                              fecha_inicio: datetime = None, 
                              fecha_fin: datetime = None) -> List[Tarea]:
        """
        Busca tareas usando filtros compuestos.
        
        Args:
            titulo (str, optional): Texto a buscar en título
            estado (str, optional): Estado a filtrar
            fecha_inicio (datetime, optional): Fecha inicio del rango
            fecha_fin (datetime, optional): Fecha fin del rango
            
        Returns:
            List[Tarea]: Lista de tareas que cumplen todos los criterios
        """
        filtros = []
        
        if titulo:
            filtros.append(crear_filtro_titulo_contiene(titulo))
        
        if estado:
            filtros.append(lambda t: hasattr(t, 'estado') and t.estado.value == estado)
        
        if fecha_inicio and fecha_fin:
            filtros.append(crear_filtro_fecha_rango(fecha_inicio, fecha_fin))
        
        if not filtros:
            return self.tareas.copy()
        
        # Crear filtro compuesto
        filtro_combinado = filtro_compuesto(*filtros)
        return [tarea for tarea in self.tareas if filtro_combinado(tarea)]
    
    # ===============================
    # ESTADÍSTICAS Y REPORTES
    # ===============================
    
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del sistema.
        
        Returns:
            Dict[str, Any]: Estadísticas del sistema
        """
        # Usar generadores para calcular estadísticas eficientemente
        estadisticas = {
            'total_usuarios': len(self.usuarios),
            'total_tareas': len(self.tareas),
            'tareas_pendientes': len(list(self.obtener_tareas_por_estado('pendiente'))),
            'tareas_en_progreso': len(list(self.obtener_tareas_por_estado('en_progreso'))),
            'tareas_completadas': len(list(self.obtener_tareas_por_estado('completada'))),
            'tareas_vencidas': len(list(self.obtener_tareas_vencidas())),
            'tareas_proximas_vencer': len(list(self.obtener_tareas_proximas_vencer())),
            'fecha_generacion': datetime.now(),
            'usuarios_con_tareas': 0,
            'usuarios_sin_tareas': 0
        }
        
        # Contar usuarios con/sin tareas
        for usuario in self.usuarios:
            if len(usuario.tareas_asignadas) > 0:
                estadisticas['usuarios_con_tareas'] += 1
            else:
                estadisticas['usuarios_sin_tareas'] += 1
        
        return estadisticas
    
    def obtener_resumen_usuarios(self) -> Generator[Dict[str, Any], None, None]:
        """
        Obtiene resumen de usuarios con sus tareas usando generadores.
        
        Yields:
            Dict[str, Any]: Información detallada de cada usuario
        """
        return generador_usuarios_con_tareas(self.usuarios, self.tareas)
    
    # ===============================
    # PERSISTENCIA
    # ===============================
    
    def guardar_todo(self, formato: str = None) -> bool:
        """
        Guarda todos los datos del sistema.
        
        Args:
            formato (str, optional): Formato a usar, por defecto el preferido
            
        Returns:
            bool: True si se guardó correctamente
        """
        formato_usar = formato or self.formato_preferido
        
        try:
            exito_usuarios = self._guardar_usuarios(formato_usar)
            exito_tareas = self._guardar_tareas(formato_usar)
            
            if exito_usuarios and exito_tareas:
                print(f"💾 Todos los datos guardados en formato {formato_usar}")
                return True
            else:
                print("❌ Error al guardar algunos datos")
                return False
                
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
            return False
    
    def cargar_todo(self, formato: str = None) -> bool:
        """
        Carga todos los datos del sistema.
        
        Args:
            formato (str, optional): Formato a usar, por defecto el preferido
            
        Returns:
            bool: True si se cargó correctamente
        """
        formato_usar = formato or self.formato_preferido
        
        try:
            self._cargar_usuarios(formato_usar)
            self._cargar_tareas(formato_usar)
            print(f"📖 Todos los datos cargados desde formato {formato_usar}")
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return False
    
    def crear_backup_completo(self) -> bool:
        """
        Crea un backup completo del sistema.
        
        Returns:
            bool: True si se creó el backup correctamente
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Guardar en ambos formatos con timestamp
            self.persistencia.json.guardar_datos(f"backup_usuarios_{timestamp}", self.usuarios)
            self.persistencia.json.guardar_datos(f"backup_tareas_{timestamp}", self.tareas)
            self.persistencia.binario.guardar_datos(f"backup_usuarios_{timestamp}", self.usuarios)
            self.persistencia.binario.guardar_datos(f"backup_tareas_{timestamp}", self.tareas)
            
            print(f"📦 Backup completo creado con timestamp: {timestamp}")
            return True
            
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return False
    
    # ===============================
    # MÉTODOS PRIVADOS
    # ===============================
    
    def _cargar_datos_iniciales(self):
        """Carga datos existentes al inicializar el sistema."""
        try:
            self._cargar_usuarios()
            self._cargar_tareas()
        except Exception as e:
            print(f"⚠️ No se pudieron cargar datos iniciales: {e}")
            # Continuar con listas vacías
    
    def _cargar_usuarios(self, formato: str = None):
        """Carga usuarios desde persistencia."""
        formato_usar = formato or self.formato_preferido
        datos_usuarios = self.persistencia.cargar_usuarios(formato_usar)
        
        if datos_usuarios:
            self.usuarios = []
            for data in datos_usuarios:
                try:
                    usuario = Usuario.from_dict(data)
                    self.usuarios.append(usuario)
                except Exception as e:
                    print(f"⚠️ Error al cargar usuario: {e}")
    
    def _cargar_tareas(self, formato: str = None):
        """Carga tareas desde persistencia."""
        formato_usar = formato or self.formato_preferido
        datos_tareas = self.persistencia.cargar_tareas(formato_usar)
        
        if datos_tareas:
            self.tareas = []
            for data in datos_tareas:
                try:
                    tarea = Tarea.from_dict(data)
                    self.tareas.append(tarea)
                except Exception as e:
                    print(f"⚠️ Error al cargar tarea: {e}")
    
    def _guardar_usuarios(self, formato: str = None) -> bool:
        """Guarda usuarios en persistencia."""
        formato_usar = formato or self.formato_preferido
        return self.persistencia.guardar_usuarios(self.usuarios, formato_usar)
    
    def _guardar_tareas(self, formato: str = None) -> bool:
        """Guarda tareas en persistencia."""
        formato_usar = formato or self.formato_preferido
        return self.persistencia.guardar_tareas(self.tareas, formato_usar)
    
    def _buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuario por email normalizado."""
        for usuario in self.usuarios:
            if usuario.email.lower() == email.lower():
                return usuario
        return None

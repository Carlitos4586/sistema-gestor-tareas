"""
Gestor principal del sistema de tareas.

Esta es la clase coordinadora que integra todos los módulos del sistema:
usuarios, tareas, persistencia, reportes y utilidades.
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Generator, List, Optional
from uuid import uuid4

# Importar sistema de logging
try:
    from ..utils.logger import (
        log_advertencia,
        log_error,
        log_exito_operacion,
        log_inicio_operacion,
        obtener_logger,
    )
except ImportError:
    from utils.logger import (
        log_advertencia,
        log_error,
        log_exito_operacion,
        log_inicio_operacion,
        obtener_logger,
    )

# Importaciones de modelos
try:
    from ..models.tarea import EstadoTarea, Tarea
    from ..models.usuario import Usuario
    from ..utils.formateo import (
        formatear_fecha_legible,
        limpiar_descripcion,
        validar_email,
    )
    from ..utils.generadores import (
        GeneradorInfinito,
        generador_tareas_por_estado,
        generador_tareas_proximas_vencer,
        generador_usuarios_con_tareas,
    )
    from .persistencia import GestorPersistencia
    from .reportes import GeneradorReportes
except ImportError:
    from models.tarea import EstadoTarea, Tarea
    from models.usuario import Usuario
    from services.persistencia import GestorPersistencia
    from services.reportes import GeneradorReportes
    from utils.formateo import (
        formatear_fecha_legible,
        limpiar_descripcion,
        validar_email,
    )
    from utils.generadores import (
        GeneradorInfinito,
        generador_tareas_por_estado,
        generador_tareas_proximas_vencer,
        generador_usuarios_con_tareas,
    )


class GestorSistema:
    """
    Clase principal que coordina todas las funcionalidades del sistema de tareas.

    Esta clase integra la gestión de usuarios, tareas, persistencia y reportes,
    proporcionando una interfaz unificada para todas las operaciones del sistema.
    """

    def __init__(self, directorio_datos: str = "data"):
        """
        Inicializa el gestor del sistema.

        Args:
            directorio_datos (str): Directorio base para almacenar datos
        """
        # Configurar logger para esta clase
        self.logger = obtener_logger("gestor_sistema")

        log_inicio_operacion(
            "Inicialización del Sistema", f"Directorio: {directorio_datos}"
        )

        self.usuarios: List[Usuario] = []
        self.tareas: List[Tarea] = []

        # Inicializar subsistemas
        self.persistencia = GestorPersistencia(directorio_datos)
        self.generador_reportes = GeneradorReportes()

        # Configurar generador de IDs únicos
        self._generador_ids = GeneradorInfinito("TASK")

        # Cargar datos existentes si los hay
        self._cargar_datos_sistema()

        # Log del éxito de inicialización
        log_exito_operacion(
            "Sistema inicializado",
            f"Usuarios: {len(self.usuarios)}, Tareas: {len(self.tareas)}",
        )

        self.logger.info(f"📁 Directorio de datos: {directorio_datos}")
        self.logger.info(f"🔧 Subsistemas configurados correctamente")

    def _cargar_datos_sistema(self) -> None:
        """Carga los datos del sistema desde el almacenamiento persistente."""
        try:
            self.logger.info("🔄 Cargando datos del sistema...")

            # Intentar cargar usuarios
            usuarios_data = self.persistencia.cargar_usuarios()
            if usuarios_data:
                self.usuarios = [Usuario.from_dict(data) for data in usuarios_data]
                self.logger.info(
                    f"👥 Cargados {len(self.usuarios)} usuarios desde persistencia"
                )
            else:
                self.logger.info("👥 No se encontraron usuarios previos")

            # Intentar cargar tareas
            tareas_data = self.persistencia.cargar_tareas()
            if tareas_data:
                self.tareas = [Tarea.from_dict(data) for data in tareas_data]
                self.logger.info(
                    f"📋 Cargadas {len(self.tareas)} tareas desde persistencia"
                )
            else:
                self.logger.info("📋 No se encontraron tareas previas")

        except Exception as e:
            log_error(
                "Error al cargar datos del sistema", "Iniciando con sistema vacío", e
            )
            # Continuar con listas vacías

    def guardar_datos_sistema(self, formato: str = "json") -> bool:
        """
        Guarda todos los datos del sistema.

        Args:
            formato (str): Formato de guardado ('json' o 'binario')

        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            # Convertir a diccionarios para persistencia
            usuarios_data = [usuario.to_dict() for usuario in self.usuarios]
            tareas_data = [tarea.to_dict() for tarea in self.tareas]

            if formato == "json":
                resultado_usuarios = self.persistencia.guardar_usuarios(usuarios_data)
                resultado_tareas = self.persistencia.guardar_tareas(tareas_data)
            elif formato == "binario":
                resultado_usuarios = self.persistencia.guardar_usuarios_binario(
                    usuarios_data
                )
                resultado_tareas = self.persistencia.guardar_tareas_binario(tareas_data)
            else:
                print(f"❌ Formato no válido: {formato}")
                return False

            if resultado_usuarios and resultado_tareas:
                print(f"✅ Datos guardados exitosamente en formato {formato}")
                return True
            else:
                print(f"❌ Error al guardar algunos datos")
                return False

        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
            return False

    def crear_backup_completo(self) -> bool:
        """
        Crea un backup completo del sistema.

        Returns:
            bool: True si el backup se creó exitosamente
        """
        try:
            resultado = self.persistencia.crear_backup()
            if resultado:
                print("🔒 Backup completo creado exitosamente")
                return True
            else:
                print("❌ Error al crear backup")
                return False
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return False

    # ===============================
    # GESTIÓN DE USUARIOS
    # ===============================

    def crear_usuario(self, nombre: str, email: str) -> Optional[Usuario]:
        """
        Crea un nuevo usuario en el sistema.

        Args:
            nombre (str): Nombre del usuario
            email (str): Email del usuario

        Returns:
            Optional[Usuario]: Usuario creado o None si hay error
        """
        log_inicio_operacion("Crear Usuario", f"{nombre} ({email})")

        # Validaciones usando utilidades de formateo
        if not nombre or not nombre.strip():
            log_error("Validación fallida", "El nombre no puede estar vacío")
            return None

        if not validar_email(email):
            log_error("Validación fallida", f"Formato de email inválido: {email}")
            return None

        # Verificar email único
        if any(u.email.lower() == email.lower() for u in self.usuarios):
            log_advertencia("Email duplicado", f"Ya existe usuario con email: {email}")
            return None

        try:
            # Crear usuario
            usuario = Usuario(nombre=nombre.strip(), email=email.lower().strip())

            self.usuarios.append(usuario)

            # Log exitoso con detalles
            log_exito_operacion(
                "Usuario creado",
                f"{usuario.nombre} ({usuario.email}) - ID: {usuario.id[:8]}...",
            )
            self.logger.info(f"👥 Total usuarios en sistema: {len(self.usuarios)}")

            return usuario

        except Exception as e:
            log_error("Error al crear usuario", f"Usuario: {nombre}", e)
            return None

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca un usuario por su email.

        Args:
            email (str): Email del usuario

        Returns:
            Optional[Usuario]: Usuario encontrado o None
        """
        email_lower = email.lower().strip()
        for usuario in self.usuarios:
            if usuario.email == email_lower:
                return usuario
        return None

    def obtener_usuario_por_id(self, usuario_id: str) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.

        Args:
            usuario_id (str): ID del usuario

        Returns:
            Optional[Usuario]: Usuario encontrado o None
        """
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def listar_usuarios_activos(self) -> Generator[Dict[str, Any], None, None]:
        """
        Genera usuarios que tienen tareas asignadas con sus detalles.

        Yields:
            Dict[str, Any]: Información del usuario con sus tareas
        """
        return generador_usuarios_con_tareas(self.usuarios, self.tareas)

    def eliminar_usuario(self, usuario_id: str) -> bool:
        """
        Elimina un usuario del sistema.

        Args:
            usuario_id (str): ID del usuario a eliminar

        Returns:
            bool: True si se eliminó exitosamente
        """
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            print(f"❌ Usuario no encontrado: {usuario_id}")
            return False

        # Verificar si tiene tareas asignadas
        tareas_asignadas = [t for t in self.tareas if t.usuario_id == usuario_id]
        if tareas_asignadas:
            print(f"⚠️ El usuario tiene {len(tareas_asignadas)} tareas asignadas.")
            print("   Reasigne o elimine las tareas antes de eliminar el usuario.")
            return False

        # Eliminar usuario
        self.usuarios.remove(usuario)
        print(f"✅ Usuario eliminado: {usuario.nombre}")
        return True

    # ===============================
    # GESTIÓN DE TAREAS
    # ===============================

    def crear_tarea(
        self,
        titulo: str,
        descripcion: str,
        fecha_limite: datetime,
        usuario_email: str = None,
    ) -> Optional[Tarea]:
        """
        Crea una nueva tarea en el sistema.

        Args:
            titulo (str): Título de la tarea
            descripcion (str): Descripción de la tarea
            fecha_limite (datetime): Fecha límite
            usuario_email (str, optional): Email del usuario asignado

        Returns:
            Optional[Tarea]: Tarea creada o None si hay error
        """
        # Validaciones básicas
        if not titulo or not titulo.strip():
            print("❌ El título de la tarea no puede estar vacío")
            return None

        # Validar fecha límite si se proporciona
        if fecha_limite and fecha_limite <= datetime.now():
            print("❌ La fecha límite debe ser futura")
            return None

        # Limpiar descripción usando utilidades
        descripcion_limpia = limpiar_descripcion(descripcion) if descripcion else None

        # Buscar usuario si se especifica
        usuario_id = None
        if usuario_email:
            usuario = self.obtener_usuario_por_email(usuario_email)
            if not usuario:
                print(f"❌ Usuario no encontrado: {usuario_email}")
                return None
            usuario_id = usuario.id

        try:
            # Crear tarea usando nuevo constructor
            tarea = Tarea(
                titulo=titulo.strip(),
                descripcion=descripcion_limpia,
                fecha_limite=fecha_limite,
                usuario_id=usuario_id,
                prioridad="baja"
            )

            self.tareas.append(tarea)

            # Actualizar lista de tareas del usuario si está asignado
            if usuario_id:
                usuario = self.obtener_usuario_por_id(usuario_id)
                if usuario and tarea.id not in usuario.tareas_asignadas:
                    usuario.tareas_asignadas.append(tarea.id)

            print(f"✅ Tarea creada: {titulo}")
            return tarea

        except Exception as e:
            print(f"❌ Error al crear tarea: {e}")
            return None

    def obtener_tarea_por_id(self, tarea_id: str) -> Optional[Tarea]:
        """
        Busca una tarea por su ID.

        Args:
            tarea_id (str): ID de la tarea

        Returns:
            Optional[Tarea]: Tarea encontrada o None
        """
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                return tarea
        return None

    def asignar_tarea(self, tarea_id: str, usuario_email: str) -> bool:
        """
        Asigna una tarea a un usuario.

        Args:
            tarea_id (str): ID de la tarea
            usuario_email (str): Email del usuario

        Returns:
            bool: True si se asignó exitosamente
        """
        tarea = self.obtener_tarea_por_id(tarea_id)
        if not tarea:
            print(f"❌ Tarea no encontrada: {tarea_id}")
            return False

        usuario = self.obtener_usuario_por_email(usuario_email)
        if not usuario:
            print(f"❌ Usuario no encontrado: {usuario_email}")
            return False

        # Desasignar de usuario anterior si existe
        if tarea.usuario_id:
            usuario_anterior = self.obtener_usuario_por_id(tarea.usuario_id)
            if usuario_anterior and tarea_id in usuario_anterior.tareas_asignadas:
                usuario_anterior.tareas_asignadas.remove(tarea_id)

        # Asignar a nuevo usuario
        tarea.usuario_id = usuario.id
        if tarea_id not in usuario.tareas_asignadas:
            usuario.tareas_asignadas.append(tarea_id)

        print(f"✅ Tarea '{tarea.titulo}' asignada a {usuario.nombre}")
        return True

    def cambiar_estado_tarea(self, tarea_id: str, nuevo_estado: str) -> bool:
        """
        Cambia el estado de una tarea.

        Args:
            tarea_id (str): ID de la tarea
            nuevo_estado (str): Nuevo estado ('pendiente', 'en_progreso', 'completada')

        Returns:
            bool: True si se cambió exitosamente
        """
        tarea = self.obtener_tarea_por_id(tarea_id)
        if not tarea:
            print(f"❌ Tarea no encontrada: {tarea_id}")
            return False

        try:
            if nuevo_estado == "pendiente":
                estado = EstadoTarea.PENDIENTE
            elif nuevo_estado == "en_progreso":
                estado = EstadoTarea.EN_PROGRESO
            elif nuevo_estado == "completada":
                estado = EstadoTarea.COMPLETADA
            else:
                print(f"❌ Estado no válido: {nuevo_estado}")
                return False

            estado_anterior = tarea.estado.value
            tarea.estado = estado
            print(
                f"✅ Estado de tarea '{tarea.titulo}' cambiado: {estado_anterior} → {nuevo_estado}"
            )
            return True

        except Exception as e:
            print(f"❌ Error al cambiar estado: {e}")
            return False

    def listar_tareas_por_estado(self, estado: str) -> Generator[Tarea, None, None]:
        """
        Lista tareas filtradas por estado usando generadores.

        Args:
            estado (str): Estado a filtrar

        Yields:
            Tarea: Tareas del estado especificado
        """
        return generador_tareas_por_estado(self.tareas, estado)

    def obtener_tareas_proximas_vencer(
        self, dias: int = 7
    ) -> Generator[Tarea, None, None]:
        """
        Obtiene tareas que están próximas a vencer.

        Args:
            dias (int): Número de días de anticipación

        Yields:
            Tarea: Tareas próximas a vencer
        """
        return generador_tareas_proximas_vencer(self.tareas, dias)

    def actualizar_tarea(self, tarea: Tarea) -> bool:
        """
        Actualiza una tarea existente en el sistema.

        Args:
            tarea (Tarea): Tarea con los datos actualizados

        Returns:
            bool: True si se actualizó exitosamente
        """
        # La tarea ya está actualizada en memoria por referencia
        # Solo necesitamos confirmar que existe
        tarea_existente = self.obtener_tarea_por_id(tarea.id)
        if tarea_existente:
            return True
        return False
    
    def eliminar_tarea(self, tarea_id: str) -> bool:
        """
        Elimina una tarea del sistema.

        Args:
            tarea_id (str): ID de la tarea a eliminar

        Returns:
            bool: True si se eliminó exitosamente
        """
        tarea = self.obtener_tarea_por_id(tarea_id)
        if not tarea:
            print(f"❌ Tarea no encontrada: {tarea_id}")
            return False

        # Remover de lista de usuario asignado
        if tarea.usuario_id:
            usuario = self.obtener_usuario_por_id(tarea.usuario_id)
            if usuario and tarea_id in usuario.tareas_asignadas:
                usuario.tareas_asignadas.remove(tarea_id)

        # Eliminar tarea
        self.tareas.remove(tarea)
        print(f"✅ Tarea eliminada: {tarea.titulo}")
        return True

    # ===============================
    # REPORTES Y ESTADÍSTICAS
    # ===============================

    def generar_reporte_usuarios(self, formato_tabla: str = "grid") -> str:
        """
        Genera reporte completo de usuarios.

        Args:
            formato_tabla (str): Formato de tabla para tabulate

        Returns:
            str: Reporte formateado
        """
        return self.generador_reportes.generar_reporte_usuarios(
            self.usuarios, self.tareas, formato_tabla
        )

    def generar_reporte_tareas(
        self, formato_tabla: str = "grid", filtrar_estado: str = None
    ) -> str:
        """
        Genera reporte completo de tareas.

        Args:
            formato_tabla (str): Formato de tabla para tabulate
            filtrar_estado (str, optional): Filtrar por estado específico

        Returns:
            str: Reporte formateado
        """
        return self.generador_reportes.generar_reporte_tareas(
            self.tareas, self.usuarios, formato_tabla, filtrar_estado
        )

    def generar_dashboard_ejecutivo(self) -> str:
        """
        Genera dashboard ejecutivo completo.

        Returns:
            str: Dashboard formateado
        """
        return self.generador_reportes.generar_dashboard_ejecutivo(
            self.usuarios, self.tareas
        )

    def generar_reporte_calendario(self, año: int, mes: int) -> str:
        """
        Genera reporte de calendario para un mes específico.

        Args:
            año (int): Año del calendario
            mes (int): Mes del calendario (1-12)

        Returns:
            str: Reporte de calendario
        """
        return self.generador_reportes.generar_reporte_calendario(self.tareas, año, mes)

    def generar_reporte_productividad(self, periodo_dias: int = 30) -> str:
        """
        Genera reporte de productividad.

        Args:
            periodo_dias (int): Período de análisis en días

        Returns:
            str: Reporte de productividad
        """
        return self.generador_reportes.generar_reporte_productividad(
            self.usuarios, self.tareas, periodo_dias
        )

    # ===============================
    # UTILIDADES Y ESTADÍSTICAS
    # ===============================

    def obtener_estadisticas_sistema(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del sistema.

        Returns:
            Dict[str, Any]: Diccionario con estadísticas
        """
        # Usar generadores para calcular estadísticas
        tareas_pendientes = list(self.listar_tareas_por_estado("pendiente"))
        tareas_en_progreso = list(self.listar_tareas_por_estado("en_progreso"))
        tareas_completadas = list(self.listar_tareas_por_estado("completada"))
        usuarios_activos = list(self.listar_usuarios_activos())
        tareas_proximas = list(self.obtener_tareas_proximas_vencer(3))

        # Calcular métricas adicionales
        total_tareas = len(self.tareas)
        porcentaje_completadas = (
            (len(tareas_completadas) / total_tareas * 100) if total_tareas > 0 else 0
        )

        tareas_vencidas = [t for t in self.tareas if t.esta_vencida()]

        return {
            "total_usuarios": len(self.usuarios),
            "usuarios_activos": len(usuarios_activos),
            "total_tareas": total_tareas,
            "tareas_pendientes": len(tareas_pendientes),
            "tareas_en_progreso": len(tareas_en_progreso),
            "tareas_completadas": len(tareas_completadas),
            "porcentaje_completadas": round(porcentaje_completadas, 2),
            "tareas_vencidas": len(tareas_vencidas),
            "tareas_proximas_vencer": len(tareas_proximas),
            "fecha_consulta": formatear_fecha_legible(datetime.now()),
        }

    def buscar_tareas(self, termino: str) -> List[Tarea]:
        """
        Busca tareas por término en título o descripción.

        Args:
            termino (str): Término de búsqueda

        Returns:
            List[Tarea]: Lista de tareas que coinciden
        """
        if not termino or not termino.strip():
            return []

        termino_lower = termino.lower().strip()
        tareas_encontradas = []

        for tarea in self.tareas:
            if termino_lower in tarea.titulo.lower() or (
                tarea.descripcion and termino_lower in tarea.descripcion.lower()
            ):
                tareas_encontradas.append(tarea)

        return tareas_encontradas

    def limpiar_tareas_vencidas(self) -> int:
        """
        Elimina tareas completadas que están vencidas hace más de 30 días.

        Returns:
            int: Número de tareas eliminadas
        """
        fecha_limite = datetime.now() - timedelta(days=30)
        tareas_a_eliminar = []

        for tarea in self.tareas:
            if (
                tarea.estado == EstadoTarea.COMPLETADA
                and tarea.fecha_limite < fecha_limite
            ):
                tareas_a_eliminar.append(tarea)

        # Eliminar tareas
        for tarea in tareas_a_eliminar:
            self.eliminar_tarea(tarea.id)

        if tareas_a_eliminar:
            print(
                f"🧹 Se eliminaron {len(tareas_a_eliminar)} tareas completadas antiguas"
            )

        return len(tareas_a_eliminar)

    def __str__(self) -> str:
        """Representación en cadena del sistema."""
        stats = self.obtener_estadisticas_sistema()
        return f"""
🚀 Sistema de Gestión de Tareas
==============================
👥 Usuarios: {stats['total_usuarios']} (Activos: {stats['usuarios_activos']})
📋 Tareas: {stats['total_tareas']} 
   • Pendientes: {stats['tareas_pendientes']}
   • En Progreso: {stats['tareas_en_progreso']} 
   • Completadas: {stats['tareas_completadas']}
📊 Progreso: {stats['porcentaje_completadas']}%
⚠️  Vencidas: {stats['tareas_vencidas']}
🔥 Próximas a vencer: {stats['tareas_proximas_vencer']}
""".strip()

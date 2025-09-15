"""
Módulo que define la clase Tarea para el sistema de gestión de tareas.

Esta clase representa una tarea en el sistema con sus propiedades básicas
y métodos para gestionar el estado y asignación.
"""

import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Optional


class EstadoTarea(Enum):
    """
    Enumeración de los posibles estados de una tarea.
    """

    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"


class Tarea:
    """
    Clase que representa una tarea en el sistema de gestión de tareas.

    Una tarea tiene propiedades básicas como título, descripción, fechas
    y puede cambiar de estado y ser reasignada a diferentes usuarios.

    Attributes:
        id (str): Identificador único de la tarea
        titulo (str): Título descriptivo de la tarea
        descripcion (str): Descripción detallada de la tarea
        fecha_creacion (datetime): Fecha y hora de creación
        fecha_limite (datetime): Fecha límite para completar la tarea
        estado (EstadoTarea): Estado actual de la tarea
        usuario_id (Optional[str]): ID del usuario asignado a la tarea
    """

    def __init__(
        self,
        titulo: str,
        descripcion: Optional[str] = None,
        fecha_limite: Optional[datetime] = None,
        usuario_id: Optional[str] = None,
        prioridad: str = "baja",
    ):
        """
        Inicializa una nueva tarea.

        Args:
            titulo (str): Título de la tarea
            descripcion (Optional[str]): Descripción detallada
            fecha_limite (Optional[datetime]): Fecha límite para completar
            usuario_id (Optional[str]): ID del usuario asignado
            prioridad (str): Prioridad de la tarea (baja, media, alta)

        Raises:
            ValueError: Si el título está vacío
        """
        # Validaciones usando métodos de cadenas
        if not titulo or not titulo.strip():
            raise ValueError("El título no puede estar vacío")

        # Validar fecha límite si se proporciona
        # Solo validar fechas futuras para NUEVAS tareas, no para datos cargados
        if (
            fecha_limite
            and fecha_limite <= datetime.now()
            and not hasattr(self, "_cargando_desde_archivo")
        ):
            raise ValueError("La fecha límite debe ser futura")

        self.id = str(uuid.uuid4())
        self.titulo = titulo.strip().title()  # Formateo de cadenas
        self.descripcion = descripcion.strip() if descripcion else None
        self.fecha_creacion = datetime.now()
        self.fecha_limite = fecha_limite
        self.fecha_finalizacion: Optional[datetime] = None
        self.estado = EstadoTarea.PENDIENTE
        self.usuario_id = usuario_id
        self.prioridad = prioridad

    def cambiar_estado(self, nuevo_estado: EstadoTarea) -> bool:
        """
        Cambia el estado de la tarea.

        Args:
            nuevo_estado (EstadoTarea): Nuevo estado para la tarea

        Returns:
            bool: True si el cambio fue exitoso

        Raises:
            ValueError: Si el nuevo estado no es válido
        """
        if not isinstance(nuevo_estado, EstadoTarea):
            raise ValueError("El estado debe ser una instancia de EstadoTarea")

        # Lógica de transición de estados
        estado_anterior = self.estado
        self.estado = nuevo_estado

        # Log del cambio (usando formateo de cadenas)
        print(f"Tarea '{self.titulo}': {estado_anterior.value} → {nuevo_estado.value}")
        return True

    def reasignar(self, nuevo_usuario_id: Optional[str]) -> bool:
        """
        Reasigna la tarea a un nuevo usuario.

        Args:
            nuevo_usuario_id (Optional[str]): ID del nuevo usuario asignado

        Returns:
            bool: True si la reasignación fue exitosa
        """
        usuario_anterior = self.usuario_id
        self.usuario_id = nuevo_usuario_id

        # Log de la reasignación usando métodos de cadenas
        if usuario_anterior and nuevo_usuario_id:
            print(
                f"Tarea '{self.titulo}' reasignada de {usuario_anterior} a {nuevo_usuario_id}"
            )
        elif nuevo_usuario_id:
            print(f"Tarea '{self.titulo}' asignada a {nuevo_usuario_id}")
        else:
            print(f"Tarea '{self.titulo}' desasignada de {usuario_anterior}")

        return True

    def calcular_dias_restantes(self) -> int:
        """
        Calcula los días restantes hasta la fecha límite.

        Returns:
            int: Número de días restantes (negativo si está vencida)
        """
        # Validar que fecha_limite sea datetime
        fecha_limite = self.fecha_limite
        if isinstance(fecha_limite, str):
            fecha_limite = datetime.fromisoformat(fecha_limite)
        
        diferencia = fecha_limite - datetime.now()
        return diferencia.days

    def esta_vencida(self) -> bool:
        """
        Verifica si la tarea está vencida.

        Returns:
            bool: True si la fecha límite ya pasó
        """
        # Validar que fecha_limite sea datetime
        fecha_limite = self.fecha_limite
        if isinstance(fecha_limite, str):
            fecha_limite = datetime.fromisoformat(fecha_limite)
        
        return datetime.now() > fecha_limite

    def obtener_duracion_estimada(self) -> int:
        """
        Calcula la duración estimada desde creación hasta fecha límite.

        Returns:
            int: Número de días de duración estimada
        """
        # Validar que fecha_limite sea datetime
        fecha_limite = self.fecha_limite
        if isinstance(fecha_limite, str):
            fecha_limite = datetime.fromisoformat(fecha_limite)
            
        fecha_creacion = self.fecha_creacion
        if isinstance(fecha_creacion, str):
            fecha_creacion = datetime.fromisoformat(fecha_creacion)
        
        diferencia = fecha_limite - fecha_creacion
        return diferencia.days

    def obtener_resumen(self) -> str:
        """
        Obtiene un resumen formateado de la tarea usando métodos de cadenas.

        Returns:
            str: Resumen legible de la tarea
        """
        dias_restantes = self.calcular_dias_restantes()
        estado_texto = self.estado.value.replace("_", " ").title()

        # Construcción de cadena con múltiples métodos de formateo
        resumen_partes = [
            f"📋 {self.titulo}",
            f"Estado: {estado_texto}",
            f"Días restantes: {dias_restantes}",
        ]

        if self.usuario_id:
            resumen_partes.append(f"Asignado a: {self.usuario_id}")

        # Join de lista usando métodos de listas
        return " | ".join(resumen_partes)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la tarea a un diccionario para serialización.

        Returns:
            Dict[str, Any]: Representación en diccionario de la tarea
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_limite": (
                self.fecha_limite.isoformat() if self.fecha_limite else None
            ),
            "fecha_finalizacion": (
                self.fecha_finalizacion.isoformat() if self.fecha_finalizacion else None
            ),
            "estado": self.estado.value,
            "usuario_id": self.usuario_id,
            "prioridad": self.prioridad,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tarea":
        """
        Crea una tarea desde un diccionario.

        Args:
            data (Dict[str, Any]): Datos de la tarea en formato diccionario

        Returns:
            Tarea: Nueva instancia de Tarea

        Raises:
            KeyError: Si faltan campos requeridos
            ValueError: Si los datos son inválidos
        """
        # Crear tarea básica
        fecha_limite = None
        if data.get("fecha_limite"):
            fecha_limite = datetime.fromisoformat(data["fecha_limite"])

        tarea = cls(
            titulo=data["titulo"],
            descripcion=data.get("descripcion"),
            fecha_limite=fecha_limite,
            usuario_id=data.get("usuario_id"),
            prioridad=data.get("prioridad", "baja"),
        )

        # Restaurar campos adicionales
        tarea.id = data["id"]
        tarea.fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        if data.get("fecha_finalizacion"):
            tarea.fecha_finalizacion = datetime.fromisoformat(
                data["fecha_finalizacion"]
            )
        tarea.estado = EstadoTarea(data["estado"])

        return tarea

    def __str__(self) -> str:
        """
        Representación en cadena de la tarea.

        Returns:
            str: Representación legible de la tarea
        """
        return f"Tarea('{self.titulo}', {self.estado.value}, {self.calcular_dias_restantes()} días)"

    def __repr__(self) -> str:
        """
        Representación técnica de la tarea.

        Returns:
            str: Representación técnica de la tarea
        """
        return f"Tarea(id='{self.id}', titulo='{self.titulo}', estado='{self.estado.value}')"

    def __eq__(self, other) -> bool:
        """
        Compara dos tareas por su ID.

        Args:
            other: Otro objeto a comparar

        Returns:
            bool: True si son la misma tarea
        """
        if not isinstance(other, Tarea):
            return False
        return self.id == other.id

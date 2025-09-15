"""
Módulo que define la clase Usuario para el sistema de gestión de tareas.

Esta clase representa un usuario en el sistema con sus propiedades básicas
y métodos para gestionar las tareas asignadas.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional


class Usuario:
    """
    Clase que representa un usuario en el sistema de gestión de tareas.
    
    Un usuario puede tener múltiples tareas asignadas y proporciona
    métodos para gestionar estas asignaciones.
    
    Attributes:
        id (str): Identificador único del usuario
        nombre (str): Nombre completo del usuario
        email (str): Dirección de correo electrónico
        fecha_registro (datetime): Fecha y hora de registro en el sistema
        tareas_asignadas (List[str]): Lista de IDs de tareas asignadas
    """
    
    def __init__(self, nombre: str, email: str, telefono: Optional[str] = None):
        """
        Inicializa un nuevo usuario.

        Args:
            nombre (str): Nombre completo del usuario
            email (str): Dirección de correo electrónico única
            telefono (Optional[str]): Número de teléfono opcional
            
        Raises:
            ValueError: Si el nombre o email están vacíos
        """
        # Validaciones básicas usando métodos de cadenas
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not email or not email.strip() or '@' not in email:
            raise ValueError("El email debe ser válido")
            
        self.id = str(uuid.uuid4())
        self.nombre = nombre.strip().title()  # Formateo de cadenas
        self.email = email.strip().lower()    # Normalización de email
        self.telefono = telefono.strip() if telefono else None
        self.fecha_registro = datetime.now()
        self.tareas_asignadas: List[str] = []
    
    def agregar_tarea(self, tarea_id: str) -> bool:
        """
        Agrega una tarea a la lista de tareas asignadas del usuario.
        
        Args:
            tarea_id (str): ID de la tarea a asignar
            
        Returns:
            bool: True si se agregó correctamente, False si ya existía
            
        Raises:
            ValueError: Si el tarea_id está vacío
        """
        if not tarea_id or not tarea_id.strip():
            raise ValueError("El ID de la tarea no puede estar vacío")
            
        # Uso de métodos de listas para verificar y agregar
        if tarea_id not in self.tareas_asignadas:
            self.tareas_asignadas.append(tarea_id)
            return True
        return False
    
    def remover_tarea(self, tarea_id: str) -> bool:
        """
        Remueve una tarea de la lista de tareas asignadas.
        
        Args:
            tarea_id (str): ID de la tarea a remover
            
        Returns:
            bool: True si se removió correctamente, False si no existía
        """
        # Uso de métodos de listas para remover
        try:
            self.tareas_asignadas.remove(tarea_id)
            return True
        except ValueError:
            return False
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas básicas del usuario.
        
        Returns:
            Dict[str, Any]: Diccionario con estadísticas del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_registro': self.fecha_registro.isoformat(),
            'total_tareas_asignadas': len(self.tareas_asignadas),
            'tareas_asignadas': self.tareas_asignadas.copy()  # Copia de la lista
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el usuario a un diccionario para serialización.

        Returns:
            Dict[str, Any]: Representación en diccionario del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat(),
            'tareas_asignadas': self.tareas_asignadas.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Usuario':
        """
        Crea un usuario desde un diccionario.
        
        Args:
            data (Dict[str, Any]): Datos del usuario en formato diccionario
            
        Returns:
            Usuario: Nueva instancia de Usuario
            
        Raises:
            KeyError: Si faltan campos requeridos
            ValueError: Si los datos son inválidos
        """
        # Crear usuario básico
        usuario = cls(data['nombre'], data['email'], data.get('telefono'))
        
        # Restaurar campos adicionales
        usuario.id = data['id']
        usuario.fecha_registro = datetime.fromisoformat(data['fecha_registro'])
        usuario.tareas_asignadas = data.get('tareas_asignadas', []).copy()
        
        return usuario
    
    def __str__(self) -> str:
        """
        Representación en cadena del usuario.
        
        Returns:
            str: Representación legible del usuario
        """
        return f"Usuario('{self.nombre}', '{self.email}', {len(self.tareas_asignadas)} tareas)"
    
    def __repr__(self) -> str:
        """
        Representación técnica del usuario.
        
        Returns:
            str: Representación técnica del usuario
        """
        return f"Usuario(id='{self.id}', nombre='{self.nombre}', email='{self.email}')"
    
    def __eq__(self, other) -> bool:
        """
        Compara dos usuarios por su ID.
        
        Args:
            other: Otro objeto a comparar
            
        Returns:
            bool: True si son el mismo usuario
        """
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id

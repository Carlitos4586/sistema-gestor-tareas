"""
Pruebas unitarias para la clase Usuario.

Este módulo contiene todas las pruebas para verificar el correcto
funcionamiento de la clase Usuario y sus métodos.
"""

import pytest
import sys
import os
from datetime import datetime

# Agregar el directorio src al path para importar las clases
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.usuario import Usuario


class TestUsuario:
    """Clase de pruebas para la clase Usuario."""
    
    def test_crear_usuario_valido(self):
        """Prueba la creación de un usuario con datos válidos."""
        # Arrange
        nombre = "juan pérez"
        email = "JUAN@EMAIL.COM"
        
        # Act
        usuario = Usuario(nombre, email)
        
        # Assert
        assert usuario.nombre == "Juan Pérez"  # Verifica formateo de cadenas
        assert usuario.email == "juan@email.com"  # Verifica normalización
        assert len(usuario.id) == 36  # UUID tiene 36 caracteres
        assert isinstance(usuario.fecha_registro, datetime)
        assert usuario.tareas_asignadas == []
    
    def test_crear_usuario_nombre_vacio(self):
        """Prueba que falle con nombre vacío."""
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            Usuario("", "test@email.com")
    
    def test_crear_usuario_nombre_solo_espacios(self):
        """Prueba que falle con nombre que solo tiene espacios."""
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            Usuario("   ", "test@email.com")
    
    def test_crear_usuario_email_vacio(self):
        """Prueba que falle con email vacío."""
        with pytest.raises(ValueError, match="El email debe ser válido"):
            Usuario("Juan Pérez", "")
    
    def test_crear_usuario_email_invalido(self):
        """Prueba que falle con email sin @."""
        with pytest.raises(ValueError, match="El email debe ser válido"):
            Usuario("Juan Pérez", "emailinvalido")
    
    def test_agregar_tarea_nueva(self):
        """Prueba agregar una tarea nueva."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        tarea_id = "tarea-123"
        
        # Act
        resultado = usuario.agregar_tarea(tarea_id)
        
        # Assert
        assert resultado is True
        assert tarea_id in usuario.tareas_asignadas
        assert len(usuario.tareas_asignadas) == 1
    
    def test_agregar_tarea_duplicada(self):
        """Prueba agregar una tarea que ya existe."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        tarea_id = "tarea-123"
        usuario.agregar_tarea(tarea_id)
        
        # Act
        resultado = usuario.agregar_tarea(tarea_id)
        
        # Assert
        assert resultado is False
        assert len(usuario.tareas_asignadas) == 1  # No se duplica
    
    def test_agregar_tarea_id_vacio(self):
        """Prueba que falle con ID de tarea vacío."""
        usuario = Usuario("Test User", "test@email.com")
        
        with pytest.raises(ValueError, match="El ID de la tarea no puede estar vacío"):
            usuario.agregar_tarea("")
    
    def test_remover_tarea_existente(self):
        """Prueba remover una tarea existente."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        tarea_id = "tarea-123"
        usuario.agregar_tarea(tarea_id)
        
        # Act
        resultado = usuario.remover_tarea(tarea_id)
        
        # Assert
        assert resultado is True
        assert tarea_id not in usuario.tareas_asignadas
        assert len(usuario.tareas_asignadas) == 0
    
    def test_remover_tarea_inexistente(self):
        """Prueba remover una tarea que no existe."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        
        # Act
        resultado = usuario.remover_tarea("tarea-inexistente")
        
        # Assert
        assert resultado is False
        assert len(usuario.tareas_asignadas) == 0
    
    def test_obtener_estadisticas(self):
        """Prueba obtener estadísticas del usuario."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        usuario.agregar_tarea("tarea-1")
        usuario.agregar_tarea("tarea-2")
        
        # Act
        stats = usuario.obtener_estadisticas()
        
        # Assert
        assert stats['id'] == usuario.id
        assert stats['nombre'] == "Test User"
        assert stats['email'] == "test@email.com"
        assert stats['total_tareas_asignadas'] == 2
        assert len(stats['tareas_asignadas']) == 2
        assert 'fecha_registro' in stats
    
    def test_to_dict(self):
        """Prueba la conversión a diccionario."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        usuario.agregar_tarea("tarea-1")
        
        # Act
        data = usuario.to_dict()
        
        # Assert
        assert data['nombre'] == "Test User"
        assert data['email'] == "test@email.com"
        assert data['id'] == usuario.id
        assert 'fecha_registro' in data
        assert data['tareas_asignadas'] == ["tarea-1"]
    
    def test_from_dict(self):
        """Prueba la creación desde diccionario."""
        # Arrange
        fecha_registro = datetime.now()
        data = {
            'id': 'test-id-123',
            'nombre': 'Test User',
            'email': 'test@email.com',
            'fecha_registro': fecha_registro.isoformat(),
            'tareas_asignadas': ['tarea-1', 'tarea-2']
        }
        
        # Act
        usuario = Usuario.from_dict(data)
        
        # Assert
        assert usuario.id == 'test-id-123'
        assert usuario.nombre == 'Test User'
        assert usuario.email == 'test@email.com'
        assert usuario.fecha_registro == fecha_registro
        assert usuario.tareas_asignadas == ['tarea-1', 'tarea-2']
    
    def test_str_representation(self):
        """Prueba la representación en cadena."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        usuario.agregar_tarea("tarea-1")
        
        # Act
        str_repr = str(usuario)
        
        # Assert
        assert "Test User" in str_repr
        assert "test@email.com" in str_repr
        assert "1 tareas" in str_repr
    
    def test_repr_representation(self):
        """Prueba la representación técnica."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        
        # Act
        repr_str = repr(usuario)
        
        # Assert
        assert "Usuario(id=" in repr_str
        assert "nombre='Test User'" in repr_str
        assert "email='test@email.com'" in repr_str
    
    def test_equality(self):
        """Prueba la comparación de usuarios."""
        # Arrange
        usuario1 = Usuario("Test User", "test@email.com")
        usuario2 = Usuario("Another User", "another@email.com")
        
        # Crear usuario con el mismo ID
        usuario3 = Usuario("Different Name", "different@email.com")
        usuario3.id = usuario1.id
        
        # Act & Assert
        assert usuario1 == usuario3  # Mismo ID
        assert usuario1 != usuario2  # Diferente ID
        assert usuario1 != "not a user"  # Tipo diferente
    
    def test_formateo_nombre_multiples_espacios(self):
        """Prueba el formateo correcto de nombres con múltiples espacios."""
        # Arrange & Act
        usuario = Usuario("  juan   carlos   pérez  ", "test@email.com")
        
        # Assert - verifica métodos de cadenas
        assert usuario.nombre == "Juan   Carlos   Pérez"
    
    def test_manejo_listas_tareas_multiples(self):
        """Prueba el manejo de listas con múltiples tareas."""
        # Arrange
        usuario = Usuario("Test User", "test@email.com")
        tareas = ["tarea-1", "tarea-2", "tarea-3", "tarea-4", "tarea-5"]
        
        # Act - uso de métodos de listas
        for tarea in tareas:
            usuario.agregar_tarea(tarea)
        
        # Assert
        assert len(usuario.tareas_asignadas) == 5
        assert all(tarea in usuario.tareas_asignadas for tarea in tareas)
        
        # Remover algunas tareas
        usuario.remover_tarea("tarea-2")
        usuario.remover_tarea("tarea-4")
        
        assert len(usuario.tareas_asignadas) == 3
        assert "tarea-2" not in usuario.tareas_asignadas
        assert "tarea-4" not in usuario.tareas_asignadas

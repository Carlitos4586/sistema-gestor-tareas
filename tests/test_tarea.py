"""
Pruebas unitarias para la clase Tarea.

Este módulo contiene todas las pruebas para verificar el correcto
funcionamiento de la clase Tarea y sus métodos.
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio src al path para importar las clases
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.tarea import Tarea, EstadoTarea


class TestTarea:
    """Clase de pruebas para la clase Tarea."""
    
    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba."""
        self.fecha_futura = datetime.now() + timedelta(days=7)
        self.titulo = "  tarea de prueba  "
        self.descripcion = "  descripción detallada de la tarea  "
        self.usuario_id = "usuario-123"
    
    def test_crear_tarea_valida(self):
        """Prueba la creación de una tarea con datos válidos."""
        # Act
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura, self.usuario_id)
        
        # Assert
        assert tarea.titulo == "Tarea De Prueba"  # Verifica formateo de cadenas
        assert tarea.descripcion == "descripción detallada de la tarea"  # Sin formateo title
        assert len(tarea.id) == 36  # UUID tiene 36 caracteres
        assert isinstance(tarea.fecha_creacion, datetime)
        assert tarea.fecha_limite == self.fecha_futura
        assert tarea.estado == EstadoTarea.PENDIENTE
        assert tarea.usuario_id == self.usuario_id
    
    def test_crear_tarea_sin_usuario(self):
        """Prueba crear tarea sin usuario asignado."""
        # Act
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        # Assert
        assert tarea.usuario_id is None
    
    def test_crear_tarea_titulo_vacio(self):
        """Prueba que falle con título vacío."""
        with pytest.raises(ValueError, match="El título no puede estar vacío"):
            Tarea("", self.descripcion, self.fecha_futura)
    
    def test_crear_tarea_titulo_solo_espacios(self):
        """Prueba que falle con título que solo tiene espacios."""
        with pytest.raises(ValueError, match="El título no puede estar vacío"):
            Tarea("   ", self.descripcion, self.fecha_futura)
    
    def test_crear_tarea_descripcion_vacia(self):
        """Prueba crear tarea con descripción vacía (debería permitirse)."""
        tarea = Tarea(self.titulo, "", self.fecha_futura)
        assert tarea.descripcion == "" or tarea.descripcion is None
    
    def test_crear_tarea_fecha_pasada(self):
        """Prueba que falle con fecha límite en el pasado."""
        fecha_pasada = datetime.now() - timedelta(days=1)
        
        with pytest.raises(ValueError, match="La fecha límite debe ser futura"):
            Tarea(self.titulo, self.descripcion, fecha_pasada)
    
    def test_cambiar_estado_valido(self):
        """Prueba cambiar a un estado válido."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        # Act
        resultado = tarea.cambiar_estado(EstadoTarea.EN_PROGRESO)
        
        # Assert
        assert resultado is True
        assert tarea.estado == EstadoTarea.EN_PROGRESO
    
    def test_cambiar_estado_invalido(self):
        """Prueba que falle con estado inválido."""
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        with pytest.raises(ValueError, match="El estado debe ser una instancia de EstadoTarea"):
            tarea.cambiar_estado("estado_invalido")
    
    def test_reasignar_usuario_nuevo(self, capsys):
        """Prueba reasignar a un nuevo usuario."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura, "usuario-original")
        nuevo_usuario = "usuario-nuevo"
        
        # Act
        resultado = tarea.reasignar(nuevo_usuario)
        captured = capsys.readouterr()
        
        # Assert
        assert resultado is True
        assert tarea.usuario_id == nuevo_usuario
        assert "reasignada de usuario-original a usuario-nuevo" in captured.out
    
    def test_reasignar_asignar_primera_vez(self, capsys):
        """Prueba asignar usuario por primera vez."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)  # Sin usuario
        usuario = "usuario-nuevo"
        
        # Act
        resultado = tarea.reasignar(usuario)
        captured = capsys.readouterr()
        
        # Assert
        assert resultado is True
        assert tarea.usuario_id == usuario
        assert "asignada a usuario-nuevo" in captured.out
    
    def test_reasignar_desasignar_usuario(self, capsys):
        """Prueba desasignar usuario."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura, "usuario-original")
        
        # Act
        resultado = tarea.reasignar(None)
        captured = capsys.readouterr()
        
        # Assert
        assert resultado is True
        assert tarea.usuario_id is None
        assert "desasignada de usuario-original" in captured.out
    
    def test_calcular_dias_restantes(self):
        """Prueba el cálculo de días restantes."""
        # Arrange
        dias_esperados = 5
        fecha_limite = datetime.now() + timedelta(days=dias_esperados)
        tarea = Tarea(self.titulo, self.descripcion, fecha_limite)
        
        # Act
        dias_restantes = tarea.calcular_dias_restantes()
        
        # Assert
        # Puede variar por diferencias de tiempo en la ejecución
        assert abs(dias_restantes - dias_esperados) <= 1
    
    def test_calcular_dias_restantes_vencida(self):
        """Prueba días restantes para tarea vencida."""
        # Arrange - usamos fecha pasada para el test
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        # Modificamos manualmente para el test
        tarea.fecha_limite = datetime.now() - timedelta(days=2)
        
        # Act
        dias_restantes = tarea.calcular_dias_restantes()
        
        # Assert
        assert dias_restantes < 0  # Número negativo para tareas vencidas
    
    def test_esta_vencida_false(self):
        """Prueba que tarea no esté vencida."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        # Act & Assert
        assert tarea.esta_vencida() is False
    
    def test_esta_vencida_true(self):
        """Prueba que tarea esté vencida."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        tarea.fecha_limite = datetime.now() - timedelta(days=1)  # Modificar para test
        
        # Act & Assert
        assert tarea.esta_vencida() is True
    
    def test_obtener_duracion_estimada(self):
        """Prueba obtener duración estimada."""
        # Arrange
        dias_duracion = 10
        fecha_limite = datetime.now() + timedelta(days=dias_duracion)
        tarea = Tarea(self.titulo, self.descripcion, fecha_limite)
        
        # Act
        duracion = tarea.obtener_duracion_estimada()
        
        # Assert
        # Puede variar ligeramente por diferencias de tiempo
        assert abs(duracion - dias_duracion) <= 1
    
    def test_obtener_resumen_con_usuario(self):
        """Prueba obtener resumen con usuario asignado."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura, self.usuario_id)
        
        # Act
        resumen = tarea.obtener_resumen()
        
        # Assert - verifica uso de métodos de cadenas
        assert "📋 Tarea De Prueba" in resumen
        assert "Estado: Pendiente" in resumen
        assert "Días restantes:" in resumen
        assert f"Asignado a: {self.usuario_id}" in resumen
    
    def test_obtener_resumen_sin_usuario(self):
        """Prueba obtener resumen sin usuario asignado."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        # Act
        resumen = tarea.obtener_resumen()
        
        # Assert
        assert "📋 Tarea De Prueba" in resumen
        assert "Estado: Pendiente" in resumen
        assert "Días restantes:" in resumen
        assert "Asignado a:" not in resumen
    
    def test_to_dict(self):
        """Prueba la conversión a diccionario."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura, self.usuario_id)
        
        # Act
        data = tarea.to_dict()
        
        # Assert
        assert data['titulo'] == "Tarea De Prueba"
        assert data['descripcion'] == "descripción detallada de la tarea"
        assert data['id'] == tarea.id
        assert data['estado'] == 'pendiente'
        assert data['usuario_id'] == self.usuario_id
        assert 'fecha_creacion' in data
        assert 'fecha_limite' in data
    
    def test_from_dict(self):
        """Prueba la creación desde diccionario."""
        # Arrange
        fecha_creacion = datetime.now()
        data = {
            'id': 'test-id-123',
            'titulo': 'Tarea Test',
            'descripcion': 'Descripción test',
            'fecha_creacion': fecha_creacion.isoformat(),
            'fecha_limite': self.fecha_futura.isoformat(),
            'estado': 'en_progreso',
            'usuario_id': 'usuario-test'
        }
        
        # Act
        tarea = Tarea.from_dict(data)
        
        # Assert
        assert tarea.id == 'test-id-123'
        assert tarea.titulo == 'Tarea Test'
        assert tarea.descripcion == 'Descripción test'
        assert tarea.fecha_creacion == fecha_creacion
        assert tarea.fecha_limite == self.fecha_futura
        assert tarea.estado == EstadoTarea.EN_PROGRESO
        assert tarea.usuario_id == 'usuario-test'
    
    def test_str_representation(self):
        """Prueba la representación en cadena."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        # Act
        str_repr = str(tarea)
        
        # Assert
        assert "Tarea De Prueba" in str_repr
        assert "pendiente" in str_repr
        assert "días" in str_repr
    
    def test_repr_representation(self):
        """Prueba la representación técnica."""
        # Arrange
        tarea = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        
        # Act
        repr_str = repr(tarea)
        
        # Assert
        assert "Tarea(id=" in repr_str
        assert "titulo='Tarea De Prueba'" in repr_str
        assert "estado='pendiente'" in repr_str
    
    def test_equality(self):
        """Prueba la comparación de tareas."""
        # Arrange
        tarea1 = Tarea(self.titulo, self.descripcion, self.fecha_futura)
        tarea2 = Tarea("Otra tarea", "Otra descripción", self.fecha_futura)
        
        # Crear tarea con el mismo ID
        tarea3 = Tarea("Diferente título", "Diferente descripción", self.fecha_futura)
        tarea3.id = tarea1.id
        
        # Act & Assert
        assert tarea1 == tarea3  # Mismo ID
        assert tarea1 != tarea2  # Diferente ID
        assert tarea1 != "not a task"  # Tipo diferente
    
    def test_estados_tarea_enum(self):
        """Prueba los valores del enum EstadoTarea."""
        # Assert
        assert EstadoTarea.PENDIENTE.value == "pendiente"
        assert EstadoTarea.EN_PROGRESO.value == "en_progreso"
        assert EstadoTarea.COMPLETADA.value == "completada"
    
    def test_formateo_cadenas_titulo_especial(self):
        """Prueba formateo especial de títulos con métodos de cadenas."""
        # Arrange
        titulos_prueba = [
            ("  proyecto web  ", "Proyecto Web"),
            ("desarrollo API", "Desarrollo Api"),
            ("TAREA URGENTE", "Tarea Urgente"),
            ("tarea-con-guiones", "Tarea-Con-Guiones")
        ]
        
        # Act & Assert
        for titulo_original, titulo_esperado in titulos_prueba:
            tarea = Tarea(titulo_original, "descripción", self.fecha_futura)
            assert tarea.titulo == titulo_esperado

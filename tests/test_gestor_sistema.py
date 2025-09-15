"""
Tests para el gestor principal del sistema de tareas.

Prueba todas las funcionalidades integradas del sistema.
"""

import unittest
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.usuario import Usuario
from models.tarea import Tarea, EstadoTarea
from services.gestor_sistema import GestorSistema


class TestGestorSistema(unittest.TestCase):
    """Tests para la clase GestorSistema."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear directorio temporal para tests
        self.temp_dir = tempfile.mkdtemp()
        self.gestor = GestorSistema(directorio_datos=self.temp_dir)
        
        # Silenciar prints del sistema para tests más limpios
        self.original_print = print
    
    def tearDown(self):
        """Limpieza después de cada test."""
        # Limpiar directorio temporal
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_inicializacion_sistema(self):
        """Test de inicialización del sistema."""
        self.assertIsInstance(self.gestor.usuarios, list)
        self.assertIsInstance(self.gestor.tareas, list)
        self.assertEqual(len(self.gestor.usuarios), 0)
        self.assertEqual(len(self.gestor.tareas), 0)
        self.assertIsNotNone(self.gestor.persistencia)
        self.assertIsNotNone(self.gestor.generador_reportes)
    
    # ===============================
    # TESTS DE GESTIÓN DE USUARIOS
    # ===============================
    
    def test_crear_usuario_exitoso(self):
        """Test de creación exitosa de usuario."""
        usuario = self.gestor.crear_usuario("Ana García", "ana@empresa.com")
        
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Ana García")
        self.assertEqual(usuario.email, "ana@empresa.com")
        self.assertEqual(len(self.gestor.usuarios), 1)
        self.assertIn(usuario, self.gestor.usuarios)
    
    def test_crear_usuario_email_invalido(self):
        """Test de creación de usuario con email inválido."""
        usuario = self.gestor.crear_usuario("Juan Pérez", "email-invalido")
        self.assertIsNone(usuario)
        self.assertEqual(len(self.gestor.usuarios), 0)
    
    def test_crear_usuario_nombre_vacio(self):
        """Test de creación de usuario con nombre vacío."""
        usuario = self.gestor.crear_usuario("", "test@empresa.com")
        self.assertIsNone(usuario)
        self.assertEqual(len(self.gestor.usuarios), 0)
        
        usuario = self.gestor.crear_usuario("   ", "test@empresa.com")
        self.assertIsNone(usuario)
        self.assertEqual(len(self.gestor.usuarios), 0)
    
    def test_crear_usuario_email_duplicado(self):
        """Test de creación de usuario con email duplicado."""
        self.gestor.crear_usuario("Usuario 1", "test@empresa.com")
        usuario2 = self.gestor.crear_usuario("Usuario 2", "test@empresa.com")
        
        self.assertIsNone(usuario2)
        self.assertEqual(len(self.gestor.usuarios), 1)
    
    def test_obtener_usuario_por_email(self):
        """Test de búsqueda de usuario por email."""
        usuario_creado = self.gestor.crear_usuario("Ana García", "ana@empresa.com")
        
        usuario_encontrado = self.gestor.obtener_usuario_por_email("ana@empresa.com")
        self.assertEqual(usuario_encontrado, usuario_creado)
        
        # Test con email en mayúsculas (debe ser case-insensitive)
        usuario_encontrado2 = self.gestor.obtener_usuario_por_email("ANA@EMPRESA.COM")
        self.assertEqual(usuario_encontrado2, usuario_creado)
        
        # Test con email inexistente
        usuario_no_existe = self.gestor.obtener_usuario_por_email("noexiste@empresa.com")
        self.assertIsNone(usuario_no_existe)
    
    def test_obtener_usuario_por_id(self):
        """Test de búsqueda de usuario por ID."""
        usuario_creado = self.gestor.crear_usuario("Carlos López", "carlos@empresa.com")
        
        usuario_encontrado = self.gestor.obtener_usuario_por_id(usuario_creado.id)
        self.assertEqual(usuario_encontrado, usuario_creado)
        
        # Test con ID inexistente
        usuario_no_existe = self.gestor.obtener_usuario_por_id("id_inexistente")
        self.assertIsNone(usuario_no_existe)
    
    def test_eliminar_usuario_exitoso(self):
        """Test de eliminación exitosa de usuario."""
        usuario = self.gestor.crear_usuario("Usuario Test", "test@empresa.com")
        usuario_id = usuario.id
        
        resultado = self.gestor.eliminar_usuario(usuario_id)
        
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.usuarios), 0)
        self.assertIsNone(self.gestor.obtener_usuario_por_id(usuario_id))
    
    def test_eliminar_usuario_inexistente(self):
        """Test de eliminación de usuario inexistente."""
        resultado = self.gestor.eliminar_usuario("id_inexistente")
        self.assertFalse(resultado)
    
    def test_eliminar_usuario_con_tareas_asignadas(self):
        """Test de eliminación de usuario que tiene tareas asignadas."""
        usuario = self.gestor.crear_usuario("Usuario Con Tareas", "usuario@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        
        # Crear tarea asignada al usuario
        self.gestor.crear_tarea(
            "Tarea de prueba",
            "Descripción",
            fecha_futura,
            usuario.email
        )
        
        resultado = self.gestor.eliminar_usuario(usuario.id)
        
        self.assertFalse(resultado)
        self.assertEqual(len(self.gestor.usuarios), 1)  # Usuario no eliminado
    
    # ===============================
    # TESTS DE GESTIÓN DE TAREAS
    # ===============================
    
    def test_crear_tarea_exitosa(self):
        """Test de creación exitosa de tarea."""
        fecha_futura = datetime.now() + timedelta(days=7)
        
        tarea = self.gestor.crear_tarea(
            "Tarea de prueba",
            "Descripción detallada",
            fecha_futura
        )
        
        self.assertIsNotNone(tarea)
        self.assertEqual(tarea.titulo, "Tarea De Prueba")
        self.assertEqual(tarea.descripcion, "Descripción detallada")
        self.assertEqual(len(self.gestor.tareas), 1)
        self.assertIn(tarea, self.gestor.tareas)
    
    def test_crear_tarea_con_usuario_asignado(self):
        """Test de creación de tarea con usuario asignado."""
        usuario = self.gestor.crear_usuario("Ana García", "ana@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        
        tarea = self.gestor.crear_tarea(
            "Tarea asignada",
            "Descripción",
            fecha_futura,
            usuario_email="ana@empresa.com"
        )
        
        self.assertIsNotNone(tarea)
        self.assertEqual(tarea.usuario_id, usuario.id)
        self.assertIn(tarea.id, usuario.tareas_asignadas)

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
    
    def test_obtener_usuario_por_email(self):
        """Test de búsqueda de usuario por email."""
        usuario_creado = self.gestor.crear_usuario("Ana García", "ana@empresa.com")
        
        usuario_encontrado = self.gestor.obtener_usuario_por_email("ana@empresa.com")
        self.assertEqual(usuario_encontrado, usuario_creado)
        
        # Test con email inexistente
        usuario_no_existe = self.gestor.obtener_usuario_por_email("noexiste@empresa.com")
        self.assertIsNone(usuario_no_existe)
    
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
        self.assertEqual(len(self.gestor.tareas), 1)
    
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
    
    def test_buscar_tareas_por_titulo(self):
        """Test de búsqueda de tareas por título."""
        fecha_futura = datetime.now() + timedelta(days=7)
        
        self.gestor.crear_tarea("Revisar código Python", "Descripción 1", fecha_futura)
        self.gestor.crear_tarea("Escribir documentación", "Descripción 2", fecha_futura)
        self.gestor.crear_tarea("Código JavaScript", "Descripción 3", fecha_futura)
        
        resultados = self.gestor.buscar_tareas("código")
        
        self.assertEqual(len(resultados), 2)
        titulos = [t.titulo for t in resultados]
        self.assertIn("Revisar Código Python", titulos)
        self.assertIn("Código Javascript", titulos)
    
    def test_cambiar_estado_tarea(self):
        """Test de cambio de estado de tarea."""
        fecha_futura = datetime.now() + timedelta(days=7)
        tarea = self.gestor.crear_tarea("Tarea", "Descripción", fecha_futura)
        
        resultado = self.gestor.cambiar_estado_tarea(tarea.id, "en_progreso")
        
        self.assertTrue(resultado)
        self.assertEqual(tarea.estado, EstadoTarea.EN_PROGRESO)
    
    def test_asignar_tarea(self):
        """Test de asignación de tarea."""
        usuario = self.gestor.crear_usuario("Carlos López", "carlos@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        tarea = self.gestor.crear_tarea("Tarea", "Descripción", fecha_futura)
        
        resultado = self.gestor.asignar_tarea(tarea.id, "carlos@empresa.com")
        
        self.assertTrue(resultado)
        self.assertEqual(tarea.usuario_id, usuario.id)
        self.assertIn(tarea.id, usuario.tareas_asignadas)
    
    def test_guardar_datos_sistema(self):
        """Test de guardado de datos del sistema."""
        # Crear datos de prueba
        self.gestor.crear_usuario("Usuario Test", "test@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        self.gestor.crear_tarea("Tarea Test", "Descripción", fecha_futura)
        
        resultado = self.gestor.guardar_datos_sistema("json")
        self.assertTrue(resultado)
        
        # Verificar que se crearon los archivos
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "json", "usuarios.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "json", "tareas.json")))
    
    def test_generar_reporte_usuarios(self):
        """Test de generación de reporte de usuarios."""
        self.gestor.crear_usuario("Ana García", "ana@empresa.com")
        
        reporte = self.gestor.generar_reporte_usuarios()
        
        self.assertIsInstance(reporte, str)
        self.assertIn("REPORTE DE USUARIOS", reporte)
        self.assertIn("Ana García", reporte)
    
    def test_generar_dashboard_ejecutivo(self):
        """Test de generación de dashboard ejecutivo."""
        # Crear datos de prueba
        usuario = self.gestor.crear_usuario("Usuario", "usuario@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        self.gestor.crear_tarea("Tarea", "Descripción", fecha_futura, usuario.email)
        
        dashboard = self.gestor.generar_dashboard_ejecutivo()
        
        self.assertIsInstance(dashboard, str)
        self.assertIn("DASHBOARD EJECUTIVO", dashboard)
        self.assertIn("MÉTRICAS CLAVE", dashboard)
    
    def test_obtener_estadisticas_sistema(self):
        """Test de obtención de estadísticas del sistema."""
        # Crear datos de prueba
        usuario = self.gestor.crear_usuario("Usuario", "usuario@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        
        tarea1 = self.gestor.crear_tarea("Tarea 1", "Descripción", fecha_futura, usuario.email)
        tarea2 = self.gestor.crear_tarea("Tarea 2", "Descripción", fecha_futura, usuario.email)
        self.gestor.cambiar_estado_tarea(tarea1.id, "en_progreso")
        self.gestor.cambiar_estado_tarea(tarea2.id, "completada")
        
        stats = self.gestor.obtener_estadisticas_sistema()
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_usuarios'], 1)
        self.assertEqual(stats['total_tareas'], 2)
        self.assertEqual(stats['tareas_en_progreso'], 1)
        self.assertEqual(stats['tareas_completadas'], 1)
        self.assertIn('fecha_consulta', stats)
    
    def test_str_representation(self):
        """Test de la representación en string del sistema."""
        # Crear algunos datos
        usuario = self.gestor.crear_usuario("Usuario", "usuario@empresa.com")
        fecha_futura = datetime.now() + timedelta(days=7)
        tarea = self.gestor.crear_tarea("Tarea", "Descripción", fecha_futura, usuario.email)
        self.gestor.cambiar_estado_tarea(tarea.id, "completada")
        
        str_repr = str(self.gestor)
        
        self.assertIn("Sistema de Gestión de Tareas", str_repr)
        self.assertIn("Usuarios: 1", str_repr)
        self.assertIn("Tareas: 1", str_repr)
        self.assertIn("Completadas: 1", str_repr)


if __name__ == '__main__':
    # Configurar unittest para mostrar más detalles en fallos
    unittest.main(verbosity=2)

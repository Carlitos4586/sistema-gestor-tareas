"""
Tests para el módulo de reportes.

Prueba la generación de reportes tabulados y estadísticas del sistema.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.usuario import Usuario
from models.tarea import Tarea, EstadoTarea
from services.reportes import GeneradorReportes


class TestGeneradorReportes(unittest.TestCase):
    """Tests para la clase GeneradorReportes."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.generador = GeneradorReportes()
        
        # Crear usuarios de prueba
        self.usuario1 = Usuario(
            nombre="Ana García",
            email="ana@empresa.com"
        )
        self.usuario1.id = "user001"  # Asignar ID después de la creación
        
        self.usuario2 = Usuario(
            nombre="Carlos López",
            email="carlos@empresa.com"
        )
        self.usuario2.id = "user002"  # Asignar ID después de la creación
        self.usuarios = [self.usuario1, self.usuario2]
        
        # Crear tareas de prueba
        fecha_futura = datetime.now() + timedelta(days=7)
        fecha_pasada = datetime.now() + timedelta(days=1)  # Cambiar a futura para evitar validación
        
        self.tarea1 = Tarea(
            titulo="Revisar código",
            descripcion="Revisar pull request #123",
            fecha_limite=fecha_futura,
            usuario_id="user001"
        )
        self.tarea1.id = "task001"  # Asignar ID después de la creación
        
        self.tarea2 = Tarea(
            titulo="Escribir documentación",
            descripcion="Documentar API REST",
            fecha_limite=fecha_pasada,
            usuario_id="user002"
        )
        self.tarea2.id = "task002"  # Asignar ID después de la creación
        self.tarea2.estado = EstadoTarea.COMPLETADA
        
        self.tarea3 = Tarea(
            titulo="Testing unitario",
            descripcion="Crear tests para módulo X",
            fecha_limite=fecha_futura,
            usuario_id="user001"
        )
        self.tarea3.id = "task003"  # Asignar ID después de la creación
        self.tarea3.estado = EstadoTarea.EN_PROGRESO
        
        self.tareas = [self.tarea1, self.tarea2, self.tarea3]
        
        # Actualizar listas de tareas asignadas
        self.usuario1.tareas_asignadas = ["task001", "task003"]
        self.usuario2.tareas_asignadas = ["task002"]
    
    def test_inicializacion_generador(self):
        """Test de inicialización del generador de reportes."""
        self.assertEqual(self.generador.formato_tabla_predeterminado, "grid")
        self.assertIsInstance(self.generador.formatos_disponibles, list)
        self.assertIn("grid", self.generador.formatos_disponibles)
        self.assertIn("simple", self.generador.formatos_disponibles)
    
    def test_reporte_usuarios_vacio(self):
        """Test de reporte de usuarios cuando no hay usuarios."""
        reporte = self.generador.generar_reporte_usuarios([], [])
        self.assertIn("No hay usuarios registrados", reporte)
    
    def test_reporte_usuarios_con_datos(self):
        """Test de reporte de usuarios con datos completos."""
        reporte = self.generador.generar_reporte_usuarios(self.usuarios, self.tareas)
        
        # Verificar elementos del reporte
        self.assertIn("REPORTE DE USUARIOS", reporte)
        self.assertIn("Ana García", reporte)
        self.assertIn("Carlos López", reporte)
        self.assertIn("ana@empresa.com", reporte)
        self.assertIn("carlos@empresa.com", reporte)
        self.assertIn("RESUMEN ESTADÍSTICO", reporte)
        self.assertIn("Total de usuarios: 2", reporte)
    
    def test_reporte_tareas_vacio(self):
        """Test de reporte de tareas cuando no hay tareas."""
        reporte = self.generador.generar_reporte_tareas([], self.usuarios)
        self.assertIn("No hay tareas", reporte)
    
    def test_reporte_tareas_con_datos(self):
        """Test de reporte de tareas con datos completos."""
        reporte = self.generador.generar_reporte_tareas(self.tareas, self.usuarios)
        
        # Verificar elementos del reporte (ajustar a formato real)
        self.assertIn("REPORTE DE TAREAS", reporte)
        self.assertIn("Revisar Código", reporte)
        self.assertIn("Escribir Documentación", reporte)
        self.assertIn("Testing Unitario", reporte)
        self.assertIn("ESTADÍSTICAS", reporte)
        self.assertIn("Total de tareas: 3", reporte)
    
    def test_reporte_tareas_filtrado_por_estado(self):
        """Test de reporte de tareas filtrado por estado."""
        reporte = self.generador.generar_reporte_tareas(
            self.tareas, self.usuarios, filtrar_estado="completada"
        )
        
        self.assertIn("COMPLETADA", reporte)
        self.assertIn("Escribir Documentación", reporte)
        self.assertNotIn("Revisar Código", reporte)
        self.assertIn("Total de tareas: 1", reporte)
    
    def test_dashboard_ejecutivo_sin_datos(self):
        """Test del dashboard cuando no hay datos."""
        dashboard = self.generador.generar_dashboard_ejecutivo([], [])
        self.assertIn("No hay datos suficientes", dashboard)
    
    def test_dashboard_ejecutivo_completo(self):
        """Test del dashboard ejecutivo completo."""
        dashboard = self.generador.generar_dashboard_ejecutivo(self.usuarios, self.tareas)
        
        # Verificar secciones principales
        self.assertIn("DASHBOARD EJECUTIVO", dashboard)
        self.assertIn("MÉTRICAS CLAVE", dashboard)
        self.assertIn("DISTRIBUCIÓN DE TAREAS POR ESTADO", dashboard)
        self.assertIn("TOP 5 USUARIOS MÁS ACTIVOS", dashboard)
        self.assertIn("TAREAS CRÍTICAS", dashboard)
        
        # Verificar métricas (ajustar al formato real)
        self.assertIn("Total Usuarios:   2", dashboard)
        self.assertIn("Total Tareas:   3", dashboard)
    
    def test_reporte_calendario(self):
        """Test de reporte de calendario."""
        año = datetime.now().year
        mes = datetime.now().month
        
        reporte = self.generador.generar_reporte_calendario(self.tareas, año, mes)
        
        self.assertIn("CALENDARIO DE TAREAS", reporte)
        self.assertIn(str(año), reporte)
        self.assertIn("DETALLE DE TAREAS DEL MES", reporte)
        self.assertIn("RESUMEN", reporte)
    
    def test_reporte_productividad_sin_datos(self):
        """Test de reporte de productividad sin datos en el período."""
        # Crear tareas muy antiguas (ajustar para evitar validación)
        fecha_antigua = datetime.now() - timedelta(days=100)
        tarea_antigua = Tarea(
            titulo="Tarea antigua",
            descripcion="Una tarea muy antigua",
            fecha_limite=datetime.now() + timedelta(days=1)  # Fecha futura para validación
        )
        tarea_antigua.id = "old001"  # Asignar ID después de la creación
        tarea_antigua.fecha_creacion = fecha_antigua
        
        reporte = self.generador.generar_reporte_productividad(
            self.usuarios, [tarea_antigua], periodo_dias=30
        )
        
        self.assertIn("No hay datos de productividad", reporte)
    
    def test_reporte_productividad_con_datos(self):
        """Test de reporte de productividad con datos del período."""
        # Ajustar fechas de creación a período reciente
        for tarea in self.tareas:
            tarea.fecha_creacion = datetime.now() - timedelta(days=10)
        
        reporte = self.generador.generar_reporte_productividad(
            self.usuarios, self.tareas, periodo_dias=30
        )
        
        self.assertIn("REPORTE DE PRODUCTIVIDAD", reporte)
        self.assertIn("MÉTRICAS GENERALES", reporte)
        self.assertIn("PRODUCTIVIDAD POR USUARIO", reporte)
        self.assertIn("TENDENCIAS SEMANALES", reporte)
        self.assertIn("RECOMENDACIONES", reporte)
    
    def test_formatos_tabla_diferentes(self):
        """Test de generación de reportes con diferentes formatos de tabla."""
        formatos = ["simple", "github", "fancy_grid"]
        
        for formato in formatos:
            reporte = self.generador.generar_reporte_usuarios(
                self.usuarios, self.tareas, formato_tabla=formato
            )
            self.assertIn("Ana García", reporte)
            self.assertIsInstance(reporte, str)
            self.assertTrue(len(reporte) > 0)
    
    def test_exportar_csv_sin_datos(self):
        """Test de exportación CSV sin datos."""
        resultado = self.generador.exportar_reporte_csv([], "test_vacio")
        self.assertIn("No hay datos para exportar", resultado)
    
    @patch('os.makedirs')
    @patch('builtins.open')
    def test_exportar_csv_con_datos(self, mock_open, mock_makedirs):
        """Test de exportación CSV con datos."""
        datos = [
            {'nombre': 'Ana', 'email': 'ana@test.com', 'tareas': 2},
            {'nombre': 'Carlos', 'email': 'carlos@test.com', 'tareas': 1}
        ]
        
        # Configurar mocks
        mock_open.return_value.__enter__.return_value.write = lambda x: None
        
        resultado = self.generador.exportar_reporte_csv(datos, "test_usuarios")
        
        # Verificar que se llamaron las funciones correctas
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
        self.assertIn("exportado exitosamente", resultado)
    
    def test_manejo_errores_datos_invalidos(self):
        """Test del manejo de errores con datos inválidos."""
        # Test con lista de usuarios None
        reporte = self.generador.generar_reporte_usuarios(None, self.tareas)
        self.assertIn("No hay usuarios", reporte)
        
        # Test con lista de tareas None
        reporte = self.generador.generar_reporte_tareas(None, self.usuarios)
        self.assertIn("No hay tareas", reporte)
    
    def test_truncado_campos_largos(self):
        """Test del truncado de campos largos en reportes."""
        # Crear tarea con título muy largo
        tarea_larga = Tarea(
            titulo="Este es un título extremadamente largo que debería ser truncado en el reporte para mantener el formato",
            descripcion="Descripción también muy larga" * 10,
            fecha_limite=datetime.now() + timedelta(days=7),
            usuario_id="user001"
        )
        tarea_larga.id = "long001"  # Asignar ID después de la creación
        
        reporte = self.generador.generar_reporte_tareas(
            [tarea_larga], self.usuarios
        )
        
        # Verificar que el título fue truncado (debería contener "...")
        self.assertIn("...", reporte)
        self.assertIn("Título Extremadamen", reporte)  # Parte del título que aparece
    
    def test_estadisticas_calculo_correcto(self):
        """Test del cálculo correcto de estadísticas en reportes."""
        dashboard = self.generador.generar_dashboard_ejecutivo(self.usuarios, self.tareas)
        
        # Verificar cálculos:
        # - 3 tareas total
        # - 1 pendiente, 1 en progreso, 1 completada
        # - Porcentaje completadas = 33.3%
        self.assertIn("Total Tareas:   3", dashboard)
        self.assertIn("33.3%", dashboard)  # Porcentage de completadas


if __name__ == '__main__':
    unittest.main()

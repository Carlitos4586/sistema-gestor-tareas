"""
Pruebas unitarias para el módulo de generadores.

Este módulo contiene todas las pruebas para verificar el correcto
funcionamiento de los generadores e iteradores personalizados.
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.usuario import Usuario
from models.tarea import Tarea, EstadoTarea
from utils.generadores import (
    IteradorTareas, generador_tareas_por_estado, generador_tareas_por_usuario,
    generador_tareas_vencidas, generador_tareas_proximas_vencer,
    generador_estadisticas_por_lote, generador_usuarios_con_tareas,
    generador_fechas_limite_calendario, filtro_compuesto,
    crear_filtro_fecha_rango, crear_filtro_titulo_contiene, GeneradorInfinito
)


class TestIteradorTareas:
    """Pruebas para la clase IteradorTareas."""
    
    def setup_method(self):
        """Configuración para cada prueba."""
        self.usuario = Usuario("Test User", "test@email.com")
        fecha_base = datetime.now() + timedelta(days=7)
        
        self.tareas = [
            Tarea("Tarea 1", "Descripción 1", fecha_base, self.usuario.id),
            Tarea("Tarea 2", "Descripción 2", fecha_base + timedelta(days=1), self.usuario.id),
            Tarea("Tarea 3", "Descripción 3", fecha_base + timedelta(days=2), None),
        ]
        
        # Cambiar estado de una tarea
        self.tareas[1].cambiar_estado(EstadoTarea.EN_PROGRESO)
    
    def test_iterador_sin_filtro(self):
        """Prueba iterador sin filtro."""
        iterador = IteradorTareas(self.tareas)
        tareas_iteradas = list(iterador)
        
        assert len(tareas_iteradas) == 3
        assert all(isinstance(tarea, Tarea) for tarea in tareas_iteradas)
    
    def test_iterador_con_filtro(self):
        """Prueba iterador con filtro."""
        filtro = lambda t: t.estado == EstadoTarea.PENDIENTE
        iterador = IteradorTareas(self.tareas, filtro)
        tareas_filtradas = list(iterador)
        
        assert len(tareas_filtradas) == 2
        assert all(t.estado == EstadoTarea.PENDIENTE for t in tareas_filtradas)
    
    def test_iterador_protocolo(self):
        """Prueba que el iterador implementa correctamente el protocolo."""
        iterador = IteradorTareas(self.tareas)
        
        # Verificar __iter__
        assert iter(iterador) is iterador
        
        # Verificar __next__
        primera_tarea = next(iterador)
        assert isinstance(primera_tarea, Tarea)


class TestGeneradores:
    """Pruebas para los generadores."""
    
    def setup_method(self):
        """Configuración para cada prueba."""
        self.usuario1 = Usuario("Usuario 1", "user1@email.com")
        self.usuario2 = Usuario("Usuario 2", "user2@email.com")
        
        fecha_base = datetime.now()
        
        # Crear tareas con diferentes estados y fechas
        self.tareas = [
            Tarea("Tarea Pendiente", "Desc 1", fecha_base + timedelta(days=1), self.usuario1.id),
            Tarea("Tarea En Progreso", "Desc 2", fecha_base + timedelta(days=5), self.usuario1.id),
            Tarea("Tarea Completada", "Desc 3", fecha_base + timedelta(days=10), self.usuario2.id),
            Tarea("Tarea Próxima", "Desc 5", fecha_base + timedelta(days=2), None),
        ]
        
        # Crear tarea vencida modificando la fecha después de la creación
        tarea_vencida = Tarea("Tarea Vencida", "Desc 4", fecha_base + timedelta(days=1), self.usuario2.id)
        tarea_vencida.fecha_limite = fecha_base - timedelta(days=2)  # Modificar para simular vencimiento
        self.tareas.append(tarea_vencida)
        
        # Configurar estados
        self.tareas[1].cambiar_estado(EstadoTarea.EN_PROGRESO)
        self.tareas[2].cambiar_estado(EstadoTarea.COMPLETADA)
    
    def test_generador_tareas_por_estado(self):
        """Prueba generador por estado."""
        # Probar tareas pendientes (2 pendientes + 1 vencida pero aún pendiente)
        pendientes = list(generador_tareas_por_estado(self.tareas, "pendiente"))
        assert len(pendientes) == 3
        
        # Probar tareas en progreso
        en_progreso = list(generador_tareas_por_estado(self.tareas, "en_progreso"))
        assert len(en_progreso) == 1
        assert en_progreso[0].titulo == "Tarea En Progreso"
    
    def test_generador_tareas_por_usuario(self):
        """Prueba generador por usuario."""
        tareas_usuario1 = list(generador_tareas_por_usuario(self.tareas, self.usuario1.id))
        assert len(tareas_usuario1) == 2
        
        tareas_usuario2 = list(generador_tareas_por_usuario(self.tareas, self.usuario2.id))
        assert len(tareas_usuario2) == 2
        
        tareas_sin_usuario = list(generador_tareas_por_usuario(self.tareas, "inexistente"))
        assert len(tareas_sin_usuario) == 0
    
    def test_generador_tareas_vencidas(self):
        """Prueba generador de tareas vencidas."""
        vencidas = list(generador_tareas_vencidas(self.tareas))
        assert len(vencidas) == 1
        assert vencidas[0].titulo == "Tarea Vencida"
    
    def test_generador_tareas_proximas_vencer(self):
        """Prueba generador de tareas próximas a vencer."""
        proximas = list(generador_tareas_proximas_vencer(self.tareas, dias=3))
        
        # Debe incluir tareas con 1 y 2 días restantes
        assert len(proximas) >= 1  # Al menos la tarea próxima
        
        # Verificar que están dentro del rango
        for tarea in proximas:
            dias_restantes = tarea.calcular_dias_restantes()
            assert 0 <= dias_restantes <= 3
    
    def test_generador_estadisticas_por_lote(self):
        """Prueba generador de estadísticas por lotes."""
        estadisticas = list(generador_estadisticas_por_lote(self.tareas, tamaño_lote=2))
        
        # Debe haber 3 lotes (2, 2, 1 tareas) - ahora tenemos 5 tareas
        assert len(estadisticas) == 3
        
        # Verificar primer lote
        primer_lote = estadisticas[0]
        assert primer_lote['lote_numero'] == 1
        assert primer_lote['total_tareas'] == 2
        assert primer_lote['rango_indices'] == (0, 1)
        
        # Verificar que todas las estadísticas tienen los campos necesarios
        for lote in estadisticas:
            assert 'pendientes' in lote
            assert 'en_progreso' in lote
            assert 'completadas' in lote
            assert 'porcentaje_completadas' in lote
    
    def test_generador_usuarios_con_tareas(self):
        """Prueba generador de usuarios con sus tareas."""
        usuarios = [self.usuario1, self.usuario2]
        usuarios_con_tareas = list(generador_usuarios_con_tareas(usuarios, self.tareas))
        
        assert len(usuarios_con_tareas) == 2
        
        # Verificar estructura de datos
        for usuario_data in usuarios_con_tareas:
            assert 'usuario' in usuario_data
            assert 'tareas' in usuario_data
            assert 'total_tareas' in usuario_data
            assert 'tareas_pendientes' in usuario_data
            assert 'tareas_en_progreso' in usuario_data
            assert 'tareas_completadas' in usuario_data
        
        # Verificar conteos para usuario1
        usuario1_data = usuarios_con_tareas[0]
        if usuario1_data['usuario'].id == self.usuario1.id:
            assert usuario1_data['total_tareas'] == 2


class TestFiltros:
    """Pruebas para las funciones de filtro."""
    
    def setup_method(self):
        """Configuración para cada prueba."""
        fecha_base = datetime.now()
        
        # Crear tareas válidas
        self.tareas = [
            Tarea("API Development", "Desarrollar API REST", fecha_base + timedelta(days=5)),
            Tarea("Database Setup", "Configurar base de datos", fecha_base + timedelta(days=15)),
        ]
        
        # Crear tarea con fecha pasada modificando después
        tarea_pasada = Tarea("Frontend Work", "Crear interfaz de usuario", fecha_base + timedelta(days=1))
        tarea_pasada.fecha_limite = fecha_base - timedelta(days=2)  # Simular fecha pasada
        self.tareas.append(tarea_pasada)
    
    def test_crear_filtro_fecha_rango(self):
        """Prueba creación de filtros por rango de fechas."""
        inicio = datetime.now() + timedelta(days=1)
        fin = datetime.now() + timedelta(days=10)
        
        filtro = crear_filtro_fecha_rango(inicio, fin)
        
        # Aplicar filtro
        tareas_filtradas = [t for t in self.tareas if filtro(t)]
        
        # Solo la primera tarea debe pasar el filtro
        assert len(tareas_filtradas) == 1
        assert tareas_filtradas[0].titulo == "Api Development"
    
    def test_crear_filtro_titulo_contiene(self):
        """Prueba creación de filtros por título."""
        filtro_api = crear_filtro_titulo_contiene("API")
        filtro_setup = crear_filtro_titulo_contiene("setup")
        
        tareas_api = [t for t in self.tareas if filtro_api(t)]
        tareas_setup = [t for t in self.tareas if filtro_setup(t)]
        
        assert len(tareas_api) == 1
        assert tareas_api[0].titulo == "Api Development"
        
        assert len(tareas_setup) == 1
        assert tareas_setup[0].titulo == "Database Setup"
    
    def test_filtro_compuesto(self):
        """Prueba filtros compuestos."""
        # Crear filtros individuales
        filtro_titulo = crear_filtro_titulo_contiene("development")
        filtro_fecha = crear_filtro_fecha_rango(
            datetime.now(),
            datetime.now() + timedelta(days=10)
        )
        
        # Crear filtro compuesto
        filtro_combinado = filtro_compuesto(filtro_titulo, filtro_fecha)
        
        # Aplicar filtro
        tareas_filtradas = [t for t in self.tareas if filtro_combinado(t)]
        
        # Debe encontrar la tarea que cumple ambos criterios
        assert len(tareas_filtradas) == 1
        assert "development" in tareas_filtradas[0].titulo.lower()


class TestGeneradorCalendario:
    """Pruebas para el generador de calendario."""
    
    def test_generador_fechas_limite_calendario(self):
        """Prueba generador de fechas para calendario."""
        año = 2025
        mes = 12
        
        # Crear tareas para diciembre 2025 (fecha futura)
        tareas = [
            Tarea("Tarea 1", "Desc 1", datetime(2025, 12, 15)),
            Tarea("Tarea 2", "Desc 2", datetime(2025, 12, 15)),
            Tarea("Tarea 3", "Desc 3", datetime(2025, 12, 25)),
            Tarea("Tarea 4", "Desc 4", datetime(2025, 11, 15)),  # Mes diferente
        ]
        
        fechas_calendario = list(generador_fechas_limite_calendario(tareas, año, mes))
        
        # Debe haber 2 días con tareas (15 y 25)
        assert len(fechas_calendario) == 2
        
        # Verificar estructura de datos
        for fecha_data in fechas_calendario:
            assert 'fecha' in fecha_data
            assert 'dia' in fecha_data
            assert 'tareas' in fecha_data
            assert 'total_tareas' in fecha_data
            assert 'resumen' in fecha_data
        
        # Verificar el día 15 (2 tareas)
        dia_15 = next(f for f in fechas_calendario if f['dia'] == 15)
        assert dia_15['total_tareas'] == 2
        assert "2 tareas" in dia_15['resumen']


class TestGeneradorInfinito:
    """Pruebas para el generador infinito."""
    
    def test_generador_infinito_basico(self):
        """Prueba funcionalidad básica del generador infinito."""
        gen = GeneradorInfinito("TEST")
        
        # Generar algunos IDs
        ids = [next(gen) for _ in range(5)]
        
        assert len(ids) == 5
        assert all(id.startswith("TEST_") for id in ids)
        assert ids[0] == "TEST_000001"
        assert ids[4] == "TEST_000005"
    
    def test_generador_infinito_protocolo(self):
        """Prueba que implementa correctamente el protocolo de iterador."""
        gen = GeneradorInfinito()
        
        # Verificar que es su propio iterador
        assert iter(gen) is gen
        
        # Verificar que genera valores únicos
        id1 = next(gen)
        id2 = next(gen)
        
        assert id1 != id2
        assert id1 == "ID_000001"
        assert id2 == "ID_000002"


class TestGeneradoresManejoMemoria:
    """Pruebas para verificar el manejo eficiente de memoria."""
    
    def test_generadores_no_cargan_todo_en_memoria(self):
        """Prueba que los generadores no cargan todos los datos en memoria."""
        # Crear una gran cantidad de tareas
        tareas_grandes = []
        fecha_base = datetime.now()
        
        for i in range(1000):  # 1000 tareas
            tarea = Tarea(f"Tarea {i}", f"Descripción {i}", fecha_base + timedelta(days=i+1))  # +1 para asegurar fecha futura
            tareas_grandes.append(tarea)
        
        # El generador debe crear sin problemas
        gen = generador_estadisticas_por_lote(tareas_grandes, tamaño_lote=100)
        
        # Solo obtener el primer lote
        primer_lote = next(gen)
        
        # Verificar que solo procesó el primer lote
        assert primer_lote['lote_numero'] == 1
        assert primer_lote['total_tareas'] == 100
    
    def test_iterador_maneja_listas_vacias(self):
        """Prueba que los generadores manejan listas vacías correctamente."""
        iterador = IteradorTareas([])
        tareas_vacias = list(iterador)
        
        assert len(tareas_vacias) == 0
        
        # Generadores con listas vacías
        assert list(generador_tareas_por_estado([], "pendiente")) == []
        assert list(generador_tareas_vencidas([])) == []
        assert list(generador_estadisticas_por_lote([])) == []

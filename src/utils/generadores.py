"""
Módulo de generadores e iteradores personalizados para el sistema de gestión de tareas.

Este módulo implementa generadores eficientes para recorrer colecciones de tareas
y usuarios, optimizando el uso de memoria y proporcionando funcionalidades
de filtrado y transformación.
"""

from typing import Iterator, List, Generator, Optional, Callable, Any, Dict
from datetime import datetime, timedelta


class IteradorTareas:
    """
    Iterador personalizado para recorrer colecciones de tareas.
    
    Implementa el protocolo de iterador con métodos __iter__ y __next__,
    permitiendo filtrado y transformación de datos durante la iteración.
    """
    
    def __init__(self, tareas: List[Any], filtro: Optional[Callable] = None):
        """
        Inicializa el iterador con una lista de tareas y un filtro opcional.
        
        Args:
            tareas (List[Any]): Lista de objetos Tarea
            filtro (Optional[Callable]): Función para filtrar tareas
        """
        self.tareas = tareas
        self.filtro = filtro
        self.indice = 0
    
    def __iter__(self) -> 'IteradorTareas':
        """Retorna el iterador."""
        return self
    
    def __next__(self) -> Any:
        """
        Retorna la siguiente tarea que cumpla con el filtro.
        
        Returns:
            Any: Siguiente tarea filtrada
            
        Raises:
            StopIteration: Cuando no hay más tareas
        """
        while self.indice < len(self.tareas):
            tarea = self.tareas[self.indice]
            self.indice += 1
            
            # Aplicar filtro si existe
            if self.filtro is None or self.filtro(tarea):
                return tarea
        
        raise StopIteration


def generador_tareas_por_estado(tareas: List[Any], estado_objetivo: str) -> Generator[Any, None, None]:
    """
    Generador que yield tareas filtradas por estado.
    
    Args:
        tareas (List[Any]): Lista de tareas
        estado_objetivo (str): Estado a filtrar
        
    Yields:
        Any: Tareas que coinciden con el estado
    """
    for tarea in tareas:
        if hasattr(tarea, 'estado') and tarea.estado.value == estado_objetivo:
            yield tarea


def generador_tareas_por_usuario(tareas: List[Any], usuario_id: str) -> Generator[Any, None, None]:
    """
    Generador que yield tareas asignadas a un usuario específico.
    
    Args:
        tareas (List[Any]): Lista de tareas
        usuario_id (str): ID del usuario
        
    Yields:
        Any: Tareas asignadas al usuario
    """
    for tarea in tareas:
        if hasattr(tarea, 'usuario_id') and tarea.usuario_id == usuario_id:
            yield tarea


def generador_tareas_vencidas(tareas: List[Any]) -> Generator[Any, None, None]:
    """
    Generador que yield tareas vencidas.
    
    Args:
        tareas (List[Any]): Lista de tareas
        
    Yields:
        Any: Tareas que están vencidas
    """
    for tarea in tareas:
        if hasattr(tarea, 'esta_vencida') and tarea.esta_vencida():
            yield tarea


def generador_tareas_proximas_vencer(tareas: List[Any], dias: int = 3) -> Generator[Any, None, None]:
    """
    Generador que yield tareas próximas a vencer en los próximos N días.
    
    Args:
        tareas (List[Any]): Lista de tareas
        dias (int): Número de días para considerar "próximo a vencer"
        
    Yields:
        Any: Tareas próximas a vencer
    """
    for tarea in tareas:
        if hasattr(tarea, 'calcular_dias_restantes'):
            dias_restantes = tarea.calcular_dias_restantes()
            if 0 <= dias_restantes <= dias:
                yield tarea


def generador_estadisticas_por_lote(tareas: List[Any], tamaño_lote: int = 10) -> Generator[Dict[str, Any], None, None]:
    """
    Generador que procesa tareas en lotes y yield estadísticas.
    
    Implementa lazy loading para manejar grandes volúmenes de datos
    de manera eficiente en memoria.
    
    Args:
        tareas (List[Any]): Lista de tareas
        tamaño_lote (int): Tamaño del lote a procesar
        
    Yields:
        Dict[str, Any]: Estadísticas del lote procesado
    """
    for i in range(0, len(tareas), tamaño_lote):
        lote = tareas[i:i + tamaño_lote]
        
        # Calcular estadísticas del lote usando métodos de listas
        total_tareas = len(lote)
        pendientes = sum(1 for t in lote if hasattr(t, 'estado') and t.estado.value == 'pendiente')
        en_progreso = sum(1 for t in lote if hasattr(t, 'estado') and t.estado.value == 'en_progreso')
        completadas = sum(1 for t in lote if hasattr(t, 'estado') and t.estado.value == 'completada')
        
        yield {
            'lote_numero': (i // tamaño_lote) + 1,
            'rango_indices': (i, min(i + tamaño_lote - 1, len(tareas) - 1)),
            'total_tareas': total_tareas,
            'pendientes': pendientes,
            'en_progreso': en_progreso,
            'completadas': completadas,
            'porcentaje_completadas': (completadas / total_tareas * 100) if total_tareas > 0 else 0
        }


def generador_usuarios_con_tareas(usuarios: List[Any], tareas: List[Any]) -> Generator[Dict[str, Any], None, None]:
    """
    Generador que combina usuarios con sus tareas asignadas.
    
    Args:
        usuarios (List[Any]): Lista de usuarios
        tareas (List[Any]): Lista de tareas
        
    Yields:
        Dict[str, Any]: Usuario con sus tareas detalladas
    """
    # Crear un diccionario de tareas por usuario_id para búsqueda eficiente
    tareas_por_usuario = {}
    for tarea in tareas:
        if hasattr(tarea, 'usuario_id') and tarea.usuario_id:
            if tarea.usuario_id not in tareas_por_usuario:
                tareas_por_usuario[tarea.usuario_id] = []
            tareas_por_usuario[tarea.usuario_id].append(tarea)
    
    # Yield cada usuario con sus tareas
    for usuario in usuarios:
        if hasattr(usuario, 'id'):
            tareas_usuario = tareas_por_usuario.get(usuario.id, [])
            yield {
                'usuario': usuario,
                'tareas': tareas_usuario,
                'total_tareas': len(tareas_usuario),
                'tareas_pendientes': [t for t in tareas_usuario if hasattr(t, 'estado') and t.estado.value == 'pendiente'],
                'tareas_en_progreso': [t for t in tareas_usuario if hasattr(t, 'estado') and t.estado.value == 'en_progreso'],
                'tareas_completadas': [t for t in tareas_usuario if hasattr(t, 'estado') and t.estado.value == 'completada']
            }


def generador_fechas_limite_calendario(tareas: List[Any], año: int, mes: int) -> Generator[Dict[str, Any], None, None]:
    """
    Generador que yield tareas organizadas por fecha límite en un mes específico.
    
    Útil para generar vistas de calendario con tareas.
    
    Args:
        tareas (List[Any]): Lista de tareas
        año (int): Año del calendario
        mes (int): Mes del calendario (1-12)
        
    Yields:
        Dict[str, Any]: Fecha con tareas asociadas
    """
    # Filtrar tareas del mes específico
    tareas_del_mes = []
    for tarea in tareas:
        if hasattr(tarea, 'fecha_limite'):
            fecha = tarea.fecha_limite
            if fecha.year == año and fecha.month == mes:
                tareas_del_mes.append(tarea)
    
    # Agrupar por día usando métodos de listas y cadenas
    tareas_por_dia = {}
    for tarea in tareas_del_mes:
        dia = tarea.fecha_limite.day
        if dia not in tareas_por_dia:
            tareas_por_dia[dia] = []
        tareas_por_dia[dia].append(tarea)
    
    # Yield cada día con sus tareas
    for dia in sorted(tareas_por_dia.keys()):
        tareas_dia = tareas_por_dia[dia]
        yield {
            'fecha': datetime(año, mes, dia).date(),
            'dia': dia,
            'tareas': tareas_dia,
            'total_tareas': len(tareas_dia),
            'resumen': f"{len(tareas_dia)} tarea{'s' if len(tareas_dia) != 1 else ''}"
        }


def filtro_compuesto(*filtros: Callable) -> Callable:
    """
    Crea un filtro compuesto que aplica múltiples filtros con AND lógico.
    
    Args:
        *filtros: Funciones de filtro a combinar
        
    Returns:
        Callable: Función de filtro compuesta
    """
    def filtro_combinado(item: Any) -> bool:
        return all(filtro(item) for filtro in filtros)
    
    return filtro_combinado


def crear_filtro_fecha_rango(fecha_inicio: datetime, fecha_fin: datetime) -> Callable:
    """
    Crea un filtro para tareas en un rango de fechas.
    
    Args:
        fecha_inicio (datetime): Fecha de inicio del rango
        fecha_fin (datetime): Fecha de fin del rango
        
    Returns:
        Callable: Función de filtro para el rango
    """
    def filtro_fecha(tarea: Any) -> bool:
        if hasattr(tarea, 'fecha_limite'):
            return fecha_inicio <= tarea.fecha_limite <= fecha_fin
        return False
    
    return filtro_fecha


def crear_filtro_titulo_contiene(texto: str) -> Callable:
    """
    Crea un filtro para tareas cuyo título contiene un texto específico.
    
    Usa métodos de cadenas para búsqueda insensible a mayúsculas.
    
    Args:
        texto (str): Texto a buscar en el título
        
    Returns:
        Callable: Función de filtro para títulos
    """
    def filtro_titulo(tarea: Any) -> bool:
        if hasattr(tarea, 'titulo'):
            return texto.lower().strip() in tarea.titulo.lower()
        return False
    
    return filtro_titulo


class GeneradorInfinito:
    """
    Generador infinito para IDs únicos (ejemplo de generador avanzado).
    """
    
    def __init__(self, prefijo: str = "ID"):
        """
        Inicializa el generador con un prefijo.
        
        Args:
            prefijo (str): Prefijo para los IDs generados
        """
        self.prefijo = prefijo
        self.contador = 0
    
    def __iter__(self) -> Iterator[str]:
        """Retorna el iterador."""
        return self
    
    def __next__(self) -> str:
        """
        Genera el siguiente ID.
        
        Returns:
            str: Próximo ID único
        """
        self.contador += 1
        return f"{self.prefijo}_{self.contador:06d}"

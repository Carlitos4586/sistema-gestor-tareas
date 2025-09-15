"""
Módulo de formateo y utilidades de cadenas y listas para el sistema de gestión de tareas.

Este módulo contiene funciones especializadas para el formateo de cadenas,
manipulación de listas y transformación de datos usando los métodos
nativos de Python.
"""

import re
import calendar
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class TipoFormato(Enum):
    """Tipos de formato disponibles para diferentes tipos de datos."""
    TITULO = "titulo"
    NOMBRE = "nombre"
    EMAIL = "email"
    DESCRIPCION = "descripcion"
    FECHA = "fecha"


def formatear_titulo(titulo: str) -> str:
    """
    Formatea un título usando métodos de cadenas.
    
    Aplica las siguientes transformaciones:
    - Elimina espacios al inicio y final
    - Convierte a Title Case
    - Reemplaza múltiples espacios con uno solo
    - Capitaliza después de guiones y puntos
    
    Args:
        titulo (str): Título a formatear
        
    Returns:
        str: Título formateado
        
    Example:
        >>> formatear_titulo("  desarrollo   de-API  rest  ")
        "Desarrollo De-Api Rest"
    """
    if not titulo:
        return ""
    
    # Usar métodos de cadenas para limpiar y formatear
    titulo = titulo.strip()  # Eliminar espacios
    titulo = re.sub(r'\s+', ' ', titulo)  # Múltiples espacios a uno
    titulo = titulo.title()  # Convertir a Title Case
    
    # Formateo especial después de guiones
    if '-' in titulo:
        partes = titulo.split('-')
        partes_formateadas = [parte.strip().title() for parte in partes]
        titulo = '-'.join(partes_formateadas)
    
    return titulo


def formatear_nombre_completo(nombre: str) -> str:
    """
    Formatea un nombre completo usando métodos de cadenas avanzados.
    
    Args:
        nombre (str): Nombre a formatear
        
    Returns:
        str: Nombre formateado correctamente
        
    Example:
        >>> formatear_nombre_completo("  JUAN   carlos  PÉREZ  ")
        "Juan Carlos Pérez"
    """
    if not nombre:
        return ""
    
    # Limpiar y dividir en palabras
    palabras = nombre.strip().split()
    
    # Formatear cada palabra usando métodos de listas y cadenas
    palabras_formateadas = []
    for palabra in palabras:
        if palabra:  # Evitar cadenas vacías
            palabra_limpia = palabra.strip().lower()
            # Capitalizar primera letra y mantener el resto en minúscula
            palabra_formateada = palabra_limpia[0].upper() + palabra_limpia[1:]
            palabras_formateadas.append(palabra_formateada)
    
    # Unir las palabras usando join()
    return ' '.join(palabras_formateadas)


def validar_email(email: str) -> bool:
    """
    Valida un email usando métodos de cadenas.
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si el email es válido
        
    Example:
        >>> validar_email("usuario@dominio.com")
        True
    """
    es_valido, _ = validar_y_formatear_email(email)
    return es_valido


def validar_y_formatear_email(email: str) -> Tuple[bool, str]:
    """
    Valida y formatea un email usando métodos de cadenas.
    
    Args:
        email (str): Email a validar y formatear
        
    Returns:
        Tuple[bool, str]: (es_valido, email_formateado)
        
    Example:
        >>> validar_y_formatear_email("  JUAN@EJEMPLO.COM  ")
        (True, "juan@ejemplo.com")
    """
    if not email:
        return False, ""
    
    # Limpiar y normalizar usando métodos de cadenas
    email_limpio = email.strip().lower()
    
    # Validación básica usando métodos de cadenas
    if '@' not in email_limpio:
        return False, email_limpio
    
    # Dividir en partes usando split()
    partes = email_limpio.split('@')
    if len(partes) != 2:
        return False, email_limpio
    
    usuario, dominio = partes
    
    # Validaciones usando métodos de cadenas
    if not usuario or not dominio:
        return False, email_limpio
    
    if '.' not in dominio:
        return False, email_limpio
    
    # Verificar caracteres válidos usando métodos de cadenas
    caracteres_validos = usuario.replace('.', '').replace('_', '').replace('-', '')
    if not caracteres_validos.isalnum():
        return False, email_limpio
    
    return True, email_limpio


def limpiar_descripcion(descripcion: str, max_lineas: int = 10) -> str:
    """
    Limpia y formatea una descripción usando métodos de cadenas.
    
    Args:
        descripcion (str): Descripción a limpiar
        max_lineas (int): Máximo número de líneas permitidas
        
    Returns:
        str: Descripción limpia y formateada
    """
    if not descripcion:
        return ""
    
    # Normalizar saltos de línea y limpiar
    descripcion = descripcion.replace('\r\n', '\n').replace('\r', '\n')
    descripcion = descripcion.strip()
    
    # Dividir en líneas y procesar usando métodos de listas
    lineas = descripcion.split('\n')
    
    # Limpiar cada línea y filtrar vacías
    lineas_limpias = []
    for linea in lineas:
        linea_limpia = linea.strip()
        if linea_limpia:  # Solo agregar líneas no vacías
            lineas_limpias.append(linea_limpia)
    
    # Limitar número de líneas usando slicing de listas
    if len(lineas_limpias) > max_lineas:
        lineas_limpias = lineas_limpias[:max_lineas]
        lineas_limpias.append("... (contenido truncado)")
    
    # Unir líneas usando join()
    return '\n'.join(lineas_limpias)


def formatear_lista_elementos(elementos: List[str], separador: str = ", ", 
                             formato_final: str = " y ") -> str:
    """
    Formatea una lista de elementos como cadena legible usando métodos de listas.
    
    Args:
        elementos (List[str]): Lista de elementos a formatear
        separador (str): Separador entre elementos
        formato_final (str): Separador antes del último elemento
        
    Returns:
        str: Cadena formateada
        
    Example:
        >>> formatear_lista_elementos(["Juan", "María", "Carlos"])
        "Juan, María y Carlos"
    """
    if not elementos:
        return ""
    
    # Filtrar elementos vacíos usando list comprehension
    elementos_filtrados = [elem.strip() for elem in elementos if elem.strip()]
    
    if not elementos_filtrados:
        return ""
    
    if len(elementos_filtrados) == 1:
        return elementos_filtrados[0]
    
    if len(elementos_filtrados) == 2:
        return elementos_filtrados[0] + formato_final + elementos_filtrados[1]
    
    # Para más de 2 elementos, usar join() creativamente
    todos_menos_ultimo = separador.join(elementos_filtrados[:-1])
    return todos_menos_ultimo + formato_final + elementos_filtrados[-1]


def extraer_palabras_clave(texto: str, min_longitud: int = 3) -> List[str]:
    """
    Extrae palabras clave de un texto usando métodos de cadenas y listas.
    
    Args:
        texto (str): Texto del cual extraer palabras clave
        min_longitud (int): Longitud mínima de las palabras
        
    Returns:
        List[str]: Lista de palabras clave únicas
    """
    if not texto:
        return []
    
    # Lista de palabras comunes a filtrar (stop words básicas)
    palabras_comunes = {
        'de', 'del', 'la', 'el', 'en', 'con', 'por', 'para', 'que', 'se', 
        'y', 'o', 'un', 'una', 'es', 'son', 'como', 'muy', 'mas', 'pero',
        'web', 'las', 'los', 'del', 'te', 'le', 'lo', 'me', 'su', 'sus'
    }
    
    # Limpiar y normalizar usando métodos de cadenas
    texto_limpio = texto.lower().strip()
    
    # Remover puntuación básica usando replace()
    puntuacion = ".,;:!?()¡¿[]{}\"'»«"
    for char in puntuacion:
        texto_limpio = texto_limpio.replace(char, ' ')
    
    # Dividir en palabras usando split()
    palabras = texto_limpio.split()
    
    # Filtrar palabras usando list comprehension y métodos de cadenas
    palabras_validas = [
        palabra.strip() 
        for palabra in palabras 
        if (palabra.strip() and 
            len(palabra.strip()) >= min_longitud and
            palabra.strip() not in palabras_comunes)
    ]
    
    # Eliminar duplicados manteniendo orden usando set y métodos de listas
    palabras_unicas = []
    for palabra in palabras_validas:
        if palabra not in palabras_unicas:
            palabras_unicas.append(palabra)
    
    return palabras_unicas


def crear_resumen_texto(texto: str, max_palabras: int = 20) -> str:
    """
    Crea un resumen de texto limitando el número de palabras.
    
    Args:
        texto (str): Texto a resumir
        max_palabras (int): Máximo número de palabras
        
    Returns:
        str: Texto resumido
    """
    if not texto:
        return ""
    
    # Dividir en palabras usando split()
    palabras = texto.strip().split()
    
    # Limitar usando slicing de listas
    if len(palabras) <= max_palabras:
        return texto.strip()
    
    # Tomar solo las primeras palabras y agregar indicador
    palabras_resumidas = palabras[:max_palabras]
    texto_resumido = ' '.join(palabras_resumidas)
    
    return texto_resumido + " ..."


def formatear_fecha_legible(fecha: datetime, incluir_hora: bool = False,
                           formato_relativo: bool = True) -> str:
    """
    Formatea una fecha de manera legible usando datetime y métodos de cadenas.
    
    Args:
        fecha (datetime): Fecha a formatear
        incluir_hora (bool): Si incluir la hora en el formato
        formato_relativo (bool): Si mostrar formato relativo (hace X días)
        
    Returns:
        str: Fecha formateada de manera legible
    """
    if not fecha:
        return ""
    
    # Formatear fecha base usando strftime y métodos de cadenas
    if incluir_hora:
        fecha_str = fecha.strftime("%d de %B de %Y a las %H:%M")
    else:
        fecha_str = fecha.strftime("%d de %B de %Y")
    
    # Traducir nombres de meses usando replace() (métodos de cadenas)
    meses_es = {
        'January': 'enero', 'February': 'febrero', 'March': 'marzo',
        'April': 'abril', 'May': 'mayo', 'June': 'junio',
        'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
        'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
    }
    
    for mes_en, mes_es in meses_es.items():
        fecha_str = fecha_str.replace(mes_en, mes_es)
    
    # Agregar información relativa si se solicita
    if formato_relativo:
        ahora = datetime.now()
        diferencia = fecha - ahora
        
        # Usar segundos totales para un cálculo más preciso
        segundos_totales = diferencia.total_seconds()
        dias = round(segundos_totales / (24 * 3600))
        
        if dias == 0:
            relativo = "hoy"
        elif dias == 1:
            relativo = "mañana"
        elif dias == -1:
            relativo = "ayer"
        elif dias > 0:
            relativo = f"en {dias} días"
        else:
            relativo = f"hace {abs(dias)} días"
        
        fecha_str = f"{fecha_str} ({relativo})"
    
    return fecha_str


def formatear_duracion(minutos: int) -> str:
    """
    Formatea una duración en minutos a formato legible.
    
    Args:
        minutos (int): Duración en minutos
        
    Returns:
        str: Duración formateada
        
    Example:
        >>> formatear_duracion(125)
        "2 horas y 5 minutos"
    """
    if minutos <= 0:
        return "0 minutos"
    
    # Calcular componentes
    horas = minutos // 60
    mins_restantes = minutos % 60
    
    # Construir cadena usando métodos de listas y cadenas
    partes = []
    
    if horas > 0:
        if horas == 1:
            partes.append("1 hora")
        else:
            partes.append(f"{horas} horas")
    
    if mins_restantes > 0:
        if mins_restantes == 1:
            partes.append("1 minuto")
        else:
            partes.append(f"{mins_restantes} minutos")
    
    # Unir usando formateo de listas
    return formatear_lista_elementos(partes)


def organizar_datos_por_categoria(datos: List[Dict[str, Any]], 
                                 campo_categoria: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Organiza una lista de datos por categorías usando métodos de listas.
    
    Args:
        datos (List[Dict[str, Any]]): Lista de datos a organizar
        campo_categoria (str): Campo que contiene la categoría
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Datos organizados por categoría
    """
    if not datos:
        return {}
    
    # Organizar usando métodos de listas y diccionarios
    datos_organizados = {}
    
    for item in datos:
        if campo_categoria in item:
            categoria = str(item[campo_categoria]).strip().lower()
            
            # Crear lista si no existe usando métodos de diccionarios
            if categoria not in datos_organizados:
                datos_organizados[categoria] = []
            
            # Agregar item usando append()
            datos_organizados[categoria].append(item)
    
    return datos_organizados


def generar_calendario_texto(año: int, mes: int, tareas_por_dia: Dict[int, List[Any]] = None) -> str:
    """
    Genera un calendario en formato texto usando el módulo calendar y métodos de cadenas.
    
    Args:
        año (int): Año del calendario
        mes (int): Mes del calendario
        tareas_por_dia (Dict[int, List[Any]]): Tareas organizadas por día
        
    Returns:
        str: Calendario en formato texto
    """
    if not tareas_por_dia:
        tareas_por_dia = {}
    
    # Generar calendario base usando el módulo calendar
    cal = calendar.monthcalendar(año, mes)
    nombre_mes = calendar.month_name[mes]
    
    # Construir encabezado usando métodos de cadenas
    lineas = []
    lineas.append(f"{nombre_mes.title()} {año}".center(28))
    lineas.append("-" * 28)
    lineas.append("Lu Ma Mi Ju Vi Sa Do")
    
    # Construir filas del calendario
    for semana in cal:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append("  ")  # Día vacío
            else:
                # Marcar días con tareas usando métodos de cadenas
                if dia in tareas_por_dia and tareas_por_dia[dia]:
                    fila.append(f"{dia:2d}*")  # Asterisco para días con tareas
                else:
                    fila.append(f"{dia:2d} ")
        
        # Unir fila usando join()
        lineas.append(" ".join(fila))
    
    # Agregar leyenda si hay tareas
    if any(tareas_por_dia.values()):
        lineas.append("")
        lineas.append("* Días con tareas programadas")
    
    # Unir todas las líneas usando join()
    return "\n".join(lineas)

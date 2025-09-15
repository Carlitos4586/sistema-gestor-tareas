"""
Pruebas unitarias para el módulo de formateo.

Este módulo contiene todas las pruebas para verificar el correcto
funcionamiento de las funciones de formateo de cadenas y listas.
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.formateo import (
    formatear_titulo, formatear_nombre_completo, validar_y_formatear_email,
    limpiar_descripcion, formatear_lista_elementos, extraer_palabras_clave,
    crear_resumen_texto, formatear_fecha_legible, formatear_duracion,
    organizar_datos_por_categoria, generar_calendario_texto, TipoFormato
)


class TestFormateoTitulo:
    """Pruebas para formateo de títulos."""
    
    def test_formatear_titulo_basico(self):
        """Prueba formateo básico de títulos."""
        titulo = "  desarrollo   de-API  rest  "
        resultado = formatear_titulo(titulo)
        
        assert resultado == "Desarrollo De-Api Rest"
    
    def test_formatear_titulo_con_guiones(self):
        """Prueba formateo de títulos con guiones."""
        titulo = "proyecto-web-frontend"
        resultado = formatear_titulo(titulo)
        
        assert resultado == "Proyecto-Web-Frontend"
    
    def test_formatear_titulo_vacio(self):
        """Prueba formateo de título vacío."""
        assert formatear_titulo("") == ""
        assert formatear_titulo("   ") == ""
        assert formatear_titulo(None) == ""
    
    def test_formatear_titulo_espacios_multiples(self):
        """Prueba eliminación de espacios múltiples."""
        titulo = "proyecto    con     muchos   espacios"
        resultado = formatear_titulo(titulo)
        
        assert resultado == "Proyecto Con Muchos Espacios"


class TestFormateoNombre:
    """Pruebas para formateo de nombres."""
    
    def test_formatear_nombre_completo_basico(self):
        """Prueba formateo básico de nombres."""
        nombre = "  JUAN   carlos  PÉREZ  "
        resultado = formatear_nombre_completo(nombre)
        
        assert resultado == "Juan Carlos Pérez"
    
    def test_formatear_nombre_minusculas(self):
        """Prueba formateo de nombres en minúsculas."""
        nombre = "maría josé martínez"
        resultado = formatear_nombre_completo(nombre)
        
        assert resultado == "María José Martínez"
    
    def test_formatear_nombre_vacio(self):
        """Prueba formateo de nombre vacío."""
        assert formatear_nombre_completo("") == ""
        assert formatear_nombre_completo("   ") == ""


class TestValidacionEmail:
    """Pruebas para validación y formateo de emails."""
    
    def test_email_valido(self):
        """Prueba email válido."""
        email = "  JUAN@EJEMPLO.COM  "
        valido, email_formateado = validar_y_formatear_email(email)
        
        assert valido is True
        assert email_formateado == "juan@ejemplo.com"
    
    def test_email_con_guion_bajo(self):
        """Prueba email con guión bajo."""
        email = "juan_carlos@ejemplo.com"
        valido, email_formateado = validar_y_formatear_email(email)
        
        assert valido is True
        assert email_formateado == "juan_carlos@ejemplo.com"
    
    def test_email_invalido_sin_arroba(self):
        """Prueba email inválido sin @."""
        valido, _ = validar_y_formatear_email("email_sin_arroba.com")
        assert valido is False
    
    def test_email_invalido_sin_punto(self):
        """Prueba email inválido sin punto en dominio."""
        valido, _ = validar_y_formatear_email("juan@ejemplocom")
        assert valido is False
    
    def test_email_vacio(self):
        """Prueba email vacío."""
        valido, _ = validar_y_formatear_email("")
        assert valido is False


class TestLimpiezaDescripcion:
    """Pruebas para limpieza de descripciones."""
    
    def test_limpiar_descripcion_basica(self):
        """Prueba limpieza básica de descripción."""
        descripcion = """  
        Línea 1 de descripción
        
        Línea 2 con contenido
        
        Línea 3 final
        """
        resultado = limpiar_descripcion(descripcion)
        
        lineas = resultado.split('\n')
        assert len(lineas) == 3
        assert "Línea 1 de descripción" in lineas
        assert "Línea 2 con contenido" in lineas
        assert "Línea 3 final" in lineas
    
    def test_limpiar_descripcion_limite_lineas(self):
        """Prueba límite de líneas en descripción."""
        lineas_largas = ['Línea ' + str(i) for i in range(15)]
        descripcion = '\n'.join(lineas_largas)
        
        resultado = limpiar_descripcion(descripcion, max_lineas=5)
        
        lineas_resultado = resultado.split('\n')
        assert len(lineas_resultado) == 6  # 5 líneas + mensaje de truncado
        assert "... (contenido truncado)" in lineas_resultado[-1]
    
    def test_limpiar_descripcion_vacia(self):
        """Prueba descripción vacía."""
        assert limpiar_descripcion("") == ""
        assert limpiar_descripcion("   ") == ""


class TestFormateoListas:
    """Pruebas para formateo de listas."""
    
    def test_formatear_lista_elementos_normal(self):
        """Prueba formateo normal de lista."""
        elementos = ["Juan", "María", "Carlos"]
        resultado = formatear_lista_elementos(elementos)
        
        assert resultado == "Juan, María y Carlos"
    
    def test_formatear_lista_dos_elementos(self):
        """Prueba formateo de lista con dos elementos."""
        elementos = ["Juan", "María"]
        resultado = formatear_lista_elementos(elementos)
        
        assert resultado == "Juan y María"
    
    def test_formatear_lista_un_elemento(self):
        """Prueba formateo de lista con un elemento."""
        elementos = ["Juan"]
        resultado = formatear_lista_elementos(elementos)
        
        assert resultado == "Juan"
    
    def test_formatear_lista_vacia(self):
        """Prueba formateo de lista vacía."""
        assert formatear_lista_elementos([]) == ""
    
    def test_formatear_lista_con_separador_personalizado(self):
        """Prueba formateo con separador personalizado."""
        elementos = ["A", "B", "C", "D"]
        resultado = formatear_lista_elementos(elementos, separador=" - ", formato_final=" and ")
        
        assert resultado == "A - B - C and D"


class TestPalabrasClave:
    """Pruebas para extracción de palabras clave."""
    
    def test_extraer_palabras_clave_basico(self):
        """Prueba extracción básica de palabras clave."""
        texto = "Desarrollo de aplicación web con Python y Django"
        palabras = extraer_palabras_clave(texto)
        
        assert "desarrollo" in palabras
        assert "aplicación" in palabras
        assert "python" in palabras
        assert "django" in palabras
        # No debe incluir palabras cortas como "de", "con", "web"
        assert "de" not in palabras
        assert "con" not in palabras
    
    def test_extraer_palabras_clave_con_puntuacion(self):
        """Prueba extracción con puntuación."""
        texto = "¡Hola! ¿Cómo estás? Muy bien, gracias."
        palabras = extraer_palabras_clave(texto, min_longitud=4)
        
        assert "hola" in palabras
        assert "cómo" in palabras
        assert "estás" in palabras
        assert "bien" in palabras
        assert "gracias" in palabras
    
    def test_extraer_palabras_clave_duplicados(self):
        """Prueba que se eliminen duplicados."""
        texto = "python python desarrollo desarrollo"
        palabras = extraer_palabras_clave(texto)
        
        assert len(palabras) == 2
        assert "python" in palabras
        assert "desarrollo" in palabras
    
    def test_extraer_palabras_clave_texto_vacio(self):
        """Prueba con texto vacío."""
        assert extraer_palabras_clave("") == []
        assert extraer_palabras_clave("   ") == []


class TestResumenTexto:
    """Pruebas para creación de resúmenes."""
    
    def test_crear_resumen_texto_corto(self):
        """Prueba resumen de texto corto."""
        texto = "Este es un texto corto"
        resultado = crear_resumen_texto(texto, max_palabras=10)
        
        assert resultado == texto.strip()
    
    def test_crear_resumen_texto_largo(self):
        """Prueba resumen de texto largo."""
        texto = "Esta es una descripción muy larga que tiene muchas palabras y debería ser truncada"
        resultado = crear_resumen_texto(texto, max_palabras=5)
        
        assert resultado == "Esta es una descripción muy ..."
        assert len(resultado.split()) == 6  # 5 palabras + "..."
    
    def test_crear_resumen_texto_vacio(self):
        """Prueba resumen de texto vacío."""
        assert crear_resumen_texto("") == ""


class TestFormateoFecha:
    """Pruebas para formateo de fechas."""
    
    def test_formatear_fecha_sin_hora(self):
        """Prueba formateo de fecha sin hora."""
        fecha = datetime(2024, 12, 15, 14, 30)
        resultado = formatear_fecha_legible(fecha, incluir_hora=False, formato_relativo=False)
        
        assert "15 de" in resultado
        assert "2024" in resultado
        assert "14:30" not in resultado
    
    def test_formatear_fecha_con_hora(self):
        """Prueba formateo de fecha con hora."""
        fecha = datetime(2024, 12, 15, 14, 30)
        resultado = formatear_fecha_legible(fecha, incluir_hora=True, formato_relativo=False)
        
        assert "15 de" in resultado
        assert "2024" in resultado
        assert "14:30" in resultado
        assert "las" in resultado
    
    def test_formatear_fecha_relativa_mañana(self):
        """Prueba formateo relativo para mañana."""
        mañana = datetime.now() + timedelta(days=1)
        resultado = formatear_fecha_legible(mañana, formato_relativo=True)
        
        assert "mañana" in resultado.lower()
    
    def test_formatear_fecha_vacia(self):
        """Prueba formateo de fecha vacía."""
        assert formatear_fecha_legible(None) == ""


class TestFormateoDuracion:
    """Pruebas para formateo de duraciones."""
    
    def test_formatear_duracion_solo_horas(self):
        """Prueba formateo de duración solo en horas."""
        resultado = formatear_duracion(120)  # 2 horas
        assert resultado == "2 horas"
    
    def test_formatear_duracion_solo_minutos(self):
        """Prueba formateo de duración solo en minutos."""
        resultado = formatear_duracion(45)  # 45 minutos
        assert resultado == "45 minutos"
    
    def test_formatear_duracion_mixta(self):
        """Prueba formateo de duración mixta."""
        resultado = formatear_duracion(125)  # 2 horas y 5 minutos
        assert resultado == "2 horas y 5 minutos"
    
    def test_formatear_duracion_una_hora(self):
        """Prueba formateo de una hora exacta."""
        resultado = formatear_duracion(60)
        assert resultado == "1 hora"
    
    def test_formatear_duracion_un_minuto(self):
        """Prueba formateo de un minuto."""
        resultado = formatear_duracion(1)
        assert resultado == "1 minuto"
    
    def test_formatear_duracion_cero(self):
        """Prueba formateo de duración cero."""
        resultado = formatear_duracion(0)
        assert resultado == "0 minutos"


class TestOrganizacionDatos:
    """Pruebas para organización de datos por categoría."""
    
    def test_organizar_datos_por_categoria(self):
        """Prueba organización básica por categoría."""
        datos = [
            {"nombre": "Tarea 1", "categoria": "Desarrollo"},
            {"nombre": "Tarea 2", "categoria": "DESARROLLO"},
            {"nombre": "Tarea 3", "categoria": "Testing"},
            {"nombre": "Tarea 4", "categoria": "testing"}
        ]
        
        organizados = organizar_datos_por_categoria(datos, "categoria")
        
        assert "desarrollo" in organizados
        assert "testing" in organizados
        assert len(organizados["desarrollo"]) == 2
        assert len(organizados["testing"]) == 2
    
    def test_organizar_datos_lista_vacia(self):
        """Prueba organización de lista vacía."""
        resultado = organizar_datos_por_categoria([], "categoria")
        assert resultado == {}


class TestGeneradorCalendario:
    """Pruebas para generador de calendario."""
    
    def test_generar_calendario_texto_basico(self):
        """Prueba generación básica de calendario."""
        calendario = generar_calendario_texto(2024, 1)  # Enero 2024
        
        assert "January 2024" in calendario or "Enero 2024" in calendario
        assert "Lu Ma Mi Ju Vi Sa Do" in calendario
        assert "1 " in calendario
        assert "31" in calendario
    
    def test_generar_calendario_con_tareas(self):
        """Prueba calendario con tareas marcadas."""
        tareas_por_dia = {
            15: ["tarea1", "tarea2"],
            25: ["tarea3"]
        }
        
        calendario = generar_calendario_texto(2024, 1, tareas_por_dia)
        
        assert "15*" in calendario  # Día con tareas marcado
        assert "25*" in calendario  # Día con tareas marcado
        assert "* Días con tareas programadas" in calendario


class TestTipoFormato:
    """Pruebas para enum TipoFormato."""
    
    def test_tipos_formato_disponibles(self):
        """Prueba que todos los tipos de formato estén disponibles."""
        assert TipoFormato.TITULO.value == "titulo"
        assert TipoFormato.NOMBRE.value == "nombre"
        assert TipoFormato.EMAIL.value == "email"
        assert TipoFormato.DESCRIPCION.value == "descripcion"
        assert TipoFormato.FECHA.value == "fecha"

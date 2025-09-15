"""
Sistema de logging simple y profesional para el proyecto.

Este módulo configura el sistema de logging de forma centralizada,
permitiendo registrar eventos importantes del sistema de manera profesional.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class ConfiguradorLogger:
    """
    Clase para configurar el sistema de logging del proyecto.

    Proporciona configuración centralizada y simple para usar
    logging profesional en el sistema.
    """

    @staticmethod
    def configurar_logger(
        nombre: str = "sistema_tareas",
        nivel: str = "INFO",
        archivo_log: str = None,
        formato_consola: bool = True,
    ) -> logging.Logger:
        """
        Configura un logger para el sistema de tareas.

        Args:
            nombre (str): Nombre del logger
            nivel (str): Nivel de logging ('DEBUG', 'INFO', 'WARNING', 'ERROR')
            archivo_log (str, optional): Nombre del archivo de log
            formato_consola (bool): Si mostrar también en consola

        Returns:
            logging.Logger: Logger configurado

        Example:
            >>> logger = ConfiguradorLogger.configurar_logger()
            >>> logger.info("✅ Sistema iniciado")
        """
        # Crear el logger
        logger = logging.getLogger(nombre)

        # Evitar duplicar handlers si ya está configurado
        if logger.handlers:
            return logger

        # Configurar nivel
        niveles = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        logger.setLevel(niveles.get(nivel.upper(), logging.INFO))

        # Formato de los mensajes
        formato = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler para consola (si se requiere)
        if formato_consola:
            handler_consola = logging.StreamHandler()
            handler_consola.setFormatter(formato)
            logger.addHandler(handler_consola)

        # Handler para archivo (si se especifica)
        if archivo_log:
            # Crear directorio logs si no existe
            Path("logs").mkdir(exist_ok=True)

            # Ruta completa del archivo
            ruta_log = Path("logs") / archivo_log

            handler_archivo = logging.FileHandler(ruta_log, encoding="utf-8")
            handler_archivo.setFormatter(formato)
            logger.addHandler(handler_archivo)

        return logger

    @staticmethod
    def obtener_logger_sistema() -> logging.Logger:
        """
        Obtiene el logger principal del sistema ya configurado.

        Returns:
            logging.Logger: Logger del sistema configurado
        """
        return ConfiguradorLogger.configurar_logger(
            nombre="sistema_tareas",
            nivel="INFO",
            archivo_log="sistema_tareas.log",
            formato_consola=True,
        )


# Configuración global para uso fácil en todo el proyecto
def obtener_logger(nombre_modulo: str = None) -> logging.Logger:
    """
    Función simple para obtener un logger configurado.

    Args:
        nombre_modulo (str, optional): Nombre del módulo (ej: "usuario", "tarea")

    Returns:
        logging.Logger: Logger configurado

    Example:
        >>> from src.utils.logger import obtener_logger
        >>> logger = obtener_logger("usuario")
        >>> logger.info("✅ Usuario creado exitosamente")
    """
    if nombre_modulo:
        nombre_completo = f"sistema_tareas.{nombre_modulo}"
    else:
        nombre_completo = "sistema_tareas"

    return ConfiguradorLogger.configurar_logger(
        nombre=nombre_completo,
        nivel="INFO",
        archivo_log="sistema_tareas.log",
        formato_consola=True,
    )


# Logger principal del sistema (para uso inmediato)
logger_sistema = obtener_logger()


def log_inicio_operacion(operacion: str, detalles: str = None):
    """
    Helper para logging de inicio de operaciones importantes.

    Args:
        operacion (str): Nombre de la operación
        detalles (str, optional): Detalles adicionales
    """
    mensaje = f"🚀 Iniciando: {operacion}"
    if detalles:
        mensaje += f" - {detalles}"
    logger_sistema.info(mensaje)


def log_exito_operacion(operacion: str, detalles: str = None):
    """
    Helper para logging de operaciones exitosas.

    Args:
        operacion (str): Nombre de la operación
        detalles (str, optional): Detalles adicionales
    """
    mensaje = f"✅ Éxito: {operacion}"
    if detalles:
        mensaje += f" - {detalles}"
    logger_sistema.info(mensaje)


def log_advertencia(mensaje: str, detalles: str = None):
    """
    Helper para logging de advertencias.

    Args:
        mensaje (str): Mensaje de advertencia
        detalles (str, optional): Detalles adicionales
    """
    mensaje_completo = f"⚠️ {mensaje}"
    if detalles:
        mensaje_completo += f" - {detalles}"
    logger_sistema.warning(mensaje_completo)


def log_error(mensaje: str, detalles: str = None, excepcion: Exception = None):
    """
    Helper para logging de errores.

    Args:
        mensaje (str): Mensaje de error
        detalles (str, optional): Detalles adicionales
        excepcion (Exception, optional): Excepción capturada
    """
    mensaje_completo = f"❌ {mensaje}"
    if detalles:
        mensaje_completo += f" - {detalles}"

    if excepcion:
        logger_sistema.error(mensaje_completo, exc_info=True)
    else:
        logger_sistema.error(mensaje_completo)


# Ejemplos de uso del sistema de logging
if __name__ == "__main__":
    """
    Ejemplos prácticos de cómo usar el sistema de logging.
    """
    print("🧠 DEMOSTRANDO SISTEMA DE LOGGING")
    print("=" * 50)

    # Logger básico
    logger = obtener_logger("demo")

    # Diferentes niveles de logging
    logger.info("✅ Esta es información general")
    logger.warning("⚠️ Esta es una advertencia")
    logger.error("❌ Este es un error")

    # Usando helpers
    log_inicio_operacion("Crear usuario", "Juan Pérez")
    log_exito_operacion("Usuario creado", "ID: 12345")
    log_advertencia("Email ya existe", "juan@empresa.com")

    # Error con excepción
    try:
        resultado = 10 / 0
    except ZeroDivisionError as e:
        log_error("Error en cálculo", "División por cero", e)

    print("\n📁 Revisa el archivo: logs/sistema_tareas.log")
    print("🎉 Demo de logging completada")


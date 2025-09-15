"""
Utilidades para el CLI interactivo del sistema de gestión de tareas.

Este módulo contiene funciones helper para manejar entrada de usuario,
validación, formateo y navegación en el CLI.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Any, List, Optional

from colorama import Back, Fore, Style, init

# Inicializar colorama para colores en terminal
init(autoreset=True)


class CLIColors:
    """Colores y estilos para el CLI."""

    # Colores principales
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT

    # Colores para datos
    USER = Fore.MAGENTA
    TASK = Fore.GREEN
    DATE = Fore.YELLOW
    NUMBER = Fore.CYAN

    # Estilos
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL


def limpiar_pantalla():
    """Limpia la pantalla del terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución hasta que el usuario presione ENTER."""
    input(f"\n{CLIColors.INFO}Presiona ENTER para continuar...{CLIColors.RESET}")


def mostrar_titulo(titulo: str):
    """
    Muestra un título formateado en el CLI.

    Args:
        titulo (str): Título a mostrar
    """
    print(f"\n{CLIColors.HEADER}{'=' * 60}")
    print(f"{titulo.center(60)}")
    print(f"{'=' * 60}{CLIColors.RESET}")


def mostrar_subtitulo(subtitulo: str):
    """
    Muestra un subtítulo formateado en el CLI.

    Args:
        subtitulo (str): Subtítulo a mostrar
    """
    print(f"\n{CLIColors.HEADER}{subtitulo}")
    print(f"{'─' * len(subtitulo)}{CLIColors.RESET}")


def mostrar_exito(mensaje: str):
    """
    Muestra un mensaje de éxito.

    Args:
        mensaje (str): Mensaje de éxito
    """
    print(f"\n{CLIColors.SUCCESS}✅ {mensaje}{CLIColors.RESET}")


def mostrar_error(mensaje: str):
    """
    Muestra un mensaje de error.

    Args:
        mensaje (str): Mensaje de error
    """
    print(f"\n{CLIColors.ERROR}❌ {mensaje}{CLIColors.RESET}")


def mostrar_advertencia(mensaje: str):
    """
    Muestra un mensaje de advertencia.

    Args:
        mensaje (str): Mensaje de advertencia
    """
    print(f"\n{CLIColors.WARNING}⚠️ {mensaje}{CLIColors.RESET}")


def mostrar_info(mensaje: str):
    """
    Muestra un mensaje informativo.

    Args:
        mensaje (str): Mensaje informativo
    """
    print(f"\n{CLIColors.INFO}ℹ️ {mensaje}{CLIColors.RESET}")


def solicitar_entrada(prompt: str, valor_por_defecto: str = None) -> str:
    """
    Solicita entrada del usuario con validación básica.

    Args:
        prompt (str): Mensaje de solicitud
        valor_por_defecto (str, optional): Valor por defecto si está vacío

    Returns:
        str: Valor ingresado por el usuario
    """
    if valor_por_defecto:
        entrada = input(
            f"{CLIColors.INFO}{prompt} [{valor_por_defecto}]: {CLIColors.RESET}"
        )
        return entrada.strip() if entrada.strip() else valor_por_defecto
    else:
        entrada = input(f"{CLIColors.INFO}{prompt}: {CLIColors.RESET}")
        return entrada.strip()


def solicitar_entrada_requerida(prompt: str) -> str:
    """
    Solicita entrada del usuario que no puede estar vacía.

    Args:
        prompt (str): Mensaje de solicitud

    Returns:
        str: Valor ingresado por el usuario
    """
    while True:
        entrada = input(f"{CLIColors.INFO}{prompt}: {CLIColors.RESET}").strip()
        if entrada:
            return entrada
        mostrar_error("Este campo no puede estar vacío. Intenta nuevamente.")


def solicitar_numero(prompt: str, minimo: int = 1, maximo: int = None) -> int:
    """
    Solicita un número del usuario con validación.

    Args:
        prompt (str): Mensaje de solicitud
        minimo (int): Valor mínimo permitido
        maximo (int, optional): Valor máximo permitido

    Returns:
        int: Número ingresado por el usuario
    """
    while True:
        try:
            entrada = input(f"{CLIColors.INFO}{prompt}: {CLIColors.RESET}")
            numero = int(entrada)

            if numero < minimo:
                mostrar_error(f"El número debe ser mayor o igual a {minimo}")
                continue

            if maximo and numero > maximo:
                mostrar_error(f"El número debe ser menor o igual a {maximo}")
                continue

            return numero

        except ValueError:
            mostrar_error("Por favor ingresa un número válido")


def solicitar_fecha(prompt: str, permitir_vacia: bool = False) -> Optional[datetime]:
    """
    Solicita una fecha del usuario con validación.

    Args:
        prompt (str): Mensaje de solicitud
        permitir_vacia (bool): Si permite entrada vacía

    Returns:
        datetime: Fecha ingresada por el usuario
    """
    print(
        f"\n{CLIColors.INFO}Formato de fecha: DD/MM/YYYY (ej: 25/12/2025){CLIColors.RESET}"
    )

    while True:
        entrada = input(f"{CLIColors.INFO}{prompt}: {CLIColors.RESET}").strip()

        if not entrada and permitir_vacia:
            return None

        if not entrada:
            mostrar_error("Este campo es requerido. Intenta nuevamente.")
            continue

        try:
            # Intentar parsear la fecha
            fecha = datetime.strptime(entrada, "%d/%m/%Y")

            # Validar que la fecha sea futura (para fechas límite) solo si no permite vacía
            if not permitir_vacia and fecha.date() <= datetime.now().date():
                mostrar_error("La fecha debe ser futura")
                continue

            return fecha

        except ValueError:
            mostrar_error("Formato de fecha inválido. Usa DD/MM/YYYY")


def confirmar_accion(mensaje: str) -> bool:
    """
    Solicita confirmación del usuario para una acción.

    Args:
        mensaje (str): Mensaje de confirmación

    Returns:
        bool: True si confirma, False si no
    """
    while True:
        respuesta = (
            input(f"{CLIColors.WARNING}{mensaje} (s/n): {CLIColors.RESET}")
            .strip()
            .lower()
        )
        if respuesta in ["s", "sí", "si", "y", "yes"]:
            return True
        elif respuesta in ["n", "no"]:
            return False
        else:
            mostrar_error("Por favor responde 's' para sí o 'n' para no")


def mostrar_menu_opciones(opciones: List[str], titulo: str = "OPCIONES") -> int:
    """
    Muestra un menú de opciones y solicita selección.

    Args:
        opciones (List[str]): Lista de opciones
        titulo (str): Título del menú

    Returns:
        int: Número de opción seleccionada (1-indexed)
    """
    mostrar_subtitulo(titulo)

    for i, opcion in enumerate(opciones, 1):
        print(f"{CLIColors.NUMBER}{i}.{CLIColors.RESET} {opcion}")

    return solicitar_numero(f"\nSelecciona una opción", minimo=1, maximo=len(opciones))


def formatear_fecha_legible(fecha: datetime) -> str:
    """
    Formatea una fecha en formato legible.

    Args:
        fecha (datetime): Fecha a formatear

    Returns:
        str: Fecha formateada legiblemente
    """
    meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    return f"{fecha.day} de {meses[fecha.month]} de {fecha.year}"


def calcular_dias_restantes(fecha_limite: datetime) -> tuple:
    """
    Calcula los días restantes hasta una fecha límite.

    Args:
        fecha_limite (datetime): Fecha límite

    Returns:
        tuple: (días_restantes, es_critica, mensaje_color)
    """
    ahora = datetime.now()
    diferencia = fecha_limite - ahora
    dias = diferencia.days

    if dias < 0:
        return dias, True, CLIColors.ERROR  # Vencida
    elif dias <= 3:
        return dias, True, CLIColors.WARNING  # Crítica
    else:
        return dias, False, CLIColors.SUCCESS  # Normal


def mostrar_estadisticas_sistema(stats: dict):
    """
    Muestra las estadísticas del sistema de forma visual.

    Args:
        stats (dict): Diccionario con estadísticas
    """
    print(f"\n{CLIColors.HEADER}📊 Estado actual del sistema:")
    print(f"{CLIColors.USER}• Usuarios: {stats.get('total_usuarios', 0)}")
    print(f"{CLIColors.TASK}• Tareas totales: {stats.get('total_tareas', 0)}")

    pendientes = stats.get("tareas_pendientes", 0)
    progreso = stats.get("tareas_en_progreso", 0)
    completadas = stats.get("tareas_completadas", 0)

    print(f"{CLIColors.WARNING}• Pendientes: {pendientes} | ", end="")
    print(f"{CLIColors.INFO}En progreso: {progreso} | ", end="")
    print(f"{CLIColors.SUCCESS}Completadas: {completadas}")
    print(f"{CLIColors.RESET}")


def manejar_error_sistema(error: Exception):
    """
    Maneja errores del sistema de forma elegante.

    Args:
        error (Exception): Error capturado
    """
    mostrar_error(f"Error del sistema: {str(error)}")
    print(
        f"\n{CLIColors.INFO}Si el error persiste, contacta al administrador del sistema.{CLIColors.RESET}"
    )
    pausar()


def salir_sistema(gestor=None):
    """Función para salir del sistema de forma elegante."""
    limpiar_pantalla()
    mostrar_titulo("¡Hasta pronto!")

    # Auto-guardado antes de salir
    if gestor:
        try:
            print(
                f"{CLIColors.INFO}💾 Guardando cambios automáticamente...{CLIColors.RESET}"
            )
            if gestor.guardar_datos_sistema("json"):
                print(
                    f"{CLIColors.SUCCESS}✅ Datos guardados exitosamente{CLIColors.RESET}"
                )
            else:
                print(
                    f"{CLIColors.WARNING}⚠️ No se pudieron guardar algunos datos{CLIColors.RESET}"
                )
        except Exception as e:
            print(f"{CLIColors.ERROR}❌ Error al guardar: {str(e)}{CLIColors.RESET}")
            respuesta = input(
                f"{CLIColors.WARNING}¿Salir sin guardar? (s/N): {CLIColors.RESET}"
            )
            if respuesta.lower() != "s":
                return False  # No salir

    print(
        f"\n{CLIColors.SUCCESS}✅ Gracias por usar el Sistema de Gestión de Tareas{CLIColors.RESET}"
    )
    print(f"{CLIColors.INFO}Desarrollado por: Carlos Bermúdez{CLIColors.RESET}")
    sys.exit(0)


def mostrar_encabezado_principal():
    """Muestra el encabezado principal del sistema."""
    limpiar_pantalla()
    print(f"{CLIColors.HEADER}")
    print("🎯 SISTEMA DE GESTIÓN DE TAREAS v1.0")
    print("==========================================")
    print(f"{CLIColors.INFO}Desarrollado por: Carlos Bermúdez{CLIColors.RESET}")


def mostrar_tabla_tareas(tareas: List[Any]):
    """
    Muestra una tabla de tareas formateada.

    Args:
        tareas (List[Any]): Lista de tareas a mostrar
    """
    if not tareas:
        mostrar_info("No hay tareas para mostrar")
        return

    print(f"\n{CLIColors.HEADER}📋 LISTA DE TAREAS:{CLIColors.RESET}")
    print(f"{CLIColors.HEADER}{'─' * 80}{CLIColors.RESET}")

    for i, tarea in enumerate(tareas, 1):
        # Estado con color (manejar tanto string como Enum)
        estado_valor = (
            tarea.estado.value if hasattr(tarea.estado, "value") else tarea.estado
        )

        if estado_valor == "completada":
            estado_color = CLIColors.SUCCESS + "✅"
        elif estado_valor == "en_progreso":
            estado_color = CLIColors.WARNING + "⏳"
        else:
            estado_color = CLIColors.INFO + "📋"

        # Prioridad con color (manejar tanto string como atributo)
        prioridad_valor = tarea.prioridad if hasattr(tarea, "prioridad") else "baja"

        if prioridad_valor == "alta":
            prioridad_color = CLIColors.ERROR + "🔴 Alta"
        elif prioridad_valor == "media":
            prioridad_color = CLIColors.WARNING + "🟡 Media"
        else:
            prioridad_color = CLIColors.SUCCESS + "🟢 Baja"

        print(
            f"{CLIColors.NUMBER}{i:2}.{CLIColors.RESET} {estado_color} {tarea.titulo[:40]:40} {prioridad_color}{CLIColors.RESET}"
        )
        if tarea.fecha_limite:
            dias, es_critica, color = calcular_dias_restantes(tarea.fecha_limite)
            if dias >= 0:
                print(f"    📅 Vence en {color}{dias} días{CLIColors.RESET}")
            else:
                print(f"    📅 {color}Vencida hace {abs(dias)} días{CLIColors.RESET}")
        print()


def mostrar_tabla_usuarios(usuarios: List[Any]):
    """
    Muestra una tabla de usuarios formateada.

    Args:
        usuarios (List[Any]): Lista de usuarios a mostrar
    """
    if not usuarios:
        mostrar_info("No hay usuarios para mostrar")
        return

    print(f"\n{CLIColors.HEADER}👥 LISTA DE USUARIOS:{CLIColors.RESET}")
    print(f"{CLIColors.HEADER}{'─' * 60}{CLIColors.RESET}")

    for i, usuario in enumerate(usuarios, 1):
        print(
            f"{CLIColors.NUMBER}{i:2}.{CLIColors.RESET} {CLIColors.USER}{usuario.nombre:25}{CLIColors.RESET} {CLIColors.INFO}({usuario.email}){CLIColors.RESET}"
        )
        print(f"    📧 {usuario.email}")
        print(f"    📱 {usuario.telefono or 'No especificado'}")
        print()

"""
Sistema de Validación Mejorado para el Sistema de Gestión de Tareas.

Este módulo proporciona validaciones robustas para garantizar la integridad
de los datos antes de que sean procesados o guardados en el sistema.
"""

import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class TipoError(Enum):
    """Tipos de errores de validación."""

    CAMPO_REQUERIDO = "campo_requerido"
    FORMATO_INVALIDO = "formato_invalido"
    VALOR_FUERA_RANGO = "valor_fuera_rango"
    REFERENCIA_INEXISTENTE = "referencia_inexistente"
    DUPLICADO = "duplicado"
    LOGICA_NEGOCIO = "logica_negocio"


class ResultadoValidacion:
    """Resultado de una operación de validación."""

    def __init__(self):
        self.es_valido = True
        self.errores: List[str] = []
        self.advertencias: List[str] = []

    def agregar_error(self, mensaje: str, tipo: TipoError = TipoError.FORMATO_INVALIDO):
        """Agrega un error de validación."""
        self.es_valido = False
        self.errores.append(f"❌ {mensaje}")

    def agregar_advertencia(self, mensaje: str):
        """Agrega una advertencia."""
        self.advertencias.append(f"⚠️ {mensaje}")


class ValidadorDatos:
    """
    Sistema de validación centralizado para todos los datos del sistema.
    """

    # Patrones de validación
    PATRON_EMAIL = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    PATRON_TELEFONO = re.compile(r"^\+?[\d\s\-\(\)]{10,20}$")

    @staticmethod
    def validar_usuario(
        data: Dict[str, Any], usuarios_existentes: List = None
    ) -> ResultadoValidacion:
        """
        Valida los datos de un usuario.

        Args:
            data (dict): Diccionario con datos del usuario
            usuarios_existentes (list): Lista de usuarios existentes para validar duplicados

        Returns:
            ResultadoValidacion: Resultado de la validación
        """
        resultado = ResultadoValidacion()
        usuarios_existentes = usuarios_existentes or []

        # Validar nombre
        nombre = data.get("nombre", "").strip()
        if not nombre:
            resultado.agregar_error("El nombre es requerido", TipoError.CAMPO_REQUERIDO)
        elif len(nombre) < 2:
            resultado.agregar_error("El nombre debe tener al menos 2 caracteres")
        elif len(nombre) > 100:
            resultado.agregar_error("El nombre no puede tener más de 100 caracteres")

        # Validar email
        email = data.get("email", "").strip().lower()
        if not email:
            resultado.agregar_error("El email es requerido", TipoError.CAMPO_REQUERIDO)
        elif not ValidadorDatos.PATRON_EMAIL.match(email):
            resultado.agregar_error(
                "Formato de email inválido", TipoError.FORMATO_INVALIDO
            )
        else:
            # Validar email único
            for usuario in usuarios_existentes:
                if hasattr(usuario, "email") and usuario.email.lower() == email:
                    resultado.agregar_error(
                        "Ya existe un usuario con este email", TipoError.DUPLICADO
                    )
                    break

        # Validar teléfono (opcional)
        telefono = data.get("telefono", "").strip()
        if telefono and not ValidadorDatos.PATRON_TELEFONO.match(telefono):
            resultado.agregar_error("Formato de teléfono inválido")

        # Validar ID (para datos cargados)
        if "id" in data:
            id_usuario = data.get("id", "").strip()
            if not id_usuario:
                resultado.agregar_error("ID de usuario no puede estar vacío")

        return resultado

    @staticmethod
    def validar_tarea(
        data: Dict[str, Any],
        usuarios_existentes: List = None,
        tareas_existentes: List = None,
    ) -> ResultadoValidacion:
        """
        Valida los datos de una tarea.

        Args:
            data (dict): Diccionario con datos de la tarea
            usuarios_existentes (list): Lista de usuarios para validar asignaciones
            tareas_existentes (list): Lista de tareas existentes

        Returns:
            ResultadoValidacion: Resultado de la validación
        """
        resultado = ResultadoValidacion()
        usuarios_existentes = usuarios_existentes or []
        tareas_existentes = tareas_existentes or []

        # Validar título
        titulo = data.get("titulo", "").strip()
        if not titulo:
            resultado.agregar_error("El título es requerido", TipoError.CAMPO_REQUERIDO)
        elif len(titulo) < 3:
            resultado.agregar_error("El título debe tener al menos 3 caracteres")
        elif len(titulo) > 200:
            resultado.agregar_error("El título no puede tener más de 200 caracteres")

        # Validar descripción (opcional)
        descripcion = data.get("descripcion", "").strip()
        if descripcion and len(descripcion) > 1000:
            resultado.agregar_error(
                "La descripción no puede tener más de 1000 caracteres"
            )

        # Validar estado
        estado = data.get("estado", "pendiente")
        estados_validos = ["pendiente", "en_progreso", "completada"]
        if estado not in estados_validos:
            resultado.agregar_error(
                f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
            )

        # Validar prioridad
        prioridad = data.get("prioridad", "baja")
        prioridades_validas = ["baja", "media", "alta"]
        if prioridad not in prioridades_validas:
            resultado.agregar_error(
                f"Prioridad inválida. Debe ser una de: {', '.join(prioridades_validas)}"
            )

        # Validar fechas
        try:
            if data.get("fecha_creacion"):
                fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
                if fecha_creacion > datetime.now():
                    resultado.agregar_advertencia("La fecha de creación es futura")
        except (ValueError, TypeError):
            resultado.agregar_error("Formato de fecha de creación inválido")

        try:
            if data.get("fecha_limite"):
                fecha_limite = datetime.fromisoformat(data["fecha_limite"])
                # Para datos cargados, solo advertir sobre fechas pasadas
                if fecha_limite < datetime.now():
                    resultado.agregar_advertencia("La fecha límite está en el pasado")
        except (ValueError, TypeError):
            resultado.agregar_error("Formato de fecha límite inválido")

        # Validar usuario asignado
        usuario_id = data.get("usuario_id")
        if usuario_id:
            usuario_encontrado = False
            for usuario in usuarios_existentes:
                if hasattr(usuario, "id") and usuario.id == usuario_id:
                    usuario_encontrado = True
                    break

            if not usuario_encontrado:
                resultado.agregar_advertencia(
                    f"Usuario asignado no encontrado: {usuario_id}"
                )

        return resultado

    @staticmethod
    def validar_integridad_sistema(usuarios: List, tareas: List) -> ResultadoValidacion:
        """
        Valida la integridad general del sistema.

        Args:
            usuarios (list): Lista de usuarios
            tareas (list): Lista de tareas

        Returns:
            ResultadoValidacion: Resultado de la validación de integridad
        """
        resultado = ResultadoValidacion()

        # Validar que no hay usuarios duplicados
        emails_usuarios = {}
        for usuario in usuarios:
            if hasattr(usuario, "email"):
                email_lower = usuario.email.lower()
                if email_lower in emails_usuarios:
                    resultado.agregar_error(f"Email duplicado: {usuario.email}")
                emails_usuarios[email_lower] = usuario

        # Validar referencias de usuario en tareas
        ids_usuarios = {u.id for u in usuarios if hasattr(u, "id")}
        for tarea in tareas:
            if hasattr(tarea, "usuario_id") and tarea.usuario_id:
                if tarea.usuario_id not in ids_usuarios:
                    resultado.agregar_advertencia(
                        f"Tarea '{tarea.titulo}' referencia usuario inexistente"
                    )

        # Estadísticas para detectar anomalías
        if len(tareas) > 0:
            tareas_sin_usuario = [
                t for t in tareas if not hasattr(t, "usuario_id") or not t.usuario_id
            ]
            if len(tareas_sin_usuario) > len(tareas) * 0.5:  # Más del 50% sin asignar
                resultado.agregar_advertencia(
                    f"{len(tareas_sin_usuario)} tareas sin usuario asignado"
                )

        # Detectar usuarios con demasiadas tareas
        if len(usuarios) > 0 and len(tareas) > 10:
            conteo_tareas = {}
            for tarea in tareas:
                if hasattr(tarea, "usuario_id") and tarea.usuario_id:
                    conteo_tareas[tarea.usuario_id] = (
                        conteo_tareas.get(tarea.usuario_id, 0) + 1
                    )

            max_tareas = max(conteo_tareas.values()) if conteo_tareas else 0
            promedio_tareas = len(tareas) / len(usuarios)

            if max_tareas > promedio_tareas * 3:  # Un usuario tiene 3x el promedio
                resultado.agregar_advertencia(
                    "Distribución desigual de tareas detectada"
                )

        return resultado

    @staticmethod
    def validar_antes_de_guardar(usuarios: List, tareas: List) -> ResultadoValidacion:
        """
        Validación completa antes de guardar datos.

        Args:
            usuarios (list): Lista de usuarios
            tareas (list): Lista de tareas

        Returns:
            ResultadoValidacion: Resultado de todas las validaciones
        """
        resultado = ResultadoValidacion()

        # Validar integridad general
        integridad = ValidadorDatos.validar_integridad_sistema(usuarios, tareas)
        resultado.errores.extend(integridad.errores)
        resultado.advertencias.extend(integridad.advertencias)

        if integridad.errores:
            resultado.es_valido = False

        # Validar que los datos se pueden serializar
        try:
            import json

            datos_prueba = {
                "usuarios": [
                    u.to_dict() if hasattr(u, "to_dict") else str(u)
                    for u in usuarios[:1]
                ],
                "tareas": [
                    t.to_dict() if hasattr(t, "to_dict") else str(t) for t in tareas[:1]
                ],
            }
            json.dumps(datos_prueba, default=str)
        except Exception as e:
            resultado.agregar_error(f"Los datos no se pueden serializar: {str(e)}")

        return resultado


def mostrar_resultado_validacion(
    resultado: ResultadoValidacion, titulo: str = "Validación"
) -> None:
    """
    Muestra el resultado de una validación de forma formateada.

    Args:
        resultado (ResultadoValidacion): Resultado a mostrar
        titulo (str): Título de la validación
    """
    from colorama import Fore, Style

    print(f"\n{Fore.CYAN + Style.BRIGHT}🔍 {titulo}:{Style.RESET_ALL}")

    if resultado.es_valido:
        print(f"{Fore.GREEN}✅ Validación exitosa{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Validación falló{Style.RESET_ALL}")

    # Mostrar errores
    if resultado.errores:
        print(f"\n{Fore.RED + Style.BRIGHT}Errores encontrados:{Style.RESET_ALL}")
        for error in resultado.errores:
            print(f"  {error}")

    # Mostrar advertencias
    if resultado.advertencias:
        print(f"\n{Fore.YELLOW + Style.BRIGHT}Advertencias:{Style.RESET_ALL}")
        for advertencia in resultado.advertencias:
            print(f"  {advertencia}")

    if not resultado.errores and not resultado.advertencias:
        print(f"{Fore.GREEN}✨ Todo perfecto{Style.RESET_ALL}")

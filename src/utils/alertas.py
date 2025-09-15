"""
Sistema de Alertas Proactivo para el Sistema de Gestión de Tareas.

Este módulo proporciona funcionalidades para generar alertas inteligentes
que mantienen al usuario informado sobre el estado crítico del sistema.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List

from colorama import Fore, Style


class SistemaAlertas:
    """
    Sistema de alertas proactivo que analiza el estado del sistema
    y genera notificaciones relevantes para el usuario.
    """

    @staticmethod
    def generar_alertas(gestor) -> List[str]:
        """
        Genera lista de alertas basadas en el estado actual del sistema.

        Args:
            gestor: Instancia del GestorSistema

        Returns:
            List[str]: Lista de mensajes de alerta formateados
        """
        alertas = []

        # 1. Tareas vencidas
        tareas_vencidas = [
            t
            for t in gestor.tareas
            if t.esta_vencida() and t.estado.value != "completada"
        ]
        if tareas_vencidas:
            alertas.append(
                f"{Fore.RED + Style.BRIGHT}🚨 {len(tareas_vencidas)} tareas VENCIDAS requieren atención{Style.RESET_ALL}"
            )

        # 2. Tareas próximas a vencer (próximas 48 horas)
        proximas_48h = SistemaAlertas._obtener_tareas_proximas(gestor.tareas, 2)
        if proximas_48h:
            alertas.append(
                f"{Fore.YELLOW + Style.BRIGHT}⚠️ {len(proximas_48h)} tareas vencen en las próximas 48h{Style.RESET_ALL}"
            )

        # 3. Usuarios sin tareas asignadas
        usuarios_sin_tareas = SistemaAlertas._obtener_usuarios_inactivos(
            gestor.usuarios, gestor.tareas
        )
        if usuarios_sin_tareas:
            alertas.append(
                f"{Fore.BLUE + Style.BRIGHT}📋 {len(usuarios_sin_tareas)} usuarios sin tareas asignadas{Style.RESET_ALL}"
            )

        # 4. Distribución desigual de tareas (usuario con >50% de las tareas)
        sobrecargado = SistemaAlertas._detectar_sobrecarga_usuarios(
            gestor.usuarios, gestor.tareas
        )
        if sobrecargado:
            alertas.append(
                f"{Fore.MAGENTA + Style.BRIGHT}⚖️ Usuario sobrecargado: {sobrecargado} con muchas tareas{Style.RESET_ALL}"
            )

        # 5. Muchas tareas en progreso simultáneamente
        en_progreso = [t for t in gestor.tareas if t.estado.value == "en_progreso"]
        if len(en_progreso) > 10:
            alertas.append(
                f"{Fore.CYAN + Style.BRIGHT}🔄 {len(en_progreso)} tareas en progreso - ¿demasiadas simultáneas?{Style.RESET_ALL}"
            )

        return alertas

    @staticmethod
    def mostrar_alertas_formateadas(alertas: List[str]) -> None:
        """
        Muestra las alertas de forma formateada en el CLI.

        Args:
            alertas (List[str]): Lista de mensajes de alerta
        """
        if alertas:
            print(
                f"\n{Fore.YELLOW + Style.BRIGHT}🔔 ALERTAS DEL SISTEMA:{Style.RESET_ALL}"
            )
            print(f"{Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
            for alerta in alertas:
                print(f"  • {alerta}")
        else:
            print(
                f"\n{Fore.GREEN + Style.BRIGHT}✅ Sin alertas - Sistema bajo control{Style.RESET_ALL}"
            )

    @staticmethod
    def _obtener_tareas_proximas(tareas, dias: int) -> List:
        """Obtiene tareas que vencen en los próximos N días."""
        fecha_limite = datetime.now() + timedelta(days=dias)
        return [
            t
            for t in tareas
            if t.fecha_limite
            and t.fecha_limite <= fecha_limite
            and not t.esta_vencida()
            and t.estado.value != "completada"
        ]

    @staticmethod
    def _obtener_usuarios_inactivos(usuarios, tareas) -> List:
        """Obtiene usuarios sin tareas asignadas."""
        usuarios_con_tareas = {t.usuario_id for t in tareas if t.usuario_id}
        return [u for u in usuarios if u.id not in usuarios_con_tareas]

    @staticmethod
    def _detectar_sobrecarga_usuarios(usuarios, tareas) -> str:
        """Detecta si un usuario tiene demasiadas tareas."""
        if not tareas or not usuarios:
            return ""

        # Contar tareas por usuario
        conteo_tareas = {}
        for tarea in tareas:
            if tarea.usuario_id and tarea.estado.value != "completada":
                conteo_tareas[tarea.usuario_id] = (
                    conteo_tareas.get(tarea.usuario_id, 0) + 1
                )

        if not conteo_tareas:
            return ""

        # Encontrar usuario con más tareas
        usuario_sobrecargado = max(conteo_tareas.items(), key=lambda x: x[1])
        total_tareas_activas = sum(conteo_tareas.values())

        # Si un usuario tiene más del 40% de las tareas activas
        if (
            usuario_sobrecargado[1] / total_tareas_activas > 0.4
            and usuario_sobrecargado[1] > 5
        ):
            # Buscar nombre del usuario
            for usuario in usuarios:
                if usuario.id == usuario_sobrecargado[0]:
                    return (
                        f"{usuario.nombre} ({usuario_sobrecargado[1]} tareas activas)"
                    )

        return ""


def mostrar_dashboard_alertas(gestor) -> None:
    """
    Función de conveniencia para mostrar el dashboard completo de alertas.

    Args:
        gestor: Instancia del GestorSistema
    """
    alertas = SistemaAlertas.generar_alertas(gestor)
    SistemaAlertas.mostrar_alertas_formateadas(alertas)


def obtener_alertas_criticas(gestor) -> int:
    """
    Obtiene el número de alertas críticas (solo vencidas).

    Args:
        gestor: Instancia del GestorSistema

    Returns:
        int: Número de alertas críticas
    """
    tareas_vencidas = [
        t for t in gestor.tareas if t.esta_vencida() and t.estado.value != "completada"
    ]
    return len(tareas_vencidas)

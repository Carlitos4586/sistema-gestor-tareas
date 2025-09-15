"""
Menú principal del CLI interactivo para el sistema de gestión de tareas.

Este módulo contiene la lógica principal de navegación y el menú principal
que conecta todas las funcionalidades del sistema.
"""

from typing import Optional

# Importaciones usando try/except para manejar diferentes contextos
try:
    from ..services.gestor_sistema import GestorSistema
    from .cli_utils import (
        manejar_error_sistema,
        mostrar_encabezado_principal,
        mostrar_estadisticas_sistema,
        mostrar_menu_opciones,
        mostrar_subtitulo,
        mostrar_titulo,
        pausar,
        salir_sistema,
    )
except ImportError:
    from cli.cli_utils import (
        manejar_error_sistema,
        mostrar_encabezado_principal,
        mostrar_estadisticas_sistema,
        mostrar_menu_opciones,
        mostrar_subtitulo,
        mostrar_titulo,
        pausar,
        salir_sistema,
    )
    from services.gestor_sistema import GestorSistema


class MenuPrincipal:
    """
    Clase que maneja el menú principal del CLI interactivo.
    """

    def __init__(self):
        """Inicializa el menú principal con el gestor del sistema."""
        try:
            self.gestor = GestorSistema()
        except Exception as e:
            manejar_error_sistema(e)

    def ejecutar(self):
        """
        Ejecuta el bucle principal del menú.
        """
        while True:
            try:
                self.mostrar_menu_principal()

            except KeyboardInterrupt:
                print("\n")
                salir_sistema(self.gestor)
            except Exception as e:
                manejar_error_sistema(e)

    def mostrar_menu_principal(self):
        """
        Muestra el menú principal y maneja la selección del usuario.
        """
        # Mostrar encabezado
        mostrar_encabezado_principal()

        # Obtener estadísticas actuales
        try:
            stats = self.gestor.obtener_estadisticas_sistema()
            mostrar_estadisticas_sistema(stats)

            # 🆕 MOSTRAR ALERTAS PROACTIVAS
            from ..utils.alertas import mostrar_dashboard_alertas

            mostrar_dashboard_alertas(self.gestor)
        except ImportError:
            # Fallback si no se puede importar el sistema de alertas
            try:
                stats = self.gestor.obtener_estadisticas_sistema()
                mostrar_estadisticas_sistema(stats)
            except Exception as e:
                print(f"Error al obtener estadísticas: {e}")
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")

        # Opciones del menú principal
        opciones = [
            "👥 Gestión de Usuarios",
            "📋 Gestión de Tareas",
            "📊 Reportes y Estadísticas",
            "🔍 Búsquedas y Filtros",
            "⚙️ Configuración del Sistema",
            "🚪 Salir",
        ]

        mostrar_titulo("MENÚ PRINCIPAL")
        seleccion = mostrar_menu_opciones(opciones)

        # Procesar selección
        if seleccion == 1:
            self.ir_gestion_usuarios()
        elif seleccion == 2:
            self.ir_gestion_tareas()
        elif seleccion == 3:
            self.ir_reportes()
        elif seleccion == 4:
            self.ir_busquedas()
        elif seleccion == 5:
            self.ir_configuracion()
        elif seleccion == 6:
            salir_sistema(self.gestor)

    def ir_gestion_usuarios(self):
        """Navega al menú de gestión de usuarios."""
        try:
            try:
                from .menu_usuarios import MenuUsuarios
            except ImportError:
                from cli.menu_usuarios import MenuUsuarios
            menu_usuarios = MenuUsuarios(self.gestor)
            menu_usuarios.mostrar_menu()
        except ImportError:
            print("⚠️ Módulo de gestión de usuarios aún no implementado")
            pausar()
        except Exception as e:
            manejar_error_sistema(e)

    def ir_gestion_tareas(self):
        """Navega al menú de gestión de tareas."""
        try:
            try:
                from .menu_tareas import MenuTareas
            except ImportError:
                from cli.menu_tareas import MenuTareas
            menu_tareas = MenuTareas(self.gestor)
            menu_tareas.mostrar_menu()
        except ImportError:
            print("⚠️ Módulo de gestión de tareas aún no implementado")
            pausar()
        except Exception as e:
            manejar_error_sistema(e)

    def ir_reportes(self):
        """Navega al menú de reportes."""
        try:
            try:
                from .menu_reportes import MenuReportes
            except ImportError:
                from cli.menu_reportes import MenuReportes
            menu_reportes = MenuReportes(self.gestor)
            menu_reportes.mostrar_menu()
        except ImportError:
            print("⚠️ Módulo de reportes aún no implementado")
            pausar()
        except Exception as e:
            manejar_error_sistema(e)

    def ir_busquedas(self):
        """Navega al menú de búsquedas."""
        try:
            try:
                from .menu_busquedas import MenuBusquedas
            except ImportError:
                from cli.menu_busquedas import MenuBusquedas
            menu_busquedas = MenuBusquedas(self.gestor)
            menu_busquedas.mostrar_menu()
        except ImportError:
            print("⚠️ Módulo de búsquedas aún no implementado")
            pausar()
        except Exception as e:
            manejar_error_sistema(e)

    def ir_configuracion(self):
        """Navega al menú de configuración."""
        try:
            try:
                from .menu_configuracion import MenuConfiguracion
            except ImportError:
                from cli.menu_configuracion import MenuConfiguracion
            menu_configuracion = MenuConfiguracion(self.gestor)
            menu_configuracion.mostrar_menu()
        except ImportError:
            print("⚠️ Módulo de configuración aún no implementado")
            pausar()
        except Exception as e:
            manejar_error_sistema(e)


def ejecutar_cli():
    """
    Función principal para ejecutar el CLI interactivo.
    """
    try:
        menu = MenuPrincipal()
        menu.ejecutar()
    except Exception as e:
        print(f"Error crítico al inicializar el sistema: {e}")
        exit(1)

#!/usr/bin/env python3
"""
Script principal para ejecutar el CLI interactivo del Sistema de Gestión de Tareas.

Este script sirve como punto de entrada principal desde el directorio raíz del proyecto.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importar los módulos
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from cli.menu_principal import ejecutar_cli

    def main():
        """
        Función principal del CLI.
        """
        try:
            print("🎯 Sistema de Gestión de Tareas v1.0")
            print("Desarrollado por: Carlos Bermúdez")
            print("=" * 50)
            ejecutar_cli()

        except KeyboardInterrupt:
            print("\n\n🚪 Programa interrumpido por el usuario.")
            from cli.cli_utils import salir_sistema

            # Intentar obtener el gestor para auto-guardar
            try:
                from services.gestor_sistema import GestorSistema

                gestor = GestorSistema()
                salir_sistema(gestor)
            except Exception:
                print("¡Hasta pronto!")
                sys.exit(0)

        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
            print("Si el error persiste, verifica la configuración del sistema.")
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de tener todas las dependencias instaladas.")
    print("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)

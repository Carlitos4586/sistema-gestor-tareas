"""
Punto de entrada principal del CLI interactivo.

Este módulo sirve como entrada principal para ejecutar la aplicación
de gestión de tareas desde línea de comandos.
"""

import sys
import os
from pathlib import Path
from menu_principal import ejecutar_cli


def main():
    """
    Función principal del CLI.
    """
    try:
        print("Iniciando Sistema de Gestión de Tareas...")
        print("-" * 50)
        ejecutar_cli()
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

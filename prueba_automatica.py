#!/usr/bin/env python3
"""
🤖 SISTEMA DE PRUEBA AUTOMÁTICA COMPLETA
Verifica que todas las funcionalidades del Sistema de Gestión de Tareas funcionan correctamente
Desarrollado por: Carlos
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Añadir src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


# Colores para output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_test_header(test_name):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}🧪 PRUEBA: {test_name}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")


def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.RESET}")


def print_info(message):
    print(f"{Colors.BLUE}ℹ️ {message}{Colors.RESET}")


class PruebaAutomatica:
    def __init__(self):
        self.errores = []
        self.exitos = 0
        self.total_pruebas = 0

    def ejecutar_todas_las_pruebas(self):
        """Ejecuta todas las pruebas automáticas del sistema"""
        print(
            f"{Colors.BOLD}{Colors.GREEN}🚀 INICIANDO PRUEBA AUTOMÁTICA COMPLETA{Colors.RESET}"
        )
        print(f"{Colors.BOLD}Proyecto: Sistema de Gestión de Tareas{Colors.RESET}")
        print(f"{Colors.BOLD}Desarrollado por: Carlos{Colors.RESET}")
        print(
            f"{Colors.BOLD}Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.RESET}"
        )

        # Lista de pruebas a ejecutar
        pruebas = [
            ("Importación de Módulos", self.probar_importaciones),
            ("Inicialización del Sistema", self.probar_inicializacion),
            ("Gestión de Usuarios", self.probar_gestion_usuarios),
            ("Gestión de Tareas", self.probar_gestion_tareas),
            ("Sistema de Reportes", self.probar_reportes),
            ("Búsquedas y Filtros", self.probar_busquedas),
            ("Persistencia de Datos", self.probar_persistencia),
        ]

        for nombre_prueba, metodo_prueba in pruebas:
            try:
                print_test_header(nombre_prueba)
                metodo_prueba()
                print_success(f"Prueba '{nombre_prueba}' COMPLETADA")
            except Exception as e:
                print_error(f"Error en prueba '{nombre_prueba}': {str(e)}")
                self.errores.append(f"{nombre_prueba}: {str(e)}")

        self.mostrar_resumen_final()

    def probar_importaciones(self):
        """Prueba que todos los módulos se importen correctamente"""
        self.total_pruebas += 1

        # Importaciones principales
        from models.tarea import EstadoTarea, Tarea
        from models.usuario import Usuario
        from services.gestor_sistema import GestorSistema
        from services.persistencia import GestorPersistencia
        from services.reportes import GeneradorReportes

        print_success("Módulos principales importados correctamente")

        # Dependencias externas
        import colorama
        import tabulate

        print_success("Dependencias externas (tabulate, colorama) disponibles")

        self.exitos += 1

    def probar_inicializacion(self):
        """Prueba la inicialización del sistema"""
        self.total_pruebas += 1

        from services.gestor_sistema import GestorSistema

        # Inicializar sistema
        self.gestor = GestorSistema()
        print_success("Sistema inicializado correctamente")

        # Verificar estadísticas iniciales
        stats = self.gestor.obtener_estadisticas_sistema()
        assert isinstance(stats, dict), "Las estadísticas deben ser un diccionario"
        assert len(stats) > 0, "Debe haber estadísticas disponibles"
        print_success(f"Estadísticas obtenidas: {len(stats)} métricas")

        self.exitos += 1

    def probar_gestion_usuarios(self):
        """Prueba la gestión completa de usuarios"""
        self.total_pruebas += 1

        # Crear usuarios de prueba
        usuarios_prueba = [
            {
                "nombre": "Carlos Bermúdez",
                "email": "carlos@empresa.com",
                "telefono": "555-0001",
                "departamento": "Desarrollo",
            },
            {
                "nombre": "Ana García",
                "email": "ana@empresa.com",
                "telefono": "555-0002",
                "departamento": "QA",
            },
            {
                "nombre": "Luis Rodríguez",
                "email": "luis@empresa.com",
                "telefono": "555-0003",
                "departamento": "DevOps",
            },
        ]

        usuarios_creados = []
        for datos in usuarios_prueba:
            usuario = self.gestor.crear_usuario(datos["nombre"], datos["email"])
            assert usuario is not None, f"No se pudo crear usuario {datos['nombre']}"
            usuarios_creados.append(usuario)
            print_success(f"Usuario creado: {datos['nombre']}")

        # Verificar usuarios creados (convertir generador a lista)
        usuarios_sistema = list(self.gestor.listar_usuarios_activos())
        assert (
            len(usuarios_sistema) == 3
        ), f"Esperados 3 usuarios, encontrados {len(usuarios_sistema)}"
        print_success(f"Total usuarios en sistema: {len(usuarios_sistema)}")

        # Buscar usuario por email
        usuario_encontrado = self.gestor.obtener_usuario_por_email("carlos@empresa.com")
        assert usuario_encontrado is not None, "Usuario no encontrado por email"
        assert (
            usuario_encontrado.nombre == "Carlos Bermúdez"
        ), "Nombre de usuario incorrecto"
        print_success("Búsqueda de usuario por email exitosa")

        self.exitos += 1

    def probar_gestion_tareas(self):
        """Prueba la gestión completa de tareas"""
        self.total_pruebas += 1

        from models.tarea import EstadoTarea

        # Obtener usuarios para asignar tareas (el método devuelve diccionarios)
        usuarios_dict = list(self.gestor.listar_usuarios_activos())
        assert len(usuarios_dict) > 0, "Debe haber usuarios para asignar tareas"

        # Extraer emails de los diccionarios
        emails_usuarios = [u["email"] for u in usuarios_dict]

        # Crear tareas de prueba
        tareas_prueba = [
            {
                "titulo": "Implementar autenticación",
                "descripcion": "Desarrollar sistema de login y registro",
                "fecha_limite": datetime.now() + timedelta(days=7),
                "usuario_id": usuarios[0].id,
                "prioridad": "alta",
            },
            {
                "titulo": "Testing de API",
                "descripcion": "Crear tests unitarios para endpoints",
                "fecha_limite": datetime.now() + timedelta(days=5),
                "usuario_id": usuarios[1].id,
                "prioridad": "media",
            },
            {
                "titulo": "Deploy en producción",
                "descripcion": "Configurar CI/CD pipeline",
                "fecha_limite": datetime.now() + timedelta(days=14),
                "usuario_id": usuarios[2].id,
                "prioridad": "baja",
            },
        ]

        tareas_creadas = []
        for i, datos in enumerate(tareas_prueba):
            tarea = self.gestor.crear_tarea(
                datos["titulo"],
                datos["descripcion"],
                datos["fecha_limite"],
                emails_usuarios[i],  # Usar email del diccionario
                datos["prioridad"],
            )
            assert tarea is not None, f"No se pudo crear tarea {datos['titulo']}"
            tareas_creadas.append(tarea)
            print_success(f"Tarea creada: {datos['titulo']}")

        # Verificar tareas creadas usando búsqueda
        todas_tareas = self.gestor.buscar_tareas(
            ""
        )  # Búsqueda vacía para obtener todas
        assert (
            len(todas_tareas) >= 3
        ), f"Esperadas al menos 3 tareas, encontradas {len(todas_tareas)}"
        print_success(f"Total tareas en sistema: {len(todas_tareas)}")

        # Cambiar estado de una tarea
        tarea_test = tareas_creadas[0]
        resultado = self.gestor.cambiar_estado_tarea(tarea_test.id, "en_progreso")
        assert resultado == True, "No se pudo actualizar estado de tarea"

        # Verificar cambio de estado
        tarea_actualizada = self.gestor.obtener_tarea_por_id(tarea_test.id)
        assert (
            tarea_actualizada.estado == EstadoTarea.EN_PROGRESO
        ), "Estado no actualizado correctamente"
        print_success("Actualización de estado de tarea exitosa")

        self.exitos += 1

    def probar_reportes(self):
        """Prueba el sistema de reportes"""
        self.total_pruebas += 1

        from services.reportes import GeneradorReportes

        reportes = GeneradorReportes()

        # Usar los reportes del gestor directamente
        reporte_usuarios = self.gestor.generar_reporte_usuarios()
        assert isinstance(reporte_usuarios, str), "El reporte debe ser una cadena"
        assert len(reporte_usuarios) > 0, "El reporte no debe estar vacío"
        print_success("Reporte de usuarios generado")

        # Reporte de tareas
        reporte_tareas = self.gestor.generar_reporte_tareas()
        assert isinstance(reporte_tareas, str), "El reporte debe ser una cadena"
        assert len(reporte_tareas) > 0, "El reporte no debe estar vacío"
        print_success("Reporte de tareas generado")

        # Dashboard ejecutivo
        dashboard = self.gestor.generar_dashboard_ejecutivo()
        assert isinstance(dashboard, str), "El dashboard debe ser una cadena"
        print_success("Dashboard ejecutivo generado")

        self.exitos += 1

    def probar_busquedas(self):
        """Prueba las funciones de búsqueda y filtrado"""
        self.total_pruebas += 1

        from models.tarea import EstadoTarea

        # Buscar tareas por estado
        tareas_pendientes = list(self.gestor.listar_tareas_por_estado("pendiente"))
        assert isinstance(tareas_pendientes, list), "Debe devolver una lista"
        print_success(
            f"Búsqueda por estado: {len(tareas_pendientes)} tareas pendientes"
        )

        # Buscar tareas por título
        tareas_auth = self.gestor.buscar_tareas("autenticación")
        assert isinstance(tareas_auth, list), "Debe devolver una lista"
        print_success(f"Búsqueda por título: {len(tareas_auth)} tareas encontradas")

        self.exitos += 1

    def probar_persistencia(self):
        """Prueba la persistencia de datos en JSON y binario"""
        self.total_pruebas += 1

        # Guardar datos en formato JSON
        resultado_json = self.gestor.guardar_datos_sistema("json")
        assert resultado_json == True, "No se pudieron guardar datos en JSON"
        print_success("Datos guardados en formato JSON")

        # Verificar que se crearon los archivos
        data_dir = Path("data/json")
        assert (data_dir / "usuarios.json").exists(), "Archivo usuarios.json no creado"
        assert (data_dir / "tareas.json").exists(), "Archivo tareas.json no creado"
        print_success("Archivos JSON verificados en disco")

        # Guardar datos en formato binario
        resultado_bin = self.gestor.guardar_datos_sistema("binario")
        assert resultado_bin == True, "No se pudieron guardar datos en binario"
        print_success("Datos guardados en formato binario")

        # Verificar archivos binarios
        data_dir_bin = Path("data/binarios")
        assert (
            data_dir_bin / "usuarios.pkl"
        ).exists(), "Archivo usuarios.pkl no creado"
        assert (data_dir_bin / "tareas.pkl").exists(), "Archivo tareas.pkl no creado"
        print_success("Archivos binarios verificados en disco")

        self.exitos += 1

    def mostrar_resumen_final(self):
        """Muestra el resumen final de todas las pruebas"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}")
        print(
            f"{Colors.BOLD}{Colors.BLUE}📊 RESUMEN FINAL DE PRUEBAS AUTOMÁTICAS{Colors.RESET}"
        )
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}")

        print(f"\n{Colors.BOLD}🎯 RESULTADOS:{Colors.RESET}")
        print(
            f"   • Total de pruebas ejecutadas: {Colors.BOLD}{self.total_pruebas}{Colors.RESET}"
        )
        print(
            f"   • Pruebas exitosas: {Colors.GREEN}{Colors.BOLD}{self.exitos}{Colors.RESET}"
        )
        print(
            f"   • Pruebas fallidas: {Colors.RED}{Colors.BOLD}{len(self.errores)}{Colors.RESET}"
        )

        if self.errores:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ ERRORES ENCONTRADOS:{Colors.RESET}")
            for i, error in enumerate(self.errores, 1):
                print(f"   {i}. {Colors.RED}{error}{Colors.RESET}")

        porcentaje_exito = (
            (self.exitos / self.total_pruebas * 100) if self.total_pruebas > 0 else 0
        )

        print(f"\n{Colors.BOLD}📈 PORCENTAJE DE ÉXITO: ", end="")
        if porcentaje_exito == 100:
            print(f"{Colors.GREEN}{porcentaje_exito:.1f}%{Colors.RESET}")
            print(
                f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡TODAS LAS PRUEBAS PASARON! SISTEMA COMPLETAMENTE FUNCIONAL{Colors.RESET}"
            )
        elif porcentaje_exito >= 80:
            print(f"{Colors.YELLOW}{porcentaje_exito:.1f}%{Colors.RESET}")
            print(
                f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ SISTEMA MAYORMENTE FUNCIONAL - Revisar errores menores{Colors.RESET}"
            )
        else:
            print(f"{Colors.RED}{porcentaje_exito:.1f}%{Colors.RESET}")
            print(
                f"\n{Colors.RED}{Colors.BOLD}🚨 SISTEMA REQUIERE CORRECCIONES - Múltiples errores detectados{Colors.RESET}"
            )

        print(f"\n{Colors.BOLD}🏆 CONCLUSIÓN:{Colors.RESET}")
        if porcentaje_exito == 100:
            print(
                f"   {Colors.GREEN}✅ El Sistema de Gestión de Tareas está LISTO PARA PRODUCCIÓN{Colors.RESET}"
            )
            print(
                f"   {Colors.GREEN}✅ Todas las funcionalidades principales operativas{Colors.RESET}"
            )
            print(f"   {Colors.GREEN}✅ Persistencia de datos verificada{Colors.RESET}")
            print(
                f"   {Colors.GREEN}✅ Integridad del sistema confirmada{Colors.RESET}"
            )
        else:
            print(
                f"   {Colors.YELLOW}⚠️ El sistema requiere correcciones antes de producción{Colors.RESET}"
            )

        print(
            f"\n{Colors.BLUE}📅 Prueba completada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.RESET}"
        )
        print(f"{Colors.BLUE}👨‍💻 Desarrollado por: Carlos{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}\n")


if __name__ == "__main__":
    prueba = PruebaAutomatica()
    try:
        prueba.ejecutar_todas_las_pruebas()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Prueba interrumpida por el usuario{Colors.RESET}")
    except Exception as e:
        print(
            f"\n{Colors.RED}❌ Error crítico durante las pruebas: {str(e)}{Colors.RESET}"
        )
        sys.exit(1)

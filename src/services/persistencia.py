"""
Sistema de persistencia para el manejo de archivos JSON y binarios.

Este módulo proporciona funcionalidades completas para guardar y cargar
datos del sistema usando tanto archivos de texto (JSON) como binarios (pickle).
Implementa el uso de los módulos os, time, datetime y manejo de archivos.
"""

import os
import json
import pickle
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple
import shutil
from pathlib import Path


class GestorArchivos:
    """
    Clase para gestionar la estructura de directorios y archivos del sistema.
    
    Utiliza el módulo os para crear y gestionar directorios de manera automática.
    """
    
    def __init__(self, directorio_base: str = "data"):
        """
        Inicializa el gestor de archivos.
        
        Args:
            directorio_base (str): Directorio base para almacenar datos
        """
        self.directorio_base = directorio_base
        self.directorio_json = os.path.join(directorio_base, "json")
        self.directorio_binarios = os.path.join(directorio_base, "binarios")
        self.directorio_backups = os.path.join(directorio_base, "backups")
        
        # Crear directorios si no existen usando os
        self._crear_directorios()
    
    def _crear_directorios(self):
        """Crea la estructura de directorios usando el módulo os."""
        directorios = [
            self.directorio_base,
            self.directorio_json,
            self.directorio_binarios,
            self.directorio_backups
        ]
        
        for directorio in directorios:
            if not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)
                print(f"📁 Directorio creado: {directorio}")
    
    def obtener_ruta_json(self, nombre_archivo: str) -> str:
        """
        Obtiene la ruta completa para un archivo JSON.
        
        Args:
            nombre_archivo (str): Nombre del archivo sin extensión
            
        Returns:
            str: Ruta completa del archivo JSON
        """
        if not nombre_archivo.endswith('.json'):
            nombre_archivo += '.json'
        return os.path.join(self.directorio_json, nombre_archivo)
    
    def obtener_ruta_binario(self, nombre_archivo: str) -> str:
        """
        Obtiene la ruta completa para un archivo binario.
        
        Args:
            nombre_archivo (str): Nombre del archivo sin extensión
            
        Returns:
            str: Ruta completa del archivo binario
        """
        if not nombre_archivo.endswith('.pkl'):
            nombre_archivo += '.pkl'
        return os.path.join(self.directorio_binarios, nombre_archivo)
    
    def obtener_ruta_backup(self, nombre_archivo: str) -> str:
        """
        Obtiene la ruta para un archivo de backup con timestamp.
        
        Args:
            nombre_archivo (str): Nombre base del archivo
            
        Returns:
            str: Ruta del archivo de backup con timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_con_timestamp = f"{nombre_archivo}_{timestamp}"
        return os.path.join(self.directorio_backups, nombre_con_timestamp)
    
    def listar_archivos(self, tipo: str = "json") -> List[str]:
        """
        Lista archivos de un tipo específico usando os.
        
        Args:
            tipo (str): Tipo de archivo ("json" o "binario")
            
        Returns:
            List[str]: Lista de nombres de archivos
        """
        if tipo == "json":
            directorio = self.directorio_json
            extension = ".json"
        elif tipo == "binario":
            directorio = self.directorio_binarios
            extension = ".pkl"
        else:
            return []
        
        try:
            archivos = os.listdir(directorio)
            return [archivo for archivo in archivos if archivo.endswith(extension)]
        except FileNotFoundError:
            return []
    
    def obtener_info_archivo(self, ruta_archivo: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un archivo usando os.stat.
        
        Args:
            ruta_archivo (str): Ruta del archivo
            
        Returns:
            Dict[str, Any]: Información del archivo
        """
        try:
            stats = os.stat(ruta_archivo)
            return {
                'existe': True,
                'tamaño': stats.st_size,
                'fecha_modificacion': datetime.fromtimestamp(stats.st_mtime),
                'fecha_acceso': datetime.fromtimestamp(stats.st_atime),
                'fecha_creacion': datetime.fromtimestamp(stats.st_ctime),
                'es_archivo': os.path.isfile(ruta_archivo),
                'es_directorio': os.path.isdir(ruta_archivo)
            }
        except FileNotFoundError:
            return {
                'existe': False,
                'tamaño': 0,
                'fecha_modificacion': None,
                'fecha_acceso': None,
                'fecha_creacion': None,
                'es_archivo': False,
                'es_directorio': False
            }


class PersistenciaJSON:
    """
    Clase para manejar persistencia en formato JSON (archivos de texto).
    
    Proporciona métodos para guardar y cargar datos en formato JSON legible.
    """
    
    def __init__(self, gestor_archivos: GestorArchivos):
        """
        Inicializa la persistencia JSON.
        
        Args:
            gestor_archivos (GestorArchivos): Gestor de archivos del sistema
        """
        self.gestor = gestor_archivos
    
    def guardar_datos(self, nombre_archivo: str, datos: Any, 
                     crear_backup: bool = True) -> bool:
        """
        Guarda datos en formato JSON.
        
        Args:
            nombre_archivo (str): Nombre del archivo
            datos (Any): Datos a guardar (deben ser serializables a JSON)
            crear_backup (bool): Si crear backup antes de guardar
            
        Returns:
            bool: True si se guardó correctamente
            
        Raises:
            ValueError: Si los datos no son serializables a JSON
            IOError: Si hay error al escribir el archivo
        """
        ruta_archivo = self.gestor.obtener_ruta_json(nombre_archivo)
        
        try:
            # Crear backup si existe el archivo y se solicita
            if crear_backup and os.path.exists(ruta_archivo):
                self._crear_backup(ruta_archivo, nombre_archivo)
            
            # Preparar datos para JSON
            datos_json = self._preparar_datos_para_json(datos)
            
            # Escribir archivo JSON con formato legible
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos_json, archivo, 
                         indent=2, 
                         ensure_ascii=False,
                         default=str)  # Convertir objetos no serializables a string
            
            print(f"💾 Datos guardados en JSON: {ruta_archivo}")
            return True
            
        except (TypeError, ValueError) as e:
            print(f"❌ Error al serializar datos a JSON: {e}")
            raise ValueError(f"Los datos no son serializables a JSON: {e}")
            
        except IOError as e:
            print(f"❌ Error al escribir archivo JSON: {e}")
            raise IOError(f"No se pudo escribir el archivo: {e}")
    
    def cargar_datos(self, nombre_archivo: str) -> Optional[Any]:
        """
        Carga datos desde un archivo JSON.
        
        Args:
            nombre_archivo (str): Nombre del archivo a cargar
            
        Returns:
            Optional[Any]: Datos cargados o None si hay error
        """
        ruta_archivo = self.gestor.obtener_ruta_json(nombre_archivo)
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            print(f"📖 Datos cargados desde JSON: {ruta_archivo}")
            return datos
            
        except FileNotFoundError:
            print(f"⚠️ Archivo JSON no encontrado: {ruta_archivo}")
            return None
            
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON: {e}")
            return None
            
        except IOError as e:
            print(f"❌ Error al leer archivo JSON: {e}")
            return None
    
    def _preparar_datos_para_json(self, datos: Any) -> Any:
        """
        Prepara datos para serialización JSON.
        
        Convierte objetos personalizados usando sus métodos to_dict().
        """
        if hasattr(datos, 'to_dict'):
            return datos.to_dict()
        elif isinstance(datos, list):
            return [self._preparar_datos_para_json(item) for item in datos]
        elif isinstance(datos, dict):
            return {key: self._preparar_datos_para_json(value) 
                   for key, value in datos.items()}
        else:
            return datos
    
    def _crear_backup(self, ruta_archivo: str, nombre_base: str):
        """Crea un backup del archivo existente."""
        ruta_backup = self.gestor.obtener_ruta_backup(f"{nombre_base}.json")
        try:
            shutil.copy2(ruta_archivo, ruta_backup)
            print(f"📋 Backup creado: {ruta_backup}")
        except IOError as e:
            print(f"⚠️ No se pudo crear backup: {e}")


class PersistenciaBinaria:
    """
    Clase para manejar persistencia en formato binario usando pickle.
    
    Proporciona métodos optimizados para guardar y cargar objetos Python complejos.
    """
    
    def __init__(self, gestor_archivos: GestorArchivos):
        """
        Inicializa la persistencia binaria.
        
        Args:
            gestor_archivos (GestorArchivos): Gestor de archivos del sistema
        """
        self.gestor = gestor_archivos
    
    def guardar_datos(self, nombre_archivo: str, datos: Any, 
                     protocolo: int = pickle.HIGHEST_PROTOCOL,
                     crear_backup: bool = True) -> bool:
        """
        Guarda datos en formato binario usando pickle.
        
        Args:
            nombre_archivo (str): Nombre del archivo
            datos (Any): Datos a guardar
            protocolo (int): Protocolo de pickle a usar
            crear_backup (bool): Si crear backup antes de guardar
            
        Returns:
            bool: True si se guardó correctamente
        """
        ruta_archivo = self.gestor.obtener_ruta_binario(nombre_archivo)
        
        try:
            # Crear backup si existe el archivo y se solicita
            if crear_backup and os.path.exists(ruta_archivo):
                self._crear_backup(ruta_archivo, nombre_archivo)
            
            # Guardar usando pickle
            with open(ruta_archivo, 'wb') as archivo:
                pickle.dump(datos, archivo, protocol=protocolo)
            
            print(f"💾 Datos guardados en binario: {ruta_archivo}")
            return True
            
        except pickle.PicklingError as e:
            print(f"❌ Error al serializar datos con pickle: {e}")
            return False
            
        except IOError as e:
            print(f"❌ Error al escribir archivo binario: {e}")
            return False
    
    def cargar_datos(self, nombre_archivo: str) -> Optional[Any]:
        """
        Carga datos desde un archivo binario.
        
        Args:
            nombre_archivo (str): Nombre del archivo a cargar
            
        Returns:
            Optional[Any]: Datos cargados o None si hay error
        """
        ruta_archivo = self.gestor.obtener_ruta_binario(nombre_archivo)
        
        try:
            with open(ruta_archivo, 'rb') as archivo:
                datos = pickle.load(archivo)
            
            print(f"📖 Datos cargados desde binario: {ruta_archivo}")
            return datos
            
        except FileNotFoundError:
            print(f"⚠️ Archivo binario no encontrado: {ruta_archivo}")
            return None
            
        except pickle.UnpicklingError as e:
            print(f"❌ Error al deserializar datos con pickle: {e}")
            return None
            
        except IOError as e:
            print(f"❌ Error al leer archivo binario: {e}")
            return None
    
    def _crear_backup(self, ruta_archivo: str, nombre_base: str):
        """Crea un backup del archivo binario existente."""
        ruta_backup = self.gestor.obtener_ruta_backup(f"{nombre_base}.pkl")
        try:
            shutil.copy2(ruta_archivo, ruta_backup)
            print(f"📋 Backup binario creado: {ruta_backup}")
        except IOError as e:
            print(f"⚠️ No se pudo crear backup binario: {e}")


class GestorPersistencia:
    """
    Clase principal que coordina la persistencia JSON y binaria.
    
    Proporciona una interfaz unificada para el manejo de datos con
    múltiples formatos y estrategias de respaldo.
    """
    
    def __init__(self, directorio_base: str = "data"):
        """
        Inicializa el gestor de persistencia completo.
        
        Args:
            directorio_base (str): Directorio base para almacenar datos
        """
        self.gestor_archivos = GestorArchivos(directorio_base)
        self.json = PersistenciaJSON(self.gestor_archivos)
        self.binario = PersistenciaBinaria(self.gestor_archivos)
        
        # Configuración de archivos del sistema
        self.archivo_usuarios = "usuarios"
        self.archivo_tareas = "tareas"
        self.archivo_configuracion = "configuracion"
        self.archivo_logs = "logs"
    
    def guardar_usuarios(self, usuarios: List[Any], formato: str = "json") -> bool:
        """
        Guarda la lista de usuarios en el formato especificado.
        
        Args:
            usuarios (List[Any]): Lista de usuarios a guardar
            formato (str): Formato de archivo ("json" o "binario")
            
        Returns:
            bool: True si se guardó correctamente
        """
        if formato == "json":
            return self.json.guardar_datos(self.archivo_usuarios, usuarios)
        elif formato == "binario":
            return self.binario.guardar_datos(self.archivo_usuarios, usuarios)
        else:
            raise ValueError("Formato debe ser 'json' o 'binario'")
    
    def cargar_usuarios(self, formato: str = "json") -> Optional[List[Any]]:
        """
        Carga la lista de usuarios desde el formato especificado.
        
        Args:
            formato (str): Formato de archivo ("json" o "binario")
            
        Returns:
            Optional[List[Any]]: Lista de usuarios o None si hay error
        """
        if formato == "json":
            return self.json.cargar_datos(self.archivo_usuarios)
        elif formato == "binario":
            return self.binario.cargar_datos(self.archivo_usuarios)
        else:
            raise ValueError("Formato debe ser 'json' o 'binario'")
    
    def guardar_tareas(self, tareas: List[Any], formato: str = "json") -> bool:
        """
        Guarda la lista de tareas en el formato especificado.
        
        Args:
            tareas (List[Any]): Lista de tareas a guardar
            formato (str): Formato de archivo ("json" o "binario")
            
        Returns:
            bool: True si se guardó correctamente
        """
        if formato == "json":
            return self.json.guardar_datos(self.archivo_tareas, tareas)
        elif formato == "binario":
            return self.binario.guardar_datos(self.archivo_tareas, tareas)
        else:
            raise ValueError("Formato debe ser 'json' o 'binario'")
    
    def cargar_tareas(self, formato: str = "json") -> Optional[List[Any]]:
        """
        Carga la lista de tareas desde el formato especificado.
        
        Args:
            formato (str): Formato de archivo ("json" o "binario")
            
        Returns:
            Optional[List[Any]]: Lista de tareas o None si hay error
        """
        if formato == "json":
            return self.json.cargar_datos(self.archivo_tareas)
        elif formato == "binario":
            return self.binario.cargar_datos(self.archivo_tareas)
        else:
            raise ValueError("Formato debe ser 'json' o 'binario'")
    
    def sincronizar_formatos(self) -> bool:
        """
        Sincroniza datos entre formatos JSON y binario.
        
        Carga desde JSON y guarda en binario como respaldo, o viceversa.
        
        Returns:
            bool: True si la sincronización fue exitosa
        """
        try:
            # Sincronizar usuarios
            usuarios_json = self.cargar_usuarios("json")
            if usuarios_json:
                self.binario.guardar_datos(f"{self.archivo_usuarios}_sync", usuarios_json)
            
            # Sincronizar tareas
            tareas_json = self.cargar_tareas("json")
            if tareas_json:
                self.binario.guardar_datos(f"{self.archivo_tareas}_sync", tareas_json)
            
            print("🔄 Sincronización entre formatos completada")
            return True
            
        except Exception as e:
            print(f"❌ Error en sincronización: {e}")
            return False
    
    def limpiar_backups_antiguos(self, dias_antiguedad: int = 7) -> int:
        """
        Limpia backups más antiguos que el número de días especificado.
        
        Args:
            dias_antiguedad (int): Número de días para considerar un backup antiguo
            
        Returns:
            int: Número de archivos eliminados
        """
        archivos_eliminados = 0
        fecha_limite = datetime.now() - timedelta(days=dias_antiguedad)
        
        try:
            archivos_backup = os.listdir(self.gestor_archivos.directorio_backups)
            
            for archivo in archivos_backup:
                ruta_completa = os.path.join(self.gestor_archivos.directorio_backups, archivo)
                info_archivo = self.gestor_archivos.obtener_info_archivo(ruta_completa)
                
                if info_archivo['existe'] and info_archivo['fecha_modificacion'] < fecha_limite:
                    os.remove(ruta_completa)
                    archivos_eliminados += 1
                    print(f"🗑️ Backup eliminado: {archivo}")
            
            print(f"🧹 Limpieza completada: {archivos_eliminados} archivos eliminados")
            return archivos_eliminados
            
        except Exception as e:
            print(f"❌ Error en limpieza de backups: {e}")
            return 0
    
    def obtener_estadisticas_almacenamiento(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del almacenamiento usando os.
        
        Returns:
            Dict[str, Any]: Estadísticas de archivos y directorios
        """
        estadisticas = {
            'archivos_json': len(self.gestor_archivos.listar_archivos("json")),
            'archivos_binarios': len(self.gestor_archivos.listar_archivos("binario")),
            'backups_totales': 0,
            'tamaño_total_mb': 0.0,
            'fecha_ultimo_backup': None
        }
        
        try:
            # Contar backups
            if os.path.exists(self.gestor_archivos.directorio_backups):
                backups = os.listdir(self.gestor_archivos.directorio_backups)
                estadisticas['backups_totales'] = len(backups)
                
                # Encontrar fecha del último backup
                if backups:
                    fechas_backup = []
                    for backup in backups:
                        ruta_backup = os.path.join(self.gestor_archivos.directorio_backups, backup)
                        info = self.gestor_archivos.obtener_info_archivo(ruta_backup)
                        if info['existe']:
                            fechas_backup.append(info['fecha_modificacion'])
                    
                    if fechas_backup:
                        estadisticas['fecha_ultimo_backup'] = max(fechas_backup)
            
            # Calcular tamaño total
            for directorio in [self.gestor_archivos.directorio_json,
                              self.gestor_archivos.directorio_binarios,
                              self.gestor_archivos.directorio_backups]:
                if os.path.exists(directorio):
                    for archivo in os.listdir(directorio):
                        ruta_completa = os.path.join(directorio, archivo)
                        if os.path.isfile(ruta_completa):
                            estadisticas['tamaño_total_mb'] += os.path.getsize(ruta_completa)
            
            # Convertir bytes a MB
            estadisticas['tamaño_total_mb'] = round(estadisticas['tamaño_total_mb'] / (1024 * 1024), 2)
            
        except Exception as e:
            print(f"⚠️ Error al calcular estadísticas: {e}")
        
        return estadisticas
    
    def guardar_usuarios_binario(self, usuarios: List[Any]) -> bool:
        """
        Método de compatibilidad para guardar usuarios en formato binario.
        
        Args:
            usuarios (List[Any]): Lista de usuarios a guardar
            
        Returns:
            bool: True si se guardó correctamente
        """
        return self.guardar_usuarios(usuarios, "binario")
    
    def guardar_tareas_binario(self, tareas: List[Any]) -> bool:
        """
        Método de compatibilidad para guardar tareas en formato binario.
        
        Args:
            tareas (List[Any]): Lista de tareas a guardar
            
        Returns:
            bool: True si se guardó correctamente
        """
        return self.guardar_tareas(tareas, "binario")
    
    def crear_backup(self) -> bool:
        """
        Crea un backup completo del sistema.
        
        Returns:
            bool: True si el backup se creó exitosamente
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Crear backup de usuarios JSON
            usuarios_json = self.cargar_usuarios("json")
            if usuarios_json:
                backup_usuarios = f"usuarios_backup_{timestamp}"
                resultado_usuarios = self.json.guardar_datos(backup_usuarios, usuarios_json, crear_backup=False)
            else:
                resultado_usuarios = True  # No hay datos que respaldar
            
            # Crear backup de tareas JSON
            tareas_json = self.cargar_tareas("json")
            if tareas_json:
                backup_tareas = f"tareas_backup_{timestamp}"
                resultado_tareas = self.json.guardar_datos(backup_tareas, tareas_json, crear_backup=False)
            else:
                resultado_tareas = True  # No hay datos que respaldar
            
            exito = resultado_usuarios and resultado_tareas
            
            if exito:
                print(f"✅ Backup completo creado con timestamp: {timestamp}")
            else:
                print("❌ Error al crear backup completo")
            
            return exito
            
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return False

"""
Menú para gestión de usuarios del CLI interactivo.

Este módulo contiene toda la lógica para el manejo de usuarios
a través del CLI interactivo.
"""

from typing import Optional

# Importaciones usando try/except para manejar diferentes contextos
try:
    from ..models.usuario import Usuario
    from .cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_tabla_usuarios, mostrar_exito, mostrar_error, 
        mostrar_advertencia, solicitar_entrada_requerida, solicitar_entrada,
        confirmar_accion, pausar, manejar_error_sistema
    )
except ImportError:
    from models.usuario import Usuario
    from cli.cli_utils import (
        mostrar_titulo, mostrar_subtitulo, mostrar_menu_opciones,
        mostrar_tabla_usuarios, mostrar_exito, mostrar_error, 
        mostrar_advertencia, solicitar_entrada_requerida, solicitar_entrada,
        confirmar_accion, pausar, manejar_error_sistema
    )


class MenuUsuarios:
    """
    Clase que maneja el menú de gestión de usuarios.
    """
    
    def __init__(self, gestor):
        """
        Inicializa el menú de usuarios.
        
        Args:
            gestor: Instancia del gestor del sistema
        """
        self.gestor = gestor
    
    def mostrar_menu(self):
        """
        Muestra el menú principal de gestión de usuarios.
        """
        while True:
            try:
                opciones = [
                    "📝 Crear nuevo usuario",
                    "👀 Ver todos los usuarios", 
                    "🔍 Buscar usuario",
                    "✏️ Editar usuario",
                    "🗑️ Eliminar usuario",
                    "👤 Ver detalles de usuario",
                    "⬅️ Volver al menú principal"
                ]
                
                mostrar_titulo("GESTIÓN DE USUARIOS")
                seleccion = mostrar_menu_opciones(opciones)
                
                if seleccion == 1:
                    self.crear_usuario()
                elif seleccion == 2:
                    self.listar_usuarios()
                elif seleccion == 3:
                    self.buscar_usuario()
                elif seleccion == 4:
                    self.editar_usuario()
                elif seleccion == 5:
                    self.eliminar_usuario()
                elif seleccion == 6:
                    self.ver_detalles_usuario()
                elif seleccion == 7:
                    break
                    
            except Exception as e:
                manejar_error_sistema(e)
    
    def crear_usuario(self):
        """Crea un nuevo usuario."""
        try:
            mostrar_titulo("CREAR NUEVO USUARIO")
            
            nombre = solicitar_entrada_requerida("Nombre completo")
            email = solicitar_entrada_requerida("Email")
            telefono = solicitar_entrada("Teléfono (opcional)")
            
            # Crear usuario usando el método del gestor
            usuario_creado = self.gestor.crear_usuario(nombre, email)
            
            if usuario_creado:
                # Añadir teléfono si se proporcionó
                if telefono:
                    usuario_creado.telefono = telefono
                mostrar_exito(f"Usuario '{nombre}' creado exitosamente")
            else:
                mostrar_error("No se pudo crear el usuario")
                
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def listar_usuarios(self):
        """Lista todos los usuarios."""
        try:
            mostrar_titulo("LISTA DE USUARIOS")
            usuarios = self.gestor.usuarios
            mostrar_tabla_usuarios(usuarios)
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def buscar_usuario(self):
        """Busca un usuario específico."""
        try:
            mostrar_titulo("BUSCAR USUARIO")
            termino = solicitar_entrada_requerida("Término de búsqueda (nombre o email)")
            
            usuarios = self.gestor.usuarios
            resultados = []
            
            for usuario in usuarios:
                if (termino.lower() in usuario.nombre.lower() or 
                    termino.lower() in usuario.email.lower()):
                    resultados.append(usuario)
            
            if resultados:
                mostrar_subtitulo(f"Resultados de búsqueda ({len(resultados)} encontrados)")
                mostrar_tabla_usuarios(resultados)
            else:
                mostrar_advertencia("No se encontraron usuarios con ese término de búsqueda")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def seleccionar_usuario(self) -> Optional[Usuario]:
        """
        Permite seleccionar un usuario de la lista.
        
        Returns:
            Usuario: Usuario seleccionado o None si no hay usuarios
        """
        usuarios = self.gestor.usuarios
        if not usuarios:
            mostrar_advertencia("No hay usuarios registrados")
            return None
        
        mostrar_tabla_usuarios(usuarios)
        
        while True:
            try:
                indice = int(solicitar_entrada_requerida("Número de usuario")) - 1
                if 0 <= indice < len(usuarios):
                    return usuarios[indice]
                else:
                    mostrar_error("Número de usuario inválido")
            except ValueError:
                mostrar_error("Por favor ingresa un número válido")
    
    def editar_usuario(self):
        """Edita un usuario existente."""
        try:
            mostrar_titulo("EDITAR USUARIO")
            
            usuario = self.seleccionar_usuario()
            if not usuario:
                pausar()
                return
            
            mostrar_subtitulo(f"Editando usuario: {usuario.nombre}")
            print(f"Deja vacío para mantener el valor actual")
            
            # Solicitar nuevos valores
            nuevo_nombre = solicitar_entrada("Nombre", usuario.nombre)
            nuevo_email = solicitar_entrada("Email", usuario.email)
            nuevo_telefono = solicitar_entrada("Teléfono", usuario.telefono or "")
            
            # Validar email único si cambió
            if nuevo_email.lower() != usuario.email.lower():
                usuarios_existentes = self.gestor.usuarios
                for u in usuarios_existentes:
                    if u.id != usuario.id and u.email.lower() == nuevo_email.lower():
                        mostrar_error("Ya existe un usuario con ese email")
                        pausar()
                        return
            
            # Actualizar usuario
            usuario.nombre = nuevo_nombre
            usuario.email = nuevo_email
            usuario.telefono = nuevo_telefono if nuevo_telefono else None
            
            # El gestor no tiene método actualizar_usuario, los cambios son directos
            mostrar_exito("Usuario actualizado exitosamente")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def eliminar_usuario(self):
        """Elimina un usuario."""
        try:
            mostrar_titulo("ELIMINAR USUARIO")
            
            usuario = self.seleccionar_usuario()
            if not usuario:
                pausar()
                return
            
            # Confirmar eliminación
            mostrar_advertencia(f"Estás a punto de eliminar el usuario: {usuario.nombre}")
            print(f"Email: {usuario.email}")
            
            if confirmar_accion("¿Estás seguro de eliminar este usuario?"):
                if self.gestor.eliminar_usuario(usuario.id):
                    mostrar_exito("Usuario eliminado exitosamente")
                else:
                    mostrar_error("No se pudo eliminar el usuario")
            else:
                mostrar_advertencia("Eliminación cancelada")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)
    
    def ver_detalles_usuario(self):
        """Muestra los detalles completos de un usuario."""
        try:
            mostrar_titulo("DETALLES DE USUARIO")
            
            usuario = self.seleccionar_usuario()
            if not usuario:
                pausar()
                return
            
            print(f"\n{'=' * 50}")
            print(f"👤 INFORMACIÓN DEL USUARIO")
            print(f"{'=' * 50}")
            print(f"ID: {usuario.id}")
            print(f"Nombre: {usuario.nombre}")
            print(f"Email: {usuario.email}")
            print(f"Teléfono: {usuario.telefono or 'No especificado'}")
            print(f"Fecha de registro: {usuario.fecha_registro.strftime('%d/%m/%Y %H:%M')}")
            
            # Obtener tareas del usuario
            try:
                tareas_usuario = [t for t in self.gestor.tareas if t.usuario_id == usuario.id]
                print(f"\n📋 TAREAS ASIGNADAS: {len(tareas_usuario)}")
                
                if tareas_usuario:
                    pendientes = len([t for t in tareas_usuario if t.estado.value == 'pendiente'])
                    en_progreso = len([t for t in tareas_usuario if t.estado.value == 'en_progreso'])
                    completadas = len([t for t in tareas_usuario if t.estado.value == 'completada'])
                    
                    print(f"  • Pendientes: {pendientes}")
                    print(f"  • En progreso: {en_progreso}")
                    print(f"  • Completadas: {completadas}")
                
            except Exception:
                print("No se pudieron obtener las tareas del usuario")
            
            pausar()
            
        except Exception as e:
            manejar_error_sistema(e)

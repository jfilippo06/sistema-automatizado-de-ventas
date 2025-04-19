import tkinter as tk
from tkinter import messagebox, filedialog
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable
import sqlite3
import os
import shutil
from datetime import datetime

class MaintenanceScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("500x370")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = CustomLabel(
            main_frame,
            text="Mantenimiento del Sistema",
            font=("Arial", 20, "bold"),
            fg="#333",
            bg="#f0f0f0"
        )
        title.pack(pady=(10, 20))

        options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        options_frame.pack(pady=(0, 10))

        buttons = [
            ("Compactar Base de Datos", self.compress_database),
            ("Exportar Base de Datos", self.export_database),
            ("Importar Base de Datos", self.import_database),
            ("Regresar", self.go_back)
        ]

        for text, command in buttons:
            btn = CustomButton(
                options_frame,
                text=text,
                command=command,
                padding=10,
                width=30
            )
            btn.pack(pady=5, ipady=10, ipadx=10)

    def get_db_path(self) -> str:
        """Obtiene la ruta completa del archivo de base de datos"""
        # Obtener el directorio base del proyecto (sistema-automatizado-de-ventas)
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # Construir la ruta completa a la base de datos
        return os.path.join(project_dir, 'sqlite_cli', 'database', 'db.db')

    def compress_database(self) -> None:
        """Comprime la base de datos SQLite"""
        confirm = messagebox.askyesno(
            "Compactar Base de Datos",
            "¿Está seguro que desea compactar la base de datos?\n"
            "Esta operación puede mejorar el rendimiento pero tomará unos momentos.",
            parent=self
        )
        
        if not confirm:
            return

        try:
            db_path = self.get_db_path()
            conn = sqlite3.connect(db_path)
            
            # Vaciar el espacio no utilizado
            conn.execute("VACUUM")
            conn.close()
            
            messagebox.showinfo(
                "Éxito",
                "Base de datos comprimida exitosamente",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo comprimir la base de datos:\n{str(e)}",
                parent=self
            )

    def export_database(self) -> None:
        """Exporta la base de datos a un archivo seleccionado por el usuario"""
        default_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar Base de Datos",
            defaultextension=".db",
            initialfile=default_filename,
            filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if not file_path:
            return  # Usuario canceló la operación

        try:
            db_path = self.get_db_path()
            shutil.copyfile(db_path, file_path)
            
            messagebox.showinfo(
                "Éxito",
                f"Base de datos exportada exitosamente a:\n{file_path}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo exportar la base de datos:\n{str(e)}",
                parent=self
            )

    def import_database(self) -> None:
        """Importa una base de datos desde un archivo seleccionado por el usuario"""
        confirm = messagebox.askyesno(
            "Importar Base de Datos",
            "ADVERTENCIA: Esta operación reemplazará la base de datos actual.\n"
            "¿Desea continuar?",
            parent=self
        )
        
        if not confirm:
            return

        file_path = filedialog.askopenfilename(
            title="Seleccionar Base de Datos",
            filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if not file_path:
            return  # Usuario canceló la operación

        try:
            db_path = self.get_db_path()
            
            # Hacer backup de la base de datos actual
            backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_filename = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            shutil.copyfile(db_path, backup_path)
            
            # Reemplazar con la nueva base de datos
            shutil.copyfile(file_path, db_path)
            
            messagebox.showinfo(
                "Éxito",
                f"Base de datos importada exitosamente desde:\n{file_path}\n\n"
                f"Se creó un backup en:\n{backup_path}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo importar la base de datos:\n{str(e)}",
                parent=self
            )

    def go_back(self) -> None:
        self.open_previous_screen_callback()
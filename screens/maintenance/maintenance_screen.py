import tkinter as tk
from tkinter import messagebox, filedialog
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable
from PIL import Image, ImageTk
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
        self.configure(bg="#f5f5f5")
        self.images = {}
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
         # Tamaño de la ventana
        window_width = 700
        window_height = 500
        
        # Calcular posición para centrar
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        # Configurar geometría centrada
        self.parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.load_and_display_images(main_frame)
        
        title = CustomLabel(
            main_frame,
            text="Mantenimiento del Sistema",
            font=("Arial", 24, "bold"),
            fg="#2356a2",
            bg="#f5f5f5"
        )
        title.pack(pady=(20, 30))
        
        buttons_frame = tk.Frame(main_frame, bg="#f5f5f5")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        buttons = [
            ("Compactar Base de Datos", "compress", "#2356a2"),
            ("Exportar Base de Datos", "export", "#3a6eb5"),
            ("Importar Base de Datos", "import", "#4d87d1"),
            ("Regresar", "back", "#d9534f")
        ]
        
        for i, (text, key, color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = self.create_menu_button(
                buttons_frame, 
                text, 
                color,
                lambda k=key: self.navigate(k))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            buttons_frame.grid_columnconfigure(col, weight=1)
            buttons_frame.grid_rowconfigure(row, weight=1)

    def load_and_display_images(self, parent):
        try:
            img_frame = tk.Frame(parent, bg="#f5f5f5")
            img_frame.pack()
            
            img_paths = [
                ("assets/republica.png", (70, 70)),
                ("assets/empresa.png", (70, 70)),
                ("assets/universidad.png", (70, 70))
            ]
            
            for path, size in img_paths:
                img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                self.images[path] = ImageTk.PhotoImage(img)
                label = tk.Label(img_frame, image=self.images[path], bg="#f5f5f5")
                label.pack(side=tk.LEFT, padx=10)
                
        except Exception as e:
            print(f"Error cargando imágenes: {e}")

    def create_menu_button(self, parent, text, bg_color, command):
        btn = tk.Frame(parent, bg=bg_color, bd=0, highlightthickness=0)
        btn.bind("<Button-1>", lambda e: command())
        
        label = tk.Label(
            btn, 
            text=text, 
            bg=bg_color, 
            fg="white", 
            font=("Arial", 11), 
            padx=10, 
            pady=15,
            wraplength=150
        )
        label.pack(fill=tk.BOTH, expand=True)
        label.bind("<Button-1>", lambda e: command())
        
        return btn

    def navigate(self, key):
        if key == "back":
            self.go_back()
        elif key == "compress":
            self.compress_database()
        elif key == "export":
            self.export_database()
        elif key == "import":
            self.import_database()

    def get_db_path(self) -> str:
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(project_dir, 'sqlite_cli', 'database', 'db.db')

    def compress_database(self) -> None:
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
        default_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar Base de Datos",
            defaultextension=".db",
            initialfile=default_filename,
            filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if not file_path:
            return

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
            return

        try:
            db_path = self.get_db_path()
            backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_filename = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            shutil.copyfile(db_path, backup_path)
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
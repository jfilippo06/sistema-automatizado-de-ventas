import tkinter as tk
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from typing import Any, Callable
from PIL import Image, ImageTk

class RecoveryScreen(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        open_previous_screen_callback: Callable[[], None],
        open_recovery_suppliers_callback: Callable[[], None],
        open_recovery_inventory_callback: Callable[[], None],
        open_recovery_service_requests_callback: Callable[[], None],
        open_recovery_services_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.open_recovery_suppliers_callback = open_recovery_suppliers_callback
        self.open_recovery_inventory_callback = open_recovery_inventory_callback
        self.open_recovery_service_requests_callback = open_recovery_service_requests_callback
        self.open_recovery_services_callback = open_recovery_services_callback
        self.configure(bg="#f5f5f5")
        self.images = {}
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("700x500")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.load_and_display_images(main_frame)
        
        title = CustomLabel(
            main_frame,
            text="Recuperación de Registros",
            font=("Arial", 24, "bold"),
            fg="#2356a2",
            bg="#f5f5f5"
        )
        title.pack(pady=(20, 30))
        
        buttons_frame = tk.Frame(main_frame, bg="#f5f5f5")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        buttons = [
            ("Gestión de Proveedores", "suppliers", "#2356a2"),
            ("Inventario de Productos", "inventory", "#3a6eb5"),
            ("Solicitudes de Servicio", "service_requests", "#4d87d1"),
            ("Gestión de Servicios", "services", "#5c9ae0"),
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
        elif key == "suppliers":
            self.recover_suppliers()
        elif key == "inventory":
            self.recover_inventory()
        elif key == "service_requests":
            self.recover_service_requests()
        elif key == "services":
            self.recover_services()

    def recover_suppliers(self) -> None:
        self.open_recovery_suppliers_callback()

    def recover_inventory(self) -> None:
        self.open_recovery_inventory_callback()

    def recover_service_requests(self) -> None:
        self.open_recovery_service_requests_callback()

    def recover_services(self) -> None:
        self.open_recovery_services_callback()

    def go_back(self) -> None:
        self.open_previous_screen_callback()
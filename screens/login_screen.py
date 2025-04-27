import tkinter as tk
from tkinter import messagebox
from typing import Any, Callable
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from utils.session_manager import SessionManager

class LoginScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_home_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_home_screen_callback = open_home_screen_callback
        self.configure(bg="#f0f0f0")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("600x500")
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 1. Título más grande y centrado
        title = CustomLabel(
            main_frame,
            text="Inicio de Sesión",
            font=("Arial", 18, "bold"),  # Tamaño aumentado
            fg="#333",
            bg="#f0f0f0"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Campos con valores por defecto "admin"
        self.username_var = tk.StringVar(value="admin")  # 2. Valor predefinido
        self.password_var = tk.StringVar(value="admin")  # 2. Valor predefinido

        # Campo de usuario
        user_label = CustomLabel(
            main_frame,
            text="Usuario:",
            font=("Arial", 12),
            fg="#555",
            bg="#f0f0f0"
        )
        user_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.user_entry = CustomEntry(
            main_frame,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=25
        )
        self.user_entry.grid(row=1, column=1, pady=5, padx=10)

        # Campo de contraseña
        password_label = CustomLabel(
            main_frame,
            text="Contraseña:",
            font=("Arial", 12),
            fg="#555",
            bg="#f0f0f0"
        )
        password_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.password_entry = CustomEntry(
            main_frame,
            textvariable=self.password_var,
            show="*",
            font=("Arial", 12),
            width=25
        )
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)

        # Botón de login
        login_btn = CustomButton(
            main_frame,
            text="Iniciar Sesión",
            command=self.authenticate,
            padding=10,
            width=15
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def authenticate(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son requeridos")
            return
        
        if SessionManager.login(username, password):
            # 3. Limpiar campos después de login exitoso
            self.username_var.set("")
            self.password_var.set("")
            self.open_home_screen_callback()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")
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
        self.configure(bg="#f5f5f5")  # Consistent background color
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("600x500")  # Slightly larger window
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Main content frame centered
        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Login title
        title = CustomLabel(
            main_frame,
            text="Inicio de Sesión",
            font=("Arial", 24, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 40))

        # Fields with default values
        self.username_var = tk.StringVar(value="admin")
        self.password_var = tk.StringVar(value="admin")

        # Username field
        user_label = CustomLabel(
            main_frame,
            text="Usuario:",
            font=("Arial", 14),
            fg="#555",
            bg="#f5f5f5"
        )
        user_label.grid(row=1, column=0, sticky="e", pady=10, padx=10)
        
        self.user_entry = CustomEntry(
            main_frame,
            textvariable=self.username_var,
            font=("Arial", 14),
            width=30,
        )
        self.user_entry.grid(row=1, column=1, pady=10, padx=10)

        # Password field
        password_label = CustomLabel(
            main_frame,
            text="Contraseña:",
            font=("Arial", 14),
            fg="#555",
            bg="#f5f5f5"
        )
        password_label.grid(row=2, column=0, sticky="e", pady=10, padx=10)
        
        self.password_entry = CustomEntry(
            main_frame,
            textvariable=self.password_var,
            show="*",
            font=("Arial", 14),
            width=30,
        )
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)

        # Login button - larger and styled
        login_btn = CustomButton(
            main_frame,
            text="Iniciar Sesión",
            command=self.authenticate,
            padding=12,
            width=20,
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=30)

    def authenticate(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son requeridos", parent=self)
            return
        
        if SessionManager.login(username, password):
            self.username_var.set("")
            self.password_var.set("")
            self.open_home_screen_callback()
        else:
            messagebox.showerror("Error", "Credenciales inválidas", parent=self)
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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
        self.configure(bg="#f5f5f5")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("600x500")  # Slightly larger window
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Contenedor principal que ocupa toda la ventana
        container = tk.Frame(self, bg="#f5f5f5")
        container.pack(fill=tk.BOTH, expand=True)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)  # permite crecer en vertical

        # ----- LADO IZQUIERDO -----
        left_frame = tk.Frame(container, bg="#dcdcdc")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        left_content = tk.Frame(left_frame, bg="#dcdcdc")
        left_content.pack(expand=True)

        try:
            logo = Image.open("assets/logo.png").resize((90, 90), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(left_content, image=logo_img, bg="#dcdcdc")
            logo_label.image = logo_img
            logo_label.pack(pady=(20, 10))
        except Exception as e:
            print("No se pudo cargar logo.png:", e)

        CustomLabel(left_content, text="Gobierno Bolivariano de Venezuela", font=("Arial", 10, "bold"), fg="black", bg="#dcdcdc").pack()
        CustomLabel(left_content, text="Ministerio del Poder Popular\npara la Educación Universitaria", font=("Arial", 9), fg="black", bg="#dcdcdc").pack(pady=(0, 15))

        CustomLabel(left_content, text="RN&M", font=("Arial", 18, "bold"), fg="red", bg="#dcdcdc").pack()
        CustomLabel(left_content, text="Servicios Integrales, C.A", font=("Arial", 10), fg="black", bg="#dcdcdc").pack()
        CustomLabel(left_content, text="Rif: J-40398174-0", font=("Arial", 9), fg="black", bg="#dcdcdc").pack(pady=(0, 15))

        try:
            tp_logo = Image.open("assets/logo_tp.png").resize((80, 80), Image.Resampling.LANCZOS)
            tp_img = ImageTk.PhotoImage(tp_logo)
            tp_label = tk.Label(left_content, image=tp_img, bg="#dcdcdc")
            tp_label.image = tp_img
            tp_label.pack(pady=(5, 0))
        except Exception as e:
            print("No se pudo cargar logo_tp.png:", e)

        # ----- LADO DERECHO -----
        right_frame = tk.Frame(container, bg="#2356a2")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        login_content = tk.Frame(right_frame, bg="#2356a2")
        login_content.pack(expand=True)

        CustomLabel(login_content, text="Login", font=("Arial", 20, "bold"), fg="white", bg="#2356a2").pack(pady=(30, 20))

        form_frame = tk.Frame(login_content, bg="#2356a2")
        form_frame.pack()

        self.username_var = tk.StringVar(value="admin")
        self.password_var = tk.StringVar(value="admin")

        CustomLabel(form_frame, text="Usuario", font=("Arial", 12), fg="white", bg="#2356a2").grid(row=0, column=0, sticky="w")
        self.user_entry = CustomEntry(form_frame, textvariable=self.username_var, width=30)
        self.user_entry.grid(row=1, column=0, pady=(0, 10))

        CustomLabel(form_frame, text="Contraseña", font=("Arial", 12), fg="white", bg="#2356a2").grid(row=2, column=0, sticky="w")
        self.password_entry = CustomEntry(form_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=3, column=0, pady=(0, 20))

        CustomButton(login_content, text="Iniciar Sesión", command=self.authenticate, width=20).pack()

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

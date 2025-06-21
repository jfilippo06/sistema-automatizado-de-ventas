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
        self.parent.geometry("700x500")  # Slightly larger window
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        container = tk.Frame(self, bg="#f5f5f5")
        container.pack(fill=tk.BOTH, expand=True)

        # ----- COLUMNAS CON PROPORCIÓN -----
        container.columnconfigure(0, weight=1)  # gris
        container.columnconfigure(1, weight=2)  # azul más ancho
        container.rowconfigure(0, weight=1)

        # ----- LADO IZQUIERDO (GRIS, columna) -----
        left_frame = tk.Frame(container, bg="#dcdcdc", width=60)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        left_frame.grid_propagate(False)  # mantener tamaño fijo
        left_frame.columnconfigure(0, weight=1)

        # Subcontenedor centrado verticalmente
        left_content = tk.Frame(left_frame, bg="#dcdcdc")
        left_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Cargar imágenes
        self.load_and_pack_image(left_content, "assets/republica.png", (100, 100))
        self.load_and_pack_image(left_content, "assets/empresa.png", (100, 100))
        self.load_and_pack_image(left_content, "assets/universidad.png", (100, 100))

        # ----- LADO DERECHO (AZUL, login) -----
        right_frame = tk.Frame(container, bg="#2356a2")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        login_content = tk.Frame(right_frame, bg="#2356a2")
        login_content.pack(expand=True)

        CustomLabel(login_content, text="Login", font=("Arial", 22, "bold"), fg="white", bg="#2356a2").pack(pady=(30, 20))

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

    def load_and_pack_image(self, parent: tk.Widget, path: str, size: tuple[int, int]) -> None:
        try:
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(parent, image=tk_img, bg="#dcdcdc")
            label.image = tk_img  # Guardar referencia
            label.pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar {path}: {e}")

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

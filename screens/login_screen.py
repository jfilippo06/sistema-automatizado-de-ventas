import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from typing import Any, Callable
from utils.session_manager import SessionManager

class LoginScreen(tk.Frame):
    def __init__(self, parent: tk.Tk, open_home_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent, bg="white")
        self.parent = parent
        self.open_home_screen_callback = open_home_screen_callback
        self.images = {}
        self.parent.bind("<Escape>", lambda e: self.parent.destroy())

        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')        
        self.parent.resizable(False, False)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        bg_image = self.load_image(self, "assets/login.jpg")
        bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        overlay = tk.Frame(self, bg="", bd=0)
        overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.75, relheight=0.65)

        overlay.columnconfigure(0, weight=1)
        overlay.columnconfigure(1, weight=2)
        overlay.rowconfigure(0, weight=1)

        # ----- IZQUIERDA -----
        left_frame = tk.Frame(overlay, bg="white")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 0), pady=0)
        left_frame.grid_propagate(False)
        left_frame.columnconfigure(0, weight=1)

        left_content = tk.Frame(left_frame, bg="white")
        left_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.load_and_pack_image(left_content, "assets/republica.png", (100, 100))
        self.load_and_pack_image(left_content, "assets/empresa.png", (100, 100))
        self.load_and_pack_image(left_content, "assets/universidad.png", (100, 100))

        # ----- DERECHA -----
        right_frame = tk.Frame(overlay, bg="", highlightthickness=0)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Fondo azul translúcido simulado
        right_overlay = tk.Canvas(right_frame, bg="#2356a2", highlightthickness=0)
        right_overlay.place(relwidth=1, relheight=1)

        login_content = tk.Frame(right_frame, bg="#2356a2")
        login_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Encabezado verde
        header = tk.Frame(login_content, bg="#2356a2", height=40)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Login",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#2356a2"
        ).pack(pady=5)

        form_frame = tk.Frame(login_content, bg="#2356a2")
        form_frame.pack(pady=40)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Usuario
        tk.Label(form_frame, text="Usuario", font=("Arial", 12), fg="white", bg="#2356a2").pack(anchor="w")
        self.user_entry = tk.Entry(form_frame, textvariable=self.username_var, font=("Arial", 12), fg="white", bg="#2356a2", insertbackground="white", borderwidth=0)
        self.user_entry.pack(fill=tk.X, padx=5)
        tk.Frame(form_frame, bg="white", height=1).pack(fill=tk.X, pady=(0, 15), padx=5)

        # Contraseña
        tk.Label(form_frame, text="Contraseña", font=("Arial", 12), fg="white", bg="#2356a2").pack(anchor="w")
        self.password_entry = tk.Entry(form_frame, textvariable=self.password_var, show="*", font=("Arial", 12), fg="white", bg="#2356a2", insertbackground="white", borderwidth=0)
        self.password_entry.pack(fill=tk.X, padx=5)
        tk.Frame(form_frame, bg="white", height=1).pack(fill=tk.X, pady=(0, 25), padx=5)

        # Botón Iniciar Sesión
        login_btn = tk.Button(
            login_content,
            text="Iniciar Sesión",
            command=self.authenticate,
            font=("Arial", 12, "bold"),
            bg="#2356a2",
            fg="white",
            activebackground="#1b417a",
            activeforeground="white",
            highlightbackground="#00FF00",
            highlightthickness=2,
            bd=0,
            padx=20,
            pady=5
        )
        login_btn.pack()

    def load_and_pack_image(self, parent: tk.Widget, path: str, size: tuple[int, int]) -> None:
        try:
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(parent, image=tk_img, bg="white")
            label.image = tk_img
            label.pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar {path}: {e}")

    def load_image(self, parent: tk.Widget, path: str) -> tk.Label:
        try:
            screen_width = self.parent.winfo_screenwidth()
            screen_height = self.parent.winfo_screenheight()
            img = Image.open(path).resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images[path] = photo
            return tk.Label(parent, image=photo, bd=0)
        except Exception as e:
            print(f"No se pudo cargar imagen de fondo {path}: {e}")
            return tk.Label(parent, bg="white")

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

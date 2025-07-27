import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.configuration.users.crud_users import CrudUser
from sqlite_cli.models.user_model import User
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class UsersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Todos los campos")
        self.configure(bg="#f5f5f5")  # Fondo general
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        # Header con título - Estilo actualizado
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Usuarios",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Frame para botón de regreso - Estilo actualizado
        back_frame = tk.Frame(header_frame, bg="#4a6fa5")
        back_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_back = CustomButton(
            back_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Frame principal para controles - Estilo actualizado
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Frame de búsqueda
        search_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Campo de búsqueda - Estilo actualizado
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 12),
            placeholder="Buscar..."
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.on_search)

        # Combobox para seleccionar campo de búsqueda - Estilo actualizado
        search_fields = [
            "Todos los campos",
            "ID",
            "Usuario",
            "Nombre",
            "Correo",
            "Rol"
        ]
        
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.search_field_var,
            values=search_fields,
            state="readonly",
            width=20
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.on_search)

        # Frame para los botones de acciones (derecha) - Estilo actualizado
        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        btn_disable = CustomButton(
            action_frame,
            text="Desactivar",
            command=self.disable_user,
            padding=8,
            width=12,
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        btn_edit = CustomButton(
            action_frame,
            text="Editar",
            command=self.edit_user,
            padding=8,
            width=10,
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_add = CustomButton(
            action_frame,
            text="Agregar",
            command=self.add_user,
            padding=8,
            width=10,
        )
        btn_add.pack(side=tk.RIGHT, padx=5)

        # Treeview frame - Estilo actualizado
        tree_frame = tk.Frame(self, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Usuario", "Nombre", "Correo", "Rol"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Usuario", 100, tk.CENTER),
            ("Nombre", 150, tk.W),
            ("Correo", 200, tk.W),
            ("Rol", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('oddrow', background='#f0f0f0')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Barra de estado - Estilo actualizado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

        self.refresh_data()

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        field = self.search_field_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        users = User.search_active(search_term, field if field != "Todos los campos" else None)
        
        for i, user in enumerate(users):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(
                user['id'],
                user['username'],
                f"{user['first_name']} {user['last_name']}",
                user['email'],
                user['role_name']
            ), tags=(tag,))
        
        self.status_bar.configure(text=f"Mostrando {len(users)} usuarios")

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.on_search()

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def add_user(self) -> None:
        CrudUser(self, mode="create", refresh_callback=self.refresh_data)

    def edit_user(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario", parent=self)
            return
            
        user_id = self.tree.item(selected[0])['values'][0]
        CrudUser(self, mode="edit", user_id=user_id, refresh_callback=self.refresh_data)

    def disable_user(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario", parent=self)
            return
            
        user_id = self.tree.item(selected[0])['values'][0]
        username = self.tree.item(selected[0])['values'][1]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea desactivar al usuario '{username}'?",
            parent=self
        )
        
        if response:
            try:
                status_inactive = next((s for s in Status.all() if s['name'] == 'inactive'), None)
                if status_inactive:
                    User.update_status(user_id, status_inactive['id'])
                    messagebox.showinfo("Éxito", "Usuario desactivado correctamente", parent=self)
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "No se encontró el estado 'inactivo'", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo desactivar el usuario: {str(e)}", parent=self)
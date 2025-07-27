import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.user_model import User
from sqlite_cli.models.person_model import Person
from sqlite_cli.models.role_model import Role
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.field_formatter import FieldFormatter

class CrudUser(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        user_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.user_id = user_id
        self.refresh_callback = refresh_callback
        
        self.title("Crear Usuario" if mode == "create" else "Editar Usuario")
        
        # Configuración de tamaño y posición centrada
        window_width = 400
        window_height = 680
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.id_number_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.role_var = tk.StringVar()
        
        # Diccionarios para traducción de roles
        self.role_translation = {
            'admin': 'Administrador',
            'employee': 'Empleado',
            'client': 'Cliente'
        }
        self.reverse_role_translation = {v: k for k, v in self.role_translation.items()}
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and user_id:
            self.load_user_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=25, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        title_text = "Nuevo Usuario" if self.mode == "create" else "Editar Usuario"
        title_label = CustomLabel(
            title_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.pack(pady=10, padx=10, anchor="w")
        
        # Definición de secciones y campos con sus tipos de formateo
        sections = [
            ("Información de Acceso", [
                ("Usuario:", self.username_var, 'name', True),
                ("Contraseña:", self.password_var, None, self.mode == "create", True),
                ("Confirmar Contraseña:", self.confirm_password_var, None, self.mode == "create", True),
                ("Rol:", self.role_var, None, True)
            ]),
            ("Información Personal", [
                ("Nombres:", self.first_name_var, 'name', True),
                ("Apellidos:", self.last_name_var, 'name', True),
                ("Cédula:", self.id_number_var, 'integer', True),
                ("Dirección:", self.address_var, 'first_name', True),
                ("Teléfono:", self.phone_var, 'phone', True),
                ("Correo:", self.email_var, 'email', True)
            ]),
            ("Información Laboral", [
                ("Departamento:", self.department_var, 'first_name', True),
                ("Cargo:", self.position_var, 'first_name', True)
            ])
        ]
        
        row_counter = 1
        for section_title, fields in sections:
            section_label = CustomLabel(
                main_frame,
                text=section_title,
                font=("Arial", 12, "bold"),
                fg="#333",
                bg="#f5f5f5"
            )
            section_label.grid(row=row_counter, column=0, columnspan=2, pady=(10, 5), sticky="w")
            row_counter += 1
            
            for field in fields:
                label, var, field_type, editable, *extra = field
                is_password = len(extra) > 0 and extra[0]
                
                field_frame = tk.Frame(main_frame, bg="#f5f5f5")
                field_frame.grid(row=row_counter, column=0, columnspan=2, sticky="ew", pady=3)
                
                field_label = CustomLabel(
                    field_frame,
                    text=label,
                    font=("Arial", 10),
                    fg="#333",
                    bg="#f5f5f5",
                    width=20,
                    anchor="w"
                )
                field_label.pack(side=tk.LEFT, padx=(0, 10))
                
                if label == "Rol:":
                    roles = Role.all()
                    # Traducimos los nombres de los roles al español para mostrar
                    values = [self.role_translation.get(role['name'].lower(), role['name']) 
                             for role in roles]
                    
                    combobox = CustomCombobox(
                        field_frame,
                        textvariable=var,
                        values=values,
                        state="readonly",
                        width=25
                    )
                    combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)
                    self.entries[label] = combobox
                else:
                    entry = CustomEntry(
                        field_frame,
                        textvariable=var,
                        font=("Arial", 10),
                        width=30,
                        state="normal" if editable else "readonly",
                        show="*" if is_password else None
                    )
                    
                    if field_type and editable:
                        FieldFormatter.bind_validation(entry, field_type)
                    
                    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
                    self.entries[label] = entry
                
                row_counter += 1

        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=row_counter, column=0, columnspan=2, pady=(20, 0), sticky="e")
        
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Guardar", 
                command=self.create_user,
                padding=8,
                width=12
            )
        else:
            btn_action = CustomButton(
                btn_frame, 
                text="Actualizar", 
                command=self.update_user,
                padding=8,
                width=12
            )
        btn_action.pack(side=tk.RIGHT, padx=5)

    def validate_required_fields(self) -> bool:
        required_fields = {
            "Usuario:": (self.entries["Usuario:"], self.username_var.get()),
            "Nombres:": (self.entries["Nombres:"], self.first_name_var.get()),
            "Apellidos:": (self.entries["Apellidos:"], self.last_name_var.get()),
            "Cédula:": (self.entries["Cédula:"], self.id_number_var.get()),
            "Rol:": (self.entries["Rol:"], self.role_var.get())
        }
        
        if not FieldFormatter.validate_required_fields(required_fields, self):
            return False
            
        if self.mode == "create":
            if not self.password_var.get():
                messagebox.showerror("Error", "La contraseña es requerida", parent=self)
                return False
                
            if self.password_var.get() != self.confirm_password_var.get():
                messagebox.showerror("Error", "Las contraseñas no coinciden", parent=self)
                return False
                
        return True

    def load_user_data(self) -> None:
        user = User.get_by_id(self.user_id)
        if not user:
            messagebox.showerror("Error", "No se pudo cargar el usuario", parent=self)
            self.destroy()
            return
        
        self.username_var.set(user['username'])
        self.first_name_var.set(user['first_name'])
        self.last_name_var.set(user['last_name'])
        self.id_number_var.set(user['id_number'])
        self.address_var.set(user['address'] or "")
        self.phone_var.set(user['phone'] or "")
        self.email_var.set(user['email'] or "")
        self.department_var.set(user['department'] or "")
        self.position_var.set(user['position'] or "")
        
        roles = Role.all()
        role = next((r for r in roles if r['id'] == user['role_id']), None)
        if role:
            # Traducimos el rol al español para mostrar
            translated_role = self.role_translation.get(role['name'].lower(), role['name'])
            self.role_var.set(translated_role)

    def create_user(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            # Obtenemos el rol en inglés para guardar en la base de datos
            selected_role_es = self.role_var.get()
            role_name_en = self.reverse_role_translation.get(selected_role_es, selected_role_es)
            
            person_id = Person.create(
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                id_number=self.id_number_var.get(),
                address=self.address_var.get() or None,
                phone=self.phone_var.get() or None,
                email=self.email_var.get() or None,
                department=self.department_var.get() or None,
                position=self.position_var.get() or None
            )
            
            role = next((r for r in Role.all() if r['name'].lower() == role_name_en.lower()), None)
            if not role:
                raise ValueError("Rol seleccionado no válido")
            
            User.create(
                username=self.username_var.get(),
                password=self.password_var.get(),
                person_id=person_id,
                role_id=role['id']
            )
            
            messagebox.showinfo("Éxito", "Usuario creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}", parent=self)

    def update_user(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            if not self.user_id:
                raise ValueError("ID de usuario no válido")
            
            user = User.get_by_id(self.user_id)
            if not user:
                raise ValueError("Usuario no encontrado")
            
            # Obtenemos el rol en inglés para guardar en la base de datos
            selected_role_es = self.role_var.get()
            role_name_en = self.reverse_role_translation.get(selected_role_es, selected_role_es)
            
            Person.update(
                person_id=user['person_id'],
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                id_number=self.id_number_var.get(),
                address=self.address_var.get() or None,
                phone=self.phone_var.get() or None,
                email=self.email_var.get() or None,
                department=self.department_var.get() or None,
                position=self.position_var.get() or None
            )
            
            role = next((r for r in Role.all() if r['name'].lower() == role_name_en.lower()), None)
            if not role:
                raise ValueError("Rol seleccionado no válido")
            
            password = self.password_var.get() if self.password_var.get() else None
            User.update(
                user_id=self.user_id,
                username=self.username_var.get(),
                person_id=user['person_id'],
                role_id=role['id'],
                password=password
            )
            
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el usuario: {str(e)}", parent=self)
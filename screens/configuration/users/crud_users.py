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
from utils.valdations import Validations

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
        self.geometry("500x600")
        self.resizable(False, False)
        
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
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and user_id:
            self.load_user_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Nuevo Usuario" if self.mode == "create" else "Editar Usuario"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Usuario:", self.username_var, 'text', True),
            ("Contraseña:", self.password_var, 'password', self.mode == "create"),
            ("Confirmar Contraseña:", self.confirm_password_var, 'password', self.mode == "create"),
            ("Nombres:", self.first_name_var, 'text', True),
            ("Apellidos:", self.last_name_var, 'text', True),
            ("Cédula:", self.id_number_var, 'text', True),
            ("Dirección:", self.address_var, 'text', True),
            ("Teléfono:", self.phone_var, 'text', True),
            ("Correo:", self.email_var, 'text', True),
            ("Departamento:", self.department_var, 'text', True),
            ("Cargo:", self.position_var, 'text', True),
            ("Rol:", self.role_var, None, True)
        ]
        
        for i, (label, var, val_type, editable) in enumerate(fields, start=1):
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 10),
                fg="#555"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=3)
            
            if label == "Rol:":
                # Obtener roles
                roles = Role.all()
                values = [role['name'] for role in roles]
                
                combobox = CustomCombobox(
                    main_frame,
                    textvariable=var,
                    values=values,
                    state="readonly",
                    width=30
                )
                combobox.grid(row=i, column=1, sticky="ew", pady=3, padx=5)
                self.entries[label] = combobox
            else:
                entry = CustomEntry(
                    main_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    width=32,
                    state="normal" if editable else "readonly",
                    show="*" if val_type == 'password' else None
                )
                
                if val_type == 'text':
                    entry.bind("<KeyRelease>", lambda e, func=self.validate_text: self.validate_entry(e, func))
                
                entry.grid(row=i, column=1, sticky="ew", pady=3, padx=5)
                self.entries[label] = entry
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(15, 5))
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Guardar", 
                command=self.create_user,
                padding=8,
                width=15
            )
        else:
            btn_action = CustomButton(
                btn_frame, 
                text="Actualizar", 
                command=self.update_user,
                padding=8,
                width=15
            )
            
        btn_action.pack(side=tk.LEFT, padx=5)
            
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

    def validate_entry(self, event: tk.Event, validation_func: Callable[[str], bool]) -> None:
        Validations.validate_entry(event, validation_func)

    def validate_text(self, text: str) -> bool:
        return Validations.validate_text(text)

    def validate_required_fields(self) -> bool:
        required_fields = {
            "Usuario:": self.username_var.get(),
            "Nombres:": self.first_name_var.get(),
            "Apellidos:": self.last_name_var.get(),
            "Cédula:": self.id_number_var.get(),
            "Rol:": self.role_var.get()
        }
        
        if not Validations.validate_required_fields(self.entries, required_fields, self):
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
        
        # Establecer rol
        roles = Role.all()
        role = next((r for r in roles if r['id'] == user['role_id']), None)
        if role:
            self.role_var.set(role['name'])

    def create_user(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            # Primero crear persona
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
            
            # Obtener ID del rol
            role = next((r for r in Role.all() if r['name'] == self.role_var.get()), None)
            if not role:
                raise ValueError("Rol seleccionado no válido")
            
            # Crear usuario
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
            
            # Obtener datos actuales del usuario
            user = User.get_by_id(self.user_id)
            if not user:
                raise ValueError("Usuario no encontrado")
            
            # Actualizar persona
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
            
            # Obtener ID del rol
            role = next((r for r in Role.all() if r['name'] == self.role_var.get()), None)
            if not role:
                raise ValueError("Rol seleccionado no válido")
            
            # Actualizar usuario
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
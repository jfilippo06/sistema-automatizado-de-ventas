import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from utils.valdations import Validations
from sqlite_cli.models.customer_model import Customer

class CrudCustomer(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        customer_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None,
        initial_id_number: Optional[str] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.customer_id = customer_id
        self.refresh_callback = refresh_callback
        
        self.title("Nuevo Cliente" if mode == "create" else "Editar Cliente")
        self.geometry("380x400")  # Aumenté el tamaño para mejor visualización
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")  # Fondo general
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.id_number_var = tk.StringVar(value=initial_id_number if initial_id_number else "")
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and customer_id:
            self.load_customer_data()

    def configure_ui(self) -> None:
        # Frame principal con fondo gris claro
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título con estilo azul
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        title_text = "Nuevo Cliente" if self.mode == "create" else "Editar Cliente"
        title_label = CustomLabel(
            title_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.pack(pady=10, padx=10, anchor="w")
        
        # Campos del formulario con validaciones específicas
        fields = [
            ("Nombres:", self.first_name_var, 'text', self.mode == "create"),
            ("Apellidos:", self.last_name_var, 'text', self.mode == "create"),
            ("Cédula:", self.id_number_var, 'id_number', self.mode == "create"),
            ("Email:", self.email_var, 'email', True),
            ("Teléfono:", self.phone_var, 'phone', True),
            ("Dirección:", self.address_var, 'text', True)
        ]
        
        for i, (label, var, val_type, editable) in enumerate(fields, start=1):
            # Frame para cada campo (mejor alineación)
            field_frame = tk.Frame(main_frame, bg="#f5f5f5")
            field_frame.grid(row=i, column=0, columnspan=2, sticky="ew", pady=5)
            
            field_label = CustomLabel(
                field_frame,
                text=label,
                font=("Arial", 10),
                fg="#333",
                bg="#f5f5f5",
                width=15,
                anchor="w"
            )
            field_label.pack(side=tk.LEFT, padx=(0, 10))
            
            entry = CustomEntry(
                field_frame,
                textvariable=var,
                font=("Arial", 10),
                width=30,
                state="normal" if editable else "readonly"
            )
            
            # Configurar validaciones según el tipo de campo
            if val_type == 'id_number':
                entry.configure(validate="key")
                entry.configure(validatecommand=(entry.register(self.validate_id_number), '%P'))
            elif val_type == 'phone':
                entry.configure(validate="key")
                entry.configure(validatecommand=(entry.register(self.validate_phone), '%P'))
            elif val_type == 'email':
                entry.bind("<FocusOut>", lambda e, entry=entry: self.validate_email(entry.get()))
            else:  # text
                entry.bind("<KeyRelease>", lambda e, func=Validations.validate_text: Validations.validate_entry(e, func))
            
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            self.entries[label] = entry
        
        # Frame para los botones con mejor espaciado
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(30, 10), sticky="e")
        
        # Botón Cancelar
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        # Botón Guardar/Actualizar
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Guardar", 
                command=self.create_customer,
                padding=8,
                width=12
            )
        else:
            btn_action = CustomButton(
                btn_frame, 
                text="Actualizar", 
                command=self.update_customer,
                padding=8,
                width=12
            )
        btn_action.pack(side=tk.RIGHT, padx=5)

    def validate_id_number(self, text: str) -> bool:
        """Valida que el texto sea un número de cédula válido (solo números, máximo 10 dígitos)"""
        if not text:
            return True
        return text.isdigit() and len(text) <= 10

    def validate_phone(self, text: str) -> bool:
        """Valida que el texto sea un número de teléfono válido"""
        if not text:
            return True
        # Permite números, espacios, guiones y paréntesis
        return all(c.isdigit() or c in ' +-()' for c in text)

    def validate_email(self, email: str) -> bool:
        """Valida el formato del email si se ha ingresado uno"""
        if email and not Validations.validate_email(email):
            messagebox.showwarning("Email inválido", 
                                 "El formato del email no es válido", 
                                 parent=self)
            return False
        return True

    def validate_required_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos y sean válidos"""
        required_fields = {
            "Nombres:": self.first_name_var.get(),
            "Apellidos:": self.last_name_var.get(),
            "Cédula:": self.id_number_var.get()
        }
        
        # Validar campos requeridos
        for label, value in required_fields.items():
            if not value:
                messagebox.showwarning("Campo requerido", 
                                     f"El campo {label[:-1]} es obligatorio", 
                                     parent=self)
                self.entries[label].focus_set()
                return False
        
        # Validaciones específicas
        if not self.validate_id_number(self.id_number_var.get()):
            messagebox.showwarning("Cédula inválida", 
                                 "La cédula debe contener solo números (máximo 10 dígitos)", 
                                 parent=self)
            self.entries["Cédula:"].focus_set()
            return False
            
        if self.email_var.get() and not Validations.validate_email(self.email_var.get()):
            messagebox.showwarning("Email inválido", 
                                 "El formato del email no es válido", 
                                 parent=self)
            self.entries["Email:"].focus_set()
            return False
            
        return True

    def load_customer_data(self) -> None:
        """Carga los datos de un cliente existente para editar."""
        try:
            if not self.customer_id:
                raise ValueError("ID de cliente no válido")
                
            customer = Customer.get_by_id(self.customer_id)
            if not customer:
                raise ValueError("Cliente no encontrado")
            
            self.first_name_var.set(customer['first_name'])
            self.last_name_var.set(customer['last_name'])
            self.id_number_var.set(customer['id_number'])
            self.email_var.set(customer.get('email', ''))
            self.phone_var.set(customer.get('phone', ''))
            self.address_var.set(customer.get('address', ''))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}", parent=self)
            self.destroy()

    def create_customer(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            # Verificar si la cédula ya existe
            existing_customer = Customer.get_by_id_number(self.id_number_var.get())
            if existing_customer:
                messagebox.showwarning("Cédula existente", 
                                     "Ya existe un cliente con esta cédula", 
                                     parent=self)
                return
            
            Customer.create(
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                id_number=self.id_number_var.get(),
                email=self.email_var.get() or None,
                phone=self.phone_var.get() or None,
                address=self.address_var.get() or None
            )
            
            messagebox.showinfo("Éxito", "Cliente creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el cliente: {str(e)}", parent=self)

    def update_customer(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            if not self.customer_id:
                raise ValueError("ID de cliente no válido")
            
            Customer.update(
                customer_id=self.customer_id,
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                id_number=self.id_number_var.get(),
                email=self.email_var.get() or None,
                phone=self.phone_var.get() or None,
                address=self.address_var.get() or None
            )
            
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente: {str(e)}", parent=self)
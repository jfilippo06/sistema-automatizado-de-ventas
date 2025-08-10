import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from utils.field_formatter import FieldFormatter
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
        self.geometry("400x450")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
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
        """Configura la interfaz de usuario con el nuevo diseño"""
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título centrado
        title_text = "Nuevo Cliente" if self.mode == "create" else "Editar Cliente"
        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(pady=(0, 15))
        
        title_label = CustomLabel(
            title_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.pack(expand=True)
        
        # Marco principal con borde
        form_frame = tk.LabelFrame(
            main_frame,
            text="Información del Cliente",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#555",
            padx=15,
            pady=15,
            relief=tk.GROOVE,
            borderwidth=2
        )
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Definición de campos con sus tipos de formateo
        fields = [
            ("Nombres:", self.first_name_var, 'name', self.mode == "create"),
            ("Apellidos:", self.last_name_var, 'name', self.mode == "create"),
            ("Cédula:", self.id_number_var, 'integer', self.mode == "create"),
            ("Email:", self.email_var, 'email', True),
            ("Teléfono:", self.phone_var, 'phone', True),
            ("Dirección:", self.address_var, 'address', True)
        ]
        
        for i, (label, var, field_type, editable) in enumerate(fields):
            # Frame para cada fila
            row_frame = tk.Frame(form_frame, bg="#f5f5f5")
            row_frame.grid(row=i, column=0, sticky="ew", pady=5)
            
            field_label = CustomLabel(
                row_frame,
                text=label,
                font=("Arial", 12),
                fg="#555",
                bg="#f5f5f5",
                width=12,
                anchor="w"
            )
            field_label.pack(side=tk.LEFT, padx=(0, 10))
            
            entry = CustomEntry(
                row_frame,
                textvariable=var,
                font=("Arial", 12),
                width=25,
                state="normal" if editable else "readonly"
            )
            
            if editable:
                FieldFormatter.bind_validation(entry, field_type)
            
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.entries[label] = entry
        
        # Frame para botones con borde
        btn_frame = tk.LabelFrame(
            main_frame,
            bg="#f5f5f5",
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=8
        )
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Contenedor interno para centrar botones
        btn_container = tk.Frame(btn_frame, bg="#f5f5f5")
        btn_container.pack(expand=True)
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_container, 
                text="Guardar", 
                command=self.create_customer,
                padding=8,
                width=12
            )
        else:
            btn_action = CustomButton(
                btn_container, 
                text="Actualizar", 
                command=self.update_customer,
                padding=8,
                width=12
            )
        btn_action.pack(side=tk.LEFT, padx=10)
        
        btn_cancel = CustomButton(
            btn_container, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=12
        )
        btn_cancel.pack(side=tk.LEFT, padx=10)

    def validate_required_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos"""
        required_fields = {
            "Nombres:": (self.entries["Nombres:"], self.first_name_var.get()),
            "Apellidos:": (self.entries["Apellidos:"], self.last_name_var.get()),
            "Cédula:": (self.entries["Cédula:"], self.id_number_var.get())
        }
        
        if not FieldFormatter.validate_required_fields(required_fields, self):
            return False
            
        # Validación adicional para email
        if self.email_var.get() and not FieldFormatter.validate_email_format(self.email_var.get(), self):
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
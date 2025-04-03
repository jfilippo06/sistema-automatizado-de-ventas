# screens/customers/crud_customer.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class CrudCustomer(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        item_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None,
        initial_id_number: Optional[str] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.item_id = item_id
        self.refresh_callback = refresh_callback
        
        self.title("Nuevo Cliente" if mode == "create" else "Editar Cliente")
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.id_number_var = tk.StringVar(value=initial_id_number if initial_id_number else "")
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_text = "Nuevo Cliente" if self.mode == "create" else "Editar Cliente"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Nombres:", self.first_name_var, 'text'),
            ("Apellidos:", self.last_name_var, 'text'),
            ("Cédula:", self.id_number_var, 'text'),
            ("Email:", self.email_var, 'text'),
            ("Teléfono:", self.phone_var, 'text'),
            ("Dirección:", self.address_var, 'text'),
            ("Estado:", self.status_var, None)
        ]
        
        self.entries = {}
        
        for i, (label, var, val_type) in enumerate(fields, start=1):
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 10),
                fg="#555"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Estado:":
                values = [s['name'] for s in Status.all()]
                combobox = CustomCombobox(
                    main_frame,
                    textvariable=var,
                    values=values,
                    state="readonly",
                    width=27
                )
                combobox.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = combobox
            else:
                entry = CustomEntry(
                    main_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    width=30
                )
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = entry

        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 10))
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Crear", 
                command=self.create_item,
                padding=8,
                width=15
            )
        else:
            btn_action = CustomButton(
                btn_frame, 
                text="Actualizar", 
                command=self.update_item,
                padding=8,
                width=15
            )
            
        btn_action.pack(side=tk.LEFT, padx=10)
            
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=10)

    def load_item_data(self) -> None:
        """Carga los datos de un cliente existente para editar."""
        try:
            if not self.item_id:
                raise ValueError("ID de cliente no válido")
                
            customer = Customer.get_by_id(self.item_id)
            if not customer:
                raise ValueError("Cliente no encontrado")
            
            self.first_name_var.set(customer['first_name'])
            self.last_name_var.set(customer['last_name'])
            self.id_number_var.set(customer['id_number'])
            self.email_var.set(customer.get('email', ''))
            self.phone_var.set(customer.get('phone', ''))
            self.address_var.set(customer.get('address', ''))
            self.status_var.set(customer.get('status_name', 'Activo'))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}", parent=self)
            self.destroy()

    def validate_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos."""
        required_fields = {
            "Nombres:": self.first_name_var.get(),
            "Apellidos:": self.last_name_var.get(),
            "Cédula:": self.id_number_var.get()
        }
        
        for field_name, value in required_fields.items():
            if not value:
                messagebox.showwarning("Campo requerido", 
                                     f"El campo {field_name} es obligatorio", 
                                     parent=self)
                self.entries[field_name].focus_set()
                return False
                
        return True

    def create_item(self) -> None:
        if not self.validate_fields():
            return
            
        try:
            status = next((s for s in Status.all() if s['name'] == self.status_var.get()), None)
            if not status:
                raise ValueError("Estado no válido")
            
            Customer.create(
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                id_number=self.id_number_var.get(),
                email=self.email_var.get() if self.email_var.get() else None,
                phone=self.phone_var.get() if self.phone_var.get() else None,
                address=self.address_var.get() if self.address_var.get() else None,
                status_id=status['id']
            )
            
            messagebox.showinfo("Éxito", "Cliente creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el cliente: {str(e)}", parent=self)

    def update_item(self) -> None:
        if not self.validate_fields():
            return
            
        try:
            if not self.item_id:
                raise ValueError("ID de cliente no válido")
                
            status = next((s for s in Status.all() if s['name'] == self.status_var.get()), None)
            if not status:
                raise ValueError("Estado no válido")
            
            Customer.update(
                customer_id=self.item_id,
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                id_number=self.id_number_var.get(),
                email=self.email_var.get() if self.email_var.get() else None,
                phone=self.phone_var.get() if self.phone_var.get() else None,
                address=self.address_var.get() if self.address_var.get() else None,
                status_id=status['id']
            )
            
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente: {str(e)}", parent=self)
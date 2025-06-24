import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.field_formatter import FieldFormatter

class CrudSupplier(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        supplier_id: Optional[int] = None, 
        initial_id_number: Optional[str] = None,
        refresh_callback: Optional[Callable[[], None]] = None,
        lock_id_number: bool = False
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.supplier_id = supplier_id
        self.refresh_callback = refresh_callback
        self.lock_id_number = lock_id_number
        
        # Configuración de la ventana
        self.title("Guardar Proveedor" if mode == "create" else "Editar Proveedor")
        self.geometry("360x500")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.id_number_var = tk.StringVar(value=initial_id_number if initial_id_number else "")
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.tax_id_var = tk.StringVar()
        self.company_var = tk.StringVar()
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and supplier_id:
            self.load_supplier_data()

    def configure_ui(self) -> None:
        """Configura la interfaz de usuario"""
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Nuevo Proveedor" if self.mode == "create" else "Editar Proveedor"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Configuración de campos editables
        if self.mode == "create":
            code_editable = True
            id_number_editable = not self.lock_id_number
        else:
            code_editable = False
            id_number_editable = False
        
        # Campos del formulario con sus tipos
        fields = [
            ("Código:", self.code_var, 'code', code_editable),
            ("Cédula:", self.id_number_var, 'id_number', id_number_editable),
            ("Nombres:", self.first_name_var, 'first_name', True),
            ("Apellidos:", self.last_name_var, 'last_name', True),
            ("Dirección:", self.address_var, 'address', True),
            ("Teléfono:", self.phone_var, 'phone', True),
            ("Email:", self.email_var, 'email', True),
            ("RIF:", self.tax_id_var, 'tax_id', True),
            ("Empresa:", self.company_var, 'company', True)
        ]
        
        for i, (label, var, field_type, editable) in enumerate(fields, start=1):
            # Etiqueta del campo
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 12),
                fg="#555",
                bg="#f5f5f5"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            # Campo de entrada
            entry = CustomEntry(
                main_frame,
                textvariable=var,
                font=("Arial", 12),
                width=35,
                state="normal" if editable else "readonly"
            )
            
            # Configurar validación y formateo
            if editable:
                FieldFormatter.bind_validation(entry, field_type)
            
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            self.entries[label] = (entry, field_type)
        
        # Frame para botones
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        # Botón principal
        btn_action = CustomButton(
            btn_frame, 
            text="Guardar" if self.mode == "create" else "Actualizar", 
            command=self.create_supplier if self.mode == "create" else self.update_supplier,
            padding=10,
            width=15
        )
        btn_action.pack(side=tk.LEFT, padx=5)
        
        # Botón Cancelar
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=10,
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

    def validate_required_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos"""
        required_fields = {
            "Código:": (self.entries["Código:"][0], self.code_var.get()),
            "Cédula:": (self.entries["Cédula:"][0], self.id_number_var.get()),
            "Nombres:": (self.entries["Nombres:"][0], self.first_name_var.get()),
            "Apellidos:": (self.entries["Apellidos:"][0], self.last_name_var.get()),
            "Dirección:": (self.entries["Dirección:"][0], self.address_var.get()),
            "Teléfono:": (self.entries["Teléfono:"][0], self.phone_var.get()),
            "Email:": (self.entries["Email:"][0], self.email_var.get()),
            "RIF:": (self.entries["RIF:"][0], self.tax_id_var.get()),
            "Empresa:": (self.entries["Empresa:"][0], self.company_var.get())
        }
        
        if not FieldFormatter.validate_required_fields(required_fields, self):
            return False
            
        # Validación adicional para email
        if not FieldFormatter.validate_email_format(self.email_var.get(), self):
            return False
            
        return True

    def load_supplier_data(self) -> None:
        """Carga los datos del proveedor para edición"""
        supplier = Supplier.get_by_id(self.supplier_id)
        if not supplier:
            messagebox.showerror("Error", "No se pudo cargar el proveedor", parent=self)
            self.destroy()
            return
        
        self.code_var.set(supplier['code'])
        self.id_number_var.set(supplier['id_number'])
        self.first_name_var.set(supplier['first_name'])
        self.last_name_var.set(supplier['last_name'])
        self.address_var.set(supplier['address'])
        self.phone_var.set(supplier['phone'])
        self.email_var.set(supplier['email'])
        self.tax_id_var.set(supplier['tax_id'])
        self.company_var.set(supplier['company'])

    def create_supplier(self) -> None:
        """Crea un nuevo proveedor"""
        if not self.validate_required_fields():
            return
            
        try:
            Supplier.create(
                code=self.code_var.get(),
                id_number=self.id_number_var.get(),
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                address=self.address_var.get(),
                phone=self.phone_var.get(),
                email=self.email_var.get(),
                tax_id=self.tax_id_var.get(),
                company=self.company_var.get(),
                status_id=1
            )
            
            messagebox.showinfo("Éxito", "Proveedor creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el proveedor: {str(e)}", parent=self)

    def update_supplier(self) -> None:
        """Actualiza un proveedor existente"""
        if not self.validate_required_fields():
            return
            
        try:
            if not self.supplier_id:
                raise ValueError("ID de proveedor no válido")
            
            Supplier.update(
                supplier_id=self.supplier_id,
                code=self.code_var.get(),
                id_number=self.id_number_var.get(),
                first_name=self.first_name_var.get(),
                last_name=self.last_name_var.get(),
                address=self.address_var.get(),
                phone=self.phone_var.get(),
                email=self.email_var.get(),
                tax_id=self.tax_id_var.get(),
                company=self.company_var.get()
            )
            
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {str(e)}", parent=self)
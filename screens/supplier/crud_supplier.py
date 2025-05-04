import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.valdations import Validations

class CrudSupplier(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        supplier_id: Optional[int] = None, 
        initial_id_number: Optional[str] = None,
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.supplier_id = supplier_id
        self.refresh_callback = refresh_callback
        
        # Configuración de la ventana
        self.title("Guardar Proveedor" if mode == "create" else "Editar Proveedor")
        self.geometry("360x500")  # Tamaño más adecuado para los campos
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")  # Fondo consistente
        
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
        
        # Título con estilo consistente
        title_text = "Nuevo Proveedor" if self.mode == "create" else "Editar Proveedor"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var, 'text', not (self.mode == "edit")),
            ("Cédula:", self.id_number_var, 'number', True),
            ("Nombres:", self.first_name_var, 'text', True),
            ("Apellidos:", self.last_name_var, 'text', True),
            ("Dirección:", self.address_var, 'text', True),
            ("Teléfono:", self.phone_var, 'number', True),
            ("Email:", self.email_var, None, True),
            ("RIF:", self.tax_id_var, 'text', True),
            ("Empresa:", self.company_var, 'text', True)
        ]
        
        for i, (label, var, val_type, editable) in enumerate(fields, start=1):
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
            
            # Configurar validaciones
            if val_type == 'number':
                entry.configure(validate="key")
                entry.configure(validatecommand=(entry.register(self.validate_integer), '%P'))
            elif val_type == 'text':
                entry.bind("<KeyRelease>", lambda e, func=self.validate_text: self.validate_entry(e, func))
            
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            self.entries[label] = entry
        
        # Frame para botones
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        # Botón principal (Guardar/Actualizar)
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

    def validate_entry(self, event: tk.Event, validation_func: Callable[[str], bool]) -> None:
        """Valida la entrada del campo"""
        Validations.validate_entry(event, validation_func)

    def validate_text(self, text: str) -> bool:
        """Valida texto general"""
        return Validations.validate_text(text)

    def validate_integer(self, text: str) -> bool:
        """Valida números enteros"""
        return Validations.validate_integer(text)

    def validate_required_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos"""
        required_fields = {
            "Código:": self.code_var.get(),
            "Cédula:": self.id_number_var.get(),
            "Nombres:": self.first_name_var.get(),
            "Apellidos:": self.last_name_var.get(),
            "Dirección:": self.address_var.get(),
            "Teléfono:": self.phone_var.get(),
            "Email:": self.email_var.get(),
            "RIF:": self.tax_id_var.get(),
            "Empresa:": self.company_var.get()
        }
        
        if not Validations.validate_required_fields(self.entries, required_fields, self):
            return False
            
        numeric_fields = {
            "Cédula:": (self.id_number_var.get(), False),
            "Teléfono:": (self.phone_var.get(), False)
        }
            
        return Validations.validate_numeric_fields(numeric_fields, self)

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
                status_id=1  # Siempre activo al crear
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
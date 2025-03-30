import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry

class CrudSupplier(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        supplier_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.supplier_id = supplier_id
        self.refresh_callback = refresh_callback
        
        self.title("Agregar Proveedor" if mode == "create" else "Editar Proveedor")
        self.geometry("550x750")
        self.resizable(False, False)
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.id_number_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.tax_id_var = tk.StringVar()
        self.company_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
        self.configure_ui()
        
        if mode == "edit" and supplier_id:
            self.load_supplier_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Nuevo Proveedor" if self.mode == "create" else "Editar Proveedor"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var),
            ("Cédula:", self.id_number_var),
            ("Nombres:", self.first_name_var),
            ("Apellidos:", self.last_name_var),
            ("Dirección:", self.address_var),
            ("Teléfono:", self.phone_var),
            ("Email:", self.email_var),
            ("RIF:", self.tax_id_var),
            ("Empresa:", self.company_var),
            ("Estado:", self.status_var)
        ]
        
        for i, (label, var) in enumerate(fields, start=1):
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 10),
                fg="#555"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Estado:":
                self.status_combobox = ttk.Combobox(
                    main_frame, 
                    textvariable=var,
                    values=[status['name'] for status in Status.all()],
                    font=("Arial", 10),
                    state="readonly"
                )
                self.status_combobox.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            else:
                entry = CustomEntry(
                    main_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    width=30
                )
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 10))
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Agregar", 
                command=self.create_supplier,
                padding=8,
                width=15
            )
        else:
            btn_action = CustomButton(
                btn_frame, 
                text="Actualizar", 
                command=self.update_supplier,
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

    def load_supplier_data(self) -> None:
        supplier = Supplier.get_by_id(self.supplier_id)
        if not supplier:
            messagebox.showerror("Error", "No se pudo cargar el proveedor")
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
        self.status_var.set(supplier['status_name'])

    def create_supplier(self) -> None:
        try:
            # Validar campos requeridos
            if not all([
                self.code_var.get(),
                self.id_number_var.get(),
                self.company_var.get()
            ]):
                raise ValueError("Código, Cédula y Empresa son campos requeridos")
                
            # Obtener el ID del estado seleccionado
            status_name = self.status_var.get()
            status = next((s for s in Status.all() if s['name'] == status_name), None)
            if not status:
                raise ValueError("Estado no válido")
            
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
                status_id=status['id']
            )
            
            messagebox.showinfo("Éxito", "Proveedor creado correctamente")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el proveedor: {str(e)}")

    def update_supplier(self) -> None:
        try:
            if not self.supplier_id:
                raise ValueError("ID de proveedor no válido")
                
            # Validar campos requeridos
            if not all([
                self.code_var.get(),
                self.id_number_var.get(),
                self.company_var.get()
            ]):
                raise ValueError("Código, Cédula y Empresa son campos requeridos")
                
            # Obtener el ID del estado seleccionado
            status_name = self.status_var.get()
            status = next((s for s in Status.all() if s['name'] == status_name), None)
            if not status:
                raise ValueError("Estado no válido")
            
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
            
            # Actualizar el estado por separado
            Supplier.update_status(self.supplier_id, status['id'])
            
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {str(e)}")
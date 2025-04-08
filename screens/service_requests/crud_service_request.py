# screens/service_requests/crud_service_request.py
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from screens.customers.crud_customer import CrudCustomer
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.service_model import Service
from sqlite_cli.models.service_request_model import ServiceRequest
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.valdations import Validations

class CrudServiceRequest(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        item_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.item_id = item_id
        self.refresh_callback = refresh_callback
        self.customer_data = None
        self.service_data = None
        
        self.title("Nueva Solicitud" if mode == "create" else "Editar Solicitud")
        self.geometry("600x350")  # Reduced height since we removed status field
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.customer_id_var = tk.StringVar()
        self.customer_name_var = tk.StringVar()
        self.service_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")
        
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()
        else:
            self.enable_fields(False)

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_text = "Nueva Solicitud" if self.mode == "create" else "Editar Solicitud"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario (removed request_status field)
        fields = [
            ("Cédula Cliente:", self.customer_id_var, 'text', None if self.mode == "edit" else self.search_customer),
            ("Nombre Cliente:", self.customer_name_var, None, None),
            ("Servicio:", self.service_var, None, None),
            ("Descripción:", self.description_var, 'text', None),
            ("Cantidad:", self.quantity_var, 'number', None)
        ]
        
        self.entries = {}
        self.widgets = {}
        
        for i, (label, var, val_type, command) in enumerate(fields, start=1):
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 10),
                fg="#555"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Cédula Cliente:":
                entry_frame = tk.Frame(main_frame)
                entry_frame.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                
                entry = CustomEntry(
                    entry_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    width=20,
                    state="readonly" if self.mode == "edit" else "normal"
                )
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                if self.mode != "edit":
                    btn_search = CustomButton(
                        entry_frame,
                        text="Buscar",
                        command=command,
                        padding=4,
                        width=8
                    )
                    btn_search.pack(side=tk.LEFT, padx=5)
                    self.widgets[label] = (entry, btn_search)
                
                self.entries[label] = entry
            elif label in ["Nombre Cliente:", "Servicio:"]:
                if label == "Servicio:":
                    values = [s['name'] for s in Service.all()]
                    state = "readonly" if self.mode == "edit" else "disabled"
                else:  # Nombre Cliente
                    values = []
                    state = "disabled"
                
                combobox = CustomCombobox(
                    main_frame,
                    textvariable=var,
                    values=values,
                    state=state,
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
                
                if val_type == 'number':
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(entry.register(self.validate_integer), '%P'))
                
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = entry

        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 10))
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Guadar", 
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

    def validate_integer(self, text: str) -> bool:
        return Validations.validate_integer(text)

    def search_customer(self) -> None:
        """Busca un cliente por su cédula."""
        id_number = self.customer_id_var.get().strip()
        if not id_number:
            messagebox.showwarning("Advertencia", "Ingrese una cédula para buscar", parent=self)
            return
        
        try:
            customer = Customer.get_by_id_number(id_number)
            if customer:
                self.customer_data = customer
                self.customer_name_var.set(f"{customer['first_name']} {customer['last_name']}")
                self.enable_fields(True)
            else:
                response = messagebox.askyesno(
                    "Cliente no encontrado", 
                    "El cliente no está registrado. ¿Desea registrarlo ahora?",
                    parent=self
                )
                if response:
                    self.register_new_customer(id_number)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el cliente: {str(e)}", parent=self)

    def register_new_customer(self, id_number: str) -> None:
        """Abre la pantalla para registrar un nuevo cliente."""
        def on_customer_created():
            self.search_customer()
        
        CrudCustomer(
            self,
            mode="create",
            initial_id_number=id_number,
            refresh_callback=on_customer_created
        )

    def enable_fields(self, enable: bool) -> None:
        """Habilita o deshabilita los campos según si hay un cliente seleccionado."""
        state = "normal" if enable else "disabled"
        readonly_state = "readonly" if enable else "disabled"
        
        self.entries["Servicio:"].configure(state=readonly_state)
        self.entries["Descripción:"].configure(state=state)
        self.entries["Cantidad:"].configure(state=state)

    def load_item_data(self) -> None:
        """Carga los datos de una solicitud existente para editar."""
        try:
            if not self.item_id:
                raise ValueError("ID de solicitud no válido")
                
            request = ServiceRequest.get_by_id(self.item_id)
            if not request:
                raise ValueError("Solicitud no encontrada")
            
            # Cargar datos del cliente
            customer = Customer.get_by_id(request['customer_id'])
            if customer:
                self.customer_data = customer
                self.customer_id_var.set(customer['id_number'])
                self.customer_name_var.set(f"{customer['first_name']} {customer['last_name']}")
            
            # Cargar datos del servicio
            service = Service.get_by_id(request['service_id'])
            if service:
                self.service_var.set(service['name'])
            
            # Cargar otros datos
            self.description_var.set(request['description'])
            self.quantity_var.set(str(request['quantity']))
            
            # Habilitar campos
            self.enable_fields(True)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}", parent=self)
            self.destroy()

    def validate_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos."""
        required_fields = {
            "Cédula Cliente:": self.customer_id_var.get(),
            "Servicio:": self.service_var.get(),
            "Descripción:": self.description_var.get(),
            "Cantidad:": self.quantity_var.get()
        }
        
        if not Validations.validate_required_fields(self.entries, required_fields, self):
            return False
            
        numeric_fields = {
            "Cantidad:": (self.quantity_var.get(), False)
        }
            
        return Validations.validate_numeric_fields(numeric_fields, self)

    def create_item(self) -> None:
        if not self.validate_fields():
            return
            
        try:
            if not self.customer_data:
                raise ValueError("Cliente no seleccionado")
                
            service_name = self.service_var.get()
            service = next((s for s in Service.all() if s['name'] == service_name), None)
            if not service:
                raise ValueError("Servicio no válido")
            
            ServiceRequest.create(
                customer_id=self.customer_data['id'],
                service_id=service['id'],
                description=self.description_var.get(),
                quantity=int(self.quantity_var.get())
            )
            
            messagebox.showinfo("Éxito", "Solicitud creada correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la solicitud: {str(e)}", parent=self)

    def update_item(self) -> None:
        if not self.validate_fields():
            return
            
        try:
            if not self.item_id:
                raise ValueError("ID de solicitud no válido")
                
            if not self.customer_data:
                raise ValueError("Cliente no seleccionado")
                
            service_name = self.service_var.get()
            service = next((s for s in Service.all() if s['name'] == service_name), None)
            if not service:
                raise ValueError("Servicio no válido")
            
            ServiceRequest.update(
                request_id=self.item_id,
                customer_id=self.customer_data['id'],
                service_id=service['id'],
                description=self.description_var.get(),
                quantity=int(self.quantity_var.get())
            )
            
            messagebox.showinfo("Éxito", "Solicitud actualizada correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la solicitud: {str(e)}", parent=self)
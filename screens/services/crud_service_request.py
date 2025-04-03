# screens/services/crud_service_request.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, Any
from screens.customers.crud_customer import CrudCustomer
from sqlite_cli.database.database import get_db_connection
from sqlite_cli.models.customer_model import Customer
from sqlite_cli.models.service_model import Service
from sqlite_cli.models.service_request_model import ServiceRequest
from sqlite_cli.models.status_model import Status
from sqlite_cli.models.request_status_model import RequestStatus
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

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
        self.geometry("600x500")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.customer_id_var = tk.StringVar()
        self.customer_name_var = tk.StringVar()
        self.service_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")
        self.request_status_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
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
        
        # Campos del formulario
        fields = [
            ("Cédula Cliente:", self.customer_id_var, 'text', self.search_customer),
            ("Nombre Cliente:", self.customer_name_var, None, None),
            ("Servicio:", self.service_var, None, None),
            ("Descripción:", self.description_var, 'text', None),
            ("Cantidad:", self.quantity_var, 'number', None),
            ("Estado Solicitud:", self.request_status_var, None, None),
            ("Estado:", self.status_var, None, None)
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
                    width=20
                )
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                btn_search = CustomButton(
                    entry_frame,
                    text="Buscar",
                    command=command,
                    padding=4,
                    width=8
                )
                btn_search.pack(side=tk.LEFT, padx=5)
                
                self.entries[label] = entry
                self.widgets[label] = (entry, btn_search)
            elif label in ["Nombre Cliente:", "Servicio:", "Estado Solicitud:", "Estado:"]:
                if label == "Servicio:":
                    values = [s['name'] for s in Service.all()]
                    state = "readonly" if self.mode == "edit" else "disabled"
                elif label == "Estado Solicitud:":
                    values = [s['name'] for s in RequestStatus.all()]
                    state = "readonly"
                elif label == "Estado:":
                    values = [s['name'] for s in Status.all()]
                    state = "readonly"
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

    def validate_integer(self, text: str) -> bool:
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False

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
            # Después de crear el cliente, intentar buscarlo de nuevo
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
        self.entries["Estado Solicitud:"].configure(state=readonly_state)
        self.entries["Estado:"].configure(state=readonly_state)

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
            self.request_status_var.set(request.get('request_status_name', 'Iniciado'))
            self.status_var.set(request.get('status_name', 'Activo'))
            
            # Habilitar campos
            self.enable_fields(True)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}", parent=self)
            self.destroy()

    @staticmethod
    def get_by_id(request_id: int) -> Optional[Dict]:
        """Obtiene una solicitud por su ID con información relacionada."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sr.*, 
                   c.first_name, c.last_name, c.id_number,
                   s.name as service_name,
                   rs.name as request_status_name,
                   st.name as status_name
            FROM service_requests sr
            JOIN customers c ON sr.customer_id = c.id
            JOIN services s ON sr.service_id = s.id
            JOIN request_status rs ON sr.request_status_id = rs.id
            JOIN status st ON sr.status_id = st.id
            WHERE sr.id = ?
        ''', (request_id,))
        item = cursor.fetchone()
        conn.close()
        return dict(item) if item else None

    def validate_fields(self) -> bool:
        """Valida que todos los campos requeridos estén completos."""
        required_fields = {
            "Cédula Cliente:": self.customer_id_var.get(),
            "Servicio:": self.service_var.get(),
            "Descripción:": self.description_var.get(),
            "Cantidad:": self.quantity_var.get(),
            "Estado Solicitud:": self.request_status_var.get()
        }
        
        for field_name, value in required_fields.items():
            if not value:
                messagebox.showwarning("Campo requerido", 
                                     f"El campo {field_name} es obligatorio", 
                                     parent=self)
                self.entries[field_name].focus_set()
                return False
                
        try:
            int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido", parent=self)
            return False
            
        return True

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
                
            request_status = next((rs for rs in RequestStatus.all() if rs['name'] == self.request_status_var.get()), None)
            if not request_status:
                raise ValueError("Estado de solicitud no válido")
                
            status = next((s for s in Status.all() if s['name'] == self.status_var.get()), None)
            if not status:
                raise ValueError("Estado no válido")
            
            ServiceRequest.create(
                customer_id=self.customer_data['id'],
                service_id=service['id'],
                description=self.description_var.get(),
                quantity=int(self.quantity_var.get()),
                request_status_id=request_status['id'],
                status_id=status['id']
            )
            
            messagebox.showinfo("Éxito", "Solicitud creada correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la solicitud: {str(e)}", parent=self)

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
                
            request_status = next((rs for rs in RequestStatus.all() if rs['name'] == self.request_status_var.get()), None)
            if not request_status:
                raise ValueError("Estado de solicitud no válido")
                
            status = next((s for s in Status.all() if s['name'] == self.status_var.get()), None)
            if not status:
                raise ValueError("Estado no válido")
            
            ServiceRequest.update(
                request_id=self.item_id,
                customer_id=self.customer_data['id'],
                service_id=service['id'],
                description=self.description_var.get(),
                quantity=int(self.quantity_var.get()),
                request_status_id=request_status['id'],
                status_id=status['id']
            )
            
            messagebox.showinfo("Éxito", "Solicitud actualizada correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la solicitud: {str(e)}", parent=self)
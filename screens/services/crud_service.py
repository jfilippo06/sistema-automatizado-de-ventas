import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.service_model import Service
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from utils.valdations import Validations

class CrudService(tk.Toplevel):
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
        
        self.title("Nuevo Servicio" if mode == "create" else "Editar Servicio")
        self.geometry("400x350")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar(value="0.0")
        self.description_var = tk.StringVar()
        
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_text = "Nuevo Servicio" if self.mode == "create" else "Editar Servicio"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var, 'text', not (self.mode == "edit")),
            ("Nombre:", self.name_var, 'text', True),
            ("Precio:", self.price_var, 'decimal', True),
            ("Descripción:", self.description_var, 'text', True)
        ]
        
        self.entries = {}
        
        for i, (label, var, val_type, editable) in enumerate(fields, start=1):
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 10),
                fg="#555"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            entry = CustomEntry(
                main_frame,
                textvariable=var,
                font=("Arial", 10),
                width=30,
                state="normal" if editable else "readonly"
            )
                
            if val_type == 'decimal':
                entry.configure(validate="key")
                entry.configure(validatecommand=(entry.register(self.validate_decimal), '%P'))
                
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

    def validate_decimal(self, text: str) -> bool:
        return Validations.validate_decimal(text)

    def validate_fields(self) -> bool:
        required_fields = {
            "Código:": self.code_var.get(),
            "Nombre:": self.name_var.get(),
            "Precio:": self.price_var.get()
        }
        
        if not Validations.validate_required_fields(self.entries, required_fields, self):
            return False
            
        numeric_fields = {
            "Precio:": (self.price_var.get(), True)
        }
            
        return Validations.validate_numeric_fields(numeric_fields, self)

    def load_item_data(self) -> None:
        try:
            if not self.item_id:
                raise ValueError("ID de servicio no válido")
                
            service = Service.get_by_id(self.item_id)
            if not service:
                raise ValueError("Servicio no encontrado")
            
            self.code_var.set(service['code'])
            self.name_var.set(service['name'])
            self.price_var.set(str(service['price']))
            self.description_var.set(service.get('description', ''))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}", parent=self)
            self.destroy()

    def create_item(self) -> None:
        if not self.validate_fields():
            return
            
        try:
            Service.create(
                code=self.code_var.get(),
                name=self.name_var.get(),
                price=float(self.price_var.get()),
                description=self.description_var.get() if self.description_var.get() else None
            )
            
            messagebox.showinfo("Éxito", "Servicio creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el servicio: {str(e)}", parent=self)

    def update_item(self) -> None:
        if not self.validate_fields():
            return
            
        try:
            if not self.item_id:
                raise ValueError("ID de servicio no válido")
                
            Service.update(
                service_id=self.item_id,
                code=self.code_var.get(),
                name=self.name_var.get(),
                price=float(self.price_var.get()),
                description=self.description_var.get() if self.description_var.get() else None
            )
            
            messagebox.showinfo("Éxito", "Servicio actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el servicio: {str(e)}", parent=self)
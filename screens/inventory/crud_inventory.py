import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class CrudInventory(tk.Toplevel):
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
        
        self.title("Agregar Producto" if mode == "create" else "Editar Producto")
        self.geometry("500x650")
        self.resizable(False, False)
        
        # Establecer relación con la ventana padre
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="0")
        self.stock_var = tk.StringVar(value="0")
        self.price_var = tk.StringVar(value="0.0")
        self.status_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_text = "Nuevo Producto" if self.mode == "create" else "Editar Producto"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var, 'text'),
            ("Producto:", self.product_var, 'text'),
            ("Cantidad:", self.quantity_var, 'number'),
            ("Stock:", self.stock_var, 'number'),
            ("Precio:", self.price_var, 'decimal'),
            ("Estado:", self.status_var, None),
            ("Proveedor:", self.supplier_var, None)
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
            
            if label in ["Estado:", "Proveedor:"]:
                values = []
                if label == "Estado:":
                    values = [status['name'] for status in Status.all()]
                    state = "readonly"
                else:
                    values = [f"{supplier['company']} ({supplier['code']})" for supplier in Supplier.all()]
                    state = "normal"
                
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
                elif val_type == 'decimal':
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(entry.register(self.validate_decimal), '%P'))
                else:  # text
                    entry.bind("<KeyRelease>", lambda e, func=self.validate_text: self.validate_entry(e, func))
                
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = entry

        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 10))
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Agregar", 
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

    # Métodos de validación
    def validate_entry(self, event: tk.Event, validation_func: Callable[[str], bool]) -> None:
        widget = event.widget
        current_text = widget.get()
        
        if not validation_func(current_text):
            widget.delete(0, tk.END)
            widget.insert(0, current_text[:-1])

    def validate_text(self, text: str) -> bool:
        return all(c.isalpha() or c.isspace() or c.isdigit() for c in text) if text else True

    def validate_integer(self, text: str) -> bool:
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False

    def validate_decimal(self, text: str) -> bool:
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False

    def validate_required_fields(self) -> bool:
        required_fields = {
            "Código:": self.code_var.get(),
            "Producto:": self.product_var.get(),
            "Cantidad:": self.quantity_var.get(),
            "Precio:": self.price_var.get(),
            "Estado:": self.status_var.get()
        }
        
        for field_name, value in required_fields.items():
            if not value:
                messagebox.showwarning("Campo requerido", 
                                     f"El campo {field_name} es obligatorio", 
                                     parent=self)
                self.entries[field_name].focus_set()
                return False
                
        # Validar valores numéricos
        try:
            int(self.quantity_var.get())
            float(self.price_var.get())
            if self.stock_var.get():
                int(self.stock_var.get())
        except ValueError:
            messagebox.showerror("Error", "Los valores numéricos no son válidos", parent=self)
            return False
            
        return True

    def load_item_data(self) -> None:
        item = InventoryItem.get_by_id(self.item_id)
        if not item:
            messagebox.showerror("Error", "No se pudo cargar el producto", parent=self)
            self.destroy()
            return
        
        self.code_var.set(item['code'])
        self.product_var.set(item['product'])
        self.quantity_var.set(str(item['quantity']))
        self.stock_var.set(str(item['stock']))
        self.price_var.set(str(item['price']))
        self.status_var.set(item['status_name'])
        
        if item.get('supplier_company'):
            suppliers = Supplier.all()
            supplier = next((s for s in suppliers if s['id'] == item['supplier_id']), None)
            if supplier:
                self.supplier_var.set(f"{supplier['company']} ({supplier['code']})")

    def create_item(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            status = next((s for s in Status.all() if s['name'] == self.status_var.get()), None)
            if not status:
                raise ValueError("Estado no válido")
            
            supplier_id = None
            if self.supplier_var.get():
                supplier_code = self.supplier_var.get().split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.all() if s['code'] == supplier_code), None)
                if supplier:
                    supplier_id = supplier['id']
            
            InventoryItem.create(
                code=self.code_var.get(),
                product=self.product_var.get(),
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()) if self.stock_var.get() else 0,
                price=float(self.price_var.get()),
                status_id=status['id'],
                supplier_id=supplier_id
            )
            
            messagebox.showinfo("Éxito", "Producto creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el producto: {str(e)}", parent=self)

    def update_item(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            if not self.item_id:
                raise ValueError("ID de producto no válido")
                
            status = next((s for s in Status.all() if s['name'] == self.status_var.get()), None)
            if not status:
                raise ValueError("Estado no válido")
            
            supplier_id = None
            if self.supplier_var.get():
                supplier_code = self.supplier_var.get().split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.all() if s['code'] == supplier_code), None)
                if supplier:
                    supplier_id = supplier['id']
            
            InventoryItem.update(
                item_id=self.item_id,
                code=self.code_var.get(),
                product=self.product_var.get(),
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()) if self.stock_var.get() else 0,
                price=float(self.price_var.get()),
                status_id=status['id'],
                supplier_id=supplier_id
            )
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {str(e)}", parent=self)
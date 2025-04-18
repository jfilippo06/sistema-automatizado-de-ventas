import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.valdations import Validations

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
        
        self.title("Guardar Producto" if mode == "create" else "Editar Producto")
        self.geometry("380x380")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="0")
        self.stock_var = tk.StringVar(value="0")
        self.price_var = tk.StringVar(value="0.0")
        self.supplier_var = tk.StringVar()
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        main_frame = tk.Frame(self, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Nuevo Producto" if self.mode == "create" else "Editar Producto"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var, 'text', not (self.mode == "edit")),
            ("Producto:", self.product_var, 'text', True),
            ("Cantidad:", self.quantity_var, 'number', True),
            ("Stock:", self.stock_var, 'number', True),
            ("Precio:", self.price_var, 'decimal', True),
            ("Proveedor:", self.supplier_var, None, True)
        ]
        
        for i, (label, var, val_type, editable) in enumerate(fields, start=1):
            field_label = CustomLabel(
                main_frame,
                text=label,
                font=("Arial", 10),
                fg="#555"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=3)
            
            if label == "Proveedor:":
                # Obtener proveedores activos
                suppliers = Supplier.search_active()
                values = [f"{supplier['company']} ({supplier['code']})" for supplier in suppliers]
                
                combobox = CustomCombobox(
                    main_frame,
                    textvariable=var,
                    values=values,
                    state="readonly",
                    width=30
                )
                combobox.grid(row=i, column=1, sticky="ew", pady=3, padx=5)
                self.entries[label] = combobox
            else:
                entry = CustomEntry(
                    main_frame,
                    textvariable=var,
                    font=("Arial", 10),
                    width=32,
                    state="normal" if editable else "readonly"
                )
                
                if val_type == 'number':
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(entry.register(self.validate_integer), '%P'))
                elif val_type == 'decimal':
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(entry.register(self.validate_decimal), '%P'))
                else:  # text
                    entry.bind("<KeyRelease>", lambda e, func=self.validate_text: self.validate_entry(e, func))
                
                entry.grid(row=i, column=1, sticky="ew", pady=3, padx=5)
                self.entries[label] = entry
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(15, 5))
        
        if self.mode == "create":
            btn_action = CustomButton(
                btn_frame, 
                text="Guardar", 
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
            
        btn_action.pack(side=tk.LEFT, padx=5)
            
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=8,
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

    def validate_entry(self, event: tk.Event, validation_func: Callable[[str], bool]) -> None:
        Validations.validate_entry(event, validation_func)

    def validate_text(self, text: str) -> bool:
        return Validations.validate_text(text)

    def validate_integer(self, text: str) -> bool:
        return Validations.validate_integer(text)

    def validate_decimal(self, text: str) -> bool:
        return Validations.validate_decimal(text)

    def validate_required_fields(self) -> bool:
        required_fields = {
            "Código:": self.code_var.get(),
            "Producto:": self.product_var.get(),
            "Cantidad:": self.quantity_var.get(),
            "Precio:": self.price_var.get()
        }
        
        if not Validations.validate_required_fields(self.entries, required_fields, self):
            return False
            
        numeric_fields = {
            "Cantidad:": (self.quantity_var.get(), False),
            "Stock:": (self.stock_var.get(), False),
            "Precio:": (self.price_var.get(), True)
        }
            
        return Validations.validate_numeric_fields(numeric_fields, self)

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
        
        if item.get('supplier_id'):
            suppliers = Supplier.search_active()
            supplier = next((s for s in suppliers if s['id'] == item['supplier_id']), None)
            if supplier:
                self.supplier_var.set(f"{supplier['company']} ({supplier['code']})")

    def create_item(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            supplier_id = None
            if self.supplier_var.get():
                supplier_code = self.supplier_var.get().split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.search_active() if s['code'] == supplier_code), None)
                if supplier:
                    supplier_id = supplier['id']
            
            InventoryItem.create(
                code=self.code_var.get(),
                product=self.product_var.get(),
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()) if self.stock_var.get() else 0,
                price=float(self.price_var.get()),
                supplier_id=supplier_id
            )
            
            messagebox.showinfo("Éxito", "Producto creado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto: {str(e)}", parent=self)

    def update_item(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            if not self.item_id:
                raise ValueError("ID de producto no válido")
            
            supplier_id = None
            if self.supplier_var.get():
                supplier_code = self.supplier_var.get().split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.search_active() if s['code'] == supplier_code), None)
                if supplier:
                    supplier_id = supplier['id']
            
            InventoryItem.update(
                item_id=self.item_id,
                code=self.code_var.get(),
                product=self.product_var.get(),
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()) if self.stock_var.get() else 0,
                price=float(self.price_var.get()),
                supplier_id=supplier_id
            )
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {str(e)}", parent=self)
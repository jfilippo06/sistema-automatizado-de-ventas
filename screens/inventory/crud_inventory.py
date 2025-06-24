import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.field_formatter import FieldFormatter
from PIL import Image, ImageTk
import os

class CrudInventory(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        item_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None,
        from_sales: bool = False,
        sales_callback: Optional[Callable[[Dict], None]] = None
    ) -> None:
        super().__init__(parent)
        self.mode = mode
        self.item_id = item_id
        self.refresh_callback = refresh_callback
        self.from_sales = from_sales
        self.sales_callback = sales_callback
        self.image_path = None
        self.current_image = None
        
        # Configuración de la ventana
        title = "Agregar al Carrito" if from_sales else ("Guardar Producto" if mode == "create" else "Editar Producto")
        self.title(title)
        self.geometry("900x700")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.min_stock_var = tk.StringVar()
        self.max_stock_var = tk.StringVar()
        self.cost_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        self.expiration_var = tk.StringVar()
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        """Configura la interfaz de usuario"""
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        title_text = "Agregar Nuevo Producto al Carrito" if self.from_sales else (
            "Nuevo Producto" if self.mode == "create" else "Editar Producto"
        )
        title_label = CustomLabel(
            form_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Definición de campos con sus tipos de formateo
        fields = [
            ("Código:", self.code_var, 'code', not (self.mode == "edit")),
            ("Producto:", self.product_var, 'name', True),
            ("Descripción:", self.description_var, 'description', True),
            ("Cantidad:", self.quantity_var, 'integer', self.mode == "create" or self.from_sales),
            ("Existencias:", self.stock_var, 'integer', self.mode == "create" and not self.from_sales),
            ("Stock mínimo:", self.min_stock_var, 'integer', not self.from_sales),
            ("Stock máximo:", self.max_stock_var, 'integer', not self.from_sales),
            ("Precio de compra:", self.cost_var, 'decimal', not self.from_sales),
            ("Precio de venta:", self.price_var, 'decimal', True),
            ("Proveedor:", self.supplier_var, None, True),
            ("Vencimiento:", self.expiration_var, 'date', not self.from_sales)
        ]
        
        for i, (label, var, field_type, editable) in enumerate(fields, start=1):
            field_label = CustomLabel(
                form_frame,
                text=label,
                font=("Arial", 12),
                fg="#555",
                bg="#f5f5f5"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Proveedor:":
                suppliers = Supplier.search_active()
                values = [f"{supplier['company']} ({supplier['code']})" for supplier in suppliers]
                
                combobox = CustomCombobox(
                    form_frame,
                    textvariable=var,
                    values=values,
                    state="readonly",
                    width=30,
                    font=("Arial", 12)
                )
                combobox.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = combobox
            else:
                entry = CustomEntry(
                    form_frame,
                    textvariable=var,
                    font=("Arial", 12),
                    width=32,
                    state="normal" if editable else "readonly"
                )
                
                if field_type and editable:
                    FieldFormatter.bind_validation(entry, field_type)
                
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = entry
        
        # Frame para botones
        btn_frame = tk.Frame(form_frame, bg="#f5f5f5")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 10))
        
        # Botón principal
        if self.from_sales:
            btn_text = "Agregar al Carrito"
            btn_command = self.add_to_cart
        else:
            btn_text = "Guardar" if self.mode == "create" else "Actualizar"
            btn_command = self.create_item if self.mode == "create" else self.update_item
        
        btn_action = CustomButton(
            btn_frame, 
            text=btn_text, 
            command=btn_command,
            padding=10,
            width=15
        )
        btn_action.pack(side=tk.LEFT, padx=5)
        
        if not self.from_sales:
            btn_load_image = CustomButton(
                btn_frame,
                text="Cargar Imagen",
                command=self.load_image,
                padding=10,
                width=15
            )
            btn_load_image.pack(side=tk.LEFT, padx=5)
        
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=10,
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

        # Frame para la imagen
        image_frame = tk.Frame(main_frame, bg="#f5f5f5", padx=20, pady=20)
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        img_container = tk.LabelFrame(
            image_frame, 
            text="Imagen del Producto", 
            font=("Arial", 12),
            bg="#f5f5f5",
            padx=10, 
            pady=10
        )
        img_container.pack(fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(
            img_container, 
            bg='white', 
            width=300, 
            height=300,
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        if self.mode == "edit" and not self.from_sales:
            info_frame = tk.Frame(form_frame, bg="#f5f5f5")
            info_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(10, 0))
            
            info_label = CustomLabel(
                info_frame,
                text="Nota: Para modificar cantidad/existencias, use los botones de ajuste",
                font=("Arial", 10),
                fg="#666",
                bg="#f5f5f5"
            )
            info_label.pack()

    def load_image(self):
        """Carga una imagen para el producto"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                img.thumbnail((300, 300))
                self.image_path = file_path
                self.current_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_image)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}", parent=self)

    def validate_required_fields(self) -> bool:
        if self.from_sales:
            required_fields = {
                "Código:": (self.entries["Código:"][0], self.code_var.get()),
                "Producto:": (self.entries["Producto:"][0], self.product_var.get()),
                "Cantidad:": (self.entries["Cantidad:"][0], self.quantity_var.get()),
                "Precio de venta:": (self.entries["Precio de venta:"][0], self.price_var.get())
            }
        else:
            required_fields = {
                "Código:": (self.entries["Código:"][0], self.code_var.get()),
                "Producto:": (self.entries["Producto:"][0], self.product_var.get()),
                "Cantidad:": (self.entries["Cantidad:"][0], self.quantity_var.get()),
                "Existencias:": (self.entries["Existencias:"][0], self.stock_var.get()),
                "Precio de compra:": (self.entries["Precio de compra:"][0], self.cost_var.get()),
                "Precio de venta:": (self.entries["Precio de venta:"][0], self.price_var.get())
            }
            
        return FieldFormatter.validate_required_fields(required_fields, self)

    def load_item_data(self) -> None:
        item = InventoryItem.get_by_id(self.item_id)
        if not item:
            messagebox.showerror("Error", "No se pudo cargar el producto", parent=self)
            self.destroy()
            return
        
        self.code_var.set(item['code'])
        self.product_var.set(item['product'])
        self.description_var.set(item['description'])
        self.quantity_var.set(str(item['quantity']))
        self.stock_var.set(str(item['stock']))
        self.min_stock_var.set(str(item['min_stock']))
        self.max_stock_var.set(str(item['max_stock']))
        self.cost_var.set(str(item['cost']))
        self.price_var.set(str(item['price']))
        self.expiration_var.set(item.get('expiration_date', ''))
        
        if item.get('supplier_id'):
            suppliers = Supplier.search_active()
            supplier = next((s for s in suppliers if s['id'] == item['supplier_id']), None)
            if supplier:
                self.supplier_var.set(f"{supplier['company']} ({supplier['code']})")
        
        if item.get('image_path'):
            self.image_path = item['image_path']
            try:
                img = Image.open(item['image_path'])
                img.thumbnail((300, 300))
                self.current_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_image)
            except Exception as e:
                print(f"Error loading image: {e}")

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
                description=self.description_var.get(),
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()),
                min_stock=int(self.min_stock_var.get()),
                max_stock=int(self.max_stock_var.get()),
                cost=float(self.cost_var.get()),
                price=float(self.price_var.get()),
                supplier_id=supplier_id,
                expiration_date=self.expiration_var.get() or None,
                image_path=self.image_path
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
                description=self.description_var.get() or None,
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()),
                min_stock=int(self.min_stock_var.get()),
                max_stock=int(self.max_stock_var.get()),
                cost=float(self.cost_var.get()),
                price=float(self.price_var.get()),
                supplier_id=supplier_id,
                expiration_date=self.expiration_var.get() or None,
                image_path=self.image_path
            )
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {str(e)}", parent=self)

    def add_to_cart(self) -> None:
        if not self.validate_required_fields():
            return
            
        try:
            if not self.sales_callback:
                raise ValueError("No se pudo agregar al carrito - función de callback no definida")
            
            product_data = {
                'id': -1,
                'code': self.code_var.get(),
                'name': self.product_var.get(),
                'description': self.description_var.get(),
                'quantity': int(self.quantity_var.get()),
                'cost': float(self.cost_var.get()),
                'unit_price': float(self.price_var.get()),
                'total': int(self.quantity_var.get()) * float(self.price_var.get()),
                'is_new': True
            }
            
            if self.supplier_var.get():
                supplier_code = self.supplier_var.get().split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.search_active() if s['code'] == supplier_code), None)
                if supplier:
                    product_data['supplier_id'] = supplier['id']
                    product_data['supplier_name'] = supplier['company']
            
            self.sales_callback(product_data)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar al carrito: {str(e)}", parent=self)
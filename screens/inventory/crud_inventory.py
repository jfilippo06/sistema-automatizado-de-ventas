import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status

class CrudInventory(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget, 
        mode: str = "create", 
        item_id: Optional[int] = None, 
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Pantalla para crear o editar productos del inventario.
        
        :param parent: Widget padre
        :param mode: 'create' o 'edit'
        :param item_id: ID del producto a editar (solo para modo 'edit')
        :param refresh_callback: Función para actualizar la tabla principal
        """
        super().__init__(parent)
        self.mode = mode
        self.item_id = item_id
        self.refresh_callback = refresh_callback
        
        self.title("Agregar Producto" if mode == "create" else "Editar Producto")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.IntVar(value=0)
        self.stock_var = tk.IntVar(value=0)
        self.price_var = tk.DoubleVar(value=0.0)
        self.status_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        """Configura los elementos de la interfaz."""
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var),
            ("Producto:", self.product_var),
            ("Cantidad:", self.quantity_var),
            ("Stock:", self.stock_var),
            ("Precio:", self.price_var),
            ("Estado:", self.status_var),
            ("Proveedor:", self.supplier_var)
        ]
        
        for i, (label, var) in enumerate(fields):
            tk.Label(main_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            if label == "Estado:":
                self.status_combobox = ttk.Combobox(
                    main_frame, 
                    textvariable=var,
                    values=[status['name'] for status in Status.all()]
                )
                self.status_combobox.grid(row=i, column=1, sticky="ew", pady=5)
            elif label == "Proveedor:":
                self.supplier_combobox = ttk.Combobox(
                    main_frame, 
                    textvariable=var,
                    values=[f"{supplier['company']} ({supplier['code']})" for supplier in Supplier.all()]
                )
                self.supplier_combobox.grid(row=i, column=1, sticky="ew", pady=5)
            else:
                entry = tk.Entry(main_frame, textvariable=var)
                entry.grid(row=i, column=1, sticky="ew", pady=5)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        if self.mode == "create":
            tk.Button(
                btn_frame, 
                text="Agregar", 
                command=self.create_item,
                width=15
            ).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(
                btn_frame, 
                text="Actualizar", 
                command=self.update_item,
                width=15
            ).pack(side=tk.LEFT, padx=10)
            
        tk.Button(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=10)

    def load_item_data(self) -> None:
        """Carga los datos del producto a editar."""
        item = InventoryItem.get_by_id(self.item_id)
        if not item:
            messagebox.showerror("Error", "No se pudo cargar el producto")
            self.destroy()
            return
        
        self.code_var.set(item['code'])
        self.product_var.set(item['product'])
        self.quantity_var.set(item['quantity'])
        self.stock_var.set(item['stock'])
        self.price_var.set(item['price'])
        self.status_var.set(item['status_name'])
        
        if item.get('supplier_company'):
            suppliers = Supplier.all()
            supplier = next((s for s in suppliers if s['id'] == item['supplier_id']), None)
            if supplier:
                self.supplier_var.set(f"{supplier['company']} ({supplier['code']})")

    def create_item(self) -> None:
        """Crea un nuevo producto en la base de datos."""
        try:
            # Obtener el ID del estado seleccionado
            status_name = self.status_var.get()
            status = next((s for s in Status.all() if s['name'] == status_name), None)
            if not status:
                raise ValueError("Estado no válido")
            
            # Obtener el ID del proveedor seleccionado (si existe)
            supplier_text = self.supplier_var.get()
            supplier_id = None
            if supplier_text:
                supplier_code = supplier_text.split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.all() if s['code'] == supplier_code), None)
                if supplier:
                    supplier_id = supplier['id']
            
            # Crear el producto
            InventoryItem.create(
                code=self.code_var.get(),
                product=self.product_var.get(),
                quantity=self.quantity_var.get(),
                stock=self.stock_var.get(),
                price=self.price_var.get(),
                status_id=status['id'],
                supplier_id=supplier_id
            )
            
            messagebox.showinfo("Éxito", "Producto creado correctamente")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el producto: {str(e)}")

    def update_item(self) -> None:
        """Actualiza un producto existente en la base de datos."""
        try:
            if not self.item_id:
                raise ValueError("ID de producto no válido")
                
            # Obtener el ID del estado seleccionado
            status_name = self.status_var.get()
            status = next((s for s in Status.all() if s['name'] == status_name), None)
            if not status:
                raise ValueError("Estado no válido")
            
            # Obtener el ID del proveedor seleccionado (si existe)
            supplier_text = self.supplier_var.get()
            supplier_id = None
            if supplier_text:
                supplier_code = supplier_text.split("(")[-1].rstrip(")")
                supplier = next((s for s in Supplier.all() if s['code'] == supplier_code), None)
                if supplier:
                    supplier_id = supplier['id']
            
            # Actualizar el producto
            InventoryItem.update(
                item_id=self.item_id,
                code=self.code_var.get(),
                product=self.product_var.get(),
                quantity=self.quantity_var.get(),
                stock=self.stock_var.get(),
                price=self.price_var.get(),
                status_id=status['id'],
                supplier_id=supplier_id
            )
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {str(e)}")


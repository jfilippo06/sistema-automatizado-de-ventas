import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable, List, Dict, Any, Optional
from screens.inventory.crud_inventory import CrudInventory
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status

class Inventory(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.geometry("1200x800")
        self.parent.resizable(True, True)
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        btn_back = tk.Button(button_frame, text="Regresar", command=self.go_back)
        btn_back.pack(side=tk.LEFT, padx=5)

        btn_add = tk.Button(button_frame, text="Agregar", command=self.add_item)
        btn_add.pack(side=tk.RIGHT, padx=5)

        btn_edit = tk.Button(button_frame, text="Editar", command=self.edit_item)
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_disable = tk.Button(button_frame, text="Deshabilitar", command=self.disable_item)
        btn_disable.pack(side=tk.RIGHT, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self, columns=(
            "ID", "Código", "Producto", "Cantidad", "Stock", 
            "Precio", "Creación", "Modificación", "Estado", "Proveedor"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 100, tk.CENTER),
            ("Producto", 200, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Stock", 80, tk.CENTER),
            ("Precio", 100, tk.E),
            ("Creación", 120, tk.CENTER),
            ("Modificación", 120, tk.CENTER),
            ("Estado", 100, tk.CENTER),
            ("Proveedor", 150, tk.W)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.refresh_data()

    def refresh_data(self) -> None:
        """Actualiza los datos en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        items = InventoryItem.all()
        for item in items:
            self.tree.insert("", tk.END, values=(
                item['id'],
                item['code'],
                item['product'],
                item['quantity'],
                item['stock'],
                f"${item['price']:.2f}",
                item['created_at'],
                item['updated_at'],
                item['status_name'],
                item.get('supplier_company', 'N/A')
            ))

    def go_back(self) -> None:
        self.open_previous_screen_callback()

    def add_item(self) -> None:
        """Abre el formulario para agregar un nuevo producto."""
        CrudInventory(self, mode="create", refresh_callback=self.refresh_data)

    def edit_item(self) -> None:
        """Abre el formulario para editar un producto existente."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        CrudInventory(self, mode="edit", item_id=item_id, refresh_callback=self.refresh_data)

    def disable_item(self) -> None:
        """Muestra un diálogo de confirmación para deshabilitar un producto."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        product_name = self.tree.item(selected[0])['values'][2]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea deshabilitar el producto '{product_name}'?"
        )
        
        if response:
            try:
                # Cambiar el estado a inactivo
                status_inactive = next((s for s in Status.all() if s['name'] == 'inactive'), None)
                if status_inactive:
                    InventoryItem.update_status(item_id, status_inactive['id'])
                    messagebox.showinfo("Éxito", "Producto deshabilitado correctamente")
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "No se encontró el estado 'inactivo'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo deshabilitar el producto: {str(e)}")
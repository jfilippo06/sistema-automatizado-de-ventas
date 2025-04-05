import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.inventory.crud_inventory import CrudInventory
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel

class Inventory(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        # Maximizar la ventana (pantalla completa)
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header con título
        header_frame = tk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = CustomLabel(
            header_frame,
            text="Gestión de Inventario",
            font=("Arial", 16, "bold"),
            fg="#333"
        )
        title_label.pack(side=tk.LEFT)

        # Frame de botones
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        btn_back = CustomButton(
            button_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10
        )
        btn_back.pack(side=tk.LEFT, padx=5)

        btn_add = CustomButton(
            button_frame,
            text="Crear",
            command=self.add_item,
            padding=8,
            width=10
        )
        btn_add.pack(side=tk.RIGHT, padx=5)

        btn_edit = CustomButton(
            button_frame,
            text="Editar",
            command=self.edit_item,
            padding=8,
            width=10
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_disable = CustomButton(
            button_frame,
            text="Deshabilitar",
            command=self.disable_item,
            padding=8,
            width=12
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Código", "Producto", "Cantidad", "Stock", 
            "Precio", "Proveedor", "Estado"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Stock", 80, tk.CENTER),
            ("Precio", 100, tk.CENTER),
            ("Proveedor", 150, tk.W),
            ("Estado", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text=f"Mostrando {len(InventoryItem.all())} productos",
            font=("Arial", 10),
            fg="#666"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.refresh_data()

    def refresh_data(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            items = InventoryItem.all()
            for item in items:
                self.tree.insert("", tk.END, values=(
                    item['id'],
                    item['code'],
                    item['product'],
                    item['quantity'],
                    item['stock'],
                    item['price'],
                    item.get('supplier_company', ''),
                    item['status_name']
                ))
            self.status_bar.configure(text=f"Mostrando {len(items)} productos")
        except Exception as e:
            self.status_bar.configure(text=f"Error al cargar datos: {str(e)}")
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {str(e)}", parent=self)

    def go_back(self) -> None:
        # Antes de regresar, asegurarnos de que la ventana vuelva al tamaño normal
        self.parent.state('normal')  # Restaurar ventana
        # O si usaste fullscreen:
        # self.parent.attributes('-fullscreen', False)
        self.open_previous_screen_callback()

    def add_item(self) -> None:
        CrudInventory(self, mode="create", refresh_callback=self.refresh_data)

    def edit_item(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        CrudInventory(self, mode="edit", item_id=item_id, refresh_callback=self.refresh_data)

    def disable_item(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        product_name = self.tree.item(selected[0])['values'][2]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea deshabilitar el producto '{product_name}'?",
            parent=self
        )
        
        if response:
            try:
                status_inactive = next((s for s in Status.all() if s['name'] == 'inactive'), None)
                if status_inactive:
                    InventoryItem.update_status(item_id, status_inactive['id'])
                    messagebox.showinfo("Éxito", "Producto deshabilitado correctamente", parent=self)
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "No se encontró el estado 'inactivo'", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo deshabilitar el producto: {str(e)}", parent=self)
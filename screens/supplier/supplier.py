import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Dict, Any
from screens.supplier.crud_supplier import CrudSupplier
from sqlite_cli.models.supplier_model import Supplier
from sqlite_cli.models.status_model import Status

class Suppliers(tk.Frame):
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

        btn_add = tk.Button(button_frame, text="Agregar", command=self.add_supplier)
        btn_add.pack(side=tk.RIGHT, padx=5)

        btn_edit = tk.Button(button_frame, text="Editar", command=self.edit_supplier)
        btn_edit.pack(side=tk.RIGHT, padx=5)

        btn_disable = tk.Button(button_frame, text="Deshabilitar", command=self.disable_supplier)
        btn_disable.pack(side=tk.RIGHT, padx=5)

        # Treeview con columna de estado
        self.tree = ttk.Treeview(self, columns=(
            "ID", "Código", "Cédula", "Nombres", "Apellidos", 
            "Dirección", "Teléfono", "Email", "RIF", "Empresa", "Estado"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Cédula", 100, tk.CENTER),
            ("Nombres", 150, tk.W),
            ("Apellidos", 150, tk.W),
            ("Dirección", 200, tk.W),
            ("Teléfono", 100, tk.CENTER),
            ("Email", 150, tk.W),
            ("RIF", 100, tk.CENTER),
            ("Empresa", 150, tk.W),
            ("Estado", 100, tk.CENTER)
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
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        suppliers = Supplier.all()
        for supplier in suppliers:
            self.tree.insert("", tk.END, values=(
                supplier['id'],
                supplier['code'],
                supplier['id_number'],
                supplier['first_name'],
                supplier['last_name'],
                supplier['address'],
                supplier['phone'],
                supplier['email'],
                supplier['tax_id'],
                supplier['company'],
                supplier['status_name']
            ))

    def go_back(self) -> None:
        self.open_previous_screen_callback()

    def add_supplier(self) -> None:
        CrudSupplier(self, mode="create", refresh_callback=self.refresh_data)

    def edit_supplier(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un proveedor")
            return
            
        supplier_id = self.tree.item(selected[0])['values'][0]
        CrudSupplier(self, mode="edit", supplier_id=supplier_id, refresh_callback=self.refresh_data)

    def disable_supplier(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un proveedor")
            return
            
        supplier_id = self.tree.item(selected[0])['values'][0]
        company_name = self.tree.item(selected[0])['values'][9]
        
        response = messagebox.askyesno(
            "Confirmar", 
            f"¿Está seguro que desea deshabilitar el proveedor '{company_name}'?"
        )
        
        if response:
            try:
                # Buscar el estado 'inactive'
                status_inactive = next((s for s in Status.all() if s['name'] == 'inactive'), None)
                if status_inactive:
                    Supplier.update_status(supplier_id, status_inactive['id'])
                    messagebox.showinfo("Éxito", "Proveedor deshabilitado correctamente")
                    self.refresh_data()
                else:
                    messagebox.showerror("Error", "No se encontró el estado 'inactivo'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo deshabilitar el proveedor: {str(e)}")
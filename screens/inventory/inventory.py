import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, List, Dict, Any
from screens.inventory.crud_inventory import CrudInventory
from screens.inventory.adjust_inventory import AdjustInventory
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.status_model import Status
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from PIL import Image, ImageTk
import os

class Inventory(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Todos los campos")
        self.current_image = None
        self.configure(bg="#f5f5f5")  # Fondo general
        self.configure_ui()
        self.refresh_data()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)
        self.refresh_data()

    def configure_ui(self) -> None:
        # Header con título - Estilo actualizado
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Productos",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Frame para botón de regreso - Estilo actualizado
        back_frame = tk.Frame(header_frame, bg="#4a6fa5")
        back_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        btn_back = CustomButton(
            back_frame,
            text="Regresar",
            command=self.go_back,
            padding=8,
            width=10,
        )
        btn_back.pack(side=tk.RIGHT)

        # Frame principal para controles - Estilo actualizado
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Frame de búsqueda
        search_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Campo de búsqueda - Estilo actualizado
        search_entry = CustomEntry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 12)
        )
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.on_search)

        # Combobox para seleccionar campo de búsqueda - Estilo actualizado
        search_fields = [
            "Todos los campos",
            "ID",
            "Código",
            "Producto",
            "Descripción",
            "Proveedor",
            "Cantidad",
            "Existencias",
            "Stock mínimo",
            "Stock máximo",
            "Precio de compra",
            "Precio de venta",
            "Vencimiento"
        ]
        
        search_combobox = CustomCombobox(
            search_frame,
            textvariable=self.search_field_var,
            values=search_fields,
            state="readonly",
            width=20
        )
        search_combobox.pack(side=tk.LEFT, padx=5)
        search_combobox.bind("<<ComboboxSelected>>", self.on_search)

        # Frame para los botones de acciones (derecha) - Estilo actualizado
        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        # Frame para la miniatura de la imagen - Estilo actualizado
        self.image_frame = tk.Frame(action_frame, bg="#f5f5f5")
        self.image_frame.pack(side=tk.LEFT, padx=5)
        
        self.image_label = tk.Label(self.image_frame, bg="#f5f5f5")
        self.image_label.pack()
        self.image_label.bind("<Button-1>", self.show_full_image)

        # Botón para entrada inicial
        btn_initial = CustomButton(
            action_frame,
            text="Entrada Inicial",
            command=self.add_item,
            padding=8,
            width=14,
        )
        btn_initial.pack(side=tk.RIGHT, padx=5)

        # Botón para ajuste positivo
        btn_positive = CustomButton(
            action_frame,
            text="Ajuste (+)",
            command=lambda: self.adjust_item("positive"),
            padding=8,
            width=10,
        )
        btn_positive.pack(side=tk.RIGHT, padx=5)

        # Botón para ajuste negativo
        btn_negative = CustomButton(
            action_frame,
            text="Ajuste (-)",
            command=lambda: self.adjust_item("negative"),
            padding=8,
            width=10,
        )
        btn_negative.pack(side=tk.RIGHT, padx=5)

        # Botón para editar (con campos bloqueados)
        btn_edit = CustomButton(
            action_frame,
            text="Editar",
            command=self.edit_item,
            padding=8,
            width=10,
        )
        btn_edit.pack(side=tk.RIGHT, padx=5)

        # Botón para deshabilitar
        btn_disable = CustomButton(
            action_frame,
            text="Deshabilitar",
            command=self.disable_item,
            padding=8,
            width=12,
        )
        btn_disable.pack(side=tk.RIGHT, padx=5)

        # Treeview frame - Estilo actualizado
        tree_frame = tk.Frame(self, bg="#f5f5f5")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Código", "Producto", "Cantidad", "Existencias", "Stock mínimo", 
            "Stock máximo", "Precio compra", "Precio venta", "Proveedor", "Vencimiento"
        ), show="headings")

        columns = [
            ("ID", 50, tk.CENTER),
            ("Código", 80, tk.CENTER),
            ("Producto", 150, tk.W),
            ("Cantidad", 80, tk.CENTER),
            ("Existencias", 80, tk.CENTER),
            ("Stock mínimo", 80, tk.CENTER),
            ("Stock máximo", 80, tk.CENTER),
            ("Precio compra", 100, tk.CENTER),
            ("Precio venta", 100, tk.CENTER),
            ("Proveedor", 150, tk.W),
            ("Vencimiento", 100, tk.CENTER)
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Barra de estado - Estilo actualizado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def on_item_selected(self, event):
        selected = self.tree.selection()
        if selected:
            item_id = self.tree.item(selected[0])['values'][0]
            item = InventoryItem.get_by_id(item_id)
            if item and item.get('image_path'):
                self.load_image_thumbnail(item['image_path'])
            else:
                self.clear_image()

    def load_image_thumbnail(self, image_path):
        try:
            if not os.path.exists(image_path):
                self.clear_image()
                return

            img = Image.open(image_path)
            img.thumbnail((50, 50))
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.clear_image()

    def clear_image(self):
        self.image_label.config(image='')
        self.current_image = None

    def show_full_image(self, event):
        if not self.current_image:
            return
            
        selected = self.tree.selection()
        if selected:
            item_id = self.tree.item(selected[0])['values'][0]
            item = InventoryItem.get_by_id(item_id)
            if item and item.get('image_path'):
                self.show_image_window(item['image_path'])

    def show_image_window(self, image_path):
        if not os.path.exists(image_path):
            messagebox.showerror("Error", "La imagen no se encuentra en la ruta especificada", parent=self)
            return

        top = tk.Toplevel(self)
        top.title("Imagen del Producto")
        top.configure(bg="#f5f5f5")
        
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        
        label = tk.Label(top, image=photo, bg="#f5f5f5")
        label.image = photo  # keep a reference!
        label.pack()

    def on_search(self, event=None) -> None:
        search_term = self.search_var.get().lower()
        field = self.search_field_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        items = InventoryItem.search_active(search_term, field if field != "Todos los campos" else None)
        
        for item in items:
            self.tree.insert("", tk.END, values=(
                item['id'],
                item['code'],
                item['product'],
                item['quantity'],
                item['stock'],
                item['min_stock'],
                item['max_stock'],
                item['cost'],
                item['price'],
                item.get('supplier_company', ''),
                item.get('expiration_date', '')
            ))
        
        self.status_bar.configure(text=f"Mostrando {len(items)} productos")
        self.clear_image()

    def refresh_data(self) -> None:
        self.search_var.set("")
        self.search_field_var.set("Todos los campos")
        self.on_search()

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def add_item(self) -> None:
        # Crear la ventana de entrada inicial
        crud_window = CrudInventory(self, mode="create", refresh_callback=self.refresh_data)
        
        # Calcular posición para centrar
        window_width = 800  # Ajusta según el tamaño de tu ventana
        window_height = 600  # Ajusta según el tamaño de tu ventana
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        crud_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def edit_item(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        
        # Crear la ventana de edición
        crud_window = CrudInventory(
            self, 
            mode="edit", 
            item_id=item_id, 
            refresh_callback=self.refresh_data
        )
        
        # Calcular posición para centrar
        window_width = 800  # Ajusta según el tamaño de tu ventana
        window_height = 600  # Ajusta según el tamaño de tu ventana
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        crud_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def adjust_item(self, adjustment_type: str) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto", parent=self)
            return
            
        item_id = self.tree.item(selected[0])['values'][0]
        
        # Centrar la ventana de ajuste
        adjust_window = AdjustInventory(
            self, 
            adjustment_type=adjustment_type, 
            item_id=item_id, 
            refresh_callback=self.refresh_data
        )
        
        # Calcular posición para centrar
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        adjust_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional, Dict, Any
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.supplier_model import Supplier
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox
from utils.valdations import Validations
from PIL import Image, ImageTk
import os

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
        self.image_path = None
        self.current_image = None
        
        # Configuración de la ventana
        self.title("Guardar Producto" if mode == "create" else "Editar Producto")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.code_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="0")
        self.stock_var = tk.StringVar(value="0")
        self.min_stock_var = tk.StringVar(value="0")
        self.max_stock_var = tk.StringVar(value="0")
        self.price_var = tk.StringVar(value="0.0")
        self.supplier_var = tk.StringVar()
        self.expiration_var = tk.StringVar()
        
        self.entries = {}
        self.configure_ui()
        
        if mode == "edit" and item_id:
            self.load_item_data()

    def configure_ui(self) -> None:
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el formulario (izquierda)
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Título con estilo consistente
        title_text = "Nuevo Producto" if self.mode == "create" else "Editar Producto"
        title_label = CustomLabel(
            form_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        fields = [
            ("Código:", self.code_var, 'text', not (self.mode == "edit")),
            ("Producto:", self.product_var, 'text', True),
            ("Cantidad:", self.quantity_var, 'number', self.mode == "create"),
            ("Existencias:", self.stock_var, 'number', self.mode == "create"),
            ("Stock mínimo:", self.min_stock_var, 'number', True),
            ("Stock máximo:", self.max_stock_var, 'number', True),
            ("Precio:", self.price_var, 'decimal', True),
            ("Proveedor:", self.supplier_var, None, True),
            ("Vencimiento:", self.expiration_var, 'date', True)
        ]
        
        for i, (label, var, val_type, editable) in enumerate(fields, start=1):
            # Etiqueta del campo
            field_label = CustomLabel(
                form_frame,
                text=label,
                font=("Arial", 12),
                fg="#555",
                bg="#f5f5f5"
            )
            field_label.grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Proveedor:":
                # Combobox para proveedores
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
            elif label == "Vencimiento:":
                # Campo de fecha con validación
                entry = CustomEntry(
                    form_frame,
                    textvariable=var,
                    font=("Arial", 12),
                    width=32,
                    state="normal" if editable else "readonly"
                )
                entry.configure(validate="key")
                entry.configure(validatecommand=(
                    entry.register(self.validate_date_input), 
                    '%P', '%d', '%i', '%S'
                ))
                entry.bind("<KeyRelease>", self.format_date_input)
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = entry
            else:
                # Campos de texto/números
                entry = CustomEntry(
                    form_frame,
                    textvariable=var,
                    font=("Arial", 12),
                    width=32,
                    state="normal" if editable else "readonly"
                )
                
                if val_type == 'number':
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(entry.register(self.validate_integer), '%P'))
                elif val_type == 'decimal':
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(entry.register(self.validate_decimal), '%P'))
                else:
                    entry.bind("<KeyRelease>", lambda e, func=self.validate_text: self.validate_entry(e, func))
                
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
                self.entries[label] = entry
        
        # Frame para botones
        btn_frame = tk.Frame(form_frame, bg="#f5f5f5")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 10))
        
        # Botón principal (Guardar/Actualizar)
        btn_action = CustomButton(
            btn_frame, 
            text="Guardar" if self.mode == "create" else "Actualizar", 
            command=self.create_item if self.mode == "create" else self.update_item,
            padding=10,
            width=15
        )
        btn_action.pack(side=tk.LEFT, padx=5)
        
        # Botón Cargar Imagen
        btn_load_image = CustomButton(
            btn_frame,
            text="Cargar Imagen",
            command=self.load_image,
            padding=10,
            width=15
        )
        btn_load_image.pack(side=tk.LEFT, padx=5)
        
        # Botón Cancelar
        btn_cancel = CustomButton(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            padding=10,
            width=15
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)

        # Frame para la imagen (derecha)
        image_frame = tk.Frame(main_frame, bg="#f5f5f5", padx=20, pady=20)
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Contenedor de imagen con borde
        img_container = tk.LabelFrame(
            image_frame, 
            text="Imagen del Producto", 
            font=("Arial", 12),
            bg="#f5f5f5",
            padx=10, 
            pady=10
        )
        img_container.pack(fill=tk.BOTH, expand=True)
        
        # Etiqueta para mostrar la imagen
        self.image_label = tk.Label(
            img_container, 
            bg='white', 
            width=300, 
            height=300,
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Nota informativa en modo edición
        if self.mode == "edit":
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

    # [Métodos de validación y funcionalidad se mantienen igual...]
    def validate_date_input(self, new_text: str, action_code: str, index: str, char: str) -> bool:
        """Valida el formato de fecha YYYY/MM/DD"""
        if action_code == '0':
            return True
        if not char.isdigit():
            return False
        if len(new_text) > 10:
            return False
        if len(new_text) >= 4 and new_text[4] != '/':
            return False
        if len(new_text) >= 7 and new_text[7] != '/':
            return False
        return True

    def format_date_input(self, event: tk.Event) -> None:
        """Formatea automáticamente la fecha con barras"""
        entry = event.widget
        text = entry.get()
        clean_text = text.replace('/', '')
        formatted = ''
        for i, char in enumerate(clean_text):
            if i == 4 or i == 6:
                formatted += '/'
            if i < 8:
                formatted += char
        if formatted != text:
            entry.delete(0, tk.END)
            entry.insert(0, formatted)

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

    # [Resto de métodos se mantienen igual...]
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
            "Existencias:": self.stock_var.get(),
            "Precio:": self.price_var.get()
        }
        
        if not Validations.validate_required_fields(self.entries, required_fields, self):
            return False
            
        numeric_fields = {
            "Cantidad:": (self.quantity_var.get(), False),
            "Existencias:": (self.stock_var.get(), False),
            "Stock mínimo:": (self.min_stock_var.get(), False),
            "Stock máximo:": (self.max_stock_var.get(), False),
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
        self.min_stock_var.set(str(item['min_stock']))
        self.max_stock_var.set(str(item['max_stock']))
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
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()),
                min_stock=int(self.min_stock_var.get()),
                max_stock=int(self.max_stock_var.get()),
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
                quantity=int(self.quantity_var.get()),
                stock=int(self.stock_var.get()),
                min_stock=int(self.min_stock_var.get()),
                max_stock=int(self.max_stock_var.get()),
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
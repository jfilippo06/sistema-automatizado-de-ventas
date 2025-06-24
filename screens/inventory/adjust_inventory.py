import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
from sqlite_cli.models.inventory_model import InventoryItem
from sqlite_cli.models.inventory_movement_model import InventoryMovement
from sqlite_cli.models.movement_type_model import MovementType
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from utils.field_formatter import FieldFormatter
from utils.session_manager import SessionManager

class AdjustInventory(tk.Toplevel):
    def __init__(
        self, 
        parent: tk.Widget,
        adjustment_type: str,
        item_id: int,
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__(parent)
        self.adjustment_type = adjustment_type
        self.item_id = item_id
        self.refresh_callback = refresh_callback
        
        # Configuración de la ventana
        self.title("Ajuste de Inventario")
        self.geometry("500x500")
        self.minsize(400, 450)
        self.configure(bg="#f5f5f5")
        
        self.transient(parent)
        self.grab_set()
        
        # Variables para los campos
        self.quantity_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        
        self.configure_ui()
        self.load_item_data()
        self.center_window()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def configure_ui(self) -> None:
        """Configura la interfaz de usuario"""
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = f"Ajuste {'Positivo (+)' if self.adjustment_type == 'positive' else 'Negativo (-)'}"
        title_label = CustomLabel(
            main_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="#333",
            bg="#f5f5f5"
        )
        title_label.pack(pady=(0, 20))
        
        # Marco para información del producto
        self.product_info_frame = tk.Frame(
            main_frame, 
            bg="white", 
            bd=1, 
            relief=tk.SOLID, 
            padx=10, 
            pady=10
        )
        self.product_info_frame.pack(fill=tk.X, pady=10)
        
        self.product_label = CustomLabel(
            self.product_info_frame,
            text="",
            font=("Arial", 12),
            fg="#555",
            justify=tk.LEFT,
            bg="white"
        )
        self.product_label.pack(anchor=tk.W)
        
        # Frame para campos de ajuste
        adjust_frame = tk.Frame(main_frame, bg="#f5f5f5")
        adjust_frame.pack(fill=tk.X, pady=10)
        
        # Campo de cantidad
        quantity_frame = tk.Frame(adjust_frame, bg="#f5f5f5")
        quantity_frame.pack(fill=tk.X, pady=5)
        
        quantity_label = CustomLabel(
            quantity_frame,
            text="Cambio en Cantidad:",
            font=("Arial", 12),
            fg="#555",
            bg="#f5f5f5"
        )
        quantity_label.pack(side=tk.LEFT, padx=5)
        
        self.quantity_entry = CustomEntry(
            quantity_frame,
            textvariable=self.quantity_var,
            font=("Arial", 12),
            width=15
        )
        FieldFormatter.bind_validation(self.quantity_entry, 'decimal')
        self.quantity_entry.pack(side=tk.RIGHT, padx=5)
        
        # Campo de existencias
        stock_frame = tk.Frame(adjust_frame, bg="#f5f5f5")
        stock_frame.pack(fill=tk.X, pady=5)
        
        stock_label = CustomLabel(
            stock_frame,
            text="Cambio en Existencias:",
            font=("Arial", 12),
            fg="#555",
            bg="#f5f5f5"
        )
        stock_label.pack(side=tk.LEFT, padx=5)
        
        self.stock_entry = CustomEntry(
            stock_frame,
            textvariable=self.stock_var,
            font=("Arial", 12),
            width=15
        )
        FieldFormatter.bind_validation(self.stock_entry, 'decimal')
        self.stock_entry.pack(side=tk.RIGHT, padx=5)
        
        # Área de notas
        notes_frame = tk.Frame(main_frame, bg="#f5f5f5")
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        notes_label = CustomLabel(
            notes_frame,
            text="Notas/Observaciones:",
            font=("Arial", 12),
            fg="#555",
            bg="#f5f5f5"
        )
        notes_label.pack(anchor=tk.W, pady=5)
        
        self.notes_text = tk.Text(
            notes_frame,
            height=2,
            width=40,
            wrap=tk.WORD,
            font=("Arial", 12),
            padx=5,
            pady=5,
            bd=1,
            relief=tk.SOLID
        )
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botón Cancelar
        btn_cancel = CustomButton(
            button_frame,
            text="Cancelar", 
            command=self.destroy,
            padding=10,
            width=15
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        # Botón Aplicar
        btn_apply = CustomButton(
            button_frame,
            text="Aplicar Ajuste", 
            command=self.apply_adjustment,
            padding=10,
            width=15
        )
        btn_apply.pack(side=tk.RIGHT, padx=5)

    def load_item_data(self):
        """Carga los datos del producto a ajustar"""
        item = InventoryItem.get_by_id(self.item_id)
        if not item:
            messagebox.showerror("Error", "No se pudo cargar el producto", parent=self)
            self.destroy()
            return
        
        self.product_label.configure(
            text=f"Producto: {item['product']}\n"
                 f"Código: {item['code']}\n"
                 f"Cantidad actual: {item['quantity']}\n"
                 f"Existencias actuales: {item['stock']}"
        )

    def apply_adjustment(self):
        """Aplica el ajuste al inventario"""
        try:
            quantity_change = float(self.quantity_var.get() or 0)
            stock_change = float(self.stock_var.get() or 0)
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            if quantity_change == 0 and stock_change == 0:
                messagebox.showwarning("Advertencia", "Debe especificar al menos un cambio", parent=self)
                return
            
            item = InventoryItem.get_by_id(self.item_id)
            if not item:
                raise ValueError("Producto no encontrado")
            
            if self.adjustment_type == "positive":
                movement_type = MovementType.get_by_name("Ajuste positivo")
                reference_type = "positive_adjustment"
                quantity_change = abs(quantity_change)
                stock_change = abs(stock_change)
            else:
                movement_type = MovementType.get_by_name("Ajuste negativo")
                reference_type = "negative_adjustment"
                quantity_change = -abs(quantity_change)
                stock_change = -abs(stock_change)
            
            if not movement_type:
                raise ValueError("Tipo de movimiento no encontrado")
            
            new_quantity = item['quantity'] + quantity_change
            new_stock = item['stock'] + stock_change
            
            if new_quantity < 0 or new_stock < 0:
                messagebox.showwarning("Advertencia", "Los valores resultantes no pueden ser negativos", parent=self)
                return
            
            user_id = SessionManager.get_user_id()
            if not user_id:
                raise ValueError("No se pudo obtener el ID del usuario")
            
            # Actualizar inventario
            InventoryItem.update(
                item_id=self.item_id,
                code=item['code'],
                product=item['product'],
                quantity=new_quantity,
                stock=new_stock,
                min_stock=item['min_stock'],
                max_stock=item['max_stock'],
                cost=item['cost'],
                price=item['price'],
                supplier_id=item.get('supplier_id'),
                expiration_date=item.get('expiration_date'),
                image_path=item.get('image_path')
            )
            
            # Registrar movimiento
            InventoryMovement.create(
                inventory_id=self.item_id,
                movement_type_id=movement_type['id'],
                quantity_change=quantity_change,
                stock_change=stock_change,
                previous_quantity=item['quantity'],
                new_quantity=new_quantity,
                previous_stock=item['stock'],
                new_stock=new_stock,
                user_id=user_id,
                reference_id=self.item_id,
                reference_type=reference_type,
                notes=notes
            )
            
            messagebox.showinfo("Éxito", "Ajuste aplicado correctamente", parent=self)
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Valor inválido: {str(e)}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el ajuste: {str(e)}", parent=self)
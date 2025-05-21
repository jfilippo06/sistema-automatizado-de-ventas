import tkinter as tk
from tkinter import ttk
from typing import Any, Callable
from widgets.custom_button import CustomButton
from widgets.custom_label import CustomLabel
from widgets.custom_entry import CustomEntry
from widgets.custom_combobox import CustomCombobox

class PurchaseOrdersScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, open_previous_screen_callback: Callable[[], None]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.open_previous_screen_callback = open_previous_screen_callback
        self.configure(bg="#f5f5f5")
        self.configure_ui()

    def pack(self, **kwargs: Any) -> None:
        self.parent.state('zoomed')
        super().pack(fill=tk.BOTH, expand=True)

    def configure_ui(self) -> None:
        # Header (manteniendo tu estilo)
        header_frame = tk.Frame(self, bg="#4a6fa5")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        title_label = CustomLabel(
            header_frame,
            text="Órdenes de Compra",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#4a6fa5"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

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

        # Contenedor principal (formulario tipo documento)
        form_frame = tk.Frame(self, bg="white", padx=20, pady=20, bd=1, relief=tk.SUNKEN)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Encabezado del documento
        doc_header_frame = tk.Frame(form_frame, bg="white")
        doc_header_frame.pack(fill=tk.X, pady=10)

        # Número de orden (derecha)
        order_num_frame = tk.Frame(doc_header_frame, bg="white")
        order_num_frame.pack(side=tk.RIGHT)

        CustomLabel(
            order_num_frame,
            text="ORDEN DE COMPRA N°:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)

        self.order_number_entry = CustomEntry(
            order_num_frame,
            font=("Arial", 12, "bold"),
            width=15,
        )
        self.order_number_entry.pack(side=tk.LEFT, padx=5)
        self.order_number_entry.insert(0, "OC-0001")  # Ejemplo

        # Logo y datos empresa (izquierda)
        company_frame = tk.Frame(doc_header_frame, bg="white")
        company_frame.pack(side=tk.LEFT)

        CustomLabel(
            company_frame,
            text="EMPRESA XYZ, C.A.",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        CustomLabel(
            company_frame,
            text="RIF: J-12345678-9",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor=tk.W)

        CustomLabel(
            company_frame,
            text="Av. Principal, Edif. Empresarial",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor=tk.W)

        # Línea divisoria
        ttk.Separator(form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Sección Proveedor
        supplier_frame = tk.Frame(form_frame, bg="white")
        supplier_frame.pack(fill=tk.X, pady=10)

        CustomLabel(
            supplier_frame,
            text="PROVEEDOR:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)

        # Campos del proveedor en 2 columnas
        supplier_fields_frame = tk.Frame(supplier_frame, bg="white")
        supplier_fields_frame.pack(fill=tk.X, pady=5)

        # Columna 1
        col1 = tk.Frame(supplier_fields_frame, bg="white")
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True)

        fields = [
            ("Nombre/Razón Social:", "supplier_name"),
            ("RIF/Cédula:", "supplier_id"),
            ("Dirección:", "supplier_address"),
            ("Teléfono:", "supplier_phone")
        ]

        for label, var_name in fields:
            frame = tk.Frame(col1, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                width=20,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            entry = CustomEntry(
                frame,
                font=("Arial", 11),
                width=40
            )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            setattr(self, var_name, entry)

        # Columna 2
        col2 = tk.Frame(supplier_fields_frame, bg="white")
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True)

        fields = [
            ("Email:", "supplier_email"),
            ("Persona Contacto:", "supplier_contact"),
            ("Cond. Pago:", "payment_terms"),
            ("Fecha Entrega:", "delivery_date")
        ]

        for label, var_name in fields:
            frame = tk.Frame(col2, bg="white")
            frame.pack(fill=tk.X, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            if var_name == "payment_terms":
                combobox = CustomCombobox(
                    frame,
                    values=["Contado", "15 días", "30 días", "60 días"],
                    font=("Arial", 11),
                    state="readonly",
                    width=18
                )
                combobox.pack(side=tk.LEFT, padx=5)
                combobox.set("Contado")
                setattr(self, var_name, combobox)
            else:
                entry = CustomEntry(
                    frame,
                    font=("Arial", 11),
                    width=25
                )
                entry.pack(side=tk.LEFT, padx=5)
                setattr(self, var_name, entry)

        # Línea divisoria
        ttk.Separator(form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Tabla de productos
        products_frame = tk.Frame(form_frame, bg="white")
        products_frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado de tabla
        table_header = tk.Frame(products_frame, bg="white")
        table_header.pack(fill=tk.X)
        
        headers = ["Código", "Descripción", "Cant.", "Precio Unit.", "Total"]
        widths = [100, 300, 80, 120, 120]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            frame = tk.Frame(table_header, bg="#4a6fa5", bd=1, relief=tk.SOLID)
            frame.pack(side=tk.LEFT)
            frame.pack_propagate(False)
            frame.configure(width=width, height=30)
            
            CustomLabel(
                frame,
                text=header,
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#4a6fa5"
            ).pack(expand=True, fill=tk.BOTH)

        # Cuerpo de la tabla (simulando filas)
        table_body = tk.Frame(products_frame, bg="white", bd=1, relief=tk.SUNKEN)
        table_body.pack(fill=tk.BOTH, expand=True)

        # Aquí irían las filas de productos, pero por ahora dejamos espacio
        placeholder = tk.Frame(table_body, bg="white", height=200)
        placeholder.pack(fill=tk.BOTH, expand=True)

        # Totales
        totals_frame = tk.Frame(form_frame, bg="white")
        totals_frame.pack(fill=tk.X, pady=10)

        # Subtotal, IVA, Total (alineados a la derecha)
        totals = [
            ("Subtotal:", "0.00"),
            ("IVA (16%):", "0.00"),
            ("TOTAL:", "0.00")
        ]

        for label, value in totals:
            frame = tk.Frame(totals_frame, bg="white")
            frame.pack(anchor=tk.E, pady=2)
            
            CustomLabel(
                frame,
                text=label,
                font=("Arial", 12, "bold"),
                bg="white",
                width=15,
                anchor=tk.E
            ).pack(side=tk.LEFT)
            
            CustomLabel(
                frame,
                text=value,
                font=("Arial", 12, "bold"),
                bg="white",
                width=15,
                anchor=tk.E
            ).pack(side=tk.LEFT)

        # Botones de acción (agrupados como en tu versión)
        controls_frame = tk.Frame(self, bg="#f5f5f5")
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        action_frame = tk.Frame(controls_frame, bg="#f5f5f5")
        action_frame.pack(side=tk.RIGHT)

        buttons = [
            ("Crear Orden", self.create_order),
            ("Limpiar", self.clear_form),
            ("Buscar Producto", self.search_product),
            ("Ver Órdenes", self.view_orders)
        ]

        for text, command in buttons:
            btn = CustomButton(
                action_frame,
                text=text,
                command=command,
                padding=8,
                width=12,
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Barra de estado
        self.status_bar = CustomLabel(
            self,
            text="Listo",
            font=("Arial", 10),
            fg="#666",
            bg="#f5f5f5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def go_back(self) -> None:
        self.parent.state('normal')
        self.open_previous_screen_callback()

    def create_order(self) -> None:
        pass

    def clear_form(self) -> None:
        pass

    def search_product(self) -> None:
        pass

    def view_orders(self) -> None:
        pass
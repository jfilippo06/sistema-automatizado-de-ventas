from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from sqlite_cli.models.tax_model import Tax

class PurchaseOrderViewer(tk.Toplevel):
    def __init__(self, parent, order_number, supplier_info, items, subtotal, taxes, total, delivery_date, created_by):
        super().__init__(parent)
        self.parent = parent
        self.title(f"Orden de Compra - {order_number}")
        
        # Configurar ventana modal centrada
        self.transient(parent)
        self.grab_set()
        
        # Tamaño fijo de la ventana (aumentado a 900px de ancho)
        window_width = 950
        window_height = 650
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición para centrar
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        
        # Frame principal con scroll y márgenes
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white", padx=15, pady=15)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Encabezado de la orden
        header_frame = tk.Frame(scrollable_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Logo e información de la empresa (izquierda)
        company_frame = tk.Frame(header_frame, bg="white")
        company_frame.pack(side="left", anchor="nw")
        
        tk.Label(company_frame, text="RN&M SERVICIOS INTEGRALES, C.A", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(company_frame, text="RIF: J-40339817-8", 
                font=("Arial", 10), bg="white").pack(anchor="w")
        tk.Label(company_frame, text="Av. Principal, Edif. Empresarial", 
                font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Número de orden y fecha (derecha)
        order_frame = tk.Frame(header_frame, bg="white")
        order_frame.pack(side="right", anchor="ne")
        
        tk.Label(order_frame, text=f"ORDEN DE COMPRA N°: {order_number}", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="e")
        tk.Label(order_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 
                font=("Arial", 10), bg="white").pack(anchor="e")
        tk.Label(order_frame, text=f"Fecha Entrega: {delivery_date}", 
                font=("Arial", 10), bg="white").pack(anchor="e")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Información del proveedor
        supplier_frame = tk.Frame(scrollable_frame, bg="white")
        supplier_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(supplier_frame, text="PROVEEDOR:", 
                font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(supplier_frame, text=supplier_info, 
                font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Tabla de productos
        table_frame = tk.Frame(scrollable_frame, bg="white")
        table_frame.pack(fill="x", pady=(0, 15))
        
        # Encabezados de la tabla
        headers = ["Código", "Descripción", "Cantidad", "P. Unitario", "Total"]
        widths = [120, 400, 80, 120, 120]  # Ajustado para el nuevo ancho
        
        header_frame = tk.Frame(table_frame, bg="#4a6fa5")
        header_frame.pack(fill="x")
        
        for header, width in zip(headers, widths):
            cell = tk.Frame(header_frame, bg="#4a6fa5", height=30, width=width)
            cell.pack_propagate(False)
            cell.pack(side="left", padx=1)
            tk.Label(cell, text=header, fg="white", bg="#4a6fa5", 
                   font=("Arial", 10, "bold"), anchor="center").pack(expand=True, fill="both")
        
        # Cuerpo de la tabla
        for item in items:
            row_frame = tk.Frame(table_frame, bg="white", height=30)
            row_frame.pack_propagate(False)
            row_frame.pack(fill="x", pady=1)
            
            values = [
                item['code'],
                item['description'],
                str(item['quantity']),
                f"{item['unit_price']:,.2f}",
                f"{item['total']:,.2f}"
            ]
            
            for value, width in zip(values, widths):
                cell = tk.Frame(row_frame, bg="white", height=30, width=width, bd=1, relief="solid")
                cell.pack_propagate(False)
                cell.pack(side="left", padx=1)
                tk.Label(cell, text=value, bg="white", 
                       font=("Arial", 10), anchor="w").pack(expand=True, fill="both")
        
        # Totales
        totals_frame = tk.Frame(scrollable_frame, bg="white")
        totals_frame.pack(fill="x", pady=(15, 20))
        
        iva_tax = Tax.get_by_name("IVA")
        
        # Subtotal y IVA (si aplica)
        if iva_tax and iva_tax.get('status_name') == 'active':
            subtotal_frame = tk.Frame(totals_frame, bg="white")
            subtotal_frame.pack(anchor="e", pady=2)
            tk.Label(subtotal_frame, text="Subtotal:", 
                    font=("Arial", 10), bg="white").pack(side="left", padx=5)
            tk.Label(subtotal_frame, text=f"{subtotal:,.2f}", 
                    font=("Arial", 10), bg="white").pack(side="left")
            
            iva_frame = tk.Frame(totals_frame, bg="white")
            iva_frame.pack(anchor="e", pady=2)
            tk.Label(iva_frame, text=f"IVA ({iva_tax['value']}%):", 
                    font=("Arial", 10), bg="white").pack(side="left", padx=5)
            tk.Label(iva_frame, text=f"{taxes:,.2f}", 
                    font=("Arial", 10), bg="white").pack(side="left")
        
        # Total
        total_frame = tk.Frame(totals_frame, bg="white")
        total_frame.pack(anchor="e", pady=(10, 0))
        tk.Label(total_frame, text="TOTAL:", 
                font=("Arial", 12, "bold"), bg="white").pack(side="left", padx=5)
        tk.Label(total_frame, text=f"{total:,.2f}", 
                font=("Arial", 12, "bold"), bg="white").pack(side="left")
        
        # Botón de regresar
        btn_frame = tk.Frame(scrollable_frame, bg="white")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        tk.Button(
            btn_frame, 
            text="Regresar", 
            command=self.destroy,
            font=("Arial", 10),
            padx=20,
            pady=5
        ).pack(side="right")
        
        # Información del creador
        creator_frame = tk.Frame(scrollable_frame, bg="white")
        creator_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(creator_frame, text=f"Creado por: {created_by}", 
                font=("Arial", 9), bg="white").pack(anchor="w")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Notas
        notes_frame = tk.Frame(scrollable_frame, bg="white")
        notes_frame.pack(fill="x", pady=(5, 15))
        
        tk.Label(notes_frame, text="Notas:", 
                font=("Arial", 9, "italic"), bg="white").pack(anchor="w")
        tk.Label(notes_frame, text="Esta orden de compra es generada automáticamente por el sistema.", 
                font=("Arial", 9, "italic"), bg="white").pack(anchor="w")
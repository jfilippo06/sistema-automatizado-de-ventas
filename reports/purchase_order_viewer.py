from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from sqlite_cli.models.tax_model import Tax
from utils.session_manager import SessionManager

class PurchaseOrderViewer(tk.Toplevel):
    def __init__(self, parent, order_id, supplier_info, items, subtotal, taxes, total):
        super().__init__(parent)
        self.parent = parent
        self.title(f"Orden de Compra - #{order_id}")
        
        # Configurar ventana modal centrada
        self.transient(parent)
        self.grab_set()
        
        # Tamaño fijo de la ventana
        window_width = 880
        window_height = 700
        
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
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, padx=15, pady=15)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Información de la empresa
        tk.Label(scrollable_frame, text="RN&M Servicios Integrales, C.A", 
                font=("Arial", 14, "bold")).pack(pady=(0, 5))
        tk.Label(scrollable_frame, text="RIF: J-40339817-8", 
                font=("Arial", 12)).pack(pady=(0, 10))
        tk.Label(scrollable_frame, text="ORDEN DE COMPRA", 
                font=("Arial", 16, "bold"), fg="#333").pack(pady=(0, 15))
        
        # Separador
        ttk.Separator(scrollable_frame).pack(fill="x", padx=10, pady=10)
        
        # Información de la orden, proveedor y empleado
        info_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        # Columna izquierda - Información de la orden
        left_frame = tk.Frame(info_frame)
        left_frame.pack(side="left", anchor="w", padx=20)
        
        tk.Label(left_frame, text=f"N° Orden: {order_id}", 
                font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(left_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(left_frame, text=f"Estado: Pendiente", 
                font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Columna derecha - Información del proveedor y empleado
        right_frame = tk.Frame(info_frame)
        right_frame.pack(side="right", anchor="e", padx=20)
        
        tk.Label(right_frame, text="Proveedor:", 
                font=("Arial", 10, "bold")).pack(anchor="e", pady=2)
        tk.Label(right_frame, text=supplier_info, 
                font=("Arial", 10)).pack(anchor="e", pady=2)
        
        tk.Label(right_frame, text="Creado por:", 
                font=("Arial", 10, "bold")).pack(anchor="e", pady=(10, 2))
        tk.Label(right_frame, text=self._get_employee_info(), 
                font=("Arial", 10)).pack(anchor="e", pady=2)
        
        # Tabla de productos
        table_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
        table_frame.pack(fill="x", pady=(0, 15))
        
        columns = ("Código", "Descripción", "Cantidad", "P. Unitario", "Total")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=min(8, len(items)))
        
        # Configurar columnas
        tree.heading("Código", text="Código")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("P. Unitario", text="P. Unitario")
        tree.heading("Total", text="Total")
        
        tree.column("Código", width=100, anchor="center")
        tree.column("Descripción", width=300, anchor="w")
        tree.column("Cantidad", width=80, anchor="center")
        tree.column("P. Unitario", width=120, anchor="e")
        tree.column("Total", width=120, anchor="e")
        
        # Insertar datos
        for item in items:
            tree.insert("", "end", values=(
                item['code'],
                item['description'],
                item['quantity'],
                f"{item['unit_price']:.2f}",
                f"{item['total']:.2f}"
            ))
        
        tree.pack(fill="x")
        
        # Totales
        totals_frame = tk.Frame(scrollable_frame, padx=10, pady=15)
        totals_frame.pack(fill="x", pady=(10, 20))
        
        iva_tax = Tax.get_by_name("IVA")
        if iva_tax and iva_tax.get('status_name') == 'active':
            tk.Label(totals_frame, text=f"Subtotal: {subtotal:.2f}",
                    font=("Arial", 10, "bold")).pack(side="right", padx=15)
            tk.Label(totals_frame, text=f"IVA ({iva_tax['value']}%): {taxes:.2f}",
                    font=("Arial", 10, "bold")).pack(side="right", padx=15)
        
        tk.Label(totals_frame, text=f"TOTAL: {total:.2f}",
                font=("Arial", 12, "bold")).pack(side="right", padx=15)
        
        # Botones
        btn_frame = tk.Frame(scrollable_frame, padx=10, pady=20)
        btn_frame.pack(fill="x")
        
        tk.Button(
            btn_frame,
            text="Cerrar",
            command=self.destroy,
            font=("Arial", 10),
            width=15
        ).pack(side="right", padx=5)

    def _get_employee_info(self) -> str:
        """Obtiene la información del empleado desde SessionManager"""
        current_user = SessionManager.get_current_user()
        
        if not current_user:
            return "No disponible"
        
        if 'first_name' in current_user and 'last_name' in current_user:
            full_name = f"{current_user['first_name']} {current_user['last_name']}"
            if current_user.get('username'):
                return f"{full_name} ({current_user['username']})"
            return full_name
        
        if 'username' in current_user:
            return current_user['username']
        
        if 'id' in current_user:
            return f"Empleado ID: {current_user['id']}"
        
        return "No disponible"
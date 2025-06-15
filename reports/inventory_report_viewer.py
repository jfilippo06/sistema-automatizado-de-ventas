import tkinter as tk
from tkinter import ttk
from datetime import datetime
from utils.session_manager import SessionManager

class InventoryReportViewer(tk.Toplevel):
    def __init__(self, parent, title, items, filters):
        super().__init__(parent)
        self.title(f"Reporte de Inventario - {datetime.now().strftime('%Y-%m-%d')}")
        self.parent = parent
        
        # Configurar ventana modal centrada
        self.transient(parent)
        self.grab_set()
        
        self.resizable(False, False)
        self.state('zoomed')
        
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
        
        # Encabezado del reporte
        header_frame = tk.Frame(scrollable_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Información de la empresa (izquierda)
        company_frame = tk.Frame(header_frame, bg="white")
        company_frame.pack(side="left", anchor="nw")
        
        tk.Label(company_frame, text="RN&M SERVICIOS INTEGRALES, C.A", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(company_frame, text="RIF: J-40339817-8", 
                font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Título y fecha (derecha)
        title_frame = tk.Frame(header_frame, bg="white")
        title_frame.pack(side="right", anchor="ne")
        
        tk.Label(title_frame, text=title, 
                font=("Arial", 14, "bold"), bg="white").pack(anchor="e")
        tk.Label(title_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                font=("Arial", 10), bg="white").pack(anchor="e")
        tk.Label(title_frame, text=f"Filtros: {filters}", 
                font=("Arial", 9), bg="white").pack(anchor="e")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Tabla de productos
        table_frame = tk.Frame(scrollable_frame, bg="white")
        table_frame.pack(fill="x", pady=(0, 15))
        
        # Encabezados de la tabla (sin Estado)
        headers = ["Código", "Producto", "Descripción", "Cantidad", "Existencias", 
                  "Stock Mín", "Stock Máx", "P. Compra", "P. Venta", "Proveedor"]
        widths = [80, 150, 300, 70, 80, 80, 80, 90, 90, 150]  # Descripción aumentada a 300
        
        header_frame = tk.Frame(table_frame, bg="#4a6fa5")
        header_frame.pack(fill="x")
        
        for header, width in zip(headers, widths):
            cell = tk.Frame(header_frame, bg="#4a6fa5", height=30)
            cell.pack_propagate(False)
            cell.pack(side="left", padx=1)
            tk.Label(cell, text=header, fg="white", bg="#4a6fa5", 
                   font=("Arial", 10, "bold")).pack(expand=True, fill="both")
            cell.config(width=width)
        
        # Cuerpo de la tabla (sin Estado)
        for item in items:
            row_frame = tk.Frame(table_frame, bg="white", height=30)
            row_frame.pack_propagate(False)
            row_frame.pack(fill="x", pady=1)
            
            expiration_date = item['expiration_date'] if item['expiration_date'] else ""
            values = [
                item['code'],
                item['product'],
                item['description'],
                str(item['quantity']),
                str(item['stock']),
                str(item['min_stock']),
                str(item['max_stock']),
                f"{item['cost']:.2f}",
                f"{item['price']:.2f}",
                item['supplier_company'] if item['supplier_company'] else ""
            ]
            
            for value, width in zip(values, widths):
                cell = tk.Frame(row_frame, bg="white", height=30, bd=1, relief="solid")
                cell.pack_propagate(False)
                cell.pack(side="left", padx=1)
                tk.Label(cell, text=value, bg="white", 
                       font=("Arial", 9)).pack(expand=True, fill="both")
                cell.config(width=width)
        
        # Totales y resumen
        summary_frame = tk.Frame(scrollable_frame, bg="white")
        summary_frame.pack(fill="x", pady=(15, 20))
        
        total_items = len(items)
        total_quantity = sum(item['quantity'] for item in items)
        total_stock = sum(item['stock'] for item in items)
        
        tk.Label(summary_frame, text=f"Total Productos: {total_items}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        tk.Label(summary_frame, text=f"Total en Almacén: {total_quantity}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        tk.Label(summary_frame, text=f"Total Existencias: {total_stock}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        
        # Información del generador
        creator_frame = tk.Frame(scrollable_frame, bg="white")
        creator_frame.pack(fill="x", pady=(20, 0))
        
        current_user = SessionManager.get_current_user()
        user_info = "No disponible"
        
        if current_user:
            if 'first_name' in current_user and 'last_name' in current_user:
                user_info = f"{current_user['first_name']} {current_user['last_name']}"
            elif 'username' in current_user:
                user_info = current_user['username']
        
        tk.Label(creator_frame, text=f"Generado por: {user_info}", 
                font=("Arial", 9), bg="white").pack(anchor="w")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Notas
        notes_frame = tk.Frame(scrollable_frame, bg="white")
        notes_frame.pack(fill="x", pady=(5, 15))
        
        tk.Label(notes_frame, text="Notas:", 
                font=("Arial", 9, "italic"), bg="white").pack(anchor="w")
        tk.Label(notes_frame, text="Este reporte fue generado automáticamente por el sistema.", 
                font=("Arial", 9, "italic"), bg="white").pack(anchor="w")
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from utils.session_manager import SessionManager

class InventoryMovementViewer(tk.Toplevel):
    def __init__(self, parent, title, product_info, movements, filters):
        super().__init__(parent)
        self.title(f"Reporte de Movimientos - {datetime.now().strftime('%Y-%m-%d')}")
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
        
        # Información del producto
        product_frame = tk.Frame(scrollable_frame, bg="white")
        product_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(product_frame, text=f"Producto: {product_info['product']}", 
                font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(product_frame, text=f"Código: {product_info['code']}", 
                font=("Arial", 10), bg="white").pack(anchor="w")
        tk.Label(product_frame, text=f"Descripción: {product_info['description']}", 
                font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Tabla de movimientos
        table_frame = tk.Frame(scrollable_frame, bg="white")
        table_frame.pack(fill="x", pady=(0, 15))
        
        # Encabezados de la tabla
        headers = ["Fecha", "Tipo", "Cambio Cant.", "Cambio Exist.", "Ant. Cant.", 
                  "Nva. Cant.", "Ant. Exist.", "Nva. Exist.", "Usuario", "Referencia", "Notas"]
        widths = [120, 100, 90, 90, 90, 90, 90, 90, 100, 100, 200]
        
        header_frame = tk.Frame(table_frame, bg="#4a6fa5")
        header_frame.pack(fill="x")
        
        for header, width in zip(headers, widths):
            cell = tk.Frame(header_frame, bg="#4a6fa5", height=30, width=width)
            cell.pack_propagate(False)
            cell.pack(side="left", padx=1)
            tk.Label(cell, text=header, fg="white", bg="#4a6fa5", 
                   font=("Arial", 10, "bold"), anchor="center").pack(expand=True, fill="both")
        
        # Cuerpo de la tabla
        for movement in movements:
            row_frame = tk.Frame(table_frame, bg="white", height=30)
            row_frame.pack_propagate(False)
            row_frame.pack(fill="x", pady=1)
            
            values = [
                movement['created_at'],
                movement['movement_type'],
                str(movement['quantity_change']),
                str(movement['stock_change']),
                str(movement['previous_quantity']),
                str(movement['new_quantity']),
                str(movement['previous_stock']),
                str(movement['new_stock']),
                movement['user'],
                f"{movement['reference_type']}" if movement['reference_type'] else "",
                movement['notes']
            ]
            
            for value, width in zip(values, widths):
                cell = tk.Frame(row_frame, bg="white", height=30, width=width, bd=1, relief="solid")
                cell.pack_propagate(False)
                cell.pack(side="left", padx=1)
                tk.Label(cell, text=value, bg="white", 
                       font=("Arial", 9), anchor="w").pack(expand=True, fill="both")
        
        # Resumen
        summary_frame = tk.Frame(scrollable_frame, bg="white")
        summary_frame.pack(fill="x", pady=(15, 20))
        
        total_movements = len(movements)
        total_quantity_change = sum(movement['quantity_change'] for movement in movements)
        total_stock_change = sum(movement['stock_change'] for movement in movements)
        
        tk.Label(summary_frame, text=f"Total Movimientos: {total_movements}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        tk.Label(summary_frame, text=f"Cambio Total en Cantidad: {total_quantity_change}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        tk.Label(summary_frame, text=f"Cambio Total en Existencias: {total_stock_change}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        
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
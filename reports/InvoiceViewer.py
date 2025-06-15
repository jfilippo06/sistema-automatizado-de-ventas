from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import os
from sqlite_cli.models.tax_model import Tax
from widgets.custom_button import CustomButton
from utils.session_manager import SessionManager

class InvoiceViewer(tk.Toplevel):
    def __init__(self, parent, invoice_id, customer_info, items, subtotal, taxes, total):
        super().__init__(parent)
        self.parent = parent
        self.title(f"Recibo Digital - #{invoice_id}")
        
        # Configurar ventana modal centrada
        self.transient(parent)
        self.grab_set()
        
        # Tamaño fijo de la ventana
        window_width = 750  # Aumentado para acomodar el margen
        window_height = 750
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición para centrar
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        
        # Frame principal con margen gris
        outer_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame interno blanco que contendrá todo el contenido
        main_frame = tk.Frame(outer_frame, bg="white", padx=5, pady=5)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Margen gris visible
        
        canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white", padx=15, pady=15)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Encabezado
        header_frame = tk.Frame(scrollable_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Información de la empresa (izquierda)
        company_frame = tk.Frame(header_frame, bg="white")
        company_frame.pack(side="left", anchor="nw")
        
        tk.Label(company_frame, text="RN&M SERVICIOS INTEGRALES, C.A", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(company_frame, text="RIF: J-40339817-8", 
                font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Número de recibo y fecha (derecha)
        invoice_frame = tk.Frame(header_frame, bg="white")
        invoice_frame.pack(side="right", anchor="ne")
        
        tk.Label(invoice_frame, text=f"RECIBO N°: {invoice_id}", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="e")
        tk.Label(invoice_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                font=("Arial", 10), bg="white").pack(anchor="e")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Información del cliente
        customer_frame = tk.Frame(scrollable_frame, bg="white")
        customer_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(customer_frame, text="CLIENTE:", 
                font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(customer_frame, text=customer_info, 
                font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Tabla de productos/servicios
        table_frame = tk.Frame(scrollable_frame, bg="white")
        table_frame.pack(fill="x", pady=(0, 15))
        
        # Encabezados de la tabla
        headers = ["Tipo", "Descripción", "Cantidad", "P. Unitario", "Total"]
        widths = [80, 300, 70, 90, 90]
        
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
            
            item_type = "Servicio" if item.get('is_service', False) else "Producto"
            values = [
                item_type,
                item['name'],
                str(item['quantity']),
                f"{item['unit_price']:.2f}",
                f"{item['total']:.2f}"
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
        if iva_tax and iva_tax.get('status_name') == 'active':
            subtotal_frame = tk.Frame(totals_frame, bg="white")
            subtotal_frame.pack(anchor="e", pady=2)
            tk.Label(subtotal_frame, text="Subtotal:", 
                    font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=5)
            tk.Label(subtotal_frame, text=f"{subtotal:.2f}", 
                    font=("Arial", 10, "bold"), bg="white").pack(side="left")
            
            iva_frame = tk.Frame(totals_frame, bg="white")
            iva_frame.pack(anchor="e", pady=2)
            tk.Label(iva_frame, text=f"IVA ({iva_tax['value']}%):", 
                    font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=5)
            tk.Label(iva_frame, text=f"{taxes:.2f}", 
                    font=("Arial", 10, "bold"), bg="white").pack(side="left")
        
        # Total
        total_frame = tk.Frame(totals_frame, bg="white")
        total_frame.pack(anchor="e", pady=(10, 0))
        tk.Label(total_frame, text="TOTAL:", 
                font=("Arial", 12, "bold"), bg="white").pack(side="left", padx=5)
        tk.Label(total_frame, text=f"{total:.2f}", 
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
            pady=5,
            bg="#f0f0f0",
            relief=tk.GROOVE
        ).pack(side="right")
        
        # Información del empleado
        employee_frame = tk.Frame(scrollable_frame, bg="white")
        employee_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(employee_frame, text=f"Atendido por: {self._get_employee_info()}", 
                font=("Arial", 9), bg="white").pack(anchor="w")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Notas
        notes_frame = tk.Frame(scrollable_frame, bg="white")
        notes_frame.pack(fill="x", pady=(5, 15))
        
        tk.Label(notes_frame, text="Notas:", 
                font=("Arial", 9, "italic"), bg="white").pack(anchor="w")
        tk.Label(notes_frame, text="Este recibo es generado automáticamente por el sistema.", 
                font=("Arial", 9, "italic"), bg="white").pack(anchor="w")
        
        if any(item.get('is_service', False) for item in items):
            tk.Label(notes_frame, text="Nota: Los servicios solicitados serán atendidos según lo acordado.",
                   font=("Arial", 9, "italic"), bg="white").pack(anchor="w")

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
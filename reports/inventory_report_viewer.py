import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from utils.session_manager import SessionManager
from utils.pdf_generator import PDFGenerator

class InventoryReportViewer(tk.Toplevel):
    def __init__(self, parent, title, items, filters):
        super().__init__(parent)
        self.title(f"Reporte de Inventario - {datetime.now().strftime('%Y-%m-%d')}")
        self.parent = parent
        self.items = items
        self.report_title = title
        self.filters = filters
        self.images = {}  # Diccionario para almacenar las imágenes
        
        # Configurar ventana modal centrada
        self.transient(parent)
        self.grab_set()
        
        self.resizable(False, False)
        self.state('zoomed')
        
        self.configure_ui()

    def configure_ui(self):
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
        
        # Información de la empresa (izquierda) - Ahora con imagen
        company_frame = tk.Frame(header_frame, bg="white")
        company_frame.pack(side="left", anchor="nw")
        
        # Cargar y mostrar imagen de la empresa
        try:
            img = Image.open("assets/empresa.png").resize((150, 70), Image.Resampling.LANCZOS)
            self.images["empresa"] = ImageTk.PhotoImage(img)
            img_label = tk.Label(company_frame, image=self.images["empresa"], bg="white")
            img_label.pack(anchor="w")
        except Exception as e:
            print(f"Error cargando imagen de empresa: {e}")
            # Fallback a texto si no se puede cargar la imagen
            tk.Label(company_frame, text="RN&M SERVICIOS INTEGRALES, C.A", 
                    font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
            tk.Label(company_frame, text="RIF: J-40339817-8", 
                    font=("Arial", 10), bg="white").pack(anchor="w")
        
        # Título y fecha (derecha)
        title_frame = tk.Frame(header_frame, bg="white")
        title_frame.pack(side="right", anchor="ne")
        
        tk.Label(title_frame, text=self.report_title, 
                font=("Arial", 14, "bold"), bg="white").pack(anchor="e")
        tk.Label(title_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                font=("Arial", 10), bg="white").pack(anchor="e")
        tk.Label(title_frame, text=f"Filtros: {self.filters}", 
                font=("Arial", 9), bg="white").pack(anchor="e")
        
        # Línea divisoria
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Tabla de productos
        table_frame = tk.Frame(scrollable_frame, bg="white")
        table_frame.pack(fill="x", pady=(0, 15))
        
        # Encabezados de la tabla (sin Estado)
        headers = ["Código", "Producto", "Descripción", "Cantidad", "Stock", 
                  "Stock Mín", "Stock Máx", "P. Compra", "P. Venta", "Proveedor"]
        widths = [80, 150, 300, 70, 80, 80, 80, 90, 90, 150]  # Descripción aumentada a 300
        
        header_frame = tk.Frame(table_frame, bg="#4a6fa5")
        header_frame.pack(fill="x")
        
        for header, width in zip(headers, widths):
            cell = tk.Frame(header_frame, bg="#4a6fa5", height=30, width=width)
            cell.pack_propagate(False)
            cell.pack(side="left", padx=1)
            tk.Label(cell, text=header, fg="white", bg="#4a6fa5", 
                   font=("Arial", 10, "bold"), anchor="center").pack(expand=True, fill="both")
        
        # Cuerpo de la tabla (sin Estado)
        for item in self.items:
            row_frame = tk.Frame(table_frame, bg="white", height=30)
            row_frame.pack_propagate(False)
            row_frame.pack(fill="x", pady=1)
            
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
                item.get('supplier_company', '')
            ]
            
            for value, width in zip(values, widths):
                cell = tk.Frame(row_frame, bg="white", height=30, width=width, bd=1, relief="solid")
                cell.pack_propagate(False)
                cell.pack(side="left", padx=1)
                tk.Label(cell, text=value, bg="white", 
                       font=("Arial", 9), anchor="w").pack(expand=True, fill="both")
        
        # Totales y resumen
        summary_frame = tk.Frame(scrollable_frame, bg="white")
        summary_frame.pack(fill="x", pady=(15, 20))
        
        total_items = len(self.items)
        total_quantity = sum(item['quantity'] for item in self.items)
        total_stock = sum(item['stock'] for item in self.items)
        
        tk.Label(summary_frame, text=f"Total Productos: {total_items}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        tk.Label(summary_frame, text=f"Total en Cantidad: {total_quantity}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        tk.Label(summary_frame, text=f"Total Stock: {total_stock}", 
                font=("Arial", 10), bg="white").pack(side="left", padx=20)
        
        # Botones de regresar y generar PDF
        btn_frame = tk.Frame(scrollable_frame, bg="white")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        # Botón de PDF
        tk.Button(
            btn_frame, 
            text="Generar PDF", 
            command=self.generate_pdf,
            font=("Arial", 10),
            padx=20,
            pady=5,
            bg="#4a6fa5",
            fg="white"
        ).pack(side="right", padx=10)
        
        # Botón de regresar
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

    def generate_pdf(self):
        """Genera el reporte en PDF usando la clase PDFGenerator"""
        PDFGenerator.generate_inventory_report(
            parent=self,
            title=self.report_title,
            items=self.items,
            filters=self.filters
        )
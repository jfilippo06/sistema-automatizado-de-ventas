from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import os
from sqlite_cli.models.tax_model import Tax
from widgets.custom_button import CustomButton

class InvoiceViewer(tk.Toplevel):
    def __init__(self, parent, invoice_id, customer_info, items, subtotal, taxes, total):
        super().__init__(parent)
        self.parent = parent
        self.title(f"Factura Digital - #{invoice_id}")
        
        # Configurar ventana modal centrada
        self.transient(parent)
        self.grab_set()
        
        # Tamaño fijo de la ventana
        window_width = 650  # Aumentado para acomodar la columna adicional
        window_height = 650
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición para centrar
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        
        # Frame principal con scroll
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Logo e información de la empresa
        try:
            logo_path = os.path.join("assets", "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((100, 100), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(scrollable_frame, image=self.logo).pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        # Información de la empresa
        tk.Label(scrollable_frame, text="RN&M Servicios Integrales, C.A", 
                font=("Arial", 14, "bold")).pack()
        tk.Label(scrollable_frame, text="RIF: J-40339817-8", 
                font=("Arial", 12)).pack()
        tk.Label(scrollable_frame, text="FACTURA", 
                font=("Arial", 16, "bold"), fg="#333").pack(pady=5)
        
        # Separador
        ttk.Separator(scrollable_frame).pack(fill="x", padx=20, pady=5)
        
        # Información de factura y cliente en dos columnas
        info_frame = tk.Frame(scrollable_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Columna izquierda - Información de factura
        left_frame = tk.Frame(info_frame)
        left_frame.pack(side="left", anchor="w")
        
        tk.Label(left_frame, text=f"N° Factura: {invoice_id}", 
                font=("Arial", 10)).pack(anchor="w")
        tk.Label(left_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                font=("Arial", 10)).pack(anchor="w")
        
        # Columna derecha - Información del cliente
        right_frame = tk.Frame(info_frame)
        right_frame.pack(side="right", anchor="e")
        
        tk.Label(right_frame, text="Cliente:", 
                font=("Arial", 10, "bold")).pack(anchor="e")
        tk.Label(right_frame, text=customer_info, 
                font=("Arial", 10)).pack(anchor="e")
        
        # Tabla de productos/servicios
        table_frame = tk.Frame(scrollable_frame)
        table_frame.pack(fill="x", padx=20, pady=10)
        
        # Nueva columna para Tipo (Producto/Servicio)
        columns = ("Tipo", "Descripción", "Cantidad", "P. Unitario", "Total")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=min(8, len(items)))
        
        # Configurar columnas
        tree.heading("Tipo", text="Tipo")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("P. Unitario", text="P. Unitario")
        tree.heading("Total", text="Total")
        
        tree.column("Tipo", width=80, anchor="center")
        tree.column("Descripción", width=220, anchor="w")
        tree.column("Cantidad", width=70, anchor="center")
        tree.column("P. Unitario", width=90, anchor="e")
        tree.column("Total", width=90, anchor="e")
        
        # Insertar datos con distinción entre productos y servicios
        for item in items:
            item_type = "Servicio" if item.get('is_service', False) else "Producto"
            tree.insert("", "end", values=(
                item_type,
                item['name'],
                item['quantity'],
                f"{item['unit_price']:.2f}",
                f"{item['total']:.2f}"
            ))
        
        tree.pack(fill="x")
        
        # Totales
        totals_frame = tk.Frame(scrollable_frame)
        totals_frame.pack(fill="x", padx=20, pady=10)
        
        iva_tax = Tax.get_by_name("IVA")
        if iva_tax and iva_tax.get('status_name') == 'active':
            tk.Label(totals_frame, text=f"Subtotal: {subtotal:.2f}",
                    font=("Arial", 10, "bold")).pack(side="right", padx=5)
            tk.Label(totals_frame, text=f"IVA ({iva_tax['value']}%): {taxes:.2f}",
                    font=("Arial", 10, "bold")).pack(side="right", padx=5)
        
        tk.Label(totals_frame, text=f"TOTAL: {total:.2f}",
                font=("Arial", 12, "bold")).pack(side="right", padx=5)
        
        # Nota sobre servicios
        if any(item.get('is_service', False) for item in items):
            note_frame = tk.Frame(scrollable_frame)
            note_frame.pack(fill="x", padx=20, pady=5)
            tk.Label(note_frame, text="Nota: Los servicios solicitados serán atendidos según lo acordado.",
                   font=("Arial", 9), fg="#666").pack(side="left")
        
        # Botones
        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(pady=10)
        
        CustomButton(button_frame, text="Imprimir Factura",
                   command=self.print_invoice, padding=6, width=18).pack(side="left", padx=10)
        CustomButton(button_frame, text="Cerrar",
                   command=self.destroy, padding=6, width=18).pack(side="right", padx=10)
    
    def print_invoice(self):
        """Función para manejar la impresión de la factura"""
        messagebox.showinfo("Imprimir", "La factura se enviará a la impresora", parent=self)
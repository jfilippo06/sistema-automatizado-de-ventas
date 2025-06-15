from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import Toplevel
from typing import List, Dict

class PDFGenerator:
    @staticmethod
    def generate_inventory_report(
        parent: Toplevel,
        title: str,
        items: List[Dict],
        filters: str,
        company_name: str = "RN&M SERVICIOS INTEGRALES, C.A",
        company_rif: str = "RIF: J-40339817-8"
    ) -> None:
        """Genera un reporte de inventario en PDF"""
        # Mostrar diálogo para guardar el archivo
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte como",
            initialfile=f"Reporte_Inventario_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )
        
        if not file_path:  # El usuario canceló
            return
        
        try:
            # Crear el documento PDF
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )
            
            # Estilos
            styles = getSampleStyleSheet()
            style_title = styles["Title"]
            style_normal = styles["Normal"]
            style_heading = styles["Heading2"]
            
            # Contenido del PDF
            elements = []
            
            # Encabezado
            elements.append(Paragraph(company_name, style_title))
            elements.append(Paragraph(company_rif, style_normal))
            elements.append(Spacer(1, 12))
            
            # Título y fecha
            elements.append(Paragraph(title, style_heading))
            elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_normal))
            elements.append(Paragraph(f"Filtros: {filters}", style_normal))
            elements.append(Spacer(1, 24))
            
            # Tabla de datos
            headers = ["Código", "Producto", "Descripción", "Cant.", "Exist.", 
                      "Mín", "Máx", "P. Compra", "P. Venta", "Proveedor"]
            
            # Preparar datos para la tabla
            data = [headers]
            for item in items:
                row = [
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
                data.append(row)
            
            # Crear tabla
            table = Table(data, colWidths=[0.7*inch, 1.2*inch, 2.0*inch, 0.5*inch, 
                                          0.5*inch, 0.5*inch, 0.5*inch, 0.7*inch, 
                                          0.7*inch, 1.2*inch])
            
            # Estilo de la tabla
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a6fa5")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 24))
            
            # Totales
            total_items = len(items)
            total_quantity = sum(item['quantity'] for item in items)
            total_stock = sum(item['stock'] for item in items)
            
            elements.append(Paragraph(f"Total Productos: {total_items}", style_normal))
            elements.append(Paragraph(f"Total en Cantidad: {total_quantity}", style_normal))
            elements.append(Paragraph(f"Total Existencias: {total_stock}", style_normal))
            elements.append(Spacer(1, 24))
            
            # Generar el PDF
            doc.build(elements)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Éxito",
                f"El reporte se ha generado correctamente en:\n{file_path}",
                parent=parent
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo generar el PDF:\n{str(e)}",
                parent=parent
            )
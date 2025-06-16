from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import Toplevel
from typing import List, Dict
from utils.session_manager import SessionManager

class InventoryReportPDF:
    @staticmethod
    def generate_inventory_report(
        parent: Toplevel,
        title: str,
        items: List[Dict],
        filters: str,
        company_name: str = "RN&M SERVICIOS INTEGRALES, C.A",
        company_rif: str = "RIF: J-40339817-8"
    ) -> None:
        """Genera un reporte de inventario en PDF en orientación horizontal"""
        # Mostrar diálogo para guardar el archivo
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte como",
            initialfile=f"Reporte_Inventario_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            parent=parent
        )
        
        if not file_path:  # El usuario canceló
            return
        
        try:
            # Crear el documento PDF en orientación horizontal
            doc = SimpleDocTemplate(
                file_path,
                pagesize=landscape(letter),
                rightMargin=20,
                leftMargin=20,
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
            header_table = Table([
                [Paragraph(company_name, style_title), "", Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_normal)],
                [Paragraph(company_rif, style_normal), "", Paragraph(f"Filtros: {filters}", style_normal)],
                ["", Paragraph(title, style_heading), ""]
            ], colWidths=[3*inch, 3*inch, 3*inch])
            
            header_table.setStyle(TableStyle([
                ('SPAN', (0,0), (0,1)),  # Combinar celdas para company info
                ('SPAN', (2,0), (2,1)),  # Combinar celdas para fecha/filtros
                ('SPAN', (1,2), (1,2)),  # Título centrado
                ('ALIGN', (1,2), (1,2), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            
            elements.append(header_table)
            elements.append(Spacer(1, 24))
            
            # Tabla de datos - ajustamos anchos para orientación horizontal
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
            
            # Anchos de columna ajustados para horizontal
            col_widths = [
                0.8*inch,  # Código
                1.2*inch,  # Producto
                2.5*inch,  # Descripción
                0.5*inch,  # Cantidad
                0.5*inch,  # Existencias
                0.5*inch,  # Mín
                0.5*inch,  # Máx
                0.7*inch,  # P. Compra
                0.7*inch,  # P. Venta
                1.5*inch   # Proveedor
            ]
            
            # Crear tabla principal
            table = Table(data, colWidths=col_widths, repeatRows=1)
            
            # Estilo de la tabla
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a6fa5")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 1), (6, -1), 'CENTER'),  # Centrar valores numéricos
                ('ALIGN', (7, 1), (8, -1), 'RIGHT'),   # Alinear precios a la derecha
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 12))
            
            # Totales
            total_items = len(items)
            total_quantity = sum(item['quantity'] for item in items)
            total_stock = sum(item['stock'] for item in items)
            
            totals_table = Table([
                [
                    Paragraph(f"<b>Total Productos:</b> {total_items}", style_normal),
                    Paragraph(f"<b>Total en Cantidad:</b> {total_quantity}", style_normal),
                    Paragraph(f"<b>Total Existencias:</b> {total_stock}", style_normal)
                ]
            ], colWidths=[3*inch, 3*inch, 3*inch])
            
            elements.append(totals_table)
            elements.append(Spacer(1, 12))
            
            # Información del generador
            current_user = SessionManager.get_current_user()
            user_info = "No disponible"
            
            if current_user:
                if 'first_name' in current_user and 'last_name' in current_user:
                    user_info = f"{current_user['first_name']} {current_user['last_name']}"
                elif 'username' in current_user:
                    user_info = current_user['username']
            
            elements.append(Paragraph(f"<b>Generado por:</b> {user_info}", style_normal))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph("<i>Este reporte fue generado automáticamente por el sistema.</i>", style_normal))
            
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
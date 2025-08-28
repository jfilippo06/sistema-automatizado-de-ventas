# Standard library imports
from datetime import datetime
from typing import List, Dict
import tkinter.messagebox as messagebox
from tkinter import Toplevel, filedialog

# ReportLab imports
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER

# Local application imports
from sqlite_cli.models.tax_model import Tax
from utils.session_manager import SessionManager

class PDFGenerator:
    @staticmethod
    def generate_inventory_report(
        parent: Toplevel,
        title: str,
        items: List[Dict],
        filters: str
    ) -> None:
        """Genera un reporte de inventario en PDF en orientación horizontal con imagen de empresa"""
        # Mostrar diálogo para guardar el archivo
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
            
            # Encabezado con imagen
            try:
                # Intentar cargar la imagen de la empresa
                logo_path = "assets/empresa.png"
                logo = Image(logo_path, width=1.5*inch, height=0.7*inch)
                
                header_table = Table([
                    [logo, "", Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_normal)],
                    ["", Paragraph(title, style_heading), Paragraph(f"Filtros: {filters}", style_normal)]
                ], colWidths=[3*inch, 3*inch, 3*inch])
                
                header_table.setStyle(TableStyle([
                    ('SPAN', (0,0), (0,1)),  # Combinar celdas para el logo
                    ('SPAN', (1,1), (1,1)),  # Título centrado
                    ('ALIGN', (1,1), (1,1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ALIGN', (2,0), (2,0), 'RIGHT'),
                    ('ALIGN', (2,1), (2,1), 'RIGHT'),
                ]))
                
            except Exception as e:
                print(f"Error cargando imagen de empresa: {e}")
                # Fallback a texto si no se puede cargar la imagen
                header_table = Table([
                    [Paragraph("RN&M SERVICIOS INTEGRALES, C.A", style_title), "", Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_normal)],
                    [Paragraph("RIF: J-40339817-8", style_normal), Paragraph(title, style_heading), Paragraph(f"Filtros: {filters}", style_normal)]
                ], colWidths=[3*inch, 3*inch, 3*inch])
                
                header_table.setStyle(TableStyle([
                    ('SPAN', (0,0), (0,1)),  # Combinar celdas para company info
                    ('SPAN', (1,1), (1,1)),  # Título centrado
                    ('ALIGN', (1,1), (1,1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ALIGN', (2,0), (2,0), 'RIGHT'),
                    ('ALIGN', (2,1), (2,1), 'RIGHT'),
                ]))
            
            elements.append(header_table)
            elements.append(Spacer(1, 24))
            
            # Tabla de datos - ajustamos anchos para orientación horizontal
            headers = ["Código", "Producto", "Descripción", "Cant.", "Stock.", 
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
                2.0*inch,  # Producto
                2.5*inch,  # Descripción
                0.5*inch,  # Cantidad
                0.5*inch,  # Stock
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
                    Paragraph(f"<b>Total Stock:</b> {total_stock}", style_normal)
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

    @staticmethod
    def generate_purchase_order(
        parent: Toplevel,
        order_number: str,
        supplier_info: str,
        items: List[Dict],
        subtotal: float,
        taxes: float,
        total: float,
        delivery_date: str,
        created_by: str
    ) -> None:
        """Genera una orden de compra en PDF idéntica a PurchaseOrderViewer con imagen de empresa"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar orden como",
            initialfile=f"Orden_Compra_{order_number}.pdf",
            parent=parent
        )
        
        if not file_path:
            return
        
        try:
            # Configuración del documento
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                rightMargin=20,
                leftMargin=20,
                topMargin=40,
                bottomMargin=40
            )
            
            # Estilos personalizados
            styles = getSampleStyleSheet()
            style_title = styles["Title"]
            style_normal = styles["Normal"]
            style_bold = ParagraphStyle(
                name='Bold',
                parent=style_normal,
                fontName='Helvetica-Bold'
            )
            style_total = ParagraphStyle(
                name='Total',
                parent=style_normal,
                fontSize=12,
                fontName='Helvetica-Bold',
                alignment=TA_RIGHT,
                spaceAfter=12
            )
            
            elements = []
            
            # Encabezado con imagen
            try:
                # Intentar cargar la imagen de la empresa
                logo_path = "assets/empresa.png"
                logo = Image(logo_path, width=1.5*inch, height=0.7*inch)
                
                header_data = [
                    [logo, "", Paragraph(
                        f"<b>ORDEN DE COMPRA N°:</b> {order_number}<br/>"
                        f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>"
                        f"<b>Fecha Entrega:</b> {delivery_date}",
                        style_normal
                    )]
                ]
                
                header_table = Table(header_data, colWidths=[3.5*inch, 0.5*inch, 3*inch])
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ]))
                
            except Exception as e:
                print(f"Error cargando imagen de empresa: {e}")
                # Fallback a texto si no se puede cargar la imagen
                header_data = [
                    [
                        Paragraph("RN&M SERVICIOS INTEGRALES, C.A", style_title),
                        "",
                        Paragraph(
                            f"<b>ORDEN DE COMPRA N°:</b> {order_number}<br/>"
                            f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>"
                            f"<b>Fecha Entrega:</b> {delivery_date}",
                            style_normal
                        )
                    ],
                    [
                        Paragraph("RIF: J-40339817-8", style_normal),
                        "",
                        ""
                    ],
                    [
                        Paragraph("Av. Principal, Edif. Empresarial", style_normal),
                        "",
                        ""
                    ]
                ]
                
                header_table = Table(header_data, colWidths=[3.5*inch, 0.5*inch, 3*inch])
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                    ('SPAN', (0,1), (1,1)),
                    ('SPAN', (0,2), (1,2)),
                ]))
            
            elements.append(header_table)
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
            elements.append(Spacer(1, 12))
            
            # Información del proveedor
            elements.append(Paragraph("<b>PROVEEDOR:</b>", style_bold))
            elements.append(Paragraph(supplier_info, style_normal))
            elements.append(Spacer(1, 15))
            
            # Tabla de productos
            headers = ["Código", "Descripción", "Cantidad", "P. Unitario", "Total"]
            col_widths = [1.2*inch, 4.0*inch, 0.8*inch, 1.2*inch, 1.2*inch]
            
            table_data = [headers]
            for item in items:
                row = [
                    item['code'],
                    item['description'],
                    str(item['quantity']),
                    f"{item['unit_price']:,.2f}",
                    f"{item['total']:,.2f}"
                ]
                table_data.append(row)
            
            items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4a6fa5")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('FONTSIZE', (0,1), (-1,-1), 9),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            
            elements.append(items_table)
            elements.append(Spacer(1, 15))
            
            # Sección de totales
            iva_tax = Tax.get_by_name("IVA")
            
            if iva_tax and iva_tax.get('status_name') == 'active':
                subtotal_table = Table([
                    ["Subtotal:", f"{subtotal:,.2f}"]
                ], colWidths=[1.5*inch, 1.5*inch])
                
                subtotal_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                
                elements.append(subtotal_table)
                
                iva_table = Table([
                    [f"IVA ({iva_tax['value']}%):", f"{taxes:,.2f}"]
                ], colWidths=[1.5*inch, 1.5*inch])
                
                iva_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                
                elements.append(iva_table)
            
            # TOTAL con formato especial
            total_table = Table([
                ["", ""],
                [
                    Paragraph("<b>TOTAL:</b>", style_total),
                    Paragraph(f"<b>{total:,.2f}</b>", style_total)
                ]
            ], colWidths=[3.5*inch, 2*inch])
            
            total_table.setStyle(TableStyle([
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            
            elements.append(total_table)
            elements.append(Spacer(1, 20))
            
            # Notas y creador
            elements.append(Paragraph("<i>Esta orden de compra es generada automáticamente por el sistema.</i>", style_normal))
            elements.append(Spacer(1, 8))
            elements.append(Paragraph(f"<b>Creado por:</b> {created_by}", style_normal))
            
            # Generar PDF
            doc.build(elements)
            
            messagebox.showinfo(
                "Éxito",
                f"La orden se ha generado correctamente en:\n{file_path}",
                parent=parent
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo generar el PDF:\n{str(e)}",
                parent=parent
            )

    @staticmethod
    def generate_invoice(
        parent: Toplevel,
        invoice_id: str,
        customer_info: str,
        items: List[Dict],
        subtotal: float,
        taxes: float,
        total: float,
        employee_info: str
    ) -> None:
        """Genera un recibo en PDF idéntico a InvoiceViewer con imagen de empresa"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar recibo como",
            initialfile=f"Recibo_{invoice_id}.pdf",
            parent=parent
        )
        
        if not file_path:
            return
        
        try:
            # Configuración del documento
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                rightMargin=20,
                leftMargin=20,
                topMargin=40,
                bottomMargin=40
            )
            
            # Estilos personalizados
            styles = getSampleStyleSheet()
            style_normal = styles["Normal"]
            style_bold = ParagraphStyle(
                name='Bold',
                parent=style_normal,
                fontName='Helvetica-Bold'
            )
            style_title = ParagraphStyle(
                name='Title',
                parent=style_normal,
                fontName='Helvetica-Bold',
                fontSize=12,
                spaceAfter=6
            )
            style_total = ParagraphStyle(
                name='Total',
                parent=style_normal,
                fontSize=12,
                fontName='Helvetica-Bold',
                alignment=TA_RIGHT,
                spaceAfter=12
            )
            style_italic = ParagraphStyle(
                name='Italic',
                parent=style_normal,
                fontName='Helvetica-Oblique',
                fontSize=9
            )
            
            elements = []
            
            # Encabezado con imagen
            try:
                # Intentar cargar la imagen de la empresa
                logo_path = "assets/empresa.png"
                logo = Image(logo_path, width=1.5*inch, height=0.7*inch)
                
                header_data = [
                    [logo, "", Paragraph(
                        f"<b>RECIBO N°:</b> {invoice_id}<br/>"
                        f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                        style_normal
                    )]
                ]
                
                header_table = Table(header_data, colWidths=[3.5*inch, 0.5*inch, 3*inch])
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ]))
                
            except Exception as e:
                print(f"Error cargando imagen de empresa: {e}")
                # Fallback a texto si no se puede cargar la imagen
                header_data = [
                    [
                        Paragraph("RN&M SERVICIOS INTEGRALES, C.A", style_title),
                        "",
                        Paragraph(
                            f"<b>RECIBO N°:</b> {invoice_id}<br/>"
                            f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                            style_normal
                        )
                    ],
                    [
                        Paragraph("RIF: J-40339817-8", style_normal),
                        "",
                        ""
                    ]
                ]
                
                header_table = Table(header_data, colWidths=[3.5*inch, 0.5*inch, 3*inch])
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                    ('SPAN', (0,1), (1,1)),
                ]))
            
            elements.append(header_table)
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
            elements.append(Spacer(1, 12))
            
            # Información del cliente
            elements.append(Paragraph("<b>CLIENTE:</b>", style_bold))
            elements.append(Paragraph(customer_info, style_normal))
            elements.append(Spacer(1, 12))
            
            # Tabla de productos/servicios
            headers = ["Tipo", "Descripción", "Cantidad", "P. Unitario", "Total"]
            col_widths = [0.8*inch, 3.0*inch, 0.7*inch, 1.0*inch, 1.0*inch]
            
            table_data = [headers]
            for item in items:
                item_type = "Servicio" if item.get('is_service', False) else "Producto"
                row = [
                    item_type,
                    item['name'],
                    str(item['quantity']),
                    f"{item['unit_price']:.2f}",
                    f"{item['total']:.2f}"
                ]
                table_data.append(row)
            
            items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4a6fa5")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('FONTSIZE', (0,1), (-1,-1), 9),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            
            elements.append(items_table)
            elements.append(Spacer(1, 12))
            
            # Totales
            iva_tax = Tax.get_by_name("IVA")
            
            if iva_tax and iva_tax.get('status_name') == 'active':
                subtotal_table = Table([
                    ["Subtotal:", f"{subtotal:.2f}"]
                ], colWidths=[1.5*inch, 1.5*inch])
                
                subtotal_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                
                elements.append(subtotal_table)
                
                iva_table = Table([
                    [f"IVA ({iva_tax['value']}%):", f"{taxes:.2f}"]
                ], colWidths=[1.5*inch, 1.5*inch])
                
                iva_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                
                elements.append(iva_table)
            
            # Total
            total_table = Table([
                ["", ""],
                [
                    Paragraph("<b>TOTAL:</b>", style_total),
                    Paragraph(f"<b>{total:.2f}</b>", style_total)
                ]
            ], colWidths=[3.5*inch, 2*inch])
            
            total_table.setStyle(TableStyle([
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            
            elements.append(total_table)
            elements.append(Spacer(1, 15))
            
            # Información del empleado
            elements.append(Paragraph(f"<b>Atendido por:</b> {employee_info}", style_normal))
            elements.append(Spacer(1, 8))
            
            # Notas
            elements.append(Paragraph("<i>Notas:</i>", style_italic))
            elements.append(Paragraph("<i>Este recibo es generado automáticamente por el sistema.</i>", style_italic))
            
            if any(item.get('is_service', False) for item in items):
                elements.append(Paragraph("<i>Nota: Los servicios solicitados serán atendidos según lo acordado.</i>", style_italic))
            
            # Generar PDF
            doc.build(elements)
            
            messagebox.showinfo(
                "Éxito",
                f"El recibo se ha generado correctamente en:\n{file_path}",
                parent=parent
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo generar el PDF:\n{str(e)}",
                parent=parent
            )
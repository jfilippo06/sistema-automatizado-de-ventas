# seeds/invoice_status_seeds.py
from database.database import get_db_connection

def seed_invoice_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    statuses = [
        ('Paid', 'Factura pagada completamente'),
        ('Pending', 'Factura pendiente de pago'),
        ('Cancelled', 'Factura anulada'),
        ('Partial', 'Factura con pago parcial')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO invoice_status (name, description)
        VALUES (?, ?)
    ''', statuses)
    
    conn.commit()
    conn.close()
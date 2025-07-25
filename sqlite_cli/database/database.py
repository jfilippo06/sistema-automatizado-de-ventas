# database/database.py
import sqlite3
import os
from typing import Optional

def get_db_connection() -> sqlite3.Connection:
    """
    Obtiene una conexión a la base de datos SQLite.
    
    :return: Una conexión a la base de datos SQLite.
    """
    # Obtener la ruta del directorio actual del script
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta completa a la base de datos
    db_path: str = os.path.join(current_dir, "db.db")
    
    # Conectar a la base de datos
    conn: sqlite3.Connection = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acceder a las filas como diccionarios
    return conn

def init_db() -> None:
    """
    Inicializa la base de datos y crea todas las tablas si no existen.
    """
    conn: sqlite3.Connection = get_db_connection()
    cursor: sqlite3.Cursor = conn.cursor()
    
    # Tabla de estados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Tabla de roles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # Tabla de personas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            id_number TEXT NOT NULL UNIQUE,
            address TEXT,
            phone TEXT,
            email TEXT,
            department TEXT,
            position TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            person_id INTEGER NOT NULL,
            status_id INTEGER NOT NULL DEFAULT 1,
            role_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (person_id) REFERENCES person(id),
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')
    
    # Tabla de proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            id_number TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            tax_id TEXT,
            company TEXT,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')
    
    # Tabla de inventario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            product TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT 0,
            quantity INTEGER NOT NULL,
            stock INTEGER NOT NULL,
            min_stock INTEGER NOT NULL DEFAULT 0,
            max_stock INTEGER NOT NULL DEFAULT 0,
            cost REAL NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status_id INTEGER NOT NULL,
            supplier_id INTEGER,
            expiration_date TEXT,
            image_path TEXT,
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    ''')

    # Tabla de tipos de movimiento (simplificada)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movement_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            affects_quantity BOOLEAN NOT NULL,
            affects_stock BOOLEAN NOT NULL,
            description TEXT  -- Columna añadida
        )
    ''')

    # Tabla de movimientos (registra cambios en quantity/stock por separado)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inventory_id INTEGER NOT NULL,
            movement_type_id INTEGER NOT NULL,
            quantity_change INTEGER DEFAULT 0,   -- Cambio en existencia física
            stock_change INTEGER DEFAULT 0,      -- Cambio en disponible para venta
            previous_quantity INTEGER NOT NULL,
            new_quantity INTEGER NOT NULL,
            previous_stock INTEGER NOT NULL,
            new_stock INTEGER NOT NULL,
            reference_id INTEGER NULL,           -- ID de factura/compra (ahora nullable)
            reference_type TEXT,                 -- Tipo de referencia (invoice, purchase, adjustment)
            user_id INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (inventory_id) REFERENCES inventory(id),
            FOREIGN KEY (movement_type_id) REFERENCES movement_types(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (reference_id) REFERENCES invoices(id) ON DELETE SET NULL  -- Relación opcional
        )
    ''')

    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            id_number TEXT NOT NULL UNIQUE,
            email TEXT,
            address TEXT,
            phone TEXT,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')
    
    # Tabla de servicios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')
    
    # Tabla de estados de solicitud
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Tabla de solicitudes de servicio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_number TEXT NOT NULL UNIQUE,
            customer_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL DEFAULT 0,
            description TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            total REAL NOT NULL,
            request_status_id INTEGER NOT NULL DEFAULT 1,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (service_id) REFERENCES services(id),
            FOREIGN KEY (employee_id) REFERENCES users(id),
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (request_status_id) REFERENCES request_status(id)
        )
    ''')

    # Tabla de monedas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            symbol TEXT NOT NULL,
            value REAL NOT NULL,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')

    # Tabla de impuestos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS taxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            value REAL NOT NULL,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')
    
    # Invoice status table (English)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Ivoice types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Invoices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            invoice_type_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            taxes REAL NOT NULL,
            total REAL NOT NULL,
            status_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (status_id) REFERENCES invoice_status(id),
            FOREIGN KEY (invoice_type_id) REFERENCES invoice_types(id)
        )
    ''')

    # Tabla de métodos de pago para facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            bank TEXT,
            amount REAL NOT NULL,
            reference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
        )
    ''')

    # Invoice details table (English)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id INTEGER,  -- Opcional (puede ser NULL si no aplica)
            service_request_id INTEGER,  -- Opcional (puede ser NULL si no aplica)
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES inventory(id),
            FOREIGN KEY (service_request_id) REFERENCES service_requests(id)
        )
    ''')

    # Tabla para los estados de órdenes de compra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_order_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabla principal de órdenes de compra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT NOT NULL UNIQUE,
            supplier_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            expected_delivery_date TEXT,
            status_id INTEGER NOT NULL,
            subtotal REAL DEFAULT 0,
            taxes REAL DEFAULT 0,
            total REAL DEFAULT 0,
            payment_terms TEXT,
            notes TEXT,
            created_by INTEGER NOT NULL,
            approved_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (status_id) REFERENCES purchase_order_status(id),
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (approved_by) REFERENCES users(id)
        )
    ''')

    # Tabla de detalles de la orden de compra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER DEFAULT 0,
            product_name TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL,
            reference_price REAL,
            subtotal REAL GENERATED ALWAYS AS (quantity * COALESCE(unit_price, 0)) STORED,
            received_quantity INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES inventory(id)
        )
    ''')

    # Tabla de bancos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            status_id INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
    ''')
    
    conn.commit()
    conn.close()
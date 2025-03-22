# models/inventory_model.py
from database.database import get_db_connection

class InventoryItem:
    @staticmethod
    def create(name, quantity, price):
        """
        Crea un nuevo ítem en la tabla `inventory`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        """
        Obtiene todos los ítems de la tabla `inventory`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()
        conn.close()
        return items
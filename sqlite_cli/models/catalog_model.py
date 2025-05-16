from sqlite_cli.database.database import get_db_connection
from typing import List, Dict, Optional

class CatalogModel:
    @staticmethod
    def get_all_products() -> List[Dict]:
        """Obtiene todos los productos activos para el catálogo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, i.code, i.product, i.stock, i.price, i.expiration_date, i.image_path, i.description
            FROM inventory i
            JOIN status st ON i.status_id = st.id
            WHERE st.name = 'active'
            ORDER BY i.product ASC
        ''')
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products

    @staticmethod
    def get_all_services() -> List[Dict]:
        """Obtiene todos los servicios activos para el catálogo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.code, s.name, s.price, s.description
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'active'
            ORDER BY s.name ASC
        ''')
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services

    @staticmethod
    def search_products(search_term: str = "") -> List[Dict]:
        """Busca productos activos para el catálogo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT i.id, i.code, i.product, i.stock, i.price, i.expiration_date, i.image_path, i.description
            FROM inventory i
            JOIN status st ON i.status_id = st.id
            WHERE st.name = 'active' AND 
                  (LOWER(i.product) LIKE ? OR 
                  LOWER(i.code) LIKE ? OR
                  LOWER(i.description) LIKE ?)
            ORDER BY i.product ASC
        '''
        
        cursor.execute(query, (f"%{search_term.lower()}%", f"%{search_term.lower()}%", f"%{search_term.lower()}%"))
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products

    @staticmethod
    def search_services(search_term: str = "") -> List[Dict]:
        """Busca servicios activos para el catálogo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT s.id, s.code, s.name, s.price, s.description
            FROM services s
            JOIN status st ON s.status_id = st.id
            WHERE st.name = 'active' AND 
                  (LOWER(s.name) LIKE ? OR 
                  LOWER(s.code) LIKE ? OR
                  LOWER(s.description) LIKE ?)
            ORDER BY s.name ASC
        '''
        
        cursor.execute(query, (f"%{search_term.lower()}%", f"%{search_term.lower()}%", f"%{search_term.lower()}%"))
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services
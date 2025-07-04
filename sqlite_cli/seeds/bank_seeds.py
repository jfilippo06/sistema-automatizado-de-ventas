from models.bank_model import Bank
from typing import List, Dict

def seed_banks() -> None:
    """Inserta los bancos principales de Venezuela en la base de datos."""
    banks: List[Dict] = [
        {'code': '0102', 'name': 'Banco de Venezuela'},
        {'code': '0104', 'name': 'Venezolano de Crédito'},
        {'code': '0105', 'name': 'Banco Mercantil'},
        {'code': '0108', 'name': 'Banco Provincial'},
        {'code': '0114', 'name': 'Bancaribe'},
        {'code': '0115', 'name': 'Banco Exterior'},
        {'code': '0116', 'name': 'Banco Occidental de Descuento'},
        {'code': '0128', 'name': 'Banco Caroní'},
        {'code': '0134', 'name': 'Banesco'},
        {'code': '0137', 'name': 'Banco Sofitasa'},
        {'code': '0138', 'name': 'Banco Plaza'},
        {'code': '0146', 'name': 'Banco de la Gente Emprendedora'},
        {'code': '0149', 'name': 'Banco del Pueblo Soberano'},
        {'code': '0151', 'name': 'BFC Banco Fondo Común'},
        {'code': '0156', 'name': '100% Banco'},
        {'code': '0157', 'name': 'DelSur Banco Universal'},
        {'code': '0163', 'name': 'Banco del Tesoro'},
        {'code': '0166', 'name': 'Banco Agrícola de Venezuela'},
        {'code': '0168', 'name': 'Bancrecer'},
        {'code': '0169', 'name': 'Mi Banco'},
        {'code': '0171', 'name': 'Banco Activo'},
        {'code': '0172', 'name': 'Bancamiga'},
        {'code': '0173', 'name': 'Banco Internacional de Desarrollo'},
        {'code': '0174', 'name': 'Banplus'},
        {'code': '0175', 'name': 'Banco Bicentenario'},
        {'code': '0176', 'name': 'Banco de la Fuerza Armada Nacional Bolivariana'},
        {'code': '0177', 'name': 'Banco de Desarrollo del Microempresario'},
        {'code': '0190', 'name': 'Citibank'},
        {'code': '0191', 'name': 'Banco Nacional de Crédito'},
    ]
    
    # Verificar si ya existen bancos
    existing_banks = Bank.all()
    if len(existing_banks) == 0:
        for bank in banks:
            Bank.create(code=bank['code'], name=bank['name'])
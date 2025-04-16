# seeds/currency_seeds.py
from models.currency_model import Currency

def seed_currencies() -> None:
    """Inserta monedas iniciales si no existen"""
    if not Currency.get_by_name("Dólar"):
        Currency.create(name="Dólar", symbol="$", value=0.0)
    
    if not Currency.get_by_name("Euro"):
        Currency.create(name="Euro", symbol="€", value=0.0)
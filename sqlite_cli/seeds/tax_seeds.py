# seeds/tax_seeds.py
from models.tax_model import Tax

def seed_taxes() -> None:
    """Inserta impuestos iniciales si no existen"""
    if not Tax.get_by_name("IVA"):
        Tax.create(name="IVA", value=0.0)
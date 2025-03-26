# cli.py
import argparse
from database.database import init_db
from seeds.status_seeds import seed_status
from seeds.supplier_seeds import seed_suppliers
from seeds.inventory_seeds import seed_inventory
from typing import Optional

def main() -> None:
    """
    Función principal para manejar los comandos de la CLI.
    """
    parser = argparse.ArgumentParser(description="CLI para gestionar el inventario.")
    parser.add_argument('command', choices=['init', 'seed', 'reset'], help="Comando a ejecutar.")
    
    args = parser.parse_args()

    if args.command == 'init':
        init_db()
        print("Base de datos inicializada.")
    elif args.command == 'seed':
        seed_status()
        seed_suppliers()
        seed_inventory()
        print("Datos iniciales insertados.")
    elif args.command == 'reset':
        init_db()
        seed_status()
        seed_suppliers()
        seed_inventory()
        print("Base de datos reinicializada con datos de ejemplo.")

if __name__ == "__main__":
    main()
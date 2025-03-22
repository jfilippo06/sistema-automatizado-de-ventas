# cli.py
import argparse
from database.database import init_db
from seeds.inventory_seeds import seed_inventory

def main():
    parser = argparse.ArgumentParser(description="CLI para gestionar el inventario.")
    parser.add_argument('command', choices=['init', 'seed', 'list', 'add', 'delete', 'update'], help="Comando a ejecutar.")
    
    # Argumentos adicionales para los comandos 'add', 'delete' y 'update'
    parser.add_argument('--name', help="Nombre del ítem.")
    parser.add_argument('--quantity', type=int, help="Cantidad del ítem.")
    parser.add_argument('--price', type=float, help="Precio del ítem.")
    parser.add_argument('--id', type=int, help="ID del ítem.")

    args = parser.parse_args()

    if args.command == 'init':
        init_db()
        print("Base de datos inicializada.")
    elif args.command == 'seed':
        seed_inventory()
        print("Datos de inventario insertados.")

if __name__ == "__main__":
    main()
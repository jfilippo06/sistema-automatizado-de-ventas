# cli.py
import argparse
from database.database import init_db
from seeds.customer_seeds import seed_customers
from seeds.inventory_seeds import seed_inventory
from seeds.service_request_seeds import seed_service_requests
from seeds.service_seeds import seed_services
from seeds.status_seeds import seed_status
from seeds.supplier_seeds import seed_suppliers
from seeds.request_status_seeds import seed_request_status
from seeds.person_seeds import seed_persons
from seeds.role_seeds import seed_roles
from seeds.user_seeds import seed_users
from seeds.currency_seeds import seed_currencies

def main() -> None:
    parser = argparse.ArgumentParser(description="CLI para gestionar el inventario.")
    parser.add_argument('command', choices=['init', 'seed', 'reset'], help="Comando a ejecutar.")
    
    args = parser.parse_args()

    if args.command == 'init':
        init_db()
        print("Base de datos inicializada.")
    elif args.command == 'seed':
        seed_status()
        seed_roles()
        seed_persons()
        seed_users()
        seed_request_status()
        seed_suppliers()
        seed_inventory()
        seed_customers()
        seed_services()
        seed_service_requests()
        seed_currencies()
        print("Datos iniciales insertados.")
    elif args.command == 'reset':
        init_db()
        seed_status()
        seed_roles()
        seed_persons()
        seed_users()
        seed_request_status()
        seed_suppliers()
        seed_inventory()
        seed_customers()
        seed_services()
        seed_service_requests()
        seed_currencies()
        seed_service_requests()
        print("Base de datos reinicializada con datos de ejemplo.")

if __name__ == "__main__":
    main()
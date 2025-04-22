import tkinter as tk
from screens.customers.customers_screen import CustomersScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.inventory.inventory import Inventory
from screens.service_requests.service_requests_screen import ServiceRequestsScreen
from screens.services.services_screen import ServicesScreen
from screens.supplier.supplier import Suppliers
from screens.configuration.configuration_screen import ConfigurationScreen
from screens.configuration.users.users_screen import UsersScreen
from screens.configuration.currency_screen import CurrencyManagementScreen
from screens.configuration.taxes_screen import TaxesManagementScreen
from screens.maintenance.maintenance_screen import MaintenanceScreen
from screens.recovery.recovery_screen import RecoveryScreen
from screens.recovery.recovery_suppliers import RecoverySuppliers
from screens.recovery.recovery_inventory import RecoveryInventory
from screens.recovery.recovery_service_requests import RecoveryServiceRequests
from screens.recovery.recovery_services import RecoveryServices
from screens.billing.billing_screen import BillingScreen

def main() -> None:
    app = tk.Tk()
    app.title("Sistema automatizado de ventas y servicios")
    app.geometry("800x600")
    app.resizable(True, True)
    
    # Callbacks para navegación
    def open_home_screen() -> None:
        login_screen.pack_forget()
        config_screen.pack_forget()
        users_screen.pack_forget()
        currency_screen.pack_forget()
        taxes_screen.pack_forget()
        maintenance_screen.pack_forget()
        recovery_screen.pack_forget()
        recovery_suppliers_screen.pack_forget()
        recovery_inventory_screen.pack_forget()
        recovery_service_requests_screen.pack_forget()
        recovery_services_screen.pack_forget()
        billing_screen.pack_forget()  # Nueva línea
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_login_screen() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
        service_requests_screen.pack_forget()
        services_screen.pack_forget()
        config_screen.pack_forget()
        users_screen.pack_forget()
        currency_screen.pack_forget()
        taxes_screen.pack_forget()
        maintenance_screen.pack_forget()
        recovery_screen.pack_forget()
        recovery_suppliers_screen.pack_forget()
        recovery_inventory_screen.pack_forget()
        recovery_service_requests_screen.pack_forget()
        recovery_services_screen.pack_forget()
        billing_screen.pack_forget()
        login_screen.pack(fill=tk.BOTH, expand=True)

    def open_inventory() -> None:
        home_screen.pack_forget()
        inventory_screen.pack(fill=tk.BOTH, expand=True)

    def open_suppliers() -> None:
        home_screen.pack_forget()
        suppliers_screen.pack(fill=tk.BOTH, expand=True)

    def open_customers() -> None:
        home_screen.pack_forget()
        customers_screen.pack(fill=tk.BOTH, expand=True)

    def open_service_requests() -> None:
        home_screen.pack_forget()
        service_requests_screen.pack(fill=tk.BOTH, expand=True)

    def open_services() -> None:
        home_screen.pack_forget()
        services_screen.pack(fill=tk.BOTH, expand=True)

    def open_config() -> None:
        home_screen.pack_forget()
        config_screen.pack(fill=tk.BOTH, expand=True)

    def open_users() -> None:
        home_screen.pack_forget()
        config_screen.pack_forget()
        users_screen.pack(fill=tk.BOTH, expand=True)

    def open_currency() -> None:
        home_screen.pack_forget()
        config_screen.pack_forget()
        currency_screen.pack(fill=tk.BOTH, expand=True)

    def open_taxes() -> None:
        home_screen.pack_forget()
        config_screen.pack_forget()
        taxes_screen.pack(fill=tk.BOTH, expand=True)

    def open_maintenance() -> None:
        home_screen.pack_forget()
        maintenance_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery() -> None:
        home_screen.pack_forget()
        recovery_screen.pack(fill=tk.BOTH, expand=True)

    def open_billing() -> None:  # Nueva función
        home_screen.pack_forget()
        billing_screen.pack(fill=tk.BOTH, expand=True)

    # Callbacks para recuperación
    def open_recovery_suppliers() -> None:
        recovery_screen.pack_forget()
        recovery_suppliers_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery_inventory() -> None:
        recovery_screen.pack_forget()
        recovery_inventory_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery_service_requests() -> None:
        recovery_screen.pack_forget()
        recovery_service_requests_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery_services() -> None:
        recovery_screen.pack_forget()
        recovery_services_screen.pack(fill=tk.BOTH, expand=True)

    # Callbacks para regresar al home
    def open_home_from_inventory() -> None:
        inventory_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_suppliers() -> None:
        suppliers_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_customers() -> None:
        customers_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_service_requests() -> None:
        service_requests_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_services() -> None:
        services_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_config() -> None:
        config_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_config_from_users() -> None:
        users_screen.pack_forget()
        config_screen.pack(fill=tk.BOTH, expand=True)

    def open_config_from_currency() -> None:
        currency_screen.pack_forget()
        config_screen.pack(fill=tk.BOTH, expand=True)

    def open_config_from_taxes() -> None:
        taxes_screen.pack_forget()
        config_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_maintenance() -> None:
        maintenance_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_recovery() -> None:
        recovery_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_billing() -> None:  # Nueva función
        billing_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    # Callbacks para regresar desde pantallas de recuperación
    def open_recovery_from_suppliers() -> None:
        recovery_suppliers_screen.pack_forget()
        recovery_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery_from_inventory() -> None:
        recovery_inventory_screen.pack_forget()
        recovery_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery_from_service_requests() -> None:
        recovery_service_requests_screen.pack_forget()
        recovery_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery_from_services() -> None:
        recovery_services_screen.pack_forget()
        recovery_screen.pack(fill=tk.BOTH, expand=True)

    # Creación de todas las pantallas
    login_screen = LoginScreen(app, open_home_screen)
    
    home_screen = HomeScreen(
        app, 
        open_login_screen, 
        open_inventory,
        open_suppliers,
        open_customers,
        open_service_requests,
        open_services,
        open_config,
        open_maintenance,
        open_recovery,
        open_billing  # Nuevo callback
    )
    
    inventory_screen = Inventory(app, open_home_from_inventory)
    suppliers_screen = Suppliers(app, open_home_from_suppliers)
    customers_screen = CustomersScreen(app, open_home_from_customers)
    service_requests_screen = ServiceRequestsScreen(app, open_home_from_service_requests)
    services_screen = ServicesScreen(app, open_home_from_services)
    config_screen = ConfigurationScreen(app, open_home_from_config, open_users, open_currency, open_taxes)
    users_screen = UsersScreen(app, open_config_from_users)
    currency_screen = CurrencyManagementScreen(app, open_config_from_currency)
    taxes_screen = TaxesManagementScreen(app, open_config_from_taxes)
    maintenance_screen = MaintenanceScreen(app, open_home_from_maintenance)
    recovery_screen = RecoveryScreen(
        app, 
        open_home_from_recovery, 
        open_recovery_suppliers,
        open_recovery_inventory,
        open_recovery_service_requests,
        open_recovery_services
    )
    recovery_suppliers_screen = RecoverySuppliers(app, open_recovery_from_suppliers)
    recovery_inventory_screen = RecoveryInventory(app, open_recovery_from_inventory)
    recovery_service_requests_screen = RecoveryServiceRequests(app, open_recovery_from_service_requests)
    recovery_services_screen = RecoveryServices(app, open_recovery_from_services)
    billing_screen = BillingScreen(app, open_home_from_billing)  # Nueva pantalla

    # Mostrar pantalla de login al iniciar
    login_screen.pack(fill=tk.BOTH, expand=True)
    app.mainloop()

if __name__ == "__main__":
    main()
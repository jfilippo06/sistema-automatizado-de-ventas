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
from screens.configuration.system_info_screen import SystemInfoScreen
from screens.maintenance.maintenance_screen import MaintenanceScreen
from screens.recovery.recovery_screen import RecoveryScreen
from screens.recovery.recovery_suppliers import RecoverySuppliers
from screens.recovery.recovery_inventory import RecoveryInventory
from screens.recovery.recovery_service_requests import RecoveryServiceRequests
from screens.recovery.recovery_services import RecoveryServices
from screens.recovery.recovery_users import RecoveryUsers
from screens.billing.billing_screen import BillingScreen
from screens.reports.reports_screen import ReportsScreen
from screens.reports.sales_report_screen import SalesReportScreen
from screens.reports.purchase_order_report_screen import PurchaseOrderReportScreen
from screens.catalog.catalog_screen import CatalogScreen
from screens.purchase_orders.purchase_orders import PurchaseOrdersScreen
from screens.reports.inventory.inventory_report_screen import InventoryReportScreen
from utils.session_manager import SessionManager

def main() -> None:
    app = tk.Tk()
    app.title("Sistema automatizado de ventas y servicios")
    app.geometry("800x600")
    app.resizable(True, True)
    
    def check_auth_and_show_home():
        if SessionManager.is_authenticated():
            open_home_screen()
        else:
            open_login_screen()

    # Callbacks para navegación
    def open_home_screen() -> None:
        for screen in all_screens:
            screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_login_screen() -> None:
        for screen in all_screens:
            screen.pack_forget()
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
        config_screen.pack_forget()
        users_screen.pack(fill=tk.BOTH, expand=True)

    def open_currency() -> None:
        config_screen.pack_forget()
        currency_screen.pack(fill=tk.BOTH, expand=True)

    def open_taxes() -> None:
        config_screen.pack_forget()
        taxes_screen.pack(fill=tk.BOTH, expand=True)

    def open_system_info() -> None:
        config_screen.pack_forget()
        system_info_screen.pack(fill=tk.BOTH, expand=True)

    def open_maintenance() -> None:
        home_screen.pack_forget()
        maintenance_screen.pack(fill=tk.BOTH, expand=True)

    def open_recovery() -> None:
        home_screen.pack_forget()
        recovery_screen.pack(fill=tk.BOTH, expand=True)

    def open_billing() -> None:
        home_screen.pack_forget()
        billing_screen.pack(fill=tk.BOTH, expand=True)

    def open_reports() -> None:
        home_screen.pack_forget()
        reports_screen.pack(fill=tk.BOTH, expand=True)

    def open_sales_report() -> None:
        home_screen.pack_forget()
        sales_report_screen.pack(fill=tk.BOTH, expand=True)

    def open_purchase_order_report() -> None:
        home_screen.pack_forget()
        purchase_order_report_screen.pack(fill=tk.BOTH, expand=True)

    def open_catalog() -> None:
        home_screen.pack_forget()
        catalog_screen.pack(fill=tk.BOTH, expand=True)

    def open_purchase_orders() -> None:
        home_screen.pack_forget()
        purchase_orders_screen.pack(fill=tk.BOTH, expand=True)

    # Callbacks para regresar
    def open_home_from_current(screen: tk.Frame) -> None:
        screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_config_from_current(screen: tk.Frame) -> None:
        screen.pack_forget()
        config_screen.pack(fill=tk.BOTH, expand=True)

    # Creación de todas las pantallas
    login_screen = LoginScreen(app, check_auth_and_show_home)
    
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
        open_billing,
        open_reports,
        open_catalog,
        open_purchase_orders,
        open_purchase_order_report
    )
    
    inventory_screen = Inventory(app, lambda: open_home_from_current(inventory_screen))
    suppliers_screen = Suppliers(app, lambda: open_home_from_current(suppliers_screen))
    customers_screen = CustomersScreen(app, lambda: open_home_from_current(customers_screen))
    service_requests_screen = ServiceRequestsScreen(app, lambda: open_home_from_current(service_requests_screen))
    services_screen = ServicesScreen(app, lambda: open_home_from_current(services_screen))
    
    # Configuración y sus sub-pantallas
    config_screen = ConfigurationScreen(
        app, 
        lambda: open_home_from_current(config_screen), 
        open_users, 
        open_currency, 
        open_taxes,
        open_system_info
    )
    users_screen = UsersScreen(app, lambda: open_config_from_current(users_screen))
    currency_screen = CurrencyManagementScreen(app, lambda: open_config_from_current(currency_screen))
    taxes_screen = TaxesManagementScreen(app, lambda: open_config_from_current(taxes_screen))
    system_info_screen = SystemInfoScreen(app, lambda: open_config_from_current(system_info_screen))
    
    maintenance_screen = MaintenanceScreen(app, lambda: open_home_from_current(maintenance_screen))
    
    # Recuperación
    recovery_suppliers_screen = RecoverySuppliers(app, lambda: [recovery_suppliers_screen.pack_forget(), recovery_screen.pack(fill=tk.BOTH, expand=True)])
    recovery_inventory_screen = RecoveryInventory(app, lambda: [recovery_inventory_screen.pack_forget(), recovery_screen.pack(fill=tk.BOTH, expand=True)])
    recovery_service_requests_screen = RecoveryServiceRequests(app, lambda: [recovery_service_requests_screen.pack_forget(), recovery_screen.pack(fill=tk.BOTH, expand=True)])
    recovery_services_screen = RecoveryServices(app, lambda: [recovery_services_screen.pack_forget(), recovery_screen.pack(fill=tk.BOTH, expand=True)])
    recovery_users_screen = RecoveryUsers(app, lambda: [recovery_users_screen.pack_forget(), recovery_screen.pack(fill=tk.BOTH, expand=True)])
    
    recovery_screen = RecoveryScreen(
        app, 
        lambda: open_home_from_current(recovery_screen),
        lambda: [recovery_screen.pack_forget(), recovery_suppliers_screen.pack(fill=tk.BOTH, expand=True)],
        lambda: [recovery_screen.pack_forget(), recovery_inventory_screen.pack(fill=tk.BOTH, expand=True)],
        lambda: [recovery_screen.pack_forget(), recovery_service_requests_screen.pack(fill=tk.BOTH, expand=True)],
        lambda: [recovery_screen.pack_forget(), recovery_services_screen.pack(fill=tk.BOTH, expand=True)],
        lambda: [recovery_screen.pack_forget(), recovery_users_screen.pack(fill=tk.BOTH, expand=True)]
    )
    
    billing_screen = BillingScreen(app, lambda: open_home_from_current(billing_screen))
    reports_screen = ReportsScreen(app, lambda: open_home_from_current(reports_screen))
    sales_report_screen = SalesReportScreen(app, lambda: open_home_from_current(sales_report_screen))
    purchase_order_report_screen = PurchaseOrderReportScreen(app, lambda: open_home_from_current(purchase_order_report_screen))
    catalog_screen = CatalogScreen(app, lambda: open_home_from_current(catalog_screen))
    purchase_orders_screen = PurchaseOrdersScreen(app, lambda: open_home_from_current(purchase_orders_screen))
    inventory_report_screen = InventoryReportScreen(
        app,
        lambda: [inventory_report_screen.pack_forget(), reports_screen.pack(fill=tk.BOTH, expand=True)]
    )

    all_screens = [
        login_screen,
        home_screen,
        inventory_screen,
        suppliers_screen,
        customers_screen,
        service_requests_screen,
        services_screen,
        config_screen,
        users_screen,
        currency_screen,
        taxes_screen,
        system_info_screen,
        maintenance_screen,
        recovery_screen,
        recovery_suppliers_screen,
        recovery_inventory_screen,
        recovery_service_requests_screen,
        recovery_services_screen,
        recovery_users_screen,
        billing_screen,
        reports_screen,
        sales_report_screen,
        purchase_order_report_screen,
        catalog_screen,
        purchase_orders_screen,
        inventory_report_screen
    ]

    check_auth_and_show_home()
    app.mainloop()

if __name__ == "__main__":
    main()
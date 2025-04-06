# main.py (actualizado)
import tkinter as tk
from screens.customers.customers_screen import CustomersScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.inventory.inventory import Inventory
from screens.service_requests.service_requests_screen import ServiceRequestsScreen
from screens.services.services_screen import ServicesScreen
from screens.supplier.supplier import Suppliers

def main() -> None:
    app = tk.Tk()
    app.title("Sistema automatizado de ventas y servicios")
    app.geometry("800x600")
    app.resizable(True, True)
    
    def open_home_screen() -> None:
        login_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_login_screen() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
        service_requests_screen.pack_forget()
        services_screen.pack_forget()
        login_screen.pack(fill=tk.BOTH, expand=True)

    def open_inventory() -> None:
        home_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
        service_requests_screen.pack_forget()
        services_screen.pack_forget()
        inventory_screen.pack(fill=tk.BOTH, expand=True)

    def open_suppliers() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        customers_screen.pack_forget()
        service_requests_screen.pack_forget()
        services_screen.pack_forget()
        suppliers_screen.pack(fill=tk.BOTH, expand=True)

    def open_customers() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        service_requests_screen.pack_forget()
        services_screen.pack_forget()
        customers_screen.pack(fill=tk.BOTH, expand=True)

    def open_service_requests() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
        services_screen.pack_forget()
        service_requests_screen.pack(fill=tk.BOTH, expand=True)

    def open_services() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
        service_requests_screen.pack_forget()
        services_screen.pack(fill=tk.BOTH, expand=True)

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

    # Create all screens
    login_screen = LoginScreen(app, open_home_screen)
    home_screen = HomeScreen(
        app, 
        open_login_screen, 
        open_inventory,
        open_suppliers,
        open_customers,
        open_service_requests,
        open_services
    )
    inventory_screen = Inventory(app, open_home_from_inventory)
    suppliers_screen = Suppliers(app, open_home_from_suppliers)
    customers_screen = CustomersScreen(app, open_home_from_customers)
    service_requests_screen = ServiceRequestsScreen(app, open_home_from_service_requests)
    services_screen = ServicesScreen(app, open_home_from_services)

    login_screen.pack(fill=tk.BOTH, expand=True)
    app.mainloop()

if __name__ == "__main__":
    main()
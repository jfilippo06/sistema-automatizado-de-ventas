import tkinter as tk
from screens.customers.customers_screen import CustomersScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.inventory.inventory import Inventory
from screens.services.services import ServicesScreen
from screens.supplier.supplier import Suppliers  # Import the new Suppliers screen

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
        services_screen.pack_forget()  # Nuevo
        login_screen.pack(fill=tk.BOTH, expand=True)

    def open_inventory() -> None:
        home_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
        services_screen.pack_forget()  # Nuevo
        inventory_screen.pack(fill=tk.BOTH, expand=True)

    def open_suppliers() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        customers_screen.pack_forget()
        services_screen.pack_forget()  # Nuevo
        suppliers_screen.pack(fill=tk.BOTH, expand=True)

    def open_customers() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        services_screen.pack_forget()  # Nuevo
        customers_screen.pack(fill=tk.BOTH, expand=True)

    def open_services() -> None:  # Nueva función
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack_forget()
        customers_screen.pack_forget()
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

    def open_home_from_services() -> None:  # Nueva función
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
        open_services  # Nuevo callback
    )
    inventory_screen = Inventory(app, open_home_from_inventory)
    suppliers_screen = Suppliers(app, open_home_from_suppliers)
    customers_screen = CustomersScreen(app, open_home_from_customers)
    services_screen = ServicesScreen(app, open_home_from_services)  # Nueva pantalla

    login_screen.pack(fill=tk.BOTH, expand=True)
    app.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.inventory.inventory import Inventory
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
        login_screen.pack(fill=tk.BOTH, expand=True)

    def open_inventory() -> None:
        home_screen.pack_forget()
        suppliers_screen.pack_forget()
        inventory_screen.pack(fill=tk.BOTH, expand=True)

    def open_suppliers() -> None:
        home_screen.pack_forget()
        inventory_screen.pack_forget()
        suppliers_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_inventory() -> None:
        inventory_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    def open_home_from_suppliers() -> None:
        suppliers_screen.pack_forget()
        home_screen.pack(fill=tk.BOTH, expand=True)

    # Create all screens
    login_screen = LoginScreen(app, open_home_screen)
    home_screen = HomeScreen(
        app, 
        open_login_screen, 
        open_inventory,
        open_suppliers  # Pass the suppliers callback
    )
    inventory_screen = Inventory(app, open_home_from_inventory)
    suppliers_screen = Suppliers(app, open_home_from_suppliers)  # Create suppliers screen

    login_screen.pack(fill=tk.BOTH, expand=True)
    app.mainloop()

if __name__ == "__main__":
    main()
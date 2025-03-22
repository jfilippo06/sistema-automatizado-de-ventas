import tkinter as tk
from screens.login_screen import LoginScreen  # Importar la pantalla de login
from screens.home_screen import HomeScreen  # Importar la pantalla de inicio
from screens.inventory.inventory import Inventory  # Importar la pantalla de inventario

def main() -> None:
    """
    Función principal que inicia la aplicación.
    """
    # Crear la instancia de la aplicación
    app: tk.Tk = tk.Tk()
    
    # Configurar el título de la ventana
    app.title("Sistema automatizado de ventas")
    
    # Configuración inicial de la ventana (puede ser sobrescrita por cada pantalla)
    app.geometry("800x600")  # Tamaño inicial
    app.resizable(True, True)  # Redimensionable por defecto
    
    # Función para abrir la pantalla de inicio (HomeScreen)
    def open_home_screen() -> None:
        """
        Oculta la pantalla de login y muestra la pantalla de inicio.
        """
        login_screen.pack_forget()  # Ocultar la pantalla de login
        home_screen.pack(fill=tk.BOTH, expand=True)  # Mostrar la pantalla de inicio

    # Función para abrir la pantalla de login (LoginScreen)
    def open_login_screen() -> None:
        """
        Oculta la pantalla de inicio y muestra la pantalla de login.
        """
        home_screen.pack_forget()  # Ocultar la pantalla de inicio
        login_screen.pack(fill=tk.BOTH, expand=True)  # Mostrar la pantalla de login

    # Función para abrir la pantalla de inventario (Inventory)
    def open_inventory() -> None:
        """
        Oculta la pantalla de inicio y muestra la pantalla de inventario.
        """
        home_screen.pack_forget()  # Ocultar la pantalla de inicio
        inventory_screen.pack(fill=tk.BOTH, expand=True)  # Mostrar la pantalla de inventario

    # Función para regresar a la pantalla de inicio (HomeScreen)
    def open_home_from_inventory() -> None:
        """
        Oculta la pantalla de inventario y muestra la pantalla de inicio.
        """
        inventory_screen.pack_forget()  # Ocultar la pantalla de inventario
        home_screen.pack(fill=tk.BOTH, expand=True)  # Mostrar la pantalla de inicio

    # Crear la instancia de la pantalla de login
    login_screen: LoginScreen = LoginScreen(app, open_home_screen)
    
    # Crear la instancia de la pantalla de inicio
    home_screen: HomeScreen = HomeScreen(app, open_login_screen, open_inventory)
    
    # Crear la instancia de la pantalla de inventario
    inventory_screen: Inventory = Inventory(app, open_home_from_inventory)
    
    # Mostrar la pantalla de login al iniciar la aplicación
    login_screen.pack(fill=tk.BOTH, expand=True)
    
    # Iniciar el bucle principal de la aplicación
    app.mainloop()

if __name__ == "__main__":
    main()
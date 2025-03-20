import tkinter as tk
from screens.login_screen import LoginScreen  # Importar la pantalla de login

def main():
    # Crear la instancia de la aplicación
    app = tk.Tk()
    
    # Configurar el título de la ventana
    app.title("Sistema automatizado de ventas")
    
    # Configuración principal de la ventana (puede ser sobrescrita por cada pantalla)
    app.geometry("800x600")  # Tamaño inicial
    app.resizable(True, True)  # Redimensionable por defecto
    
    # Crear la instancia de la pantalla de login
    login_screen = LoginScreen(app)
    login_screen.pack(fill=tk.BOTH, expand=True)
    
    # Iniciar el bucle principal de la aplicación
    app.mainloop()

if __name__ == "__main__":
    main()
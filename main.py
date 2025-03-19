import tkinter as tk
from screens.home_screen import HomeScreen

def main():
    # Crear la instancia de la aplicación
    app = tk.Tk()
    
    # Configurar el título de la ventana
    app.title("My Tkinter App")
    
    # Configurar el tamaño de la ventana
    app.geometry("800x600")
    
    # Crear la instancia de la pantalla principal
    home_screen = HomeScreen(app)
    home_screen.pack(fill=tk.BOTH, expand=True)
    
    # Iniciar el bucle principal de la aplicación
    app.mainloop()

if __name__ == "__main__":
    main()
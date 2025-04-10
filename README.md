Guía Completa para Configurar Entorno Virtual en Python (Windows)
Requisitos Previos
✅ Python 3.x instalado
✅ pip actualizado (python -m pip install --upgrade pip)

Pasos para Configuración
Abrir terminal
Presiona Win + R, escribe cmd y presiona Enter (o usa PowerShell)

Instalar virtualenv

bash
Copy
pip install virtualenv
Navegar a tu proyecto

bash
Copy
cd ruta\a\tu\proyecto
Crear entorno virtual

bash
Copy
python -m virtualenv env
(Se creará una carpeta env con todo lo necesario)

Activar el entorno

bash
Copy
.\env\Scripts\activate
🔹 Verás (env) al inicio de la línea de comandos cuando esté activado

Instalar dependencias

bash
Copy
pip install -r requirements.txt
Verificar instalación

bash
Copy
pip list
(Debes ver solo los paquetes instalados en tu entorno virtual)

Comandos Útiles
Comando	Descripción
deactivate	Desactiva el entorno virtual
where python	Muestra la ruta del Python actualmente en uso
pip freeze > requirements.txt	Genera archivo de dependencias
Recomendaciones
✨ Siempre activa el entorno antes de trabajar en el proyecto

🚫 No incluyas la carpeta env en tu control de versiones (agrégala a .gitignore)

🔄 Actualiza requirements.txt cuando instales nuevos paquetes:

bash
Copy
pip freeze > requirements.txt
Solución de Problemas Comunes
Si activate no funciona:

Ejecuta PowerShell como administrador

Ejecuta: Set-ExecutionPolicy RemoteSigned

Intenta nuevamente

Si tienes errores de permisos:

bash
Copy
python -m venv --clear env
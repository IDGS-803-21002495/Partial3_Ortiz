# Pizzeria 

Este es un sistema de gestión de pedidos para una pizzería, desarrollado con Flask, SQLAlchemy y Flask-Login. Permite a los usuarios registrar pedidos, ver pedidos hechos por fecha y el acceso controlado al sistema por medio de un login

## Características
- Inicio de sesión para usuarios registrados.
- Registro y visualización de pedidos de pizzas.
- Filtrado de pedidos por fecha.
- Eliminación de pedidos.

## Tecnologías Utilizadas

- **Flask**: Framework web para Python.
- **SQLAlchemy**: ORM para la gestión de bases de datos.
- **Flask-Login**: Manejo de sesiones de usuario.
- **Flask-WTF**: Manejo de formularios y validación.
- **Werkzeug**: Para el hashing de contraseñas.


## Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/IDGS-803-21002495/Partial3_Ortiz.git
   cd Partital3_Ortiz
  
2. **Crea un entorno virtual**:
   ```bash
   python -m venv env

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt

4. **Configura la base de datos**:
   - Asegúrate de que la base de datos esté configurada en config.py.
   - Crea la base de datos pizzeria en tu gestor de base de datos.
   - Agrega los usuarios que tendran acceso a la aplicación. **Recuerda que la contraseña esta en hash**.

5. **Ejecuta la aplicación**:
   ```bash
   py app.py

[**Para consultar más información sobre el uso de Flask-Login consulte aquí:**] (https://drive.google.com/file/d/1YcgK1A6wiycxfwKX0x9tmid-VVzcy7Sl/view?usp=sharing)

   
   

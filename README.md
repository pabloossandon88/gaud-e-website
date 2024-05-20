# Guía de Configuración para Gaud-E

Para ejecutar la página de Gaud-E localmente, sigue estos pasos:

1. **Clonar el Repositorio:**
   - Abre tu terminal y ejecuta:
     ```shell
     $ git clone git@github.com:Gaude10/gaud-e.git
     ```
   - Luego, navega hasta el directorio del proyecto:
     ```shell
     $ cd gaud-e
     ```

2. **Configurar un Entorno Virtual:**
   - Crea un entorno virtual para aislar las dependencias del proyecto:
     ```shell
     $ python -m venv venv
     ```
   - Activa el entorno virtual:
     - En Windows:
       ```shell
       $ venv\Scripts\activate
       ```
     - En macOS/Linux:
       ```shell
       $ source venv/bin/activate
       ```

3. **Instalar Dependencias:**
   - Instala las dependencias del proyecto utilizando pip:
     ```shell
     $ pip install -r requirements.txt
     ```

4. **Ejecutar el Servidor Local:**
   - Una vez instaladas las dependencias, ejecuta el servidor con el siguiente comando:
     ```shell
     $ python manage.py runserver
     ```

¡Listo! Ahora puedes acceder a la página Gaud-E localmente desde tu navegador.

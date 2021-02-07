# INSTALACIÓN

## DESCARGA O CLONACIÓN DEL REPOSITORIO

- Abrimos Visual Studio Code.

- Descargamos la carpeta del repositorio GitHub y la guardamos en nuestra área de trabajo.

- También podemos crear una carpeta vacía con el nombre que nosotros queremos y clonar el repositorio en esa carpeta.
    - Para ello en la página principal de Visual Studio Code seleccionamos clonar repositorio.
    - Pegamos la URL desde Github y seleccionamos donde clonar la carpeta.

## CREACIÓN DEL ENTORNO VIRTUAL

- Una vez tenemos el repositorio del Proyecto_Flask procedemos a crear nuestro entorno virtual:
    - En nuestro terminal ejecutamos python3 -m venv <nombre_del_entorno> (Este será el nombre con el que llamemos al entorno virtual).
    - Ejemplo:
        -  python3 -m venv venv 
    - Ahora activamos el entorno virtual (para Mac):
    - source <nombre_del_entorno>/bin/activate.

- Dentro de la carpeta raiz del proyecto creamos el archivo .env
    - Dentro del archivo .env introducimos lo siguiente:
        - FLASK_APP=run.py
        - FLASK_ENV=development

## INSTALACIÓN DE DEPENDENCIAS

- Ejecutamos en el terminal el siguiente comando para instalar los paquetes Python contenidos en el archivo requirements.txt:
    - pip install -r requirements.txt

## GENERACION DEL FICHERO DE CONFIGURACIÓN

- Ahora crearemos nuestro fichero de configuración con nuestras claves, para ello:
    - Copiamos el fichero config_template.py
    - Renombramos el archivo llamandolo config.py
        - En este archivo tendremos que modificar las claves de acesso.
        - Comenzamos cambiando la clave de SECRET_KEY, por una contraseña propia.

## OBTENCIÓN DEL API CONTAINER

- En la dirección https://coinmarketcap.com/api/ realizamos el registro para obtener nuestra API_KEY en el plan gratuito.
- Una vez registrados, copiamos la clave de nuesra API_KEY en el archivo config.py que hemos creado, en el apartado API_KEY.

## CREACIÓN DE LA BASE DE DATOS

- En nuestro terminal ejecutamos el script crear_bbdd.py
- Dentro de la carpeta movement, creamos una subcarpeta llamada data.
    - Movemos la base de datos creada 'database.db' a la carpeta data que acabamos de crear dentro de movements.
- En nuestro fichero config.py, modificamos el apartado DB_FILE, por la ruta de nuestra base de datos. En este caso 'movements/data/database.db'

## EJECUCIÓN

- Nos aseguramos de tener el entorno virtual activado. Si no lo está lo activamos como vimos en el primer paso de la instalación.
- En nuestro terminal ejecutamos flask run para poder acceder a la aplicación web.

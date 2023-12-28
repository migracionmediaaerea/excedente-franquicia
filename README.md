# Django Template  
<sub><sub> Si estas viendo este archivo en VSCode, sera importante verlo mejor aplastando `CTRL + SHIFT + P` y buscar `Markdown: Open Preview`  </sub></sub>

## Descripción referente a la nueva estructura
Gracias a esta nueva estructura, el desarrollador no necesitara tener instalado una versión de Python en especifico, no tendrán que instalar librerías de otros lados, bases de datos solas, etc.
Solo será necesario que se tenga instalado Docker, hacer el tutorial de abajo, para que se pueda correr el proyecto sin tanto show.

## Requisitos
- WSL v2 (en caso de estar en Windows)
- Docker Desktop/Engine
- ~~Python 3.8+~~
- ~~WKHTMLTOPDF~~
- ~~GTK+ (en caso de estar en Windows)~~

## Primeros pasos
1. Clonar el archivo **`.env.example`** y renombrarlo como **`.env`**
1. Configurar el archivo **`.env`** nuevo, pero esto no es tan necesario, ya que así como viene asi funciona perfectamente
	- Si el proyecto es nuevo (o la opción `SECRET_KEY` esta vacía) sera necesario generar una llave secreta que será compartida en todo el proyecto usando los comandos de [esta sección](#crear-una-secret_key-nueva) y subir el cambio también en el archivo de ejemplo **`.env.example`** al repositorio de GitHub.
1. Estar en el [directorio actual](#directorio-actual) en la terminal
1. Para inicializar el proyecto, primero deberas crear y correr migraciones de la base de datos [siguiendo estos pasos](#correr-migraciones).
1. Gracias al paso anterior, ya se te habra descargado y configurado todo lo necesario, deberas ahora ejecutar el comando `docker-compose up` para correr todo el proyecto de Django con su base de datos.
1. Comprobar si http://localhost:3000 da señal
1. Para crear un superusuario, [lee esta sección](#crear-un-superusuario)
1. Saber como [poder volver a correr el proyecto después](#correr-proyecto)

# Comandos de utilidad
## Correr migraciones
1. Se deberá correr los siguientes comandos:
	```bash
	docker-compose run --rm django python manage.py makemigrations
	docker-compose run --rm django python manage.py migrate
	```

## Crear un superusuario
1. Se deberá correr el siguiente comando:
	```bash
	docker-compose run --rm django python manage.py createsuperuser
	```
1. Recuerda que deberas agregar tu modelo actual en el archivo **admin.py** de la app en cuestión para que sea enlistada su entidad en el administrador de Django

## Crear una SECRET_KEY nueva
1. Esto solo deberá ser corrido si el repositorio no tiene una **SECRET_KEY**
1. Se deberá correr el siguiente comando:
	```bash
	docker-compose run --rm django openssl rand -hex 32
	```
1. El código será copiado y pegado tanto en el **.env.example** y **.env**
1. Subir el cambio a GitHub para que todos tengamos la misma llave.

## Crear una app
1. Se deberá crear la app con el siguiente comando:
	```bash
	docker-compose run --rm django python manage.py startapp NOMBRE_APP
	```
1. En el archivo general de **urls.py** (ubicado en <ins>djangotemplate/</ins>) agregar su ruta, además de importarla y su 'urlpattern'
1. En el archivo de **settings.py** (ubicado en <ins>djangotemplate/</ins>) agregar el nombre de la app dentro de **INSTALLED_APPS**
1. Copia el archivo **urls.py** de la <ins>app de ejemplo (exampleApp)</ins> en tu <ins>app nueva</ins> y cambia todas las referencias necesarias
1. Copia el archivo **models.py** y **forms.py** de la <ins>app de ejemplo (exampleApp)</ins> y adecua su lógica que sea la adecuada para tu nueva app
1. Posiblemente tengas que cambiar la lógica de **views.py**

## Correr comando dentro del contenedor de Django
1. La estructura del comando es la siguiente (en caso de que necesites saberlo)
	```bash
	docker-compose run --rm <contenedor> <comando>
	```
1. Por ejemplo, si el contenedor donde esta **Python+Django** se llama `django` y si queremos correr solo `python manage.py` el comando seria:
	```bash
	docker-compose run --rm django python manage.py
	```
1. Si es necesario, se puede correr una terminal dentro del contenedor para correr varios comandos utilizando `bash`
	```bash
	docker-compose run --rm django bash
	```

## Correr proyecto
Hay dos formas para poder correr el proyecto, las cuales son:
  
- Correr el proyecto desde un comando
	1. Estar en el [directorio actual](#directorio-actual) 
	1. Correr el siguiente comando [o este alternativo](#correr-contenedor-en-segundo-plano):
		```bash
		docker-compose up
		```
	1. Si cierras la pestaña/terminal donde se esta corriendo el proyecto, el proyecto también se cerrara.
  
- Correr el proyecto desde Docker Desktop
	1. Abrir Docker Desktop
	1. Ubicar el contenedor que tiene el nombre del repositorio
	1. Darle al iniciar


# Notas
## Correr contenedor en segundo plano
- Si prefieres que el contenedor corra en segundo plano y este no se cierre al cerrar accidentalmente la pestaña del contenedor o cerrar VSCode y tener la terminal del contenedor en otro lado puedes correr el proyecto usando:
	```bash
	docker-compose up -d
	```
- Los mensajes de la terminal del contenedor se pueden ver ubicando el contenedor en Docker Desktop, o con el siguiente comando
	```bash
	docker-compose logs -f
	```
- Si cierras la pestaña o el comando, seguirá corriendo el contenedor en el fondo

## Directorio actual
- Es necesario que en tu terminal estés en la ruta del proyecto actual para poder correr los comandos de `docker-compose`

## Nuevo requirement
- Para instalar un requirement nuevo, debera ser desde [dentro del contenedor de Django](#correr-comando-dentro-del-contenedor-de-django)
- Cuando instales el requirement, es necesario que lo agregues **<ins>MANUALMENTE</ins>** al archivo de **requirements.txt** y no usar el comando de `pip freeze` ya que hay una libreria custom que el comando de `freeze` no referencia automáticamente correctamente  

		Si hay dudas, preguntenme jajaja Atte: @ClaudioBo

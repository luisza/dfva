Instalación
================

.. note:: Sin hacer, esto solo para quienes estén familiarizados con django y para entorno de desarrollo

Instale las dependencias
--------------------------

Clone el repositorio desde

::

    git clone https://github.com/luisza/dfva.git

Instale las dependencias (es recomendable utilizar un entorno virtual)

::

   pip install -r requirements.txt

Modifique el archivo dfva/settings.py según la documentación.

Cree una CA con OpenSSL
-------------------------

Cree la carpeta internal_ca con el siguiente contenido.

::

  internal_ca/
  ├── ca_cert.pem
  └── ca_key.pem


Se utiliza el siguiente comando para generar la CA.

.. code:: bash

  #!/bin/bash 
  mkdir -p db
  mkdir -p ca
  /bin/echo -n '01' > db/serial.txt
  touch db/index.txt
  touch db/index.txt.attr

  openssl req -days 2922 -config openssl.cnf -newkey rsa:4096 -nodes -out ca/cert.pem -x509 -keyout ca/key.pem
  openssl x509 -outform der -in ca/cert.pem -out ca/cert.crt


Este es un archivo openssl.cnf de ejemplo :download:`descargar <_static/openssl.cnf>`.

En settings.py agregue:

.. code:: python 

  CA_PATH = os.path.join(BASE_DIR, 'internal_ca')
  CA_CERT = os.path.join(CA_PATH, 'ca_cert.pem')
  CA_KEY = os.path.join(CA_PATH, 'ca_key.pem')


Ejecute la creación de la base de datos.
-------------------------------------------

Asegurese de configurar la base de datos, y el motor de base de datos


::

   python manage.py migrate


Corra el programa
--------------------

::

  python manage.py runserver


Corra las tareas syncrónicas
-------------------------------

Para desarrollo puede no ser necessario corre las tareas asyncrónicas encargadas de notificar a aplicaciones externas.

Si se desea la funcionalidad de notificaciones con tiempo entonces deben ejecutarse en otra pestaña

::
  
  celery -A dfva worker -l info -B

Settings de interés
---------------------

- FVA_HOST = "http://localhost:8001/":  Url donde está corriendo el simulador del FVA BCCR
- STUB_SCHEME = 'http':  Esquema para el Servicio SOAP del BCCR
- STUB_HOST = "localhost:8001":  Máquina del servicio SOAP del BCCR
- RECEPTOR_HOST = "http://localhost:8000/": url base donde se recibirán las notificaciones del FVA BCCR
- DEFAULT_BUSSINESS = 1  Identificador del negocio del FVA BCCR
- DEFAULT_ENTITY = 1  Identificador de la entidad del FVA BCCR
- RECEPTOR_CLIENT = 'receptor.client'   cliente que recibe las respuestas del FVA BCCR
- DFVA_REMOVE_AUTHENTICATION = 5 tiempo en minutos de vida de la autenticación
- DFVA_REMOVE_SIGN = 20  tiempo en minutos de vida de la firma
- DFVA_PERSON_SESSION = 25  duración en minutos de la sesión de una persona

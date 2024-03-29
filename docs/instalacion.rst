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

.. warning:: 

    Solo requiere **un manejador de CA**, puede usar una CA con Python CertBuilder o integrarse con DOGTAG (son excluyentes entre si)

Instalación de una CA dummy
---------------------------------------

Cree la carpeta internal_ca y ejecute el siguiente comando para generar la CA.

.. code:: bash

  python manage.py  crea_ca

Se generará los siguientes archivos:

::

  internal_ca/
  ├── ca_cert.pem
  └── ca_key.pem
  └── crl.pem

Cambie los permisos de los archivos

::

  cd internal_ca/
  chmod 600 ca_cert.pem  ca_key.pem crl.pem

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
   python manage.py createsuperuser
   python manage.py create_admin_institution

Importante create_admin_institution requiere de tener al menos un usuario superadminsitrador.

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

Instalación de Dogtag manager
--------------------------------

Se requiere la biblioteca `dogtag-pki`, y esta a su vez depende de python-nss que tiene como dependencia `libnss3-dev` por eso ejecutar:

.. code:: bash

    apt-get install libnss3-dev
    pip install dogtag-pki


Agregue en settings.py 

.. code:: bash

    CAMANAGER_CLASS="corebase.ca_management.dogtag"
    DOGTAG_HOST='localhost'
    DOGTAG_PORT='8443'
    DOGTAG_SCHEME='https'
    DOGTAG_AGENT_PEM_CERTIFICATE_PATH=os.path.join(BASE_DIR, 'admin_cert.pem')
    DOGTAG_CERTIFICATE_SCHEME={
    'O': 'EXAMPLE.COM'    
    }
    DOGTAG_CERT_REQUESTER='dfva'
    DOGTAG_CERT_REQUESTER_EMAIL='dfva@example.com'


.. note:: 

    Puede instalar una sistema PKI para pruebas utilizando una imágen en docker de la siguiente forma.

    .. warning:: Es recomendable correrla en una máquina con más de 2Gb de RAM  

    Permite activar IPV6 

    .. code:: bash 

       cat /etc/docker/daemon.json 
       {
         "ipv6": true,
         "fixed-cidr-v6": "2001:db8:1::/64"
       }

    .. code:: bash 

       docker run --name freeipa-server-container --privileged -ti   \
       -h  ipa.mifirmacr.org  \
       -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
       -p 53:53/udp -p 53:53 \
       -p 80:80 -p 443:443 -p 389:389 -p 636:636 -p 88:88 -p 464:464 \
       -p 88:88/udp -p 464:464/udp -p 123:123/udp -p 7389:7389 \
       -p 8443:8443 -p 8080:8080 -p 9445:9445 \
       --security-opt seccomp=unconfined \
       --tmpfs /run --tmpfs /tmp \
       -v /var/lib/ipa-data:/data:Z freeipa/freeipa-server \
       --realm=mifirmacr.org \
       --ds-password=LDAPPASSWORD \
       --admin-password=ADMINPASSWORD 

    Se requiere que el usuario sea un agente de Dogtag, de lo contrario no se autenticará, para extraer el certificado pkcs12 del usuario admin que además es un agente 
    dogtag debe buscar la llave en 

    .. code:: bash

        docker exec -ti <nombre maquina> bash
        cat /data/root/ca-agent.p12 | base64 

    para descomprimir y convertir a pem se recomienda algo como :

    .. code:: bash

        echo "codigo base64" | base64 -d > ca-agent.p12 
        openssl pkcs12 -in ca-agent.p12 -out admin_cert.pem -nodes

    La contraseña es la misma que ds-password osea en este caso LDAPPASSWORD

Una vez instalado puede ejecutar

.. code:: bash

    python manage.py runserver

Y acceder a http://localhost:8000 y a partir de ahí iniciar las configuraciones necesarias.

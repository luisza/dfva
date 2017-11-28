Aspectos de seguridad
=========================


Comunicación
--------------------------

DFVA es una aplicación RESTFull por lo que usa JSON como modelo de representación de objetos, los objetos son enviados vía POST sobre un canal de comunicación
HTTPS.  
Las peticiones tienen el siguiente formato:

* **data_hash:** Suma hash de datos de tamaño máximo 130 caracteres, usando el algoritmo especificado 
* **algorithm:** Algoritmo con que se construye data_hash, debe ser alguno de los siguientes: sha256, sha384, sha512
* **public_certificate:** Certificado de autenticación 
* **data:** Datos de solicitud de autenticación encriptados usando AES Modo EAX con la llave de sesión encriptada con PKCS1_OAEP.

Además se envía un atributo identificador que depende del tipo de conversación que se quiera entablar, actualmente se pueden comunicar con DFVA: 
una institución (**institution**) con el uuid proporcionado en dfva y una persona (**person**) con su número de identificación (ver formato_). 

.. _formato: http://pyfva.readthedocs.io/en/latest/formatos.html

DFVA verifica que *data_hash* sea igual al generado a partir de data utilizando el algoritmo indicado.

Las respuestas tienen el siguiente formato:

* **data_hash:** Suma hash de datos de tamaño máximo 130 caracteres, usando el algoritmo especificado 
* **algorithm:** Algoritmo con que se construye data_hash, debe ser alguno de los siguientes: sha256, sha384, sha512 *por defecto sha515*
* **data:** Datos de respuesta encriptados usando AES Modo EAX con la llave de sesión encriptada con PKCS1_OAEP.

DFVA intenta desencriptar lo suministrado en data utilizando los juegos de llaves explicados acontinuación:

Institución
~~~~~~~~~~~~~~

Para manejar instituciones se debe crear una institución en la plataforma, al crearse se generará una llave privada, una llave pública y un certificado.

La llave privada corresponde a la llave privada de la institución y será utilizada para desencriptar las respuestas de dfva,

La llave pública corresponde a la llave pública de DFVA que se utilizará para encriptar la información que se envía en data.  

En DFVA se construye dos pares de llaves por cada institución.

* **Llaves de la aplicación:** La llave privada se entrega y la llave pública se guarda y nunca es revelada.
* **Llaves del servicio:** La llave privada se guarda y nunca es revelada y la llave pública se entrega a la institución.

Los juegos de llaves encriptados y el certificado se guardan en la base de datos, excepto la llave privada de la institución, la cual nunca es almacenada en la báse de datos y solo se muestra una vez al usuario.
Debido a que tanto las llaves privadas y las públicas son exclusivas de cada institución y generadas dentro de DFVA la llave pública de la institución nunca es expuesta asegurando aún más la comunicación RSA.

.. note::  Se utiliza el SECRET_KEY de Django para generar una llave de encripción para los atributos almacenados en la base de datos, por lo que asegurece cambiar el valor por defecto.

Persona
~~~~~~~~~~~~~~

Para la comunicación con personas se utiliza la encripción provista por los dispositivos PKCS11, de ahí se extrae:

* Un certificado de Autenticación.
* Un certificado de Firma.

En mis pruebas el certificado de firma tiene una llave privada que no permite desencriptar, por lo que solo se utiliza autenticación para comunicación.

Cuando una persona desea comunicarse con DFVA lo primero que reliza el programa es negociar el token de autenticación, el token es encriptado utilizando la llave pública del certificado de Autenticación en DFVA y enviado a la aplicación, dicho token solo puede ser desencriptado con el dispositivo PKCS11 y la llave privada de auteticación.

El token será utilizado como token de sesión en el algoritmo AES Modo EAX al encriptar data y deberá ser enviado firmado utilizando alguna de las llaves privadas del dispositivo (según contexto) y se comprobará en DFVA que el token sea correcto antes de proceder a desencriptar la información.



Almacenamiento
------------------

.. note:: FALTA, Actualemente se guarda la información de verificación en forma plana en una base de datos y nunca se borra, autenticación y firma ya mueve a logs la información.

.. warning:: FALTA, Manejo información sobre los modelos de personas, la información descrita corresponde únicamente a institutiones.

DFVA se basa en Django por lo que soporta todas las bases de datos que este framework soporta, pero recomendamos Postgresql 9.4 o superior. 

Las solicitudes de autenticación tiene un tiempo de vida de al menos 5 minutos (configurables), así una solicitud de autenticación se guardará en la base de datos por el tiempo definido, luego se extrae y se guarda en un archivo de log especiamente diseñado para guardar las solicitudes.

Las solicitudes de firma tienen un tiempo de vida de al menos 20 minutos (configurables), así una solicitud de firma se guardará por el tiempo definido y luego se guardará en un archivo de logs diseñado para guardar estas solicitudes. No se guarda el documento firmado, solo el registro de que se firmó y su suma hash.


Se pretende que las verificaciones de documentos y certificados y las revisiones de suscriptor conectado no se guarden en la base de datos (FALTA).

DFVA trabaja con tareas asincrónicas llamadas cada 5 y 20 minutos las cuales se encargan de revisar cuales peticiones han vencido el plazo y deben enviarse a logs, debido a este comportamiento algunas peticiones tendrán una duración entre 5-9 minutos para autenticación y 20 a 39 minutos para firma antes de ser enviadas a logs.   Debido a que se provee la opción de solicitar la información de una petición para clientes no web esta información debe permanecer por un periodo de tiempo, además los mecanismos de control propios impedirá que una petición cuyo tiempo de vida haya caducado pueda ser obtenida por un cliente.



Bitácoras
------------------

DFVA usa al máximo el sistema de bitácoras de Django por lo que es ampliamente configurable.  Actualmente genera los siguientes logs:

* **pyfva (debug, info, errors):** Bitácoras de comunicación con BCCR FVA
* **dfva (debug, info, errors):** Bitácoras de funcionamiento interno de DFVA.
* **dfva_authentication (info):** Bitácora de solicitudes de autenticación
* **dfva_sign (info):**  Bitácora de solicitudes de firma.

Las bitácoras **dfva_authentication**, **dfva_sign** guardan los objecto en formato json.  Actualmente la mayoría de los datos guardados son volcados a estas bitácoras.


Transporte
------------------

Se recomienda implementar HTTP Strict Transport Security (HSTS) en el sistemas en producción.

Disponibilidad
-------------------

DFVA está basado en Django y utiliza todos los mecanismos provistos por este, así también posee todas las bondades en cuanto a escalabilidad. Por ello DFVA es escalable tanto Horizontal como Verticalmente.

Aunque AES EAX no es thread safe, solo se utiliza un hilo por encripción y abonando el hecho que Django es thread safe, se concidera que DFVA posee la capacidad de ejecutarse en entornos multi-hilo, con un pequeño impacto en los tiempos de encripción.

.. note:: Más pruebas del comportamiento multihilo son recomendables.

Manejo de los certificados
---------------------------

DFVA es versatil y permite configurar el manejador de certificados, con ello permite comunicarse con la infraestructura de PKI que se desee.

Actualmente, se soporta la integración con Dogtag_ y también se soporta CA's creadas con OpenSSL para desarrollo utilizando el manejador **CA simple con OpenSSL**

.. _Dogtag: http://pki.fedoraproject.org/wiki/PKI_Main_Page

CA Simple con OpenSSL
~~~~~~~~~~~~~~~~~~~~~~~~

La emisión de certificados, se genera 

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

DogTag
~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Para la instalación ver la sección de instalación de DFVA.

Dogtag es una aplicación que se integra con FreeIPA para proporcionar una robusta infraestructura PKI, actualmente el cliente desarrollado se integra con el API rest de Dogtag para generar, validar y revocar certificados.

Una aspecto importante de la implementación es que requiere que el usuario utilizado sea un agente de Dogtag capaz de solicitar y aprovar certificados, por lo que la aplicación será capaz de generar certificados en Dogtag de forma automática, debe contemparse esta situación dentro de la política de la PKI.

Dentro del proceso de solicitud de certificados se genera un objeto X509Request (certificate signing request csr) utilizando el esquema proporcionado en `DOGTAG_CERTIFICATE_SCHEME` exceptuando los campos OU y CN que corresponden a:

- OU =  institution unit
- CN = domain

Ambos recolectados desde la interfaz.

En la validación del certificado se utiliza el `serial_number` del certificado para solicitar el estado del mismo en Dogtag. Además se valida el issuer sea identico al issuer de la instalación de Dogtag, así se garantiza que dicho certificado fue emitido por el issuer y que el serial_number es el adecuado.


Encripción
-------------

Se recomienda utilizar transporte https para la puesta en producción de esta plataforma, aún así DFVA posee una segunda capa de encripción, utilizando los algoritmos.

- **AES EAX:** Algoritmo simetrico, utilizado para encriptar el contenido, posee un token de sessión y un atributo IV (nonce). Este par debe ser único en cada encripción, osea no se puede repetir el IV con el mismo token de sessión.  Actualmente tanto el token de sessión como el IV son de 16 bytes.
 
- **PKCS1 OAEP:**  Algoritmo de encripción asimétrico, es utilizado para encriptar el token de sessión.   También conocido como RSA/NONE/OAEPWithSHA1AndMGF1Padding en ambiente java.

Estructura de la encripción es:   Token encriptado + IV (nonce) + datos encriptados.

.. warning:: en algunas implementaciones como en java se incluye dentro de los datos encriptados el IV al final, por lo que debe removerse y ponerse después del token encriptado.




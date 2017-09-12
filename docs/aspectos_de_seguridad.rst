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
* **Laves del servicio:** La llave privada se guarda y nunca es revelada y la llave pública se entrega a la institución.

Debido a que tanto las llaves privadas y las públicas son exclusivas de cada institución y generadas dentro de DFVA la llave pública de la institución nunca es expuesta asegurando aún más la comunicación RSA.


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

DFVA se basa en Django por lo que soporta todas las bases de datos que este framework soporta, pero recomendamos Postgresql 9.4 o superior. 

Las solicitudes de autenticación tiene un tiempo de vida de al menos 5 minutos (configurables), así una solicitud de autenticación se guardará en la base de datos por el tiempo definido, luego se extrae y se guarda en un archivo de log especiamente diseñado para guardar las solicitudes.

Las solicitudes de firma tienen un tiempo de vida de al menos 20 minutos (configurables), así una solicitud de firma se guardará por el tiempo definido y luego se guardará en un archivo de logs diseñado para guardar estas solicitudes. No se guarda el documento firmado, solo el registro de que se firmó y su suma hash.


Se pretende que las verificaciones de documentos y certificados y las revisiones de suscriptor conectado no se guarden en la base de datos (FALTA).

DFVA trabaja con tareas asincrónicas llamadas cada 5 y 20 minutos las cuales se encargan de revisar cuales peticiones han vencido el plazo y deben enviarse a logs, debido a este comportamiento algunas peticiones tendrán una duración entre 5-9 minutos para autenticación y 20 a 39 minutos para firma antes de ser enviadas a logs.   Debido a que se provee la opción de solicitar la información de una petición para clientes no web esta información debe permanecer por un periodo de tiempo, además los mecanismos de control propios impedirá que una petición cuyo tiempo de vida haya caducado pueda ser obtenida por un cliente.

Transporte
------------------

Se recomienda implementar HTTP Strict Transport Security (HSTS) en el sistemas en producción.


Emisión de certificados
--------------------------

.. note:: Actualmente se utiliza una CA interna generada con openSSL, debido a que no tenemos los fondos para un HSM :(.

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

.. note:: Se espera contar con un HSM para proporcionar mayor seguridad. 




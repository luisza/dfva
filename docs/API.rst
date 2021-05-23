API de Comunicación
=====================

DFVA es una aplicación RESTFull por lo que usa JSON como modelo de representación de objetos, los objetos son enviados vía POST sobre un canal de comunicación
HTTPS.  
Las peticiones tienen el siguiente formato:

* **data_hash:** Suma hash de datos de tamaño máximo 130 caracteres, usando el algoritmo especificado 
* **algorithm:** Algoritmo con que se construye data_hash, debe ser alguno de los siguientes: sha256, sha384, sha512
* **public_certificate:** Certificado de autenticación 
* **data:** Datos de solicitud de autenticación encriptados usando AES con la llave de sesión encriptada con PKCS1_OAEP.
* **encrypt_method:** (opcional, por defecto: "aes_eax") Método de encripción del contenido ("aes_eax", "aes-256-cfb")  

Además se envía un atributo identificador que depende del tipo de conversación que se quiera entablar, actualmente se pueden comunicar con DFVA: 
una institución (**institution**) con el uuid proporcionado en dfva y una persona (**person**) con su número de identificación (ver formato_). 

.. _formato: http://pyfva.readthedocs.io/en/latest/formatos.html

DFVA verifica que *data_hash* sea igual al generado a partir de data utilizando el algoritmo indicado.

Las respuestas tienen el siguiente formato:

* **data_hash:** Suma hash de datos de tamaño máximo 130 caracteres, usando el algoritmo especificado 
* **algorithm:** Algoritmo con que se construye data_hash, debe ser alguno de los siguientes: sha256, sha384, sha512 *por defecto sha515*
* **data:** Datos de respuesta encriptados usando AES Modo EAX con la llave de sesión encriptada con PKCS1_OAEP.


Instituciones
----------------

Autenticación
~~~~~~~~~~~~~~~

.. automethod::  institution.authenticator.views.AuthenticateRequestViewSet.institution 
.. automethod::  institution.authenticator.views.AuthenticateRequestViewSet.institution_show
.. automethod::  institution.authenticator.views.AuthenticateRequestViewSet.institution_delete

Firma
~~~~~~~~~~~~~~~

.. automethod::  institution.signer.views.SignRequestViewSet.institution 
.. automethod::  institution.signer.views.SignRequestViewSet.institution_show
.. automethod::  institution.signer.views.SignRequestViewSet.institution_delete

Validación
~~~~~~~~~~~~~~~

.. automethod::  institution.validator.views.ValidateInstitutionViewSet.institution_certificate
.. automethod::  institution.validator.views.ValidateInstitutionViewSet.institution_document
.. automethod::  institution.validator.views.ValidateSubscriptorInstitutionViewSet.institution_suscriptor_connected

Personas
------------


Autenticación
~~~~~~~~~~~~~~

.. autoclass::  person.authenticator.views.AuthenticatePersonView

Firma
~~~~~~~~~~~~~~~

.. autoclass::  person.signer.views.SignPersonView

Validación
~~~~~~~~~~~~~~~

.. autoclass::  person.validator.views.ValidateCertificatePersonViewSet
.. autoclass::  person.validator.views.ValidateDocumentPersonViewSet
.. autoclass::  person.validator.views.ValidateSubscriptorPersonViewSet

Login
~~~~~~~~

.. automethod::  person.views.PersonLoginView.list
.. automethod::  person.views.PersonLoginView.create


Notififcación para Instituciones
----------------------------------

.. autofunction::  receptor.notify.send_notification



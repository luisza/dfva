Riesgos identificados
============================

Los riesgos aquí descritos responden a escenarios y comportamientos de SIFVA que podrían llevar a un riesgo para la implementación, este lugar no es una lista de vulnerabilidades conocidas y todos los riesgos descritos han sido tratados y mitigados, pero en honor al trabajo realizado en este proyecto y en aras de demostrar que los desarrolladores de SIFVA nos tomamos en serio la seguridad hacemos público aquellos riegos identificados que podrían poner en peligro la implementación de este software.

Almacenamiento
-----------------

Almacenamiento de llaves y certificados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las llaves privadas de los servicios se guardan en la base de datos, por ello todas llaves privadas usadas por los servicios (no las llaves privadas de las aplicaciones) son almacenadas en la base de datos. 

**Mitigación**

Para mitigar este riesgos se realiza:

- Se Guardan encriptadas las llaves y certificados de la institución en la base de datos utilizando  AES Modo EAX.
- Se utiliza `SECRET_KEY` de Django para generar una llave de encripción para AES.
- No se almacela la llave privada de la aplicación.
- Aseguramiento de la base de datos en producción

Almacenamiento de peticiones y respuestas de firma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las peticiones al BCCR FVA deben esperar a la respuesta del BCCR que tiene como política “No nos llame, nosotros lo llamamos”.  Por ello deben almacenarse en una base de datos.  Por ello existe el riesgo que la información de las peticiones almacenadas en la base de datos puedan ser accedidas por extraño si la configuración del manejador de base de datos presenta alguna vulnerabilidad. 

Además afecta el rendimiento de consulta de peticiones con respecto al número de peticiones por minuto en el sistema.


**Mitigación**

- Almacenar las peticiones por un tiempo fijo pero configurable, para autenticación por defecto se espera 5 minutos y para firma 20 minutos.  
- Aseguramiento de la base de datos en producción
- Indexación de modelos de peticiones


Almacenamiento de bitácoras y auditoría
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SIFVA y PyFVA poseen un completo sistema de bitácoras, haciendo uso completo de `Django logging`_ emitiendo mensajes en los niveles Información, Debug, Warning, Error.  Por defecto se guardan las bitácoras en disco provocando 2 afectaciones; 1) llenar el disco con logs, 2) fuga de información producto de los logs 

**Mitigación**

- Configurar adecuadamente el sistema de logs, revisar `Django logging`_ y configurar un sistema de compresión y rotación de logs.

.. _`Django logging`: https://docs.djangoproject.com/en/1.11/topics/logging/

Almacenamientos de peticiones HTTP 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al firmar un documento se requiere que se envíen en el mensaje REST vía POST. Normalmente los servidores de contenido como Apache o Nginx almacenan las peticiones en memoria pero limitan el tamaño, y si se deseea aumentar el tamaño se utiliza el sistema de archivos.  Así existe el riesgo de que alguien intente aprovechar esta particularidad para incrustar código malicioso e intentarlo ejecutar desde el sistema de archivos del sistema operativo. 

**Mitigación**

- Debe mitigarse a nivel de implementación del servicio y configurando adecuadamente Nginx o Apache.

Serialización y deserialización de comunicaciones
----------------------------------------------------

Deserialización de Json
~~~~~~~~~~~~~~~~~~~~~~~~~

Toda la comunicación entre SIFVA y las instituciones o personas se realiza utilizando JSON, por lo que alguien podría intentar insertar código malicioso para hacer romper los mecanismos de deserialización y con ello afectar el servicio.

**Mitigación**

- SIFVA utiliza la última versión de Django Rest Framework y confía en la seguridad de este proyecto en el manejo de deserialización JSON.

Serialización de XML (Pyfva)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un atacante podría intentar construir una petición maliciosa que rompa el serializador de XML para incrustar información que altere el comportamiento de la petición a nivel de BCCR FVA.

**Mitigación**

- Se confía en la biblioteca Soapfish_ para la elaboración de XML.
- La deserialización de XML se confía en que el único que envía XML es el BCCR.

.. _Soapfish: https://github.com/soapteam/soapfish

Disponibilidad
-----------------

Sustitución del servicio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SIFVA es código abierto y libre, por lo que cualquiera puede configurar una instalación e intentar hacerse pasar por SIFVA válido.


**Mitigación**

- Doble uso de llaves RSA y el cifrado de las comunicaciones ayuda a mitigarlo.  La llave privada de la apliación solo la debería conocer la aplicación y la llave privada del servicio solo la conoce SIFVA por lo que un sustituto no puede desencriptar las peticiones o enviar respuestas falsas.
- Cada institución debe crear mecanismos necesarios para resguardar las llaves RSA y los certificados.


Continuidad del servicio 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SIFVA no provee ninguna herramienta para prevenir ataques de denegación de servicio.


**Mitigación**

- SIFVA está implementado para poder lanzarse en sistema distribuidos y balanceados, por lo que una buena infraestructura puede mitigar este tipo de ataques.
- SIFVA No utiliza sesiones de estado, y cada petición se inicia y termina en una operación atómica.


Si los servicios del BCCR no están disponibles SIFVA no funciona.

**Mitigación**

- SIFVA siempre enviará un mensaje de error al cliente indicando que la transacción no se pudo realizar, por lo que el servicio de SIFVA segurá disponible.

Integridad
--------------

Integridad de las peticiones 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Algún atacante podría intentar un *Man in the Middle* para alterar el contenido de las peticiones y respuestas. Además una aplicación podría proponer hacer una petición por un canal no seguro.

**Mitigación**

- SIFVA, podría ser implementado sobre HTTP sin perder la integridad y confidencialidad de los datos, gracias al doble mecanismo de encripción. Aun así se recomienda encarecidamente utilizar HTTPS en producción.

Integridad de las respuestas del BCCR FVA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un atacante podría hacerse pasar por el BCCR FVA y emitir respuestas a peticiones para por ejemplo suplantar identidad o falsificación de documentos.

**Mitigación**

- SIFVA posee una variable de configuración obligatoria llamada `ALLOWED_BCCR_IP` donde se especifican las direcciones IP de los servidores del BCCR que envían respuestas, cualquier IP que no esté listada en esta variable se le denegará el acceso.


Confidencialidad
----------------------

Suplantación de identidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Personas:**  

Alguien podría intentar hacerse pasar por otra persona. 

**Mitigación**

- Toda petición a SIFVA es encriptada usando el mecanismo provisto por el dispositivo PKCS11 y verificado usando el certificado digital.  Por lo tanto la autenticación de la persona es inequivoca.

* **Instituciones:**

Alguna institución enviar peticiones diciendo ser otra institución.

- Debido al doble sistema de encripción, para poder ser una institución valida se debe encriptar y desencriptar con las llaves RSA provistas, cualquier otra llave no importa si es válida para otra institución no lo será si el código de la institución es modificado.




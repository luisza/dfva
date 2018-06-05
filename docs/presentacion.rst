Descripción General
==========================

DFVA pretente ser un cliente para el firmado digital avanzado, la autenticación mediante certificados digitales y la validación de certificados y documentos.

Proporciona soporte para instituciones y personas utilizando:

* Para instituciones se utiliza una CA interna de certificados o Dogtag.
* Para personas PKCS11 para comunicarse directamente con la tarjeta de firma.

Tantos las personas como las instituciones pueden:

* Solicitar una autenticación.
* Firmar un documento XML (transacciones), ODF, MS Office, PDF.
* Validar un certificado emitido.
* Validar un documento XML, ODF, MS Office, PDF.

Clientes disponibles 
---------------------

.. warning::  Todos los clientes están en etapa de desarrollo  

Personas
~~~~~~~~~~

* **dfva_client** (https://github.com/luisza/dfva_client/) : Cliente en python para interactuar con DFVA con soporte a PKCS11 para personas.

Instituciones
~~~~~~~~~~~~~~~~~

* **dfva_java** (https://github.com/luisza/dfva_java/) : Cliente en java para interactuar con DFVA para instituciones.
* **dfva_php** (https://github.com/luisza/dfva_php/) : Cliente en php para interactuar con DFVA para instituciones.
* **dfva_python** (https://github.com/luisza/dfva_python/) : Cliente en python para interactuar con DFVA para instituciones.
* **dfva_c** * (https://github.com/luisza/dfva_c/) : Cliente en c++ para interactuar con DFVA para instituciones.
* **dfva_c#** * (https://github.com/luisza/dfva_csharp/) : Cliente en c# para interactuar con DFVA para instituciones.
* **dfva_html** (https://github.com/luisza/dfva_html/) : Cliente en javascript/html/css para captar información del usuario y mostrar los códigos provistos por dfva para instituciones.

Conexión con el BCCR (interno)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **pyfva** (https://github.com/solvo/pyfva) : Interactura con el FVA del BCCR, útil en instituciones.


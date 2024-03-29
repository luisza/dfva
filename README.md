```
Nota Este proyecto no está finalizado aún 
```
Este proyecto pretente ser un cliente para el firmado digital avanzado, la autenticación mediante certificados digitales y la validación de certificados y documentos.

Proporciona soporte para instituciones y personas utilizando:

* Para instituciones se utiliza una CA interna de certificados (PKCS11 en un futuro).
* Para personas PKCS11 para comunicarse directamente con la tarjeta de firma.

Tantos las personas como las instituciones pueden:

- Solicitar una autenticación.
- Firmar un documento xml (transacciones), ODF, MS Office, PDF.
- Validar un certificado emitido.
- Validar un documento xml, odf, Ms Office, pdf. 


Documentación
===============

Por supuesto la documentación está en [aquí](http://dfva.readthedocs.io)


Configuración de inicio
==========================

.. code:: bash

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py crea_ca
    python manage.py create_admin_institution


Ejecutar la aplicación
===============================

.. code:: bash

    python manage.py runserver
    celery worker -A dfva -l info -B



Proyectos complementarios
==============================

* [pyfva](https://github.com/solvo/pyfva) : Interactura con el FVA del BCCR, útil en instituciones.
* [dfva_client](https://github.com/luisza/dfva_client/) : Cliente en python para interactuar con DFVA con soporte a PKCS11 para personas.
* [dfva_java](https://github.com/luisza/dfva_java/) : Cliente en java para interactuar con DFVA para instituciones.
* [dfva_python](https://github.com/luisza/dfva_python/) : Cliente en python para interactuar con DFVA para instituciones.
* [dfva_c](https://github.com/luisza/dfva_c/) : Cliente en c/c++ para interactuar con DFVA para instituciones.
* [dfva_csharp](https://github.com/luisza/dfva_csharp/) : Cliente en C# para interactuar con DFVA para instituciones.
* [dfva_html](https://github.com/luisza/dfva_html/) : Cliente en javascript/html/css para captar información del usuario y mostrar los códigos provistos por dfva para instituciones.


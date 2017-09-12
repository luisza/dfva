¿Cómo Contribuir? 
===================

Entorno de desarrollo
-------------------------

Para poder desarrollar DFVA core necesita tener:

* Lector PKCS11 
* Firma digital de Costa Rica
* Simulador de FVA.
* Entorno instalado

Antes de proceder con cualquier cambio ejecute las pruebas en su entorno y asegurese que todas corran.

Testing
---------

Debe crear las siguientes variables de entorno antes de correr una prueba.

.. code:: bash

    export PKCS11_PIN=<PIN de desbloqueo de la tarjeta digital>
    export PYTHONPATH=:$PYTHONPATH:<ruta del cliente DFVA de personas>/dfva_client

Ejecute las pruebas 

.. code:: bash

    python manage.py test


.. note:: Es importante que el PIN sea correcto de lo contrario bloqueará la tarjeta y no podrá utilizarla más.

Recuerde que una contribución con pruebas será mejor aceptada y contribuye a la estabilidad del sistema.

Reportar Issues
-----------------

Utilize los issues_ de github para reportar cualquier problema encontrado en DFVA.

.. _issues: https://github.com/luisza/dfva/issues

Por favor usar la sección de issues de cada cliente si el problema es del cliente y no del core de DFVA.


Pull Request
----------------

Todos son bienvenidos utilizando la sección de `pull request`_ de github.

.. _pull request: https://github.com/luisza/dfva/pulls


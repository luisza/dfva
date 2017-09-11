Instalación
================

.. note:: Sin hacer, esto solo para quienes estén familiarizados con django y para entorno de desarrollo

Instale las dependencias

::

   pip install -r requirements.txt

Modifique el archivo dfva/settings.py según la documentación.


Ejecute la creación de la base de datos.

::

   python manage.py migrate

Corra el programa

::

  python manage.py runserver

Cree la carpeta internal_ca con el siguiente contenido.

::

  internal_ca/
  ├── ca_cert.pem
  └── ca_key.pem



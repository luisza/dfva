Como hacer un deploy completo para desarrollo de la infraestructura
========================================================================

Esta documentación es para la construcción de SIFVA y los diferentes servicios requeridos.
Se construye a partir de docker, la instalación del mismo está fuera del alcance de esta bitácora, ver
https://docs.docker.com/engine/install/debian/.

Debe tener los siguientes proyectos en una carpeta común:

- dfva
- fvabccr_simulador

Creación de las imágenes
---------------------------

Dentro de `fvabccr_simulador` ejecute:

.. code:: bash

    docker build -t dfva/fva_bccr .


Dentro de `dfva` ejecute:

.. code:: bash

    docker build -t dfva/dfva .


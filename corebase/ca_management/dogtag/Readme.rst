Dependencias
===============

Se requiere la biblioteca `dogtag-pki`, y esta a su vez depende de python-nss que tiene como dependencia `libnss3-dev` por eso ejecutar:

.. code:: bash

    apt-get install libnss3-dev
    pip install dogtag-pki


Usando docker para pruebas
=============================

Instalar una sistema PKI puede ser una ardua tarea, se requiere instalar DS389, FreeIPA y Dogtag, por eso para pruebas es recomendable utilizar la imagen 
de docker de la siguiente forma.

.. warning:: Es recomendable correrla en una máquina con más de 2Gb de RAM  

.. code:: bash 

   docker run --name freeipa-server-container -t  \
   -h  ipa.mifirmacr.org  \
   -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
   -p 53:53/udp -p 53:53 \
   -p 80:80 -p 443:443 -p 389:389 -p 636:636 -p 88:88 -p 464:464 \
   -p 88:88/udp -p 464:464/udp -p 123:123/udp -p 7389:7389 \
   -p 8443:8443-p 8080:8080 -p 9445:9445 \
   --security-opt seccomp=unconfined \
   --tmpfs /run --tmpfs /tmp \
   -v /var/lib/ipa-data:/data:Z freeipa/freeipa-server \
   --realm=mifirmacr.org \
   --ds-password=LDAPPASSWORD \
   --admin-password=ADMINPASSWORD 

Observación
========================

Se requiere que el usuario sea un agente de Dogtag, de lo contrario no se autenticará, para extraer el certificado pkcs12 del usuario admin que además es un agente 
dogtag debe buscar la llave en 

.. code:: bash

    docker exec -ti <nombre maquina> bash
    cat /data/root/ca-agent.p12 | base64 
    cat /data/root/.dogtag/pki-tomcat/ca/pkcs12_password.conf

para descomprimir y convertir a pem se recomienda algo como :

.. code:: bash

    echo "codigo base64" | base64 -d > ca-agent.p12 
    openssl pkcs12 -in ca-agent.p12 -out admin_cert.pem -nodes

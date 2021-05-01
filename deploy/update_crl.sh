#!/bin/bash

wget -O persona_juridica.crl http://fdi.sinpe.fi.cr/repositorio/CA%20SINPE%20-%20PERSONA%20JURIDICA%20v2(1).crl

wget  --ca-certificate=/certs/ca_nacional_de_CR.pem  -O ca_politica_juridica.crl https://www.firmadigital.go.cr/repositorio/CA%20POLITICA%20PERSONA%20JURIDICA%20-%20COSTA%20RICA%20v2.crl
wget  --ca-certificate=/certs/ca_nacional_de_CR.pem  -O ca_naciona.crl http://www.firmadigital.go.cr/repositorio/CA%20RAIZ%20NACIONAL%20-%20COSTA%20RICA%20v2.crl

openssl crl -in persona_juridica.crl -inform DER -out persona_juridica.pem
openssl crl -in ca_politica_juridica.crl -inform DER -out ca_politica_juridica.pem
openssl crl -in ca_naciona.crl -inform DER -out ca_nacional.pem
cat persona_juridica.pem ca_politica_juridica.pem ca_nacional.pem > ca_politica_juridica_crl.pem
if [ $? == 0 ]; then
    var_date=`date`
    echo "Convirtiendo certificado el $var_date" >> /var/log/conviert_crl.log
    mv ca_politica_juridica_crl.pem /certs/ca_politica_juridica_crl.pem
    service nginx reload
fi
rm ca_politica_juridica.crl



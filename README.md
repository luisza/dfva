```
Nota Este proyecto no está finalizado aún 
```
Este proyecto pretente ser un cliente para el firmado digital avanzado, la autenticación mediante certificados digitales y la validación de certificados y documentos.

Proporciona soporte para instituciones y personas utilizando:

* Para instituciones se utiliza una CA interna de certificados (PKCS11 en un futuro).
* Para personas PKCS11 para comunicarse directamente con la tarjeta de firma.

Tantos las personas como las instituciones pueden:

- Solicitar una autenticación.
- Firmar un documento xml (transacciones), ODF, MS Office.
- Validar un certificado emitido.
- Validar un documento xml. 


Proyectos complementarios
==============================

* [pyfva](https://github.com/solvo/pyfva) : Interactura con el FVA del BCCR, útil en instituciones.
* [dfva_client](https://github.com/luisza/dfva_client/) : Cliente en python para interactuar con DFVA con soporte a PKCS11 para personas.
* [dfva_java](https://github.com/luisza/dfva_java/) : Cliente en java para interactuar con DFVA para instituciones.


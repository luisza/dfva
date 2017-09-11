API de Comunicación
=====================

Instituciones
----------------

Autenticación
~~~~~~~~~~~~~~~

.. automethod::  authenticator.views.AuthenticateRequestViewSet.institution 
.. automethod::  authenticator.views.AuthenticateRequestViewSet.institution_show

Firma
~~~~~~~~~~~~~~~

.. automethod::  signer.views.SignRequestViewSet.institution 
.. automethod::  signer.views.SignRequestViewSet.institution_show

Validación
~~~~~~~~~~~~~~~

.. automethod::  validator.views.ValidateInstitutionViewSet.institution_certificate
.. automethod::  validator.views.ValidateInstitutionViewSet.institution_document
.. automethod::  validator.views.ValidateSubscriptorViewSet.institution_suscriptor_connected

Personas
------------


Autenticación
~~~~~~~~~~~~~~

.. automethod::  authenticator.views.AuthenticatePersonRequestViewSet.person
.. automethod::  authenticator.views.AuthenticatePersonRequestViewSet.person_show

Firma
~~~~~~~~~~~~~~~

.. automethod::  signer.views.SignPersonRequestViewSet.person
.. automethod::  signer.views.SignPersonRequestViewSet.person_show

Validación
~~~~~~~~~~~~~~~

.. automethod::  validator.views.ValidatePersonViewSet.person_certificate
.. automethod::  validator.views.ValidatePersonViewSet.person_document
.. automethod::  validator.views.ValidateSubscriptorViewSet.person_suscriptor_connected


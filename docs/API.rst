API de Comunicación
=====================

Instituciones
----------------

Autenticación
~~~~~~~~~~~~~~~

.. automethod::  institution.authenticator.views.AuthenticateRequestViewSet.institution 
.. automethod::  institution.authenticator.views.AuthenticateRequestViewSet.institution_show

Firma
~~~~~~~~~~~~~~~

.. automethod::  institution.signer.views.SignRequestViewSet.institution 
.. automethod::  institution.signer.views.SignRequestViewSet.institution_show

Validación
~~~~~~~~~~~~~~~

.. automethod::  institution.validator.views.ValidateInstitutionViewSet.institution_certificate
.. automethod::  institution.validator.views.ValidateInstitutionViewSet.institution_document
.. automethod::  institution.validator.views.ValidateSubscriptorInstitutionViewSet.institution_suscriptor_connected

Personas
------------


Autenticación
~~~~~~~~~~~~~~

.. automethod::  person.authenticator.views.AuthenticatePersonRequestViewSet.person
.. automethod::  person.authenticator.views.AuthenticatePersonRequestViewSet.person_show

Firma
~~~~~~~~~~~~~~~

.. automethod::  person.signer.views.SignPersonRequestViewSet.person
.. automethod::  person.signer.views.SignPersonRequestViewSet.person_show

Validación
~~~~~~~~~~~~~~~

.. automethod::  person.validator.views.ValidatePersonViewSet.person_certificate
.. automethod::  person.validator.views.ValidatePersonViewSet.person_document
.. automethod::  person.validator.views.ValidateSubscriptorPersonViewSet.person_suscriptor_connected

Login
~~~~~~~~

.. automethod::  person.views.PersonLoginView.create

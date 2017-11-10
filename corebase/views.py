# encoding: utf-8


'''
Created on 18/7/2017

@author: luisza
'''


# Create your views here.

from __future__ import unicode_literals

from rest_framework.settings import api_settings
from rest_framework.response import Response
from corebase.rsa import get_reponse_person_data_encrypted
from pyfva.constants import get_text_representation
import logging
from corebase.rsa import get_reponse_institution_data_encrypted
from rest_framework import status
logger = logging.getLogger('dfva')




class ViewSetBase:

    def get_encrypted_response(self, data, serializer):
        dev = {}
        if "institution" in serializer.fields:
            dev = get_reponse_institution_data_encrypted(
                data, serializer.institution,
                algorithm=serializer.data.get('algorithm', "sha512"))
        else:  # person
            dev = get_reponse_person_data_encrypted(
                data,
                serializer.person.authenticate_certificate if hasattr(
                    serializer, 'person') else None,
                algorithm=serializer.data.get('algorithm', "sha512"))

        return dev

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            logger.debug('Data create Response: %r' % (serializer.adr,))
            # adr.is_valid(raise_exception=False)
            logger.info('Response create ok %s' %
                        (serializer.data['data_hash']))

            return Response(self.get_encrypted_response(adr.data, serializer), status=status.HTTP_201_CREATED, headers=headers)
        logger.info('Response create ERROR %s' %
                    (serializer.data['data_hash'] if 'data_hash' in serializer.data else '',))
        return self.get_error_response(serializer)

    def show(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=False):
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            logger.debug('Data create Response: %r' % (serializer.adr,))
            logger.info('Response show ok %s' %
                        (serializer.data['data_hash'], ))
            # adr.is_valid(raise_exception=False)
            return Response(self.get_encrypted_response(adr.data, serializer),
                            status=status.HTTP_201_CREATED, headers=headers)

        logger.info('Response show ERROR %s' %
                    (serializer.data['data_hash'] if 'data_hash' in serializer.data else '',))
        return self.get_error_response(serializer)


    def delete(self, request, *args, **kwargs):
        dev = False
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=False):
            if hasattr(serializer.adr, "authenticaterequest"):
                serializer.adr.authenticaterequest.delete()
            if hasattr(serializer.adr, "signrequest"):
                serializer.adr.signrequest.delete()
            serializer.adr.delete()
            dev = True
        response ={'result': dev}
        headers = self.get_success_headers(response)
        return Response(self.get_encrypted_response(response, serializer),
                            status=status.HTTP_201_CREATED, headers=headers)  
            
    def get_error_response(self, serializer):
        dev = {"error_info": serializer._errors,
               'code': 'N/D',
               'status': 2,
               'status_text': get_text_representation(
                   self.DEFAULT_ERROR,  2),
               'id_transaction': 0
               }
        logger.debug('ViewSetBase Error %r' %
                     (dev, ))
        return Response(self.get_encrypted_response(dev, serializer))




class BaseSuscriptor(ViewSetBase):
    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'is_connected': serializer.save()
        }

        # adr.is_valid(raise_exception=False)
        return Response(data, status=status.HTTP_200_OK)

    def get_error_response(self, serializer):
        return Response({
            'is_connected':  False,
            'info_error': serializer._errors
        }, status=status.HTTP_200_OK)


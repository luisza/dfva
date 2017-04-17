from django.http.response import JsonResponse
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from authenticator.models import AuthenticateRequest
from authenticator.serializer import Authenticate_Request_Serializer,\
    Authenticate_Response_Serializer


# Create your views here.


class AuthenticateRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Solicita una petición de autenticación para un usuario """

    serializer_class = Authenticate_Request_Serializer
    queryset = AuthenticateRequest.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        adr = Authenticate_Response_Serializer(serializer.adr)
        # adr.is_valid(raise_exception=False)
        return Response(adr.data, status=status.HTTP_201_CREATED, headers=headers)

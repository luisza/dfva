from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from authenticator.models import Authenticate_Request
from authenticator.serializer import Authenticate_Request_Serializer,\
    Authenticate_Response_Serializer


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def authenticate(request, format=None):
    """
    post:
    Create a new user instance.


    """
    data = JSONParser().parse(request)
    serializer = Authenticate_Request_Serializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        Authenticate_Response_Serializer(instance)

    return JsonResponse(serializer.errors, status=400)


class Authenticate_Request_ViewSet(mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """Solicita una petición de autenticación para un usuario """
    serializer_class = Authenticate_Request_Serializer
    queryset = Authenticate_Request.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

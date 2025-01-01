from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.core.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@swagger_auto_schema(
    methods=['post'],
    operation_description='Realiza o logout, invalidando o token de refresh.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token de refresh')
        }
    ),
    responses={
        200: openapi.Response('Logout bem-sucedido'),
        400: openapi.Response('Erro no logout')
    }
)
@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'detail': 'Logout bem-sucedido.'}, status=200)
    except Exception as e:
        return Response({'detail': 'Erro no logout: ' + str(e)}, status=400)

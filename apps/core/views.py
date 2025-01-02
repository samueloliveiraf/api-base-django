from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.core.serializers import CustomTokenObtainPairSerializer

from django.core.mail import send_mail
from rest_framework import status
from django.conf import settings


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


@swagger_auto_schema(
    methods=['post'],
    operation_description="Envie um e-mail de recuperação de senha "
                          "se o e-mail fornecido estiver associado a um usuário.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do usuário'),
        },
        required=['email']
    ),
    responses={
        200: openapi.Response(
            description="E-mail enviado com sucesso.",
        ),
        400: openapi.Response(
            description="Requisição inválida.",
        ),
        404: openapi.Response(
            description="Usuário não encontrado.",
        ),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_view(request):
    email = request.data.get('email')
    if not email:
        return Response({'detail': 'O e-mail é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({'detail': 'Nenhum usuário encontrado com este e-mail.'}, status=status.HTTP_404_NOT_FOUND)

    uidb64 = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
    token = default_token_generator.make_token(user)

    reset_link = f'{request.build_absolute_uri("/reset/")}{uidb64}/{token}/'

    send_mail(
        subject='Solicitação de redefinição de senha',
        message=f'Use o link a seguir para redefinir sua senha: {reset_link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {'detail': 'E-mail de redefinição de senha enviado com sucesso.'},
        status=status.HTTP_200_OK
    )
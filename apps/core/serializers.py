from datetime import timedelta

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth.signals import user_logged_in
from apps.core.models import LoginRecord, LoginAttempt
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from django.utils.timezone import now


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if not user:
            raise AuthenticationFailed('Credenciais inválidas.')

        login_attempt, created = LoginAttempt.objects.get_or_create(user=user)
        if login_attempt.blocked_until and login_attempt.blocked_until > now():
            time_left = (login_attempt.blocked_until - now()).seconds // 60
            raise AuthenticationFailed(f'A conta está bloqueada. Tente novamente em {time_left} minutos.')

        authenticated_user = authenticate(username=username, password=password)
        if not authenticated_user:
            login_attempt.attempts += 1
            login_attempt.last_attempt = now()

            if login_attempt.attempts == 2:
                login_attempt.save()
                raise AuthenticationFailed(
                    'Você errou a senha duas vezes. Se errar novamente, '
                    'sua conta será bloqueada por 5 minutos.'
                )

            if login_attempt.attempts >= 3:
                login_attempt.blocked_until = now() + timedelta(minutes=5)
                login_attempt.attempts = 0
                login_attempt.save()
                raise AuthenticationFailed(
                    'A conta está bloqueada devido a muitas tentativas malsucedidas. '
                    'Tente novamente em 5 minutos.')

            login_attempt.save()
            raise AuthenticationFailed('Credenciais inválidas.')

        login_attempt.attempts = 0
        login_attempt.blocked_until = None
        login_attempt.save()

        data = super().validate(attrs)
        user = self.user

        request = self.context.get('request')
        if request:
            user_logged_in.send(sender=user.__class__, request=request, user=user)

        access_token = data.get('access')
        refresh_token = data.get('refresh')

        ip = get_client_ip(request)

        LoginRecord.objects.create(
            user=user,
            ip_address=ip,
            access_token=access_token,
            refresh_token=refresh_token
        )

        return data


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductsSerializer
from .models import Product


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.filter(user=user)
        else:
            return JsonResponse({'detail': 'Usuário não autenticado'}, status=401)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

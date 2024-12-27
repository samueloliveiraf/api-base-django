from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from apps.products.views import ProductsViewSet

router_v1 = DefaultRouter()
router_v1.register(r'products', ProductsViewSet, basename='products-v1')

schema_view = get_schema_view(
    openapi.Info(
        title='API de Itens',
        default_version='v1',
        description='Documentação da API de itens',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contato@exemplo.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('v1/', include(router_v1.urls)),
]

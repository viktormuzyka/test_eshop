from django.urls import path
from store.api import auth_api, product_api, order_api
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from django.urls import path, include


# Define Swagger schema view for automatic documentation
schema_view = get_schema_view(
   openapi.Info(
      title="My Store API",
      default_version='v1',
      description="API documentation for the e-commerce store.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@mystore.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('api/', include('store.api.urls')),
    # Swagger UI - add this path to view your API documentation
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

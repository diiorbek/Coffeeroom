from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/',include('Coffeeroom.urls')),
    path('api/account/', include('account.urls')),
    path('api/order/', include('Order.urls')),

    # Schema generatsiyasi
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    
    # Swagger UI
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    
    # Redoc UI
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
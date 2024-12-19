from django.contrib import admin
from django.urls import path, include
from accounts.views import create_paypal_order, execute_payment  # Import views from accounts app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Include the accounts app URLs
    path('create_paypal_order/', create_paypal_order, name='create_paypal_order'),
    path('execute/', execute_payment, name='execute_payment'),
]

# Serve media files during development (only needed in development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


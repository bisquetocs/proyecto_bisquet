
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('provider/', include('provider.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
]

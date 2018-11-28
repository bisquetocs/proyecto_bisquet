
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('provider/', include('provider.urls')),
    path('franchise/', include('franchise.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.views.generic import TemplateView
urlpatterns += [
    path('', TemplateView.as_view(template_name='index.html'), name='frontend'),
]

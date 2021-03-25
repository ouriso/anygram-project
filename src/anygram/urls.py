from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

handler404 = "anygram.views.page_not_found" # noqa
handler500 = "anygram.views.server_error" # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
    path('api/v1/', include('api.urls')),
    path('cart/', include('cart.urls')),
    path('about/author/', TemplateView.as_view(
        template_name='about/author.html'
    ), name='about_author'),
    path('about/tech/', TemplateView.as_view(
        template_name='about/technologies.html'
    ), name='about_tech'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

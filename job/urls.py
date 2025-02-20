"""job URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.static import serve

def test_email(request):
    try:
        send_mail(
            'Test Subject',
            'Test Message',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Email failed: {str(e)}')

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobapp.urls')),
    path('', include('account.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('project_app.urls')),
    path('test-email/', test_email, name='test-email'),
    path('health/', health_check, name='health_check'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

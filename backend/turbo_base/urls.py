from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from rest_framework_simplejwt.views import TokenVerifyView


@api_view(['GET'])
def api_root(request):
    return Response({
        'description': 'Turbo Note Taker API',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
            },
            'categories': '/api/categories/',
            'notes': '/api/notes/',
        }
    })


schema_view = get_schema_view(
    title='Turbo Note Taker API',
    renderer_classes=[JSONRenderer, BrowsableAPIRenderer],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('note_taker.urls')),
    path('api/schema/', schema_view, name='api_schema'),
]

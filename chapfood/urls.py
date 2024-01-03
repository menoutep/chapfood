"""
URL configuration for chapfood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from notifications.consumers import NotificationType1Consumer,NotificationType2Consumer,NotificationType3Consumer,NotificationType4Consumer,CartUpdateConsumer
urlpatterns = [
    path("", include("base.urls")),
    path("accounts/", include("accounts.urls")),
    path("livreurs/", include("livreurs.urls")),
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    
]

websocket_urlpatterns = [
    path("ws/notification_type1/", NotificationType1Consumer.as_asgi()),
    path("ws/notification_type2/", NotificationType2Consumer.as_asgi()),
    path("ws/notification_type3/", NotificationType3Consumer.as_asgi()),
    path("ws/notification_type4/", NotificationType4Consumer.as_asgi()),
    path("ws/cart_item_count/", CartUpdateConsumer.as_asgi()),
 

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
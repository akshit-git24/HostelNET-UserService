from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from accounts.api import app as uni_router
from django.conf import settings
from django.conf.urls.static import static
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from accounts.controllers import CustomNinjaJWTController

api = NinjaExtraAPI(title="HostelNet Auth API")
api.register_controllers(CustomNinjaJWTController)

api.add_router("auth", uni_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from accounts.controllers import CustomNinjaJWTController

# -----------------------------
# SINGLE ROOT API
# -----------------------------
api = NinjaExtraAPI(
    title="HostelNet Auth API",
    version="1.0.0",
)

# JWT + custom auth controllers
api.register_controllers(
    NinjaJWTDefaultController,
    CustomNinjaJWTController,
)

# -----------------------------
# Django URLs
# -----------------------------
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from authentication.views import UserCreation

router = SimpleRouter()
router.register('', UserCreation, basename='signup')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', include(router.urls)),
    ]
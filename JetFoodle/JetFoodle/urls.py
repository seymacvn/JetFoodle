from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from system import views


urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('system/', include("system.urls")),
    path('user/', include("user.urls")),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

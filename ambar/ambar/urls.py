from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ambarapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('iletisim/', views.contact, name='contact'),
    path('hizmetler/<slug:slug>/', views.service_detail, name='service_detail'),
    path('guzergahlar/<slug:slug>/', views.route_detail, name='route_detail'),
    path('hakkimizda/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

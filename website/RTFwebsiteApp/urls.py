from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html', views.main_page, name='main_page'),
    path('reference-info.html', views.information, name='information'),
    path('acticles.html', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('employment.html/', views.employment, name='employment'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""Router: /app"""
from django.urls import re_path
from django.conf import settings				###upload
from django.conf.urls.static import static		###upload

from . import views


urlpatterns = [
    re_path(r'^$', views.frontpage, name='index'),
    re_path(r'^settings/$', views.settings),
    re_path(r'^add_category$', views.add_category),
    re_path(r'^delete_category/(?P<category>\w+)',views.delete_category),

    re_path(r'^add_record$', views.add_record),
    re_path(r'^delete_record$', views.delete_record),

    re_path(r'^upload/', views.upload, name='upload'), ###upload
]

###upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import include, re_path
from . import views

from django.conf import settings				###upload
from django.conf.urls.static import static		###upload


urlpatterns = [
    re_path(r'^$', views.frontpage, name='index'),
    re_path(r'^settings/$', views.settings),
    re_path(r'^add_category$', views.addCategory),
    re_path(r'^delete_category/(?P<category>\w+)',views.deleteCategory),

    re_path(r'^add_record$', views.addRecord),
    re_path(r'^delete_record$', views.deleteRecord),

    re_path(r'^upload/', views.upload, name='upload'), ###upload
]

###upload
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

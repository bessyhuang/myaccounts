from django.conf.urls import url
from . import views

from django.conf import settings				###upload
from django.conf.urls.static import static		###upload


urlpatterns = [
    url(r'^$', views.frontpage),
    url(r'^settings/$', views.settings),
    url(r'^add_category$', views.addCategory),
    url(r'^delete_category/(?P<category>\w+)',views.deleteCategory),

    url(r'^add_record$', views.addRecord),
    url(r'^delete_record$', views.deleteRecord),

    url(r'^upload/', views.upload, name='upload'), ###upload
]

###upload
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url, include
from apps.therapy import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'therapy'

urlpatterns = [
    url(r'^inicio/$', views.therapy_request, name='home'),
    url(r'^(?P<pk>[0-9]+)/$', views.session_detail, name='therapy-detail'),
    url(r'^crear/$', views.session_create, name='therapy-create'),
    url(r'^(?P<pk>[0-9]+)/editar/$', views.session_update, name='therapy-edit'),
    url(r'^(?P<pk>[0-9]+)/eliminar/$', views.session_delete, name='therapy-delete'),
    url(r'^$', views.log_in, name='log-in'),
    url(r'^log-out/$', views.log_out, name='log-out'),
    url(r'^terapias/$', views.therapy_request, name='therapy-request'),
    url(r'^seguimiento/(?P<pk>\d+)/$', views.therapy_followup, name='therapy-followup'),
    url(r'^perfil/(?P<pk>[0-9]+)/editar/$', views.profile_edit, name='profile-edit'),
    url(r'^comunidad/$', views.therapy_forums, name='therapy-forums'),
    url(r'^comunidad/(?P<pk>[0-9]+)/$', views.thread_detail_view, name='thread-detail'),
    url(r'^comunidad/crear/$', views.thread_create, name='thread-create'),
    url(r'^comunidad/(?P<pk>[0-9]+)/responder/$', views.thread_reply, name='thread-reply'),
    url(r'^comunidad/(?P<pk>[0-9]+)/editar/$', views.thread_update, name='thread-edit'),
    url(r'^comunidad/(?P<pk>[0-9]+)/eliminar/$', views.thread_delete, name='thread-delete'),
    url(r'^recursos/$', views.therapy_resources, name='therapy-resources'),
    url(r'^recursos/crear/$', views.resource_create, name='resource-create'),
    url(r'^recursos/(?P<pk>[0-9]+)/editar/$', views.resource_edit, name='resource-edit'),
    url(r'^recursos/(?P<pk>[0-9]+)/eliminar/$', views.resource_delete, name='resource-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
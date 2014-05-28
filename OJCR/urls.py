from django.conf.urls import patterns, include, url
from OJCR import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.login_register, name='login_register'),
    url(r'^login/$', views.login_register, name='login_register'),
    url(r'^logout/$', views.do_logout, name='do_logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^add/$', views.add_class, name='add_class'),
    url(r'^remove/(\d{1,5})/$', views.remove_class,name='remove_class'),
    url(r'^edit/(\d{1,5})/$', views.edit_class,name='edit_class'),
    url(r'^download/(\d{1,5})/$', views.download_class,name='download_class'),
)

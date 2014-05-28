from django.conf.urls import patterns, include, url
from OJCR import urls

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^demo/', include('OJCR.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from trip_constructor.views import login, register, get_visa_constructor, profile, logout #, get_requirements
import settings


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # custom urls
    # url(r'^requirements/$', get_requirements, name=get_requirements),
    url(r'^register/$', register, name="register"),
    url(r'^constructor/$', get_visa_constructor, name="get_visa_constructor"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^logout/$', logout, name="logout"),
    # the root url must be the last
    url(r'^$', login, name="login"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
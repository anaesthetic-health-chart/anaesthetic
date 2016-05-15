from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from opal.urls import urlpatterns as opatterns
from anaesthetic.api import ListOfDrugs

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anaesthetic/drugs_list/', ListOfDrugs.as_view({'get': 'list'})),
)

urlpatterns += opatterns

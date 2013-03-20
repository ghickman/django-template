from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    # Used to serve specific static media such as tiny_mce
    url(r'^direct-static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATICFILES_DIR,
    }),
)

urlpatterns += staticfiles_urlpatterns()

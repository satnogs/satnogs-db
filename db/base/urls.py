from django.conf.urls import patterns, url

urlpatterns = patterns(
    'db.base.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', 'about', name='about'),
    url(r'^faq/$', 'faq', name='faq'),
    url(r'^satellite/(?P<norad>[0-9]+)/$', 'satellite', name='satellite'),
    url(r'^suggestion/$', 'suggestion', name='suggestion'),
    url(r'^robots\.txt$', 'robots', name='robots'),
)

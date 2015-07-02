from django.conf.urls import patterns, url

urlpatterns = patterns(
    'db.base.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', 'about', name='about'),
    url(r'^faq/$', 'faq', name='faq'),
    url(r'^suggestion/$', 'suggestion', name='suggestion'),
)

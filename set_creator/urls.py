from django.conf.urls import patterns, url


urlpatterns = patterns('set_creator.views',
    url(r'^$', "test", name='home'),
)

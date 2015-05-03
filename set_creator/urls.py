from django.conf.urls import patterns, url


urlpatterns = patterns('set_creator.views',
    url(r'^$', "set_list", name='set_list'),
    url(r'^new$', "set_new", name='set_new'),
    url(r'^(?P<pk>\d+)$', "set_detail", name='set'),
    url(r'^term/(?P<pk>\d+)$', "term_detail", name='set_term'),
    url(r'^add_term/(?P<pk>\d+)$', "add_term", name='set_add_term'),
    url(r'^add_terms/(?P<pk>\d+)$', "add_terms", name='set_add_terms'),
    url(r'^remove_term/(?P<set_pk>\d+)/(?P<term_pk>\d+)$', "remove_term", name='set_remove_term'),
)

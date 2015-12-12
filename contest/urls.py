from django.conf.urls import patterns, url

urlpatterns = patterns('contest.views',
     url(r'^make_guess$', "make_guess"),
     url(r'^data', "get_data"),
)

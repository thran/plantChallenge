from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from lazysignup.decorators import allow_lazy_user


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/', include('proso_user.urls')),
    url(r'^models/', include('proso_models.urls')),
    url(r'^ab/', include('proso_ab.urls')),
    url(r'^common/', include('proso_common.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^convert/', include('lazysignup.urls')),
    # url(r'^feedback/', include('proso_feedback.urls')),
    url(r'^flashcards/', include('proso_flashcards.urls')),
    url(r'', include('social_auth.urls')),

    url(r'^typehead', "practice.views.typehead"),
    url(r'^.*$', allow_lazy_user(TemplateView.as_view(template_name="index.html")), name='home'),
)

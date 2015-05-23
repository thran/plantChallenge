from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from plantchallenge import settings

admin.autodiscover()
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
patterns('',
    url(r'^user/', include('proso_user.urls')),
    url(r'^models/', include('proso_models.urls')),
    url(r'^ab/', include('proso_ab.urls')),
    url(r'^common/', include('proso_common.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^convert/', include('lazysignup.urls')),
    # url(r'^feedback/', include('proso_feedback.urls')),
    url(r'^flashcards/', include('proso_flashcards.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^sets/', include('set_creator.urls')),

    url(r'^typehead$', "practice.views.typehead"),
    url(r'^typehead-all$', "practice.views.typehead", {"exclude_short": False}),
    url(r'^.*$', "practice.views.home", name='home'),
)

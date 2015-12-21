from django.conf.urls import include, url
from django.contrib import admin
from app.views import index, rest_get, rest_post, view, create, signup, signin, signout

urlpatterns = [

    # Basic views

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', index),
    url(r'^$', index),
    url(r'^view/(.*)', view),
    url(r'^create/$', create),

    # REST APIs

    url(r'^rest/get/(.*)/$', rest_get),
    url(r'^rest/post/(.*)/$', rest_post),

    # User sign up / sign in / sign out

    url(r'^signup/$', signup),
    url(r'^signin/$', signin),
    url(r'^signout/$', signout),

]

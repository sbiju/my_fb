from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_detail,
    post_update,
    post_delete,
    post_share,
    post_shared_list,
    NewBlogPostView,
    post_list_all,
    contact_us,

    )

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^shared/$', post_shared_list, name='shared_list'),
    url(r'^all/$', post_list_all, name='all_list'),
    url(r'^contact/$', contact_us, name='contact_us'),
    url(r'^create/$', NewBlogPostView.as_view(), name='create',),

    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/share/$', post_share, name='share'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),

]





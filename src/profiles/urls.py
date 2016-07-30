from django.conf.urls import url
from .views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)


urlpatterns = [

    url(r'^$', UserListView.as_view(), name="user_list"),
    url(r'^(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^add/$', UserCreateView.as_view(), name="user_create"),
    url(r'^(?P<pk>\d+)/delete/$', UserDeleteView.as_view(), name='user_delete'),
    url(r'^(?P<pk>\d+)/edit/$', UserUpdateView.as_view(), name='user_update'),
]
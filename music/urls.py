from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),

    # registration from
    url(r'^register/$', views.UserFromView.as_view(), name="register"),

    # in form of music/545/ or other
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),

    # type of music/45/favourite
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name="favorite"),

    # add form url music/album/add/
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),

    # update form url music/album/2(id)/
    url(r'album/(?P<pk>[0-9]+)/update/$', views.AlbumUpdate.as_view(),name='album-update'),

    # update form url music/album/2(id)/
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),

    # add songs
    url(r'song/add', views.AddSong.as_view(), name='add-song'),

    # delete songs
    url(r'^songs/(?P<pk>[0-9]+)/delete/', views.DeleteSong.as_view(), name='delete-song'),

    # all songs
    url(r'^songs/$', views.allsongs, name='all-songs'),



    url(r'^runcode/$', views.runCode, name="run-code"),
    # url(r'^runcode/response/$', views.codeResponse, name="run-code-text"),

]
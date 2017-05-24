# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import Http404
from django.views import generic
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
# for registriation
from django.contrib.auth import authenticate, login
from .regForm import UserForm
from django.views.generic import View

# for compiler
from subprocess import Popen, PIPE
import time


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class AddSong(CreateView):
    model = Song
    fields = ['song', 'file_type', 'song_title', 'is_favorite']


class DeleteSong(DeleteView):
    model = Song
    success_url = reverse_lazy('music:all-songs')


def allsongs(request):
    all_songs = Song.objects.all()
    context = {
        'all_songs': all_songs,
    }
    return render(request, 'music/songs.html', context)


class UserFromView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # if user send GET request ie. open this url
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # if user send POST request after filling this form
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalize) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # authenticate will return object of credentials if it is correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:  # check  whether user is active ie not banned by admin
                    login(request, user)
                    context = {
                        'querySet': username,
                    }
                    return render(request, 'music/index.html', context)
                    # return redirect('music:index')
        # if both are wrong then send back to login page
        return render(request, self.template_name, {'form': form})

















# def index(request):
#     all_albums = Album.objects.all()
#     # template = loader.get_template('music/index.html')
#     context = {
#         'all_albums': all_albums,
#     }
#     return render(request, 'music/index.html', context)
#
#
# def detail(request, album_id):
#     # try:
#     #     album = Album.objects.get(pk=album_id)
#     # except album.DoesNotExist:
#     #     raise Http404("Album does not found!")
#     album = get_object_or_404(Album, id=album_id)
#     return render(request, 'music/detail.html', {'album': album})


def favorite(request,album_id):
    album = get_object_or_404(Album, id=album_id)
    try:
        selected_song = album.song_set.get(id=request.POST['song'])
    except (KeyError, Song.DoesnotExist):
        return render(request,'music/detail.html', {
            'album': album,
            'error_message': "You don't select a valid song!",
        })
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})


def runCode(request):

    filename = "123.cpp"
    pipe = Popen('g++ ' + filename, shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)
    p1 = pipe.communicate()

    if p1[1]:
        return HttpResponse(p1[1])

    pipe = Popen('time ./a.out ;echo Process returned $?', shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)

    start = time.time()

    for i in range(1000000):
        val = str(i) + '\n'
        pipe.stdin.write(val)
        pipe.stdin.flush()
        # res = pipe.stdout.readline().strip()
        # print res
        if time.time() - start > 5:
            print "tle"
            break

    r = pipe.communicate()

    context = {
        'answer': str(r[0]),
        'time': str(r),
        'total_time': str(time.time() - start),
    }

    return render(request, 'music/python.html', context)
#
# def codeResponse(request):
#
#
#     return HttpResponse('<p>'+str(text)+'</p>')

# def detail(request, album_id):
#     return HttpResponse("<h1> details of album: " + str(album_id) + "</h1>")

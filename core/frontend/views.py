# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil

from django.shortcuts import render
from frontend.forms import DocumentForm
from frontend.models import UserProfile, t_test, t_history, t_schedule, t_schedsettings, t_group, t_group_test
from frontend.models import temp_main, temp_case, temp_keywords, temp_library, temp_variables, temp_pers_keywords, \
    temp_test_keywords, t_threads, t_tags, t_tags_route
from rest_framework import viewsets
from frontend.serializers import t_testSerializer, temp_mainSerializer, UserSerializer, temp_caseSerializer, temp_keywordsSerializer, \
    temp_variablesSerializer, temp_pers_keywordsSerializer, temp_test_keywordsSerializer, temp_librarySerializer, t_scheduleSerializer, \
    t_groupSerializer, t_group_testSerializer, t_historySerializer,t_threadsSerializer, t_tagsSerializer, t_tags_routeSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from frontend.permissions import IsOwnerOrReadOnly

from tenant_schemas.utils import (get_tenant_model, remove_www,
                                  get_public_schema_name)


test_main = temp_main.objects.all()
test_case = temp_case.objects.all()
test_var = temp_variables.objects.all()
test_lib = temp_library.objects.all()


@login_required
def index(request, **kwargs):
    global test_main
    uGroup = request.user.groups.all()
    # menu_list = kwargs['menu']
    context = RequestContext(request)
    
    schema_name = request.META.get('HTTP_X_DTS_SCHEMA', get_public_schema_name())
  
    test_sched = t_schedsettings.objects.all()

    context_dict = {'all_test': test_main, 't_sched': test_sched, 'uGroup': uGroup}
    response = render(request, 'base_home.html', context_dict, context)

    return response


@login_required
# Viev for history threads list
def h_list(request, **kwargs):
    global test_main
    uGroup = request.user.groups.all()
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_test': test_main, 'uGroup': uGroup}
    response = render(request, 'base_history.html', context_dict, context)

    return response


@login_required
def temp_main(request, **kwargs):
    global test_main
    uGroup = request.user.groups.all()
    # Back home if no Teatadmin group for that user
    if not 1 in [i.id for i in uGroup]: return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_test': test_main, 'uGroup': uGroup}
    response = render(request, 'base_tmain.html', context_dict, context)

    return response


@login_required
def temp_case(request, **kwargs):
    global test_case
    uGroup = request.user.groups.all()
    # Back home if no Teatadmin group for that user
    if not 1 in [i.id for i in uGroup]: return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case, 'uGroup': uGroup}
    response = render(request, 'base_tcase.html', context_dict, context)

    return response


@login_required
def temp_group(request, **kwargs):
    global test_case
    uGroup = request.user.groups.all()
    # Back home if no Teatadmin group for that user
    if not 1 in [i.id for i in uGroup]:return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case, 'uGroup': uGroup}
    response = render(request, 'base_tgroup.html', context_dict, context)

    return response


@login_required
def temp_var(request, **kwargs):
    global test_var
    uGroup = request.user.groups.all()
    # Back home if no Teatadmin group for that user
    if not 1 in [i.id for i in uGroup]: return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_var': test_var, 'uGroup': uGroup}
    response = render(request, 'base_tvar.html', context_dict, context)

    return response


@login_required
def temp_lib(request, **kwargs):
    global test_lib
    uGroup = request.user.groups.all()
    # Back home if no Teatadmin group for that user
    if not 1 in [i.id for i in uGroup]: return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_lib': test_lib, 'uGroup': uGroup}
    response = render(request, 'base_tlib.html', context_dict, context)

    return response


@login_required
def temp_lib(request, **kwargs):
    global test_case
    ugroup = request.user.groups.all()
    # Back home if no Teatadmin group for that user
    if not 1 in [i.id for i in ugroup]: return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case, 'ugroup': ugroup}
    response = render(request, 'base_tcase.html', context_dict, context)

    return response


@login_required
def f_upload(request, **kwargs):
    current_user = request.user
    err_msg = ""
    global test_case
    uGroup = request.user.groups.all()
    if request.method == 'POST':
        if request.POST['dfolder']:
            try:
                dest_dir = 'media/documents/'+os.path.basename(request.POST['dfolder'])
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                copytree(str(request.POST['dfolder']),dest_dir)
            except Exception as e:
                err_msg = e.args
                print(e.args)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            docload = form.save()
            docload.owner = current_user.id
            docload.dmessage = err_msg
            docload.save()
            return HttpResponseRedirect('/files/')
    else:
        form = DocumentForm()
    response = render(request, 'base_files.html', {
        'form': form, 'uGroup': uGroup
    })
    return response


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
        for root, subdirs, files in os.walk(d):
            for filename in files:
                print("To->",os.path.join(root, filename))


def login_register(request, **kwargs):
    context = RequestContext(request)
    # menu_list = kwargs['menu']
    registered = False
    if request.method == 'POST':
        # Grab information from the RAW form
        user_form = UserForm(data=request.POST)
        user_profile = UserProfile(data=request.POST)
        if user_form.is_valid() and user_profile.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = user_profile.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, user_profile.errors)
    else:
        user_form = UserForm()
        user_profile = UserProfile()

    return render(request, 'login.html',
                  {'user_form': user_form, 'user_profile': user_profile, 'registered': registered}, context)


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("User not active")
        else:
            return HttpResponse('Your user dont exist')
    else:
        return render(request, 'login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    return response


#API Viewset Class

class t_testViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = t_test.objects.all()
    serializer_class = t_testSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_mainViewSet(viewsets.ModelViewSet):

    queryset = test_main
    serializer_class = temp_mainSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_caseViewSet(viewsets.ModelViewSet):

    queryset = test_case
    serializer_class = temp_caseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_keywordsViewSet(viewsets.ModelViewSet):

    queryset = temp_keywords.objects.all()
    serializer_class = temp_keywordsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_variablesViewSet(viewsets.ModelViewSet):

    queryset = test_var
    serializer_class = temp_variablesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_pers_keywordsViewSet(viewsets.ModelViewSet):

    queryset = temp_pers_keywords.objects.all()
    serializer_class = temp_pers_keywordsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_test_keywordsViewSet(viewsets.ModelViewSet):

    queryset = temp_test_keywords.objects.all()
    serializer_class = temp_test_keywordsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class temp_libraryViewSet(viewsets.ModelViewSet):

    queryset = test_lib
    serializer_class = temp_librarySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_scheduleViewSet(viewsets.ModelViewSet):

    queryset = t_schedule.objects.all()
    serializer_class = t_scheduleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_groupViewSet(viewsets.ModelViewSet):

    queryset = t_group.objects.all()
    serializer_class = t_group_testSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_group_testViewSet(viewsets.ModelViewSet):

    queryset = t_group_test.objects.all()
    serializer_class = t_group_testSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_historyViewSet(viewsets.ModelViewSet):

    queryset = t_history.objects.all()
    serializer_class = t_historySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_threadsViewSet(viewsets.ModelViewSet):

    queryset = t_threads.objects.all()
    serializer_class = t_threadsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_tagsViewSet(viewsets.ModelViewSet):

    queryset = t_tags.objects.all()
    serializer_class = t_tagsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class t_tags_routeViewSet(viewsets.ModelViewSet):

    queryset = t_tags_route.objects.all()
    serializer_class = t_tags_routeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
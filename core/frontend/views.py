# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import stripe

from django.shortcuts import render
from frontend.forms import DocumentForm
import simplejson
from selenium import webdriver
from frontend.models import UserProfile, t_test, t_history, t_schedule, t_schedsettings, t_group, t_group_test
from frontend.models import temp_main, temp_case, temp_keywords, temp_library, temp_variables, temp_pers_keywords, \
    temp_test_keywords, t_threads, t_tags, t_tags_route, settings_gen, jra_settings, jra_history
from rest_framework import viewsets
from frontend.serializers import t_testSerializer, temp_mainSerializer, UserSerializer, temp_caseSerializer, temp_keywordsSerializer, \
    temp_variablesSerializer, temp_pers_keywordsSerializer, temp_test_keywordsSerializer, temp_librarySerializer, t_scheduleSerializer, \
    t_groupSerializer, t_group_testSerializer, t_historySerializer,t_threadsSerializer, t_tagsSerializer, t_tags_routeSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from frontend.permissions import IsOwnerOrReadOnly

from jira import JIRA

import boto3
import json
import hashlib

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
     
    test_sched = t_schedsettings.objects.all()

    context_dict = {'all_test': test_main, 't_sched': test_sched, 'uGroup': uGroup}
    response = render(request, 'base_home.html', context_dict, context)

    return response


@login_required
@csrf_exempt
# Viev for history threads list
def h_list(request, **kwargs):
    global test_main
    uCookie = request.COOKIES.get('demoF', '')
    
    if request.is_ajax():
        schema_name = settings_gen.objects.get(id=1).tenant_name
        j_file = "frontend/static/out/"+request.POST['tpid']+"/log.html"
        #Connection first get user and pass from tab
        jadd = ""
        juser = ""
        jpass = ""

        jFile = False
        response = []
        
        errarg = ""
        connData = jra_settings.objects.all()
        for i in connData:
            jadd = i.j_address.strip()
            juser = i.j_user.strip()
            jpass = i.j_pass.strip()
        
        try:
            options = {'server': jadd}
            jira = JIRA(options, basic_auth=(juser, jpass))
            #if auth ok continue
            # Get the issue.
            try:
                issue = jira.issue(request.POST['jissue'])
                #If issue is ok add element:
                # Add a comment to the issue.
                if request.POST['jcom']:
                    jira.add_comment(issue, request.POST['jcom'])

                #add log file
                if str(request.POST['jfile'].strip()) == 'true':
                    try:
                        jira.add_attachment(issue,j_file)
                        jFile = True
                    except Exception as ef:
                        errarg = ef.args

            except Exception as ei:
                errarg = ei.args

        except Exception as e:
            errarg = e.args

        #check if error is nauthorized Access, too long for be displayed, i trunk it
        strerr = 'Unauthorized'
        if strerr in str(errarg): errarg = "(401, 'Unauthorized (401), Check Jira settings connection data.')"
        
        #Now if all is ok add new line to the table
        jra_ev = jra_history(j_tid=request.POST['tid'], j_issue=request.POST['jissue'], j_comment=request.POST['jcom'], j_file=jFile, dt=str(datetime.now()), j_error=errarg)
        jra_ev.save()
        
        #Query for have already inserted jira records
        
        
        vallabel = {}
        vallabel['csrfmiddlewaretoken'] = request.POST['csrfmiddlewaretoken']
        vallabel['j_err'] = errarg
        response.append(vallabel)
        json = simplejson.dumps(response)
        return HttpResponse(json, content_type='application/json')

    else:
        pass
    
    #EXTRA AJAX, NORMAL BEHAVIOUR
    #First check if is first time with no threads, if is new, home redirect to active else continue

    a = t_threads.objects.all()[:1]
    if not a : return HttpResponseRedirect('/active')

    uGroup = request.user.groups.all()
    # menu_list = kwargs['menu']
    context = RequestContext(request)
    print("Il tuo cookie e: ",uCookie)
    context_dict = {'all_test': test_main, 'uGroup': uGroup, 'uCookie':uCookie}
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
    #if not 1 in [i.id for i in uGroup]:return HttpResponseRedirect('/')
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
def ext_lib(request, **kwargs):
    global test_case

    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case}
    response = render(request, 'base_extlib.html', context_dict, context)

    return response

    
def legal_terms(request, **kwargs):
    global test_case

    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case}
    response = render(request, 'base_legal.html', context_dict, context)

    return response
    
    
def lic_register(request, reg_status=None, **kwargs):
    global test_case
    
    #Retreive stripe API keys
    stripe.api_key = getattr(settings, "STRIPE_KEY", None)
    sg = settings_gen.objects.all()
    """
    #First check if pay tupe field is blank, oterwise redirect to home
    c_plan = None
    c_tenant = None
    sg = settings_gen.objects.all()
    for i in sg:
        c_plan=i.paid_plan
        c_tenant = i.tenant_name
        c_email = i.reg_email

    if not c_plan:
    """
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case, 'all_set': sg}
    if request.method == 'POST':

        #First create customer on stripe and get id (ito insert into table)
        hash_object = hashlib.md5(bytes(request.POST['taxid'], 'utf-8'))
        try:
            #First create the token
            token = stripe.Token.create(
                card={
                    'number':str(request.POST['gatewayCardNumber']).strip(),
                    'exp_month':request.POST['expiryDateMonth'],
                    'exp_year':request.POST['expiryDateYear'],
                    'name': request.POST['ccName'],
                    'cvc':request.POST['cardCVC'],
                    'address_city': request.POST['city'],
                    'address_state': request.POST['state'],
                    'address_line1': request.POST['address1'],
                    'address_line2': request.POST['address2'],
                    'address_zip': request.POST['postcode']
                },
            )

            cus = stripe.Customer.create(
                description="Customer for "+request.POST['organisationname'],
                email=request.POST['c_email'],
                source=token.id,
                tax_info={
                        'tax_id':request.POST['taxid'],
                        'type':'vat'
                    }
            )

            #NOW IF IS FLAT THE CHOISE I HAVE TO CREATE AN ACTIVE MONTLY SUBSCRIPTION FOR E149
            if request.POST['plan_type'].strip() == 'flat':

                """
                s_plan = stripe.Plan.create(
                    amount=149,
                    interval="month",
                    product={
                        "name": "Aida FLAT"
                    },
                    currency="eur",
                )
                """
                s_plan = getattr(settings, "PROD149_KEY", None)
                stripe.Subscription.create(
                    customer=cus['id'],
                    tax_percent=22.0,
                    items=[
                        {
                            "plan": s_plan,
                        },
                    ]
                )
            
            #Then update table with informations
            """
            t = settings_gen.objects.get(tenant_name=c_tenant)
            t.on_trial = 'False'
            t.stripe_id = cus['id']
            t.first_name = request.POST['firstname']
            t.last_name = request.POST['lastname']
            t.comp_name = request.POST['organisationname']
            t.addr_1 = request.POST['address1']
            t.addr_2 = request.POST['address2']
            t.city = request.POST['city']
            t.state_prov = request.POST['state']
            t.postal_zip = request.POST['postcode']
            t.country = request.POST['country']
            t.tax_id = request.POST['taxid']
            t.paid_plan = request.POST['plan_type']
            t.save()
            """
        except Exception as e:
            print('e->',e)
               
       #If all done redirect to homepage and send thanks email
        return HttpResponseRedirect('/register')
    else:
        response = render(request, 'base_register.html', context_dict, context)

        return response
    #else:
        #return HttpResponseRedirect('/')


@login_required
def sys_usage(request, **kwargs):
    global test_case

    #HERE WE'LL HAVE TO USE LAMBDA CALL FOR RETRIVE LIST OF USAGE FROM LIC_USAGE
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case}
    response = render(request, 'base_usage.html', context_dict, context)

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
    client = boto3.client("lambda")
    schema_name = request.META.get('HTTP_X_DTS_SCHEMA', get_public_schema_name())
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #check if user is active or not
        pay_c = {
                "ev_type": "G",
                "tenant": schema_name
            }
            
        cli_id = client.invoke(
            FunctionName='aida_lic_get',
            InvocationType='RequestResponse',
            Payload=json.dumps(pay_c)
        )
                
        #id_cli = cli_id['Payload'].read().decode('utf-8')[1]
        
        #Check if user in lic is active or if there is a connection
        try:
            site_active = json.loads(cli_id['Payload'].read().decode())[3]
        except Exception as e:
            site_active = False
        
        if site_active:
            #Now check if in settings_gen table tenant_name there is tenant, otherwise add it
            t_set = settings_gen.objects.all()

            if not t_set:
                #ten_add = settings_gen(tenant_name = schema_name)
                #ten_add.save()
                return HttpResponse("General license not active.\n\n Please contact support@myaida.io for more details.")

            dact = ""
            istrial = False
            for x in t_set:
                dact = x.created_on
                istrial = x.on_trial

            #Now check if user is in trial mode after 30 days, if yes redirect to register page otherwise continue
            d0 = date.today().strftime("%Y-%m-%d")
            d0 = datetime.strptime(d0, '%Y-%m-%d')
            d1 = datetime.strptime(str(dact.date()), '%Y-%m-%d')
            delta = (d0-d1)

            #Disabled because we decide to keep demo account every open
            """
            if delta.days > 30 and istrial:
                return HttpResponseRedirect('/register')
            """

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("User not active")
            else:
                return HttpResponse('Your user dont exist or password is wrong')
        else:
            return HttpResponse("SITE NOT ACTIVE ON DATACENTER! \n\n Your license does not seem to be active on our datacenters, we remind you that the internet connection must be working in order to use Aida, \n in case there are no line problems you can contact the Aida's system administrators for more information")
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
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import stripe
import requests

from django.shortcuts import render
from frontend.forms import DocumentForm
import simplejson
import logging
from frontend.template_export import start
from ajaxfuncs.template_import import import_internal
from selenium import webdriver
from frontend.models import UserProfile, t_test, t_history, t_schedule, t_schedsettings, t_group, t_group_test
from frontend.models import t_threads, t_tags, t_tags_route, settings_gen, jra_settings, jra_history
from backend.models import temp_keywords, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords
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
from frontend.getdata import get_lic
from dal import autocomplete

from jira import JIRA

import boto3
from botocore.exceptions import ClientError
import json
import hashlib

from tenant_schemas.utils import (get_tenant_model, remove_www,
                                  get_public_schema_name)


test_main = temp_main.objects.all()
test_case = temp_case.objects.all()
test_var = temp_variables.objects.all()
test_lib = temp_library.objects.all()

#Global schema variable populated on login (row 553)
schemaname = None;


def handler500(request):
    return render(request, '500.html', status=500)

@login_required
def index(request, **kwargs):
    global test_main
    uCookie = request.COOKIES.get('demoF', '')
    uGroup = request.user.groups.all()
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    test_sched = t_schedsettings.objects.all()

    context_dict = {'all_test': test_main, 't_sched': test_sched, 'uGroup': uGroup, 'uCookie':uCookie}
    #response = render(request, 'base_home.html', context_dict, context)
    #For IE compatibility remove context

    response = render(request, 'base_home.html', context_dict)

    return response


@login_required
@csrf_exempt
# Viev for history threads list
def h_list(request, **kwargs):
    global test_main

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
    #if not a : return HttpResponseRedirect('/')

    uGroup = request.user.groups.all()
    # menu_list = kwargs['menu']
    context = RequestContext(request)
    context_dict = {'all_test': test_main, 'uGroup': uGroup}
    response = render(request, 'base_history.html', context_dict)

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
    response = render(request, 'base_tmain.html', context_dict)

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
    response = render(request, 'base_tcase.html', context_dict)

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
    response = render(request, 'base_tgroup.html', context_dict)

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
    response = render(request, 'base_tvar.html', context_dict)

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
    response = render(request, 'base_tlib.html', context_dict)

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
    response = render(request, 'base_tcase.html', context_dict)

    return response


@login_required
def temp_assist(request, templ_id=None, **kwargs):

    con_stat = "<div><strong>NO DATA</strong></div>"
    if templ_id:
        b_templ = 'base_tassist_status.html'

        if templ_id == 'busy':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='red'>TEMPLATE ALREADY PRESENT</font></strong></p><br><strong>The template you are trying to import already exists in your enviroment.<br>For data integrity issues it is not possible to import two templates with the same name.<br><br>If you want to re-import a template, you must first change the name of the one in your library.<br><br><br><div><a href='/tassist'><button class='btn btn-block btn-success btn-lg'>BACK TO AIDA ASSIST</button></a></div></div></div></div>"
        elif templ_id == 'ok':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='green'>NEW TEMPLATE IMPORTED!</font></strong></p><br><strong>The template you imported was added correctly in your environment.<br>At this point you will find it already active both in the list of templates to be run and within your Template Manager area, where you can modify the configuration as you wish.<br><br><br><div><a href='/tassist'><button class='btn btn-block btn-success btn-lg'>BACK TO AIDA ASSIST</button></a></div></div></div></div>"
        elif templ_id == 'fail':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='red'>SOMETHING WENT WRONG</font></strong></p><br><strong>The import process of the selected template was not successful.<br><br>An error notification has been sent automatically to cathedral, which will analyze and correct the bug as soon as possible. we ask you to try the operation again later.<br><br><br><div><a href='/tassist'><button class='btn btn-block btn-success btn-lg'>GO TO AIDA PROJECT HOMEPAGE</button></a></div></div></div></div>"
        else:
            return HttpResponseRedirect('/')
    else:
        b_templ = 'base_tassist.html'


    context = RequestContext(request)

    context_dict = {'tmessage': con_stat}
    response = render(request, b_templ, context_dict)

    return response



@login_required
def go_ccredit(request, lic_num=None, **kwargs):

    #requests.post('https://www.cathedral.ai/test', data={'lid':lic_num,})
    return HttpResponseRedirect('https://www.cathedral.ai')


@login_required
def temp_publish(request, reg_status=None, **kwargs):

    global test_case
    uGroup = request.user.groups.all()

    b_temp = 'base_tpublish.html'
    con_stat = None
    if reg_status:
        b_temp = 'base_register_status.html'
        if reg_status == 'TOK':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg' style='font-size:38px;’><font color='blue'>PUBLICATION IN PROGRESS</font></p><br><strong>Thank you for your publication request!</strong><br><br>Our team of engineers will take care of evaluating all the aspects of compatibility about your template for our store and, if so, will proceed to authorize the publication.<br><br>You will receive a summary email as soon as the validation process is completed.<br>We remember that if the template had already been published, no further publication request can be sent.<br><br>To find out the status of your requests, consult the table on the template publication page from your Cathedral environment.<br><br><br><div><a href='/'><button class='btn btn-block btn-success btn-lg'>GO TO HOMEPAGE</button></a><br><a href='/tpublish'><button class='btn btn-block btn-primary btn-lg'>PUBLISH ANOTHER TEMPLATE</button></a></div></div></div></div>"
        elif reg_status == 'TKO':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='red'>FAIL!</font></strong></p><br><strong>The registration process for your new Aida account has not been completed successfully.</strong><br><br>Probably some of the data entered in the previous mask are not correct or there has been an internal error of the service.<br><br>Try to re-enter your registration data or report to our technical assistance the problem.<br><br><div><button onclick='javascript:location.href=https://aidaproject.io/contact;' class='btn btn-block btn-danger btn-lg'>REPORT THE PROBLEM</button><br><a href='/register/retry'><button class='btn btn-block btn-success btn-lg'>RETRY THE REGISTRATION PROCES</button></a></div></div></div></div>"
        else:
            return HttpResponseRedirect('/tpublish/')
    # Back home if no Teatadmin group for that user
    #if not 1 in [i.id for i in uGroup]:return HttpResponseRedirect('/')
    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case, 'uGroup': uGroup, 'the_stat': con_stat}
    response = render(request, b_temp, context_dict)

    return response


@login_required
def temp_clone(request, t_id=None, **kwargs):

    try:
        if not request.POST._mutable:
            request.POST._mutable = True

        request.POST['idTempl'] = t_id
        exp_dict = start(request, internal='yes')
        import_internal(json.dumps(exp_dict[0]))
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return HttpResponseRedirect('/logout')

    return HttpResponseRedirect('/admin/backend/temp_main/')

@login_required
def ext_lib(request, **kwargs):
    global test_case

    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case}
    response = render(request, 'base_extlib.html', context_dict)

    return response


def legal_terms(request, **kwargs):
    global test_case

    # menu_list = kwargs['menu']
    context = RequestContext(request)

    context_dict = {'all_case': test_case}
    response = render(request, 'base_legal.html', context_dict)

    return response


def lic_register(request, reg_status=None, **kwargs):
    global test_case

    #Retreive stripe API keys
    stripe.api_key = getattr(settings, "STRIPE_KEY", None)
    sg = settings_gen.objects.all()
    b_temp = 'base_register.html'
    con_stat = None
    if reg_status:
        b_temp = 'base_register_status.html'
        if reg_status == 'OK':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='green'>SUCCESS!</font></strong></p><br><strong>The registration request of your aida account was successful.</strong><br><br>Our staff will take care of your request and will proceed in the shortest possible time to carry out all the necessary operations to allow you to use aida without restrictions.<br><br>As soon as the registration procedure is complete you will receive an email to the address you specify in registration proces containing all the necessary data Using your new aida environment, if you do not receive the activation email within 24 hours, try checking your spam box.<br><br><br><div><a href='https://aidaproject.io'><button class='btn btn-block btn-success btn-lg'>GO TO AIDA PROJECT HOMEPAGE</button></a></div></div></div></div>"
        elif reg_status == 'KO':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='red'>FAIL!</font></strong></p><br><strong>The registration process for your new Aida account has not been completed successfully.</strong><br><br>Probably some of the data entered in the previous mask are not correct or there has been an internal error of the service.<br><br>Try to re-enter your registration data or report to our technical assistance the problem.<br><br><div><button onclick='javascript:location.href=https://aidaproject.io/contact;' class='btn btn-block btn-danger btn-lg'>REPORT THE PROBLEM</button><br><a href='/register/retry'><button class='btn btn-block btn-success btn-lg'>RETRY THE REGISTRATION PROCES</button></a></div></div></div></div>"
        elif reg_status == 'KO_USER':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='red'>USER ALREADY REGISTERED!</font></strong></p><br><strong>The email address you are trying to register is already associated to an active user in aida.</strong><br><br>If you do not remember your user's password, you can change it from the login panel using the 'Forgot password?' Link.<br>To change the preferences related to your user, within aida it is sufficient going to the username that appears at the top right to open the account control panel.<br><br><div><button onclick='javascript:location.href='https://aidaproject.io' class='btn btn-block btn-danger btn-lg'>GO TO AIDA HOME</button><br><a href='/register/retry'><button class='btn btn-block btn-success btn-lg'>RETRY THE REGISTRATION PROCES</button></a></div></div></div></div>"
        else:
            return HttpResponseRedirect('/register/')
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

    context_dict = {'all_case': test_case, 'all_set': sg, 'the_stat': con_stat}
    if request.method == 'POST':

        #First of all check if there is already a customer with the same email address registeed in strupe:
        same_email = 0
        cu_list = stripe.Customer.list()
        for x in cu_list:
            if x.email.upper().strip() == request.POST['c_email'].upper().strip():
                same_email += 1

        if same_email == 0:
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
                        #tax_percent=22.0,
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
                #If all done add to sendy customers list, redirect to homepage and send thanks email
                client = boto3.client("lambda")
                payload = {
                            "evtype": "customer",
                            "user_id": "1",
                            "fname": request.POST['firstname'],
                            "email": request.POST['c_email'],
                            "gdpr": "1",
                            "country": request.POST['country'],
                            "business": request.POST['organisationname'],
                            "active": "N",
                            "phone": "00-0000"
                        }

                try:
                    client.invoke(
                        FunctionName='aidasendy',
                        InvocationType='RequestResponse',
                        Payload=json.dumps(payload)
                    )
                except ClientError as er2:  # if you see a ClientError, catch it as e
                    print("Error lambda--> view379", er2)  # print the client error info to console
                    return HttpResponseRedirect('/register/KO/')


                return HttpResponseRedirect('/register/OK')
            except Exception as e:
                print('e->',e)
                return HttpResponseRedirect('/register/KO/')
        else:
            return HttpResponseRedirect('/register/KO_USER/')
    else:
        response = render(request, b_temp, context_dict)
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
    response = render(request, 'base_usage.html', context_dict)

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
                  {'user_form': user_form, 'user_profile': user_profile, 'registered': registered})


def user_login(request, log_err=None):
    context = RequestContext(request)
    client = boto3.client("lambda")
    #For tenant use only
    #schema_name = request.META.get('HTTP_X_DTS_SCHEMA', get_public_schema_name())
    schema_name = 'public'
    global schemaname
    schemaname = schema_name
    #Getting license number
    try:
        lnum = settings_gen.objects.values_list('lic_num',flat=True).get(id=1)
    except Exception as e:
        lnum = None

    #check if iexplorer
    user_agent = request.META['HTTP_USER_AGENT'].lower()
    if 'trident' in user_agent or 'msie' in user_agent:
        response = render(request, 'base_noie.html', {})
        return response



    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #check if user is active or not
        pay_c = {
                "ev_type": "G",
                "tenant": schema_name
            }

        try:

            cli_id = get_lic()
            """
            #Using AWS Lambda...avoided
            cli_id = client.invoke(
                FunctionName='aida_lic_get',
                InvocationType='RequestResponse',
                Payload=json.dumps(pay_c)
            )
            """

            try:
                #site_active = json.loads(cli_id['Payload'].read().decode())[3]
                site_active = cli_id['LDATA'][1]
            except Exception as e:
                site_active = False

            if site_active:
                # Now check if in settings_gen table tenant_name there is tenant, otherwise add it
                t_set = settings_gen.objects.all()

                if not t_set:
                    # ten_add = settings_gen(tenant_name = schema_name)
                    # ten_add.save()
                    return HttpResponse(
                        "General license not active.\n\n Please contact support@myaida.io for more details.")

                dact = ""
                istrial = False
                for x in t_set:
                    dact = x.created_on
                    istrial = x.on_trial

                """
                # Now check if user is in trial mode after 30 days, if yes redirect to register page otherwise continue
                d0 = date.today().strftime("%Y-%m-%d")
                d0 = datetime.strptime(d0, '%Y-%m-%d')
                d1 = datetime.strptime(str(dact.date()), '%Y-%m-%d')
                delta = (d0 - d1)

                # Disabled because we decide to keep demo account every open
                
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
                    return HttpResponseRedirect('/login/log_error')
                    # return HttpResponse('Your user dont exist or password is wrong')
                    # return render(request, 'login.html', {'l_err': log_err})
            else:
                return HttpResponse(
                    "ENVIROMENT NOT ACTIVE ON DATACENTER! \n\n Your license does not seem to be active on our datacenters, we remind you that the internet connection must be working in order to use Cathedral, \n in case there are no line problems you can contact the Cathedral's system administrators (4u@cathedral.ai) for more information")
        except Exception as awerr:
            print(awerr)
            return HttpResponse("INTERNET CONNETCTION NOT WORKING! We remind you that the internet connection must be working in order to use Cathedral, \n in case there are no line problems you can contact the Cathedral's system administrators (4u@cathedral.ai) for more information")


        #id_cli = cli_id['Payload'].read().decode('utf-8')[1]

        #Check if user in lic is active or if there is a connection

    else:
        #First check if a license is present, otherwise redirect to registration page
        if lnum:
            #Now check if license number is correct (not modification direcly from db)
            #code here

            return render(request, 'login.html', {'l_err': log_err})
        else:
            response = HttpResponseRedirect('/act_lic')
            return response

@csrf_exempt
def regoractivate(request, reg_status=None, **kwargs):

    global test_case

    b_temp = 'base_activate.html'
    con_stat = ""
    if reg_status:
        b_temp = 'base_register_status.html'
        if reg_status == 'OK':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg' style='font-size:58px;'><font color='green'>SUCCESS!</font></p><br><strong>The registration request of your Cathedral account was successful.</strong><br><br>Your Cathedral enviroment is active. You can log-in now using the credentials received by email when you register the product at the first time.<br><br>We remind you that, as suggested, it is advisable to change the password after the first access.<br><br><br><div><a href='/'><button class='btn btn-block btn-success btn-lg'>GO TO LOGIN HOMEPAGE</button></a></div></div></div></div>"
        elif reg_status == 'ERROR':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg' style='font-size:58px;'><font color='red'>FAIL!</font></p><br><strong>The registration process for your new Cathedral account has not been completed successfully.</strong><br><br>Probably some of the data entered in the previous mask are not correct or there has been an internal error of the service.<br><br>Try to re-enter your license data or register your data for receive a new license number.<br><br><div><button onclick='javascript:location.href='https://54.84.90.108/licensing' class='btn btn-block btn-success btn-lg'>REGISTER YOUR PRODUCT</button><br><a href='/act_lic/'><button class='btn btn-block btn-primary btn-lg'>RETRY THE ACTIVATION PROCES</button></a></div></div></div></div>"
        else:
            return HttpResponseRedirect('/act_lic/')

    if request.method == 'POST':

            response = []
            vallabel = {}
            client = boto3.client("lambda")

            #check for license
            pay_c = {
                    "ev_type": "G",
                    "tenant": request.POST.get('act_code', '').upper()
                }

            cli_id = client.invoke(
                FunctionName='aida_lic_get',
                InvocationType='RequestResponse',
                Payload=json.dumps(pay_c)
            )

            #id_cli = cli_id['Payload'].read().decode('utf-8')[1]

            #Check if user in lic is active or if there is a connection
            try:
                #site_active = json.loads(cli_id['Payload'].read().decode())[0]
                site_active = json.loads(cli_id['Payload'].read())

                if site_active == "null":
                    vallabel['RetMsg'] = 'ERROR'
                    return HttpResponseRedirect('/act_lic/ERROR/')
                else:
                    #first update settings_gen table
                    settings_gen.objects.filter(id=1).update(lic_num=request.POST.get('act_code', '').upper())
                    vallabel['RetMsg'] = 'OK'
                    return HttpResponseRedirect('/act_lic/OK/')

            except Exception as e:

                return HttpResponse("ENVIROMENT NOT ACTIVE ON DATACENTER OR INTERNET CONNECTION DOWN! \n\n Your license does not seem to be active on our datacenters, we remind you that the internet connection must be working in order to use Cathedral, \n in case there are no line problems you can contact the Cathedral's system administrators (4u@cathedral.ai) for more information")
    else:

        context_dict = {'all_case': test_case, 'the_stat': con_stat}
        response = render(request, b_temp, context_dict)

        return response

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


#The autocomplete class for temp_test, then registered in urls and in forms
class temp_test_keywordsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = temp_keywords.objects.all()

        if self.q:
            qs = qs.filter(human__istartswith=self.q)

        return qs


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

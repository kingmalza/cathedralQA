# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import stripe
import requests

from django.shortcuts import render
from django.core.management import call_command
from frontend.forms import DocumentForm
import simplejson
import logging
import psycopg2
from frontend.template_export import start
from frontend import get_sendy
from ajaxfuncs.template_import import import_internal
from selenium import webdriver
from frontend.models import UserProfile, t_test, t_history, t_schedule, t_schedsettings, t_group, t_group_test
from frontend.models import t_threads, t_tags, t_tags_route, settings_gen, jra_settings, jra_history
from backend.models import temp_keywords, temp_main as tmt, temp_case as tct, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords, \
    suite_libs
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


import json
import hashlib

from tenant_schemas.utils import (get_tenant_model, remove_www, get_public_schema_name)


test_main = tmt.objects.all()
test_case = tct.objects.all()
test_var = temp_variables.objects.all()
test_lib = temp_library.objects.all()

#Global schema variable populated on login (row 553)
schemaname = None;

tk = ['Add Cookie','Add Location Strategy','Alert Should Be Present','Alert Should Not Be Present','Assign Id To Element','Capture Page Screenshot','Checkbox Should Be Selected','Checkbox Should Not Be Selected','Choose Cancel On Next Confirmation','Choose File','Choose Ok On Next Confirmation','Clear Element Text','Click Button','Click Element','Click Element At Coordinates','Click Image','Click Link','Close All Browsers','Close Browser','Close Window','Confirm Action','Create Webdriver','Current Frame Contains','Current Frame Should Contain','Current Frame Should Not Contain','Delete All Cookies','Delete Cookie','Dismiss Alert','Double Click Element','Drag And Drop','Drag And Drop By Offset','Element Should Be Disabled','Element Should Be Enabled','Element Should Be Focused','Element Should Be Visible','Element Should Contain','Element Should Not Be Visible','Element Should Not Contain','Element Text Should Be','Execute Async Javascript','Execute Javascript','Focus','Frame Should Contain','Get Alert Message','Get All Links','Get Cookie','Get Cookie Value','Get Cookies','Get Element Attribute','Get Element Count','Get Element Size','Get Horizontal Position','Get List Items','Get Location','Get Locations','Get Matching Xpath Count','Get Selected List Label','Get Selected List Labels','Get Selected List Value','Get Selected List Values','Get Selenium Implicit Wait','Get Selenium Speed','Get Selenium Timeout','Get Source','Get Table Cell','Get Text','Get Title','Get Value','Get Vertical Position','Get WebElement','Get WebElements','Get Window Handles','Get Window Identifiers','Get Window Names','Get Window Position','Get Window Size','Get Window Titles','Go Back','Go To','Handle Alert','Input Password','Input Text','Input Text Into Alert','Input Text Into Prompt','List Selection Should Be','List Should Have No Selections','List Windows','Location Should Be','Location Should Contain','Locator Should Match X Times','Log','Log Location','Log Source','Log Title','Maximize Browser Window','Mouse Down','Mouse Down On Image','Mouse Down On Link','Mouse Out','Mouse Over','Mouse Up','Open Browser','Open Context Menu','Page Should Contain','Page Should Contain Button','Page Should Contain Checkbox','Page Should Contain Element','Page Should Contain Image','Page Should Contain Link','Page Should Contain List','Page Should Contain Radio Button','Page Should Contain Textfield','Page Should Not Contain','Page Should Not Contain Button','Page Should Not Contain Checkbox','Page Should Not Contain Element','Page Should Not Contain Image','Page Should Not Contain Link','Page Should Not Contain List','Page Should Not Contain Radio Button','Page Should Not Contain Textfield','Press Key','Radio Button Should Be Set To','Radio Button Should Not Be Selected','Register Keyword To Run On Failure','Reload Page','Remove Location Strategy','Select All From List','Select Checkbox','Select Frame','Select From List','Select From List By Index','Select From List By Label','Select From List By Value','Select Radio Button','Select Window','Set Browser Implicit Wait','Set Focus To Element','Set Screenshot Directory','Set Selenium Implicit Wait','Set Selenium Speed','Set Selenium Timeout','Set Window Position','Set Window Size','Simulate','Simulate Event','Submit Form','Switch Browser','Table Cell Should Contain','Table Column Should Contain','Table Footer Should Contain','Table Header Should Contain','Table Row Should Contain','Table Should Contain','Textarea Should Contain','Textarea Value Should Be','Textfield Should Contain','Textfield Value Should Be','Title Should Be','Unselect All From List','Unselect Checkbox','Unselect Frame','Unselect From List','Unselect From List By Index','Unselect From List By Label','Unselect From List By Value','Wait For Condition','Wait Until Element Contains','Wait Until Element Does Not Contain','Wait Until Element Is Enabled','Wait Until Element Is Not Visible','Wait Until Element Is Visible','Wait Until Page Contains','Wait Until Page Contains Element','Wait Until Page Does Not Contain','Wait Until Page Does Not Contain Element','Xpath Should Match X Times','[Documentation]','Sleep','Pause Execution',':FOR','\\','Directory Should Exist','Should Be Equal','[Arguments]','...']


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

"""
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
"""


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
def ask_template(request, **kwargs):

    #GET settings_gen stripe_id if present
    try:
        cli_id = get_lic()
        lic_buy = cli_id['LDATA'][9]
        if cli_id['LDATA'][9]:
            context_dict = {'licnum': lic_buy.strip()}
            response = render(request, 'base_ask.html', context_dict)
        else:
            return HttpResponseRedirect('https://cathedral.ai/gocard/'+cli_id['LDATA'][0].strip())
        return response
    except Exception:
        return HttpResponseRedirect('https://cathedral.ai/#contactus')


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
    #For tenant use only
    schema_name = request.META.get('HTTP_X_DTS_SCHEMA', get_public_schema_name())
    #schema_name = 'public'
    global schemaname
    schemaname = schema_name
    print("Schema: ",schemaname)
    #Getting license number
    try:
        lnum = settings_gen.objects.values_list('lic_num',flat=True).get(id=1)
    except Exception as e:
        print("Exception in licnu: ", e)
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
        """
        #First check if a license is present, otherwise redirect to registration page
        if lnum:
            #Now check if license number is correct (not modification direcly from db)
            #code here
            return render(request, 'login.html', {'l_err': log_err})
        else:
            #If you whnt to mamage auto registration in case of no license
            response = HttpResponseRedirect('/act_lic')
            return response
        """
        return render(request, 'login.html', {'l_err': log_err})

@csrf_exempt
def regoractivate(request, reg_status=None, **kwargs):

    global test_case

    b_temp = 'base_activate.html'
    con_stat = ""
    if reg_status:
        b_temp = 'base_register_status.html'
        if reg_status == 'OK':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg' style='font-size:58px;'><font color='green'>SUCCESS!</font></p><br><strong>The registration request of your Cathedral Studio account was successful.</strong><br><br>Your Cathedral enviroment is active. You can log-in now using the credentials received by email when you register the product at the first time.<br><br>We remind you that, as suggested, it is advisable to change the password after the first access.<br><br><br><div><a href='/'><button class='btn btn-block btn-success btn-lg'>GO TO LOGIN HOMEPAGE</button></a></div></div></div></div>"
        elif reg_status == 'ERROR':
            con_stat = "<div id='overlay_demo' style='display:block'><div id='text-demo'><div class='login-box-body'><p class='login-box-msg' style='font-size:58px;'><font color='red'>FAIL!</font></p><br><strong>The registration process for your new Cathedral account has not been completed successfully.</strong><br><br>Probably some of the data entered in the previous mask are not correct or there has been an internal error of the service.<br><br>Try to re-enter your license data or register your data for receive a new license number.<br><br><div><button onclick='javascript:location.href='https://54.84.90.108/licensing' class='btn btn-block btn-success btn-lg'>REGISTER YOUR PRODUCT</button><br><a href='/act_lic/'><button class='btn btn-block btn-primary btn-lg'>RETRY THE ACTIVATION PROCES</button></a></div></div></div></div>"
        else:
            return HttpResponseRedirect('/act_lic/')

    if request.method == 'POST':

            response = []
            vallabel = {}

            cparam = getattr(settings, "LIC_PARAM", None)

            vallabel = {}


            conn = psycopg2.connect(**cparam)
            conn.autocommit = True

            cur = conn.cursor()

            s_query = "SELECT * FROM a_lic WHERE lic_num='%s';" % request.POST['act_code']
            cur.execute(s_query)
            A = cur.fetchone()

            vallabel['LDATA'] = A

            conn.commit()
            cur.close()
            conn.close()

            #Check if license exist on server
            if not A:
                return HttpResponse("LICENSE DOES NOT EXIST! \n\n TThe license you are trying to activate does not exist on our database. Try going back and verify that you have typed all the characters correctly. \n For more informations you can contact the Cathedral's system administrators (4u@cathedral.ai)")

            if vallabel['LDATA'][2] :
                return HttpResponse("LICENSE ALREADY REGISTERED! \n\n The license you are trying to register is already active on our systems and therefore cannot be activated again, \n For more informations you can contact the Cathedral's system administrators (4u@cathedral.ai)")
            else:
                # first check if settings is already populated
                t_set = settings_gen.objects.all()
                if t_set:
                    settings_gen.objects.filter(id=1).update(lic_num=vallabel['LDATA'][0])
                else:
                    s_ins = settings_gen(lic_num=vallabel['LDATA'][0])
                    s_ins.save()

                #Update a_lic activation date
                conn = psycopg2.connect(**cparam)
                conn.autocommit = True

                cur = conn.cursor()

                u_query = "UPDATE public.a_lic SET activate_date='%s' WHERE lic_num='%s';" % (date.today().strftime("%Y-%m-%d"), vallabel['LDATA'][0])
                cur.execute(u_query)

                conn.commit()
                cur.close()
                conn.close()

                #Update sendy list
                sendy_dict = {'user_id': '1',
                              'email': vallabel['LDATA'][10],
                              'evtype': 'customer_activate'
                              }

                get_sendy.lambda_handler(sendy_dict)

                vallabel['RetMsg'] = 'OK'
                return HttpResponseRedirect('/act_lic/OK/')

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


#The autocomplete class for temp_test, then registered in urls and in forms
class temp_mainAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = tmt.objects.all()

        if self.q:
            qs = qs.filter(descr__istartswith=self.q).order_by('descr')

        return qs


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

#The autocomplete class for temp_test, then registered in urls and in forms
class temp_test_keywords_tc_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = tct.objects.all()

        tmain = self.forwarded.get('main_id', None)

        if tmain:
            qs = qs.filter(main_id=tmain)

        if self.q:
            qs = qs.filter(descr__istartswith=self.q)

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

#The autocomplete class for temp_test, then registered in urls and in forms
class temp_libraryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = suite_libs.objects.all()

        if self.q:
            qs = qs.filter(lib_name__istartswith=self.q)

        return qs


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

#Execute this command before startup, method call in urls
def one_time_startup():
    call_command('makemigrations')
    call_command('migrate_schemas')
    #Check if there are records in temp_keywords, otherwise insert
    ct = temp_keywords.objects.all().count()
    if ct == 0:
        global tk
        for i in tk:
            addkey = temp_keywords(descr=str(i), human=str(i), owner_id=None)
            addkey.save()

    ts = t_schedsettings.objects.all().count()
    if ts == 0:
        sched1 = t_schedsettings(sched_desc='Once', sched_command='once')
        sched2 = t_schedsettings(sched_desc='Every minutes', sched_command='everymin')
        sched3 = t_schedsettings(sched_desc='Every hour', sched_command='everyhour')
        sched4 = t_schedsettings(sched_desc='Every day', sched_command='everyday')

        sched1.save()
        sched2.save()
        sched3.save()
        sched4.save()

    sl = suite_libs.objects.all().count()
    if sl == 0:
        lib1 = suite_libs(name='Buit-In', descr='Robot Framework buitin libraries', lib_name='', status='ACTIVE',
                          docs='http://robotframework.org/robotframework/latest/libraries/BuiltIn.html')
        lib2 = suite_libs(name='Archive library', descr='Library for handling zip- and tar-archives',
                          lib_name='ArchiveLibrary', status='ACTIVE',
                          docs='http://bulkan.github.io/robotframework-archivelibrary/')
        lib3 = suite_libs(name='Django Library', descr='Library for Django, a Python web framework',
                          lib_name='DjangoLibrary', status='ACTIVE',
                          docs='https://kitconcept.github.io/robotframework-djangolibrary/')
        lib4 = suite_libs(name='FTP library', descr='Library for testing and using FTP server', lib_name='FtpLibrary',
                          status='ACTIVE', docs='https://kowalpy.github.io/Robot-Framework-FTP-Library/FtpLibrary.html')
        lib5 = suite_libs(name='RESTinstance', descr='Test library for HTTP JSON APIs', lib_name='REST',
                          status='ACTIVE', docs='https://asyrjasalo.github.io/RESTinstance/')
        lib6 = suite_libs(name='SSHLibrary',
                          descr='Enables executing commands on remote machines over an SSH connection. Also supports transfering files using SFTP',
                          lib_name='SSHLibrary', status='ACTIVE',
                          docs='https://github.com/robotframework/SSHLibrary#usage')
        lib7 = suite_libs(name='Diff Library', descr='Library to diff two files together', lib_name='DiffLibrary',
                          status='ACTIVE', docs='https://bulkan.github.io/robotframework-difflibrary/')
        lib8 = suite_libs(name='robotframework-faker', descr='Library for Faker, a fake test data generator',
                          lib_name='FakerLibrary', status='ACTIVE',
                          docs='https://guykisel.github.io/robotframework-faker/')
        lib9 = suite_libs(name='HTTP library (Requests)',
                          descr='Library for HTTP level testing using Request internally.', lib_name='RequestsLibrary',
                          status='ACTIVE', docs='http://bulkan.github.io/robotframework-requests/')
        lib10 = suite_libs(name='TFTPLibrary', descr='Library for interacting over Trivial File Transfer Portocol.',
                           lib_name='TftpLibrary', status='ACTIVE',
                           docs='https://kowalpy.github.io/Robot-Framework-TFTP-Library/TftpLibrary.html')
        lib11 = suite_libs(name='AppiumLibrary', descr='Library for Android- and iOS-testing.',
                           lib_name='AppiumLibrary', status='ACTIVE',
                           docs='http://serhatbolsu.github.io/robotframework-appiumlibrary/AppiumLibrary.html')
        lib12 = suite_libs(name='Selenium', descr='Selenium2Library is a web testing library.',
                           lib_name='SeleniumLibrary',
                           status='ACTIVE',
                           docs='http://robotframework.org/Selenium2Library/Selenium2Library.html')
        lib13 = suite_libs(name='Database Library',
                           descr='Allow you to query your database, compatible* with any Database API Specification 2.0 module.',
                           lib_name='DatabaseLibrary',
                           status='ACTIVE',
                           docs='https://www.python.org/dev/peps/pep-0249/')
        lib14 = suite_libs(name='JayDeBeApi', descr='Allows to connect from Python code to databases using Java JDBC',
                           lib_name='SeleniumLibrary',
                           status='ACTIVE',
                           docs='https://github.com/baztian/jaydebeapi#id2')
        lib15 = suite_libs(name='HttpLibrary.HTTP', descr='HttpLibrary for Robot Framework',
                           lib_name='HttpLibrary.HTTP',
                           status='ACTIVE',
                           docs='http://peritus.github.io/robotframework-httplibrary/HttpLibrary.html')
        lib16 = suite_libs(name='RequestsLibrary',
                           descr='RequestsLibrary is a test library that uses the Requests HTTP client.',
                           lib_name='RequestsLibrary',
                           status='ACTIVE',
                           docs='http://bulkan.github.io/robotframework-requests/')
        lib17 = suite_libs(name='ExcelLibrary',
                           descr='Robot Framework library for working with Excel documents, based on openpyxl.',
                           lib_name='ExcelLibrary',
                           status='ACTIVE',
                           docs='https://rawgit.com/peterservice-rnd/robotframework-excellib/master/docs/ExcelLibrary.html')
        lib19 = suite_libs(name='JsonValidator',
                           descr='Robot Framework library for JSON validation based on JSONSchema, JSONPath, JSONSelect.',
                           lib_name='JsonValidator',
                           status='ACTIVE',
                           docs='https://github.com/peterservice-rnd/robotframework-jsonvalidator/tree/master/docs')
        lib20 = suite_libs(name='OracleDB',
                           descr='Robot Framework library for working with Oracle database, using cx_Oracle.',
                           lib_name='OracleDB',
                           status='ACTIVE',
                           docs='https://github.com/peterservice-rnd/robotframework-oracledb/tree/master/docs')
        lib21 = suite_libs(name='PostgreSQLDB',
                           descr='Robot Framework library for working with PostgreSQL database, using psycopg2.',
                           lib_name='PostgreSQLDB',
                           status='ACTIVE',
                           docs='https://github.com/peterservice-rnd/robotframework-postgresqldb/tree/master/docs')
        lib22 = suite_libs(name='React Library',
                           descr='ReactLibrary is a Robot Framework library for React.',
                           lib_name='React Library',
                           status='ACTIVE',
                           docs='')
        lib23 = suite_libs(name='SnmpLibrary',
                           descr='SNMPLibrary is a Robot Framework test library for testing SNMP.',
                           lib_name='SnmpLibrary',
                           status='ACTIVE',
                           docs='http://kontron.github.io/robotframework-snmplibrary/SnmpLibrary.html')
        lib24 = suite_libs(name='winregistry.robot',
                           descr='Minimalist library aimed at working with Windows Registry.',
                           lib_name='winregistry.robot',
                           status='ACTIVE',
                           docs='https://github.com/shpaker/winregistry')

        lib1.save()
        lib2.save()
        lib3.save()
        lib4.save()
        lib5.save()
        lib6.save()
        lib7.save()
        lib8.save()
        lib9.save()
        lib10.save()
        lib11.save()
        lib12.save()
        lib13.save()
        lib14.save()
        lib15.save()
        lib16.save()
        lib17.save()
        lib19.save()
        lib20.save()
        lib21.save()
        lib22.save()
        lib23.save()
        lib24.save()

    #Check if almeno a use exist otherwise create one
    us = User.objects.all().count()
    if us == 0:
        User.objects.create_superuser('cathedral', '', 'Ca17653bu!');

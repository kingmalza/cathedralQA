
"""
Alessandro Malzanini
Methods for import template by id and reformat in customer schema
"""

import sys
import os
import simplejson
import threading
import schedule
import django
import psycopg2
import json
import subprocess, signal
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext



from frontend.models import temp_main


sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


connection_parameters = {
    'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
    'database': 'helium_ai',
    'user': 'kingmalza',
    'password': '11235813post',
}

#Method for list template in Aida Assist page
def list_templ(c_tenant):

    tt_list = []

    #List template from helium_ai db except for that loaded by user
    global connection_parameters

    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True

    ck_cursor = conn.cursor()
    #retreive only data for generating row preview in mask only if not inserted by user or in viewed there is all or user tenant
    ck_cursor.execute("SELECT id,descr,notes,u_libs,num_down,export_source,view_by FROM public.aida_export WHERE export_id NOT LIKE '" + c_tenant + "%' AND (view_by LIKE '%"+c_tenant+"%' OR view_by = 'all')")
    rec_main = ck_cursor.fetchall()
    for row in rec_main:
        tt_list.append({'tt_id': row[0],
                        'tt_tit': row[1],
                        'tt_note': row[2],
                        'tt_libs': row[3],
                        'tt_ndown': row[4],
                        'tt_exported': row[5],
                        'tt_view': row[6]
                        })

    ck_cursor.close()
    conn.close()

    return tt_list


#Method for import template
#Decorated because called directly from a link in url.py
@login_required
@csrf_exempt
def import_templ(request):

    #t_dict come directly from javascript
    if request.POST:

        tmainl = ""
        tlocal = []

        #First retreive exported struct and check if name not exist already
        global connection_parameters

        conn = psycopg2.connect(**connection_parameters)
        conn.autocommit = True

        ck_cursor = conn.cursor()
        # retreive only data for generating row preview in mask only if not inserted by user or in viewed there is all or user tenant
        ck_cursor.execute("SELECT py_dict FROM public.aida_export WHERE id = " + request.POST['idimp'])
        rec_main = ck_cursor.fetchall()
        for x in rec_main: tmainl = json.loads(x[0])

        ck_cursor.close()
        conn.close()

        #Check if not esist a template with the same name
        local_t = temp_main.objects.all()
        for t in local_t: tlocal.append(t.descr.upper())
        if tmainl['t_main'][0]['t_name'].upper() not in tlocal:
            #REMOVE PASS AND START IMPORT PROCESS!!!
            pass
        else:
            #NOW PRINT, THEN TO TRASFORM IN A GUI MESSAGE
            print("Template with same name already exist")

        return HttpResponseRedirect('/tassist')

    else:
        return HttpResponseRedirect('/')


    response = render(request)
    return response



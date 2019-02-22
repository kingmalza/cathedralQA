
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
from django.contrib.auth.models import User
from django.template import RequestContext



from frontend.models import temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_keywords, temp_pers_keywords


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

        #Extract all present keywords
        l_key = temp_keywords.objects.all()

        #Check if not esist a template with the same name
        local_t = temp_main.objects.all()
        for t in local_t: tlocal.append(t.descr.upper())
        #if tmainl['t_main'][0]['t_name'].upper() not in tlocal:
        if tmainl['t_main'][0]['t_name'].upper() not in [l.descr.upper() for l in local_t]:
            #1. Import temp_main proces and save the inseerted id
            main_save = temp_main(descr=tmainl['t_main'][0]['t_name'],
                                  notes=tmainl['t_main'][0]['t_notes'],
                                  dt=str(datetime.now()),
                                  owner_id=1,
                                  expected=tmainl['t_main'][0]['t_expected'],
                                  precond=tmainl['t_main'][0]['t_precond'],
                                  steps=tmainl['t_main'][0]['t_steps'])

            main_save.save()
            main_id = main_save.id

            #2. Import test case
            for a in range(len(tmainl['t_case'])):
                case_save = temp_case(descr=tmainl['t_case'][a]['tc_desr'],
                                      main_id_id=main_id,
                                      owner_id=1,
                                      dt=str(datetime.now()))
                case_save.save()
                case_id = case_save.id

            #3. Import variables
            for a in range(len(tmainl['t_vars'])):
                var_save = temp_variables(v_key=tmainl['t_vars'][a]['tv_key'],
                                          v_val=tmainl['t_vars'][a]['tv_val'],
                                          main_id_id=main_id,
                                          owner_id=1,
                                          dt=str(datetime.now()))
                var_save.save()

            #4. Import temp_library
            for a in range(len(tmainl['t_libs'])):
                lib_save = temp_library(l_type=tmainl['t_libs'][a]['tl_type'],
                                        l_val=tmainl['t_libs'][a]['tl_val'],
                                        main_id_id=main_id,
                                        owner_id=1,
                                        dt=str(datetime.now()),
                                        l_group=tmainl['t_libs'][a]['tl_group'])
                lib_save.save()

            # 5. Import temp_test_keywords
            for a in range(len(tmainl['t_ttk'])):
                #first check if key ecist in table temp keywords, otherwise add it
                if tmainl['t_ttk'][a]['tk_descr'] not in [x.descr for x in l_key]:
                    t_key = temp_keywords(descr=tmainl['t_ttk'][a]['tk_descr'],
                                          human=tmainl['t_ttk'][a]['tk_descr'],
                                          personal=True,
                                          owner_id=1,
                                          dt=str(datetime.now()))
                    t_key.save()
                    last_key = t_key.id
                else:
                    qa = temp_keywords.objects.filter(descr=tmainl['t_ttk'][a]['tk_descr']).only('id')
                    for q in qa: last_key = q.id


                ttk_save = temp_test_keywords(key_val=tmainl['t_ttk'][a]['tk_kval'],
                                              key_group=tmainl['t_ttk'][a]['tk_kgroup'],
                                              key_id_id=last_key,
                                              main_id_id=main_id,
                                              test_id_id=case_id,
                                              owner_id=1,
                                              dt=str(datetime.now()))

                ttk_save.save()

            #6. Import temp_pers_keywords
            for a in range(len(tmainl['t_tpk'])):
                # Check if exist first key then second
                if tmainl['t_tpk'][a]['tp_key1'] not in [x.descr for x in l_key]:
                    t_key = temp_keywords(descr=tmainl['t_tpk'][a]['tp_key1'],
                                          human=tmainl['t_tpk'][a]['tp_key1'],
                                          personal=True,
                                          owner_id=1,
                                          dt=str(datetime.now()))
                    t_key.save()
                    first_key = t_key.id
                else:
                    qa = temp_keywords.objects.filter(descr=tmainl['t_tpk'][a]['tp_key1']).only('id')
                    for q in qa: first_key = q.id
                #Second
                if tmainl['t_tpk'][a]['tp_key2'] not in [x.descr for x in l_key]:
                    t_key = temp_keywords(descr=tmainl['t_tpk'][a]['tp_key2'],
                                          human=tmainl['t_tpk'][a]['tp_key2'],
                                          personal=False,
                                          owner_id=1,
                                          dt=str(datetime.now()))
                    t_key.save()
                    second_key = t_key.id
                else:
                    qa = temp_keywords.objects.filter(descr=tmainl['t_tpk'][a]['tp_key2']).only('id')
                    for q in qa: second_key = q.id

                tpk_save = temp_pers_keywords(pers_id_id=first_key,
                                              strd_id_id=second_key,
                                              variable_val=tmainl['t_tpk'][a]['tp_kval'],
                                              main_id_id=main_id,
                                              owner_id=1,
                                              dt=str(datetime.now()))

                tpk_save.save()

            return HttpResponseRedirect('/tassist/ok')
        else:

            return HttpResponseRedirect('/tassist/busy')
            

        return HttpResponseRedirect('/tassist')

    else:
        return HttpResponseRedirect('/')


    response = render(request)
    return response



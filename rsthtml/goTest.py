from rsthtml.rst import PrepareRst as pr
from rsthtml.rst import MakeRst as mr
from rsthtml.rst import MakeHtml as mh
from django.http import HttpResponse, HttpRequest
from robot import run as run_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from copy import deepcopy

import simplejson
import random
import string
import json
import sys
import schedule
import time
import datetime
import threading
if sys.version_info[0] < 3:
    import Queue as que
else:
    import queue as que
import subprocess
from botocore.exceptions import ClientError
import re

from tenant_schemas.utils import (get_tenant_model, remove_www,
                                  get_public_schema_name)

from itertools import groupby, product
from operator import itemgetter

from frontend.models import t_history, t_time, t_threads, t_group, t_group_test, temp_main, t_proj_route, t_tags_route, t_proj, t_tags, settings_gen

t_list = {};
jobqueue = que.Queue()


# Methos used for create a unique list of values and perform for cycle on the variables
def product_by_grouping(lst):
    grps = [list(grp) for _, grp in groupby(lst, key=itemgetter(0))]
    return product(*grps)


def userdet(sessid):
    session = Session.objects.get(session_key=sessid)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    user = User.objects.get(id=uid)
    return user


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def goProc(mainId, varlist, t_inst, s_tag, s_type, u_id, sc_type, sc_val, run_type, tx_group='NoGroup'):
    print("Varlist---> ", varlist)
    p_oper = 'SC'
    varlist_a = deepcopy(varlist)
    varlist_b = deepcopy(varlist)
    for li in varlist_a:
        if li[0][0:3] == 'bs_':
            p_oper = li[1]
            varlist_b.remove(li)
        else:
            print("poper--->", p_oper)
            if p_oper == 'RN':
                num1 = int(li[1].split('-')[0].strip())
                num2 = int(li[1].split('-')[1].strip())
                li[1] = str(int(random.randint(num1, num2)))
            elif p_oper == 'RS':
                li[1] = randomword(int(li[1]))

    #Clean varlist_a
    for x in varlist_a:
        if x[0][0:3] == 'bs_':
            varlist_a.remove(x)


    g_id = None
    cli_id = None
    id_cli = 999

    #Time at the start
    dtime1 = str(datetime.datetime.now())
    # Start
    # 1 - Table preparation
    table_case = pr(mainId, "TC")
    table_key = pr(mainId, "TK")
    table_setting = pr(mainId, "TS")

    # 2 - MakeRst
    mrr1 = mr(table_setting.rst)
    mrr3 = mr(table_case.rst)
    mrr4 = mr(table_key.rst)
    mrr2 = mr(varlist_a)

    #globrst = mrr2+mrr1+mrr3+mrr4
    globrst = mrr2.rstab+mrr1.rstab+mrr3.rstab+mrr4.rstab

    # 3 - MakeHTML and Run test
    # We need to make this a thread then when is stopped save dta in db
    # t = threading.Thread(target=mh, args=(mrr1, mrr2, mrr3, mrr4,))

    global t_list

    # if not t_inst in t_list: t_list[t_inst] = mh(mrr3, mrr4, mrr2, mrr1)
    t_list[t_inst] = mh(mrr2, mrr1, mrr3, mrr4)

    start_time = time.time()
    l = threading.enumerate()

    if not t_list[t_inst].isAlive():
        try:
            t_list[t_inst].start()
        except:
            #lpath = t_list[t_inst].create_html
            t_list[t_inst].run()

        t_list[t_inst].join()  # wait till threads have finished.
        #run_test(t_list[t_inst].retval['fpath'], outputdir=t_list[t_inst].retval['fdir'], level='TRACE')
        subprocess.call(['python', 'golog.py', t_list[t_inst].retval['fpath'], t_list[t_inst].retval['fdir']])
    # Try to store data into db
    try:
        # Cop content of xml in db
        xmlcont = parsefile(t_list[t_inst].retval['fdir'] + "output.xml")

        if xmlcont != "":
            htmlcont = parsefile(t_list[t_inst].retval['fpath'])
            #Extract just Thread name
            pattern = "(Thread-\d+)"
            #t_full = str(threading.current_thread())
            t = str(threading.get_ident())
            #match = re.search(pattern, t_full)
            #t = str(match.group(0))
            #t = threading.current_thread()
            if s_type == "TG":
                g_id = t_group_test.objects.get(id_temp=mainId)
            # Count FAIL and PASS values into xml
            t_pass = str(xmlcont).count('PASS')
            t_fail = str(xmlcont).count('FAIL')
            try:
                test_save = t_history(test_main=temp_main.objects.get(id=mainId), exec_status="TERMINATE",
                                  xml_result=xmlcont,
                                  html_test=htmlcont, var_test=varlist_a, pid=t_list[t_inst].retval['pid'],
                                  user_id=User.objects.get(id=u_id), group_id=t_group.objects.get(id=g_id.id_grp_id), pass_num=t_pass,  fail_num=t_fail,
                                  test_type=s_type, test_group=tx_group, sched_type=sc_type, sched_val=sc_val, thread_name=t)
            except Exception:
                test_save = t_history(test_main=temp_main.objects.get(id=mainId), exec_status="TERMINATE",
                                      xml_result=xmlcont,
                                      html_test=htmlcont, var_test=varlist_a, pid=t_list[t_inst].retval['pid'],
                                      user_id=User.objects.get(id=u_id),
                                        pass_num=t_pass, fail_num=t_fail,
                                      test_type=s_type, test_group=tx_group, sched_type=sc_type, sched_val=sc_val,
                                      thread_name=t)


            test_save.save()

            # Time at the end
            dtime2 = str(datetime.datetime.now())

            elapsed = time.time() - start_time
            test_time = t_time(history_main=t_history.objects.get(id=test_save.id), elapsed_t=elapsed, stop_data=dtime2)
            test_time.save()

            thread_save = t_threads(id_test=t_history.objects.get(id=test_save.id), id_time=t_time.objects.get(id=test_time.id), thread_id=t_list[t_inst].getName(),
                                    thread_main=t, thread_stag=s_tag, thread_status="STARTED", thread_ttype=s_type, thread_runtype=run_type, thread_tgroup=tx_group, thread_stype=sc_type, thread_sval=sc_val)
            thread_save.save()

    except Exception as e:
        print("Errore_gotest:", e.args)


def run_threaded(job_func, P1, P2, P3, P4, P5, P6, P7, P8, P8_1, P9='NoGroup'):
    job_thread = threading.Thread(target=job_func(P1, P2, P3, P4, P5, P6, P7, P8, P8_1, P9))
    job_thread.start()


@csrf_exempt
def startTest(request, i=[0]):

    if request.is_ajax():
        #Check if there are already 5 started process, if this get message
        ThreadsActNum = t_threads.objects.values('thread_stag').filter(~Q(thread_status='DEAD')).distinct().count()
        limitMsg = None
        response = []
        if ThreadsActNum <= 4:
            u_id = int(request.user.id)
            main_list = []
            sset = 'once'
            sval = ""
            reqT = request.POST.get('ttype')
            runT = request.POST.get('runtype')
            # Decode the json from start js func
            json_string = request.POST.get('des')  # passed from JavaScript
            # Schedule settings comming from form
            if reqT == "ST":
                sset = request.POST.get('sched_sel')
                sval = request.POST.get('sched_val')
                gval = 'NoGroup'
            stag = request.POST.get('t_id')

            if request.POST.get('ttype') == 'PA':
                proj_list = t_proj_route.objects.filter(proj_id=request.POST.get('mainID'), main_id__active = True)
                for x in proj_list:
                    #Python3 replace unicode with str
                    #mainId = unicode(x.main_id_id)
                    mainId = str(x.main_id_id)
                    main_list.append(mainId)
                #Search aggregation descr
                try:
                    proj_search = t_proj.objects.filter(id=int(request.POST.get('group_val')))
                    for p in proj_search:
                        gval = p.descr
                except:
                    gval='DataError'
            elif request.POST.get('ttype') == 'TA':
                proj_list = t_tags_route.objects.filter(tag_id=request.POST.get('mainID'), main_id__active = True)
                for x in proj_list:
                    #mainId = unicode(x.main_id_id)
                    #Python3 replace unicode with str
                    mainId = str(x.main_id_id)
                    main_list.append(mainId)
                # Search aggregation descr
                try:
                    proj_search = t_tags.objects.filter(id=int(request.POST.get('group_val')))
                    for p in proj_search:
                        gval = p.descr
                except:
                    gval = 'DataError'
            elif request.POST.get('ttype') == 'TG':
                proj_list = t_group_test.objects.filter(id_grp=request.POST.get('mainID'), id_temp__active = True)
                for x in proj_list:
                    #Python3 replace unicode with str
                    #mainId = unicode(x.id_temp_id)
                    mainId = str(x.id_temp_id)
                    main_list.append(mainId)
                # Search aggregation descr
                try:
                    proj_search = t_group.objects.filter(id=int(request.POST.get('group_val')))
                    for p in proj_search:
                        gval = p.descr
                except:
                    gval = 'DataError'
            else:
                mainId = request.POST.get('mainID')
                main_list.append(mainId)

            # var to use for evaluate variables
            varlist = simplejson.loads(json_string)

            # cycle fror clean the data
            idTest = 0
            new_l = []
            new_l.insert(0, ["Variables", ""])

            for li in varlist:
                if 'tab_' in li[0]:
                    #if new_l and idTest != 0:
                        #goProc(idTest, new_l, 1, stag, reqT, u_id)
                        #time.sleep(15)
                    idTest = int(li[0].split("tab_", 1)[-1])
                    new_l = []
                    new_l.insert(0, ["Variables", ""])
                else:
                    new_l.append(li)

            # varlist.insert(0, ["Variables", ""])

            # goProc(mainId, varlist)
            i[0] += 1
            ###LIST OV VALUES TRANSFORMATION
            temp_l = []
            for i in new_l:
                if i[1] is not None:
                    sp = i[1].split('__')
                    if len(sp) > 1:
                        for x in sp:
                            temp_l.append([i[0], x])

                    else:
                        temp_l.append(i)
                else:
                    temp_l.append(i)

            #Now create list of lists of unique values
            a = list(product_by_grouping(temp_l))
            new_one = []
            for x in a:
                new_one.append(list(x))
            ###

            global jobqueue
            # in each case start first cycle immediately
            for xl in new_one:
                    for iid in main_list:
                        try:
                            goProc(iid, xl, 1, stag, reqT, u_id, sset, sval, runT, gval)
                            time.sleep(2)
                        except Exception as e:
                            print("Exception in goproc 306: ",e.args)
            if sset != 'once':
                ##IMPORTANT!##
                ##If multiple value in variable execution is related to all value only for Once selection, in case of scheduled just first value is executed

                # set tag with currentproc number

                # check if is every hour and set sval to None
                #if sset == 'everyhour': sval = None
                sched_dict = {
                    'everymin': 'schedule.every(int(sval)).minutes.do(run_threaded,goProc, mainId, new_one[0], i[0], stag, reqT, int(u_id), sset, sval, runT, gval).tag(str(stag))',
                    'everyhour': 'schedule.every().hour.do(run_threaded,goProc, mainId, new_one[0], i[0], stag, reqT, int(u_id), sset, sval, runT, gval).tag(str(stag))',
                    'everyday': 'schedule.every().day.at(str(sval)).do(run_threaded,goProc, mainId, new_one[0], i[0], stag, reqT, int(u_id), sset, sval, runT, gval).tag(str(stag))'}
                try:
                    eval(sched_dict[sset])
                    while 1:
                        schedule.run_pending()
                        time.sleep(1)

                except Exception as e:
                    print("Error in schedule settings! Check values-> gotest323",e)

        else:
            limitMsg = 'Concurrent threads limit reached (Max concurrent proceses allowed are 5)'

        vallabel = {'Rmessage': limitMsg,}
        response.append(vallabel)
        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )
    else:
        pass


def parsefile(filepath):
    parsecont = ""
    with open(filepath, 'r') as input:
        while True:
            data = input.read(100000)
            if data == '':
                break
            parsecont = parsecont + data

    return parsecont

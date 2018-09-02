from rsthtml.rst import PrepareRst as pr
from rsthtml.rst import MakeRst as mr
from rsthtml.rst import MakeHtml as mh
from django.http import HttpResponse
from robot import run as run_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import simplejson
import sys
import schedule
import time
import threading
if sys.version_info[0] < 3:
    import Queue as que
else:
    import queue as que
import subprocess
import re


from itertools import groupby, product
from operator import itemgetter

from frontend.models import t_history, t_time, t_threads, t_group, t_group_test, temp_main, t_proj_route, t_tags_route, t_proj, t_tags

t_list = {};
jobqueue = que.Queue()


# Methos used for create a unique list of values and perform for cycle on the variables
def product_by_grouping(lst):
    grps = [list(grp) for _, grp in groupby(lst, key=itemgetter(0))]
    return product(*grps)


def userdet(sessid):
    session = Session.objects.get(session_key=sessid)
    session_data = session.get_decoded()
    print (session_data)
    uid = session_data.get('_auth_user_id')
    user = User.objects.get(id=uid)
    return user


def goProc(mainId, varlist, t_inst, s_tag, s_type, u_id, sc_type, sc_val, tx_group='NoGroup'):
    g_id = None

    # Start
    # 1 - Table preparation
    table_case = pr(mainId, "TC")
    table_key = pr(mainId, "TK")
    table_setting = pr(mainId, "TS")

    # 2 - MakeRst
    mrr1 = mr(table_setting.rst)
    mrr3 = mr(table_case.rst)
    mrr4 = mr(table_key.rst)
    mrr2 = mr(varlist)

    # 3 - MakeHTML and Run test
    # We need to make this a thread then when is stopped save dta in db
    # t = threading.Thread(target=mh, args=(mrr1, mrr2, mrr3, mrr4,))

    global t_list
    print("TLIST IS -->", t_list)

    # if not t_inst in t_list: t_list[t_inst] = mh(mrr3, mrr4, mrr2, mrr1)
    t_list[t_inst] = mh(mrr2, mrr1, mrr3, mrr4)

    start_time = time.time()
    l = threading.enumerate()
    print("The thread is:", t_list[t_inst])
    print("Current thread is", threading.current_thread())
    print("enumerate", l)
    print("THREAD IN ENUMERATE: ", (threading.current_thread() in l))
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
        print("TINS IS ---->>>> ", t_inst)
        xmlcont = parsefile(t_list[t_inst].retval['fdir'] + "output.xml")
        if xmlcont != "":
            htmlcont = parsefile(t_list[t_inst].retval['fpath'])
            #Extract just Thread name
            pattern = "(Thread-\d+)"
            t_full = str(threading.current_thread())
            match = re.search(pattern, t_full)
            t = str(match.group(0))
            #t = threading.current_thread()
            if s_type == "TG": g_id = t_group.objects.get(id=mainId)
            # Count FAIL and PASS values into xml
            t_pass = str(xmlcont).count('PASS')
            t_fail = str(xmlcont).count('FAIL')
            test_save = t_history(test_main=temp_main.objects.get(id=mainId), exec_status="TERMINATE",
                                  xml_result=xmlcont,
                                  html_test=htmlcont, var_test=varlist, pid=t_list[t_inst].retval['pid'],
                                  user_id=User.objects.get(id=u_id), group_id=g_id, pass_num=t_pass, fail_num=t_fail,
                                  test_type=s_type, test_group=tx_group, sched_type=sc_type, sched_val=sc_val, thread_name=t)

            test_save.save()
            print("Valori prima %s - %s - %s" % (t_list[t_inst].getName(), t, s_tag))
            thread_save = t_threads(id_test=t_history.objects.get(id=test_save.id), thread_id=t_list[t_inst].getName(),
                                    thread_main=t, thread_stag=s_tag, thread_status="STARTED", thread_ttype=s_type, thread_tgroup=tx_group, thread_stype=sc_type, thread_sval=sc_val)
            thread_save.save()

            elapsed = time.time() - start_time

            test_time = t_time(history_main=test_save.id, elapsed_t=elapsed)
            test_time.save()
    except Exception as e:
        print("Errore:", e.args)


def run_threaded(job_func, P1, P2, P3, P4, P5, P6, P7, P8, P9='NoGroup'):
    job_thread = threading.Thread(target=job_func(P1, P2, P3, P4, P5, P6, P7, P8, P9))
    job_thread.start()


@csrf_exempt
def startTest(request, i=[0]):

    if request.is_ajax():
        u_id = request.user.id
        response = []
        main_list = []
        sset = 'once'
        sval = ""
        reqT = request.POST.get('ttype')
        # Decode the json from start js func
        json_string = request.POST.get('des')  # passed from JavaScript
        print("json = ", json_string)
        # Schedule settings comming from form
        if reqT == "ST":
            sset = request.POST.get('sched_sel')
            sval = request.POST.get('sched_val')
            gval = 'NoGroup'
        stag = request.POST.get('t_id')
        print("Sel:%s val:%s" % (sset, sval))

        if request.POST.get('ttype') == 'PA':
            proj_list = t_proj_route.objects.filter(proj_id=request.POST.get('mainID'))
            for x in proj_list:
                mainId = unicode(x.main_id_id)
                main_list.append(mainId)
            #Search aggregation descr
            try:
                proj_search = t_proj.objects.filter(id=int(request.POST.get('group_val')))
                for p in proj_search:
                    gval = p.descr
            except:
                gval='DataError'
        elif request.POST.get('ttype') == 'TA':
            proj_list = t_tags_route.objects.filter(tag_id=request.POST.get('mainID'))
            for x in proj_list:
                mainId = unicode(x.main_id_id)
                main_list.append(mainId)
            # Search aggregation descr
            try:
                proj_search = t_tags.objects.filter(id=int(request.POST.get('group_val')))
                for p in proj_search:
                    gval = p.descr
            except:
                gval = 'DataError'
        elif request.POST.get('ttype') == 'TG':
            proj_list = t_group_test.objects.filter(id_grp=request.POST.get('mainID'))
            for x in proj_list:
                mainId = unicode(x.id_temp_id)
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
        print('varrlistt--->', varlist)
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
        print('temp_l--->',temp_l)
        #Now create list of lists of unique values
        a = list(product_by_grouping(temp_l))
        new_one = []
        for x in a:
            new_one.append(list(x))

        print('new_one: ', new_one)
        ###

        global jobqueue
        # in each case start first cycle immediately
        for xl in new_one:
                for iid in main_list:
                    goProc(iid, xl, 1, stag, reqT, u_id, sset, sval, gval)
                    time.sleep(5)
        if sset != 'once':
            ##IMPORTANT!##
            ##If multiple value in variable execution is related to all value only for Once selection, in case of scheduled just first value is executed

            # set tag with currentproc number

            # check if is every hour and set sval to None
            #if sset == 'everyhour': sval = None
            sched_dict = {
                'everymin': 'schedule.every(int(sval)).minutes.do(run_threaded,goProc, mainId, new_one[0], i[0], stag, reqT, int(u_id), sset, sval, gval).tag(str(stag))',
                'everyhour': 'schedule.every().hour.do(run_threaded,goProc, mainId, new_one[0], i[0], stag, reqT, int(u_id), sset, sval, gval).tag(str(stag))',
                'everyday': 'schedule.every().day.at(str(sval)).do(run_threaded,goProc, mainId, new_one[0], i[0], stag, reqT, int(u_id), sset, sval, gval).tag(str(stag))'}
            print("SCHEDULE->>", sset, sval)
            try:
                eval(sched_dict[sset])
                while 1:
                    schedule.run_pending()
                    time.sleep(1)

            except Exception as e:
                print("Error in schedule settings! Check values->",e)

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

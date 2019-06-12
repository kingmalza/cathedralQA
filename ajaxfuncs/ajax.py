import sys
import os
import simplejson
import threading
import schedule
import django
import subprocess, signal
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from rsthtml.rst import PrepareRst as pr
from rsthtml.rst import MakeRst as mr
from rsthtml.rst import MakeHtml as mh
from rsthtml.goTest import parsefile

import lxml.etree as etree

from jira import JIRA

from frontend.models import temp_main, temp_case, temp_variables, t_threads, t_history, t_group, t_group_test, \
    t_tags, t_tags_route, t_proj, t_proj_route, Document, jra_settings, jra_history

sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


@csrf_exempt
def mainoptions(request):
    if request.is_ajax():

        if request.POST['selType'] == "TG":
            g_list = []
            # HERE WE HAVE TO SELECT THE temp_variables related to test in t_group_test
            # First create my list from group selection
            try:
                mainGroup = t_group_test.objects.filter(id_grp=int(request.POST['mainID']), id_temp__active = True).order_by('temp_ord')
                for i in mainGroup.iterator(): g_list.append(i.id_temp.id)
            except:
                pass
            # Now filter variables based on multiple temp main
            mainOptions = temp_variables.objects.filter(main_id__in=g_list)
        elif request.POST['selType'] == "ST":
            mainOptions = temp_variables.objects.filter(main_id=int(request.POST['mainID']))
            # If mainOptions is blank insert new nodata line
            if not mainOptions:
                try:
                    p = temp_variables(v_key='noData', v_val='noVal',
                                   main_id=temp_main.objects.get(id=int(request.POST['mainID'])), owner_id=1)
                    p.save()
                except:
                    pass
        elif request.POST['selType'] == "TA":
            # is a TA
            t_list = []
            # HERE WE HAVE TO SELECT THE temp_variables related to test in t_tags_route
            # First create my list from tags selection
            try:
                mainTags = t_tags_route.objects.filter(tag_id=int(request.POST['mainID']), main_id__active = True).order_by('main_id')
                for i in mainTags.iterator(): t_list.append(i.main_id.id)
            except:
                pass

            # Now filter variables based on multiple temp main
            mainOptions = temp_variables.objects.filter(main_id__in=t_list)

        else:
            # is a TP
            t_list = []
            # HERE WE HAVE TO SELECT THE temp_variables related to test in t_proj_route
            # First create my list from projs selection

            try:
                mainProjs = t_proj_route.objects.filter(proj_id=int(request.POST['mainID']), main_id__active = True).order_by('main_id')
                for i in mainProjs.iterator():
                    t_list.append(i.main_id.id)
            except:
                pass
            # Now filter variables based on multiple temp main
            mainOptions = temp_variables.objects.filter(main_id__in=t_list)


        #Now i have toretreive html for display in preview div
        #------------RST AND HTML PREPARATION--------------------------

        # 1 - Table preparation
        table_case = pr(request.POST['mainID'], "TC")
        table_key = pr(request.POST['mainID'], "TK")
        table_setting = pr(request.POST['mainID'], "TS")
        #In this case take the default variables
        #table_var = pr(request.POST['mainID'], "TV")

        # 2 - MakeRst
        mrr1 = mr(table_setting.rst)
        mrr3 = mr(table_case.rst)
        mrr4 = mr(table_key.rst)

        # 3 - Clean string returned for display roperly
        cmr1 = mrr1.rstab.replace("-","").replace("+","")
        cmr2 = mrr3.rstab.replace("-", "").replace("+","")
        cmr3 = mrr4.rstab.replace("-", "").replace("+","")
        #------------------------------------------------------------

        response = []
        for i in mainOptions.iterator():
            vallabel = {'OptionID': i.id, 'OptionKey': i.v_key, 'OptionVal': i.v_val, 'OptionMain': i.main_id.id,
                        'OptionDescr': i.main_id.descr, 'OptionNote': i.main_id.notes}
            response.append(vallabel)
        valrst = {'r_settings': cmr1, 'r_case': cmr2, 'r_key': cmr3}
        response.append(valrst)
        json = simplejson.dumps(response)
        print(json)
        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
def tabrefresh(request):
    lorder = request.POST['tab_ord']
    ise = request.POST['isearch']
    qsearch = str(request.POST['tab_search'])
    l = threading.enumerate()
    if request.is_ajax():

        activeThreads = t_threads.objects.filter(~Q(thread_status='DEAD'))
        # activeThreads = t_threads.objects.all().values('thread_stag').annotate(total=Count(
        # 'thread_stag')).order_by('thread_status') Check if threads are active instead change the alive val from table
        for i in activeThreads:
            if not i.thread_main in str(l):
                t_threads.objects.filter(thread_main=i.thread_main).update(thread_status='DEAD')
        # If order is different from id i have to ungroup results
        # Rescan table and groub by thread_stag

        if qsearch == 'noSearch':
            activeThreads = t_threads.objects.filter(~Q(thread_status='DEAD')).select_related().distinct('thread_stag')
        else:
            strfin = ''
            a = []
            kwargs = {}
            a = qsearch.split(',')
            for li in range(0, len(a)):
                b = a[li].split(':')
                kw = b[0].upper()
                val = b[1].strip()
                if kw == 'ID':
                    kwargs['id__contains'] = val
                elif kw == 'TEST NAME':
                    kwargs['id_test__test_main__descr__contains'] = val
                elif kw == 'TEST TYPE':
                    kwargs['thread_ttype__contains'] = str(val)
                elif kw == 'TEST GROUP':
                    kwargs['thread_tgroup__contains'] = val
                elif kw == 'SCHEDULE TYPE':
                    kwargs['thread_stype__contains'] = val
                elif kw == 'RUN TYPE':
                    kwargs['thread_runtype__contains'] = val
                elif kw == 'SCHEDULE VALUE':
                    kwargs['thread_sval__contains'] = val
                elif kw == 'THREAD':
                    kwargs['thread_main__contains'] = val
                elif kw == 'START':
                    kwargs['thread_startd__contains'] = val
                elif kw == 'USER':
                    kwargs['id_test__user_id__username__contains'] = val

            activeThreads = t_threads.objects.filter(~Q(thread_status='DEAD'), **kwargs).select_related().distinct(
                'thread_stag')
            #afilexec = "%s%s%s" % ("activeThreads = t_threads.objects.filter(~Q(thread_status='DEAD'),", strfin[1:], ").select_related().distinct('thread_stag')")
            #exec(afilexec)
            #exec afilexec in {}
            #execstring(afilexec)


        # Create pass/faiil sequence for inline graph
        sep = ','

        response = []

        for i in activeThreads:
            vallabel = {}
            p, f = [], []
            vallabel['tID'] = i.id
            vallabel['OptionName'] = i.id_test.test_main.descr
            vallabel['OptionType'] = i.thread_ttype
            vallabel['OptionRuntype'] = i.thread_runtype
            vallabel['OptionGroup'] = i.thread_tgroup
            vallabel['OptionSched'] = i.thread_stype
            vallabel['OptionSchedVal'] = i.thread_sval
            vallabel['OptionID'] = i.thread_id
            vallabel['OptionUUID'] = i.thread_stag
            vallabel['OptionSdate'] = str(i.thread_startd.strftime("%Y-%d-%m %H:%M:%S"))
            vallabel['OptionUser'] = str(i.id_test.user_id)
            vallabel['OptionStatus'] = i.thread_status
            vallabel['OptionTest'] = i.id_test.id
            # Create inline data for pass/fail
            p = ['1' for x in range(i.id_test.pass_num)]
            f = ['-1' for x in range(i.id_test.fail_num)]
            seq_pf = sep.join(p + f)
            vallabel['InlineData'] = seq_pf
            # Now i find number of total cycle groupping by thread_stag
            tn = t_threads.objects.filter(thread_stag=str(i.thread_stag)).aggregate(tcount=Count('thread_stag'))
            vallabel['OptionNumT'] = tn['tcount']
            response.append(vallabel)

        if str(lorder != ''):
            if str(ise) == '+':
                response = sorted(response, key=lambda k: k[str(lorder)], reverse=True)
            else:
                response = sorted(response, key=lambda k: k[str(lorder)])

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
def filerefresh(request):
    if request.is_ajax():
        totDocs = Document.objects.all().order_by('-id')

        response = []

        for i in totDocs:
            vallabel = {}
            vallabel['fID'] = i.id
            vallabel['fDescr'] = i.description
            vallabel['fDoc'] = str(i.document)
            vallabel['fData'] = str(i.uploaded_at)
            vallabel['fOwner'] = str(i.owner)
            vallabel['fDpath'] = str(i.dfolder)
            vallabel['fDmessage'] = str(i.dmessage)
            response.append(vallabel)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
# Method for populate counters in menu
def ecount(request):
    if request.is_ajax():

        # Count quantity of active threads,killed,testcase etc for display in menu
        TestMainNum = temp_main.objects.all().count()
        # Active and hidle threads
        ThreadsActNum = t_threads.objects.values('thread_stag').filter(~Q(thread_status='DEAD')).distinct().count()
        ThreadsHideNum = t_threads.objects.values('thread_stag').filter(thread_status='DEAD').distinct().count()
        # Limit killed thread num visualization is to hight the number in table
        if ThreadsHideNum > 10000: ThreadsHideNum = '>10000'

        response = []
        vallabel = {'TCnum': TestMainNum, 'TAnum': ThreadsActNum, 'TKnum': ThreadsHideNum}
        response.append(vallabel)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
# Populate the timeline for selected thread
def tlinemgm(request):
    if request.is_ajax():
        #If request come from active form i retreive last 5 results, otherwise (History) last 20
        if str(request.POST['fView']) == "active":
            thread_list = t_threads.objects.filter(thread_stag=str(request.POST['tTag'])).select_related()[:5]
        else:
            thread_list = t_threads.objects.filter(thread_stag=str(request.POST['tTag'])).select_related()[:20]

        #Now check if there is in jira settings something or not
        jra_set = jra_settings.objects.all()
        j_set = None
        for x in jra_set: j_set = x.id

        response = []

        for i in thread_list:
            vallabel = {'t_id': i.id, 'th_id': i.thread_id, 't_stag': i.thread_stag, 't_exec': str(i.id_test.exec_data.strftime("%Y-%d-%m %H:%M:%S")), 't_xml': i.id_test.xml_result,
                        't_html': i.id_test.html_test, 't_var': i.id_test.var_test, 't_pid': i.id_test.pid,
                        't_user': str(i.id_test.user_id), 't_main': str(i.id_test.test_main), 't_jira': j_set}

            response.append(vallabel)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
# For jira integration post
def jpost(request):
    if request.is_ajax():

        jh_list = jra_history.objects.filter(j_tid=str(request.POST['thId'])).select_related()

        response = []

        for i in jh_list:
            vallabel = {'j_id': i.id, 'j_issue': i.j_issue, 'j_com': i.j_comment, 'j_file': i.j_file, 'j_date': str(i.dt), 'j_err': i.j_error}

            response.append(vallabel)

        json = simplejson.dumps(response)

        return HttpResponse(json, content_type='application/json')

    else:
        pass


@csrf_exempt
def tselect(request):
    l = threading.enumerate()
    if request.is_ajax():
        if request.POST['selType'] == "ST":
            selData = temp_main.objects.filter(active=True)
        elif request.POST['selType'] == "TG":
            selData = t_group.objects.all()
        elif request.POST['selType'] == "TA":
            selData = t_tags.objects.all()
        else:
            selData = t_proj.objects.all()

        response = []
        for i in selData:
            vallabel = {}
            vallabel['selID'] = i.id
            vallabel['selDescr'] = i.descr
            if request.POST['selType'] == "ST":
                vallabel['OptionNote'] = i.notes
                vallabel['OptionDt'] = i.dt
                vallabel['OptionTtype'] = i.t_type
            vallabel['selType'] = request.POST['selType']
            response.append(vallabel)
        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
def tstopper(request):
    l = threading.enumerate()
    # user connected and user thread generator
    u_conn = request.user.id
    u_thread = 0
    response = []

    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    """
    for line in out.splitlines():
        print(line)
    """

    if request.is_ajax():
        specThread = t_threads.objects.filter(thread_stag=str(request.POST['tData']))
        for i in specThread:
            u_thread = i.id_test.user_id.id
            tuid = i.thread_stag
        try:
            if int(u_conn) == int(u_thread):
                schedule.clear(str(tuid), )
                t_threads.objects.filter(thread_stag=str(request.POST['tData'])).update(thread_status='DEAD',
                                                                                        thread_stopd=datetime.now())
            else:
                vallabel = {}
                vallabel['userKo'] = 'noAuth'
                response.append(vallabel)
        except Exception as e:
            print("Cannot stop schedulr -> ", e)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass

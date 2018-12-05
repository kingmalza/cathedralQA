import sys
import os
import simplejson
import threading
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from frontend.models import temp_main, temp_case, temp_variables, t_threads, t_history, t_group, t_group_test

import django

sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


@csrf_exempt
def histrefresh(request, lorder='-id'):
    l = threading.enumerate()

    if request.is_ajax():
        # l = logging.getLogger('django.db.backends')
        # l.setLevel(logging.DEBUG)
        # l.addHandler(logging.StreamHandler())
        if request.POST['tab_ord'] is not None: lorder = request.POST['tab_ord']

        if request.POST['tab_slice'] == 1 or int(request.POST['isearch']) == 1:
            x, y = 0, 20
        else:
            x = (int(request.POST['tab_slice']) - 1) * 20
            y = x + 20

        # Queryes for fetch total and average data (fast as possible)
        #allThreads = t_threads.objects.filter(thread_status='DEAD')

        op = t_history.objects.aggregate(Sum('pass_num'))
        of = t_history.objects.aggregate(Sum('fail_num'))
        pnum = op['pass_num__sum']
        fnum = of['fail_num__sum']
        # First check if is typed a search term
        if request.POST['tab_search'] == 'noSearch':
            ordered = t_threads.objects.filter(thread_status='DEAD').select_related().order_by(lorder)[x:y]
            #Here i create a list of distinct thread_main values for calculate and manage in js the history threads list
            a = t_threads.objects.values_list('thread_main').distinct()
            dis_thread = list(a)
            oCount = t_threads.objects.filter(thread_status='DEAD').count()
            twarnings = t_threads.objects.filter(thread_status='DEAD',thread_stopd__isnull=True).count()
        # if is typed check if is a correct name of columns, otherwise make generic standard query
        else:
            strfin = ''
            a = []
            a = request.POST['tab_search'].split(',')
            for li in range(0,len(a)):
                b = a[li].split(':')
                if b[0].upper() == 'ID':
                    strfin = strfin + ',id__contains=' + b[1]
                elif b[0].upper() == 'TEST NAME':
                    strfin = strfin + ',id_test__test_main__descr__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'TEST TYPE':
                    strfin = strfin + ',thread_ttype__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'TEST GROUP':
                    strfin = strfin + ',thread_tgroup__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'SCHEDULE':
                    strfin = strfin + ',thread_stype__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'THREAD NAME':
                    strfin = strfin + ',thread_main__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'START':
                    strfin = strfin + ',thread_startd__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'STOP':
                    strfin = strfin + ',thread_stopd__contains=' + "'"+b[1].strip()+"'"
                elif b[0].upper() == 'USER':
                    strfin, strperc = strfin + ',id_test__user_id__contains=' + "'"+b[1].strip()+"'"


            strexec1 = "%s%s%s" % ("ordered = t_threads.objects.filter(thread_status='DEAD',",strfin[1:],").select_related().order_by(lorder)[x:y]")
            strexec2 = "%s%s%s" % ("oCount = t_threads.objects.filter(thread_status='DEAD',",strfin[1:],").count()")
            strexec3 = "%s%s%s" % ("twarnings = t_threads.objects.filter(thread_status='DEAD',",strfin[1:],",thread_stopd__isnull=True).count()")

            try:
                exec(strexec1)
                exec(strexec2)
                exec(strexec3)

            except Exception as e:
                print('Search exception ->',e)

            #Recalculate pass and failures nums
            pnum = 0
            fnum = 0
            for x in ordered:
                p1 = t_history.objects.values('pass_num').filter(id=x.id_test_id)
                f1 = t_history.objects.values('fail_num').filter(id=x.id_test_id)
                pnum = pnum + p1[0]['pass_num']
                fnum = fnum + f1[0]['fail_num']
        # allThreadsF = t_threads.objects.filter(thread_status='DEAD').select_related().distinct('thread_stag')[x:y]
        # order the thread list by id desc
        # ordered = sorted(allThreadsF, key=operator.attrgetter('id'), reverse=True)

        # All pass and fail
        try:
            percp = (pnum * 100) / (pnum + fnum)
            percf = (fnum * 100) / (pnum + fnum)
        except Exception as e:
            percp=0
            percf=0

        response = []

        for i in ordered:
            vallabel = {'tID': i.id, 'tTest': str(i.id_test.test_main), 'OptionID': i.thread_id,
                        'OptionUUID': i.thread_stag, 'OptionMain': i.thread_main,
                        'OptionSdate': str(i.thread_startd)[:19], 'OptionStopdate': str(i.thread_stopd)[:19],
                        'OptionUser': str(i.id_test.user_id), 'OptionTest': i.id_test.id, 'OptionType': i.thread_ttype,
                        'OptionGroup': i.thread_tgroup,
                        'OptionStype': i.thread_stype, 'OptionSval': i.thread_sval}
            # Create inline data for pass/fail
            p = ['1' for x in range(i.id_test.pass_num)]
            f = ['-1' for x in range(i.id_test.fail_num)]
            vallabel['OptionPass'] = len(p)
            vallabel['OptionFail'] = len(f)
            # Now i find number of total cycle groupping by thread_stag
            tn = t_threads.objects.filter(thread_stag=str(i.thread_stag)).aggregate(tcount=Count('thread_stag'))
            vallabel['OptionNumT'] = tn['tcount']

            vallabel['TotData'] = oCount
            vallabel['Unique'] = dis_thread
            vallabel['wData'] = twarnings
            vallabel['PercPass'] = round(percp, 2)
            vallabel['PercFail'] = round(percf, 2)

            response.append(vallabel)

        response.append(oCount)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass

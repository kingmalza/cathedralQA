import sys
import os
import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from frontend.models import t_threads, t_history, t_group, t_group_test
from backend.models import temp_keywords, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords
=======
from frontend.models import temp_main, temp_case, temp_variables, t_threads, t_history, t_group, t_group_test
>>>>>>> master

import django

sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


@csrf_exempt
# Method for populate counters in menu
def mainTgroup(request):
    if request.is_ajax():

        # Create First table from t_group_tet
<<<<<<< HEAD
        tmain = t_group.objects.select_related().all().select_related()
=======
        tmain = t_group.objects.select_related().all()
>>>>>>> master

        response = []

        for i in tmain:
            vallabel = {'t_ID': i.id, 't_ord': i.descr, 't_grp': i.g_prior, 't_temp': i.g_desc, 't_active': i.active,
<<<<<<< HEAD
                        't_user': str(i.owner_id)}
=======
                        't_user': str(i.user_id)}
>>>>>>> master

            response.append(vallabel)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass


@csrf_exempt
# Method for populate counters in menu
def subTgroup(request):
    if request.is_ajax():

        # Create First table from t_group_tet
        tmain = t_history.objects.filter(group_id=request.POST['tSub']).select_related()

        response = []

        for i in tmain:
            vallabel = {'t_ID': i.id, 't_data': str(i.exec_data), 't_status': i.exec_status, 't_user': str(i.user_id),
                        't_pass': i.pass_num, 't_fail': i.fail_num}

            response.append(vallabel)

        json = simplejson.dumps(response)

        return HttpResponse(
            json, content_type='application/json'
        )

    else:
        pass

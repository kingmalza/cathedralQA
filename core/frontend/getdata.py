import psycopg2
import json
import simplejson
import datetime
from django.conf import settings
from frontend.models import settings_gen
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()


def get_lic():
    cparam = getattr(settings, "LIC_PARAM", None)

    vallabel = {}

    # GET lic number and expose global
    a = settings_gen.objects.values_list('lic_num', flat=True)
    for i in a: lic_num = i

    conn = psycopg2.connect(**cparam)
    conn.autocommit = True

    cur = conn.cursor()

    s_query = "SELECT * FROM a_lic WHERE lic_num='%s';" % lic_num
    cur.execute(s_query)
    A = cur.fetchone()

    vallabel['LDATA'] = A

    conn.commit()
    cur.close()
    conn.close()

    return vallabel

    #return json.dumps(response, default = myconverter)


@csrf_exempt
def market_data(request):
    response = []
    vallabel = {}
    id_template = request.POST['idt']

    if request.is_ajax() and id_template:
        cparam = getattr(settings, "EXPORT_PARAM", None)

        conn = psycopg2.connect(**cparam)
        conn.autocommit = True

        cur = conn.cursor()

        s_query = "SELECT py_dict,store_descr_long,descr FROM aida_export WHERE id='%s';" % id_template
        cur.execute(s_query)
        A = cur.fetchone()

        vallabel['TSTRUCT'] = A[0]
        vallabel['TDESCRL'] = A[1]
        vallabel['TTITLE'] = A[2]


        response.append(vallabel)
        json = simplejson.dumps(response)
        return HttpResponse(json, content_type='application/json')
    else:
        pass
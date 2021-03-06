import psycopg2
import json
import simplejson
import datetime
from django.conf import settings
from frontend.models import settings_gen
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from json2html import *


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


def ins_ask(ask_data):
    cparam = getattr(settings, "LIC_PARAM", None)

    try:
        conn = psycopg2.connect(**cparam)
        conn.autocommit = True

        cur = conn.cursor()

        s_query = "INSERT INTO a_ask (lnum,datar,ttype,precond,steps,expres,scode,tdescr,evaluated) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','N');" % (ask_data['lnum'],str(datetime.datetime.now()),ask_data['ttype'],ask_data['precond'],ask_data['steps'],ask_data['expres'],ask_data['scode'],ask_data['tdescr'])
        cur.execute(s_query)

        conn.commit()
        cur.close()
        conn.close()

        return 'OK'
    except Exception as e:
        print("Errorrr->",e)
        return e


@csrf_exempt
def market_data(request):
    response = []
    vallabel = {}
    id_template = request.POST['idt']

    if request.is_ajax() and id_template:
        cparam = getattr(settings, "EXPORT_PARAM", None)

        #Get stripe_id from lic table if present
        sid = get_lic()

        conn = psycopg2.connect(**cparam)
        conn.autocommit = True

        cur = conn.cursor()

        s_query = "SELECT py_dict,store_descr_long,descr,adv_img,adv_desc,adv_url FROM aida_export WHERE id='%s';" % id_template
        cur.execute(s_query)
        A = cur.fetchone()
        #advanced
        #py_html = json2html.convert(json=A[0], table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
        #Basic
        py_html = json2html.convert(json=A[0])

        vallabel['TSTRUCT'] = A[0]
        vallabel['TDESCRL'] = A[1]
        vallabel['TTITLE'] = A[2]
        vallabel['ADSIMG'] = A[3]
        vallabel['ADSDESC'] = A[4]
        vallabel['ADSURL'] = A[5]
        vallabel['THTML'] = py_html
        vallabel['SID'] = sid['LDATA'][9]
        vallabel['LICN'] = sid['LDATA'][0]


        response.append(vallabel)
        json = simplejson.dumps(response)
        return HttpResponse(json, content_type='application/json')
    else:
        pass
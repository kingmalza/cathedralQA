import psycopg2
import json
import datetime
from django.conf import settings
from frontend.models import settings_gen


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

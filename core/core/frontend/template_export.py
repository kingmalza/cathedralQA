"""
Alessandro Malzanini
Methods for export template by id and save in shared DB

For export a template method is still manual:

1.comment line 25
2. from command line (locally) go to /volumes/bigdata/projects/helium/web/core and type python -m idlelib.idle (afetr accessed virtualenv)
3. from frontend.template_export import start
4. start("<template_id>")
5. When export finisch UNCOMMENT line 25
"""

# !/usr/bin/python

import psycopg2
import json
import datetime
import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from frontend.getdata import get_lic

# if launch export manual from idlelib.idle, comment this
from frontend.models import import_his, settings_gen

from django.core.mail import send_mail


class MultiDimensionalArrayEncoder(json.JSONEncoder):
    def encode(self, obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
                return {'__tuple__': True, 'items': item}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                return {key: hint_tuples(value) for key, value in item.items()}
            else:
                return item

        return super(MultiDimensionalArrayEncoder, self).encode(hint_tuples(obj))

def hinted_tuple_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    else:
        return obj


@csrf_exempt
def start(request):
    if request.is_ajax():

        #First of all check if user have stripe_id, otherwise redirect to cthedral card registration form
        ck_stripe = get_lic()

        response = []
        vallabel = {}

        if (ck_stripe['LDATA'][9]):

            id_templ = request.POST['idTempl']
            # CHANGE THESE TO pubblic IN STANDALONE MODE!!
            schema = 'helium'
            d_base = 'helium_web'

            internal = False

            connection_parameters = {
                'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
                'database': d_base,
                'user': 'kingmalza',
                'password': '11235813post',
            }

            conn = psycopg2.connect(**connection_parameters)
            conn.autocommit = True

            try:
                pydict = main(schema, id_templ, conn)

                # If this function was called from view.py temp_clone (internal) return just dict
                if internal:
                    conn.close()
                    return pydict
                # print(json.dumps(pydict, indent=4))
                rload = load_data(pydict, id_templ, schema, request.POST['tDescr'][0:200], request.POST['tDescrl'][0:700], request.POST['tCover'], request.POST['tPrice'])

                conn.close()
                vallabel['Error'] = rload
                # return HttpResponseRedirect('/tpublish/TOK/')

            except Exception as e:
                vallabel['Error'] = e
                # return HttpResponseRedirect('/tpublish/TKO/')

            response.append(vallabel)
            jsonret = simplejson.dumps(response)

            return HttpResponse(
                jsonret, content_type='application/json'
            )
        else:
            #There is no stripe_id param so i redirect to cathedral credit card registration view then page
            l_data = ck_stripe['LDATA']
            #return HttpResponseRedirect('/gocard/'+l_data[0]+'/')
            l_num = settings_gen.objects.values_list('lic_num', flat=True).get(id=1)
            vallabel['LNUM'] = l_num
            vallabel['Error'] = 'Nostripe'
            # return HttpResponseRedirect('/tpublish/TKO/')

            response.append(vallabel)
            jsonret = simplejson.dumps(response)

            return HttpResponse(
                jsonret, content_type='application/json'
            )



    else:

        pass



def main(schema, id_templ, conn, p_force=False):
    t_html = None
    t_descr = []
    t_ulib = set()
    slib = ""
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    tmain_list = []
    tcase_list = []
    tvar_list = []
    tlib_list = []
    ttk_list = []
    tpk_list = []
    # schema tab
    t_main = schema + '.frontend_temp_main'
    t_case = schema + '.frontend_temp_case'
    t_var = schema + '.frontend_temp_variables'
    t_libs = schema + '.frontend_temp_library'

    # execute our Query
    try:
        cursor.execute("SELECT * FROM " + t_main + " WHERE id= " + id_templ)

        # retrieve the records from the database
        rec_main = cursor.fetchall()
        tmain_list.append({'t_name': rec_main[0][1],
                           't_type': rec_main[0][9],
                           't_notes': rec_main[0][2],
                           't_expected': rec_main[0][5],
                           't_precond': rec_main[0][6],
                           't_steps': rec_main[0][7]})

        cursor.execute("SELECT * FROM " + t_case + " WHERE main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tcase_list.append({'tc_desr': row[1],
                               't_owner': row[3]})

        cursor.execute("SELECT * FROM " + t_var + " WHERE main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tvar_list.append({'tv_key': row[1],
                              'tv_val': row[2],
                              't_owner': row[4]})

        cursor.execute("SELECT * FROM " + t_libs + " WHERE main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tlib_list.append({'tl_type': row[1],
                              'tl_val': row[2],
                              'tl_group': row[6],
                              't_owner': row[4]
                              })

            if row[1] == 'Library': t_ulib.add(row[2])

        cursor.execute(
            "SELECT key_val, key_group, main_id_id, test_id_id, ftk.descr, ftk.owner_id FROM helium.frontend_temp_test_keywords as ftt, helium.frontend_temp_keywords as ftk WHERE ftt.key_id_id = ftk.id AND ftt.main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in reversed(rec_main):
            ttk_list.append({'tk_kval': row[0],
                             'tk_kgroup': row[1],
                             'tk_descr': row[4],
                             't_owner': row[5]
                             })

        cursor.execute(
            "SELECT t.id, t.pers_id_id, t.standard_id_id, l1.descr AS desc_l1,l2.descr AS desc_l2,t.variable_val, t.owner_id FROM helium.frontend_temp_pers_keywords t LEFT JOIN helium.frontend_temp_keywords l1 ON t.pers_id_id = l1.id LEFT JOIN helium.frontend_temp_keywords l2 ON t.standard_id_id = l2.id WHERE t.main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tpk_list.append({'tp_key1': row[3],
                             'tp_key2': row[4],
                             'tp_kval': row[5],
                             't_owner': row[6]
                             })

        # Now retreive the pid from histoy (for html)
        # cursor.execute("SELECT format('%s',html_test) FROM demo.frontend_t_history as fth WHERE fth.html_test ~* '[^a-z0-9]' AND fth.test_main_id = " + id_templ + " LIMIT 1")
        cursor.execute(
            "SELECT pid FROM helium.frontend_t_history as fth WHERE fth.test_main_id = " + id_templ + "ORDER BY id DESC LIMIT 1")
        rec_main = cursor.fetchall()
        for row in rec_main:
            t_html = str(row[0])

        #Encode json for touple dict ec
        enc = MultiDimensionalArrayEncoder()
        ttk_list_enc = enc.encode(ttk_list).replace("'","")
        tmain_list_enc = enc.encode(tmain_list).replace("'", "")
        tcase_list_enc = enc.encode(tcase_list).replace("'", "")
        tvar_list_enc = enc.encode(tvar_list).replace("'", "")
        tlib_list_enc = enc.encode(tlib_list).replace("'", "")
        tpk_list_enc = enc.encode(tpk_list).replace("'", "")

        j_dict = {'t_main': tmain_list_enc, 't_case': tcase_list_enc, 't_vars': tvar_list_enc, 't_libs': tlib_list_enc,
                  't_ttk': ttk_list_enc, 't_tpk': tpk_list_enc}


        t_descr.append(tmain_list[0]['t_name'])
        t_descr.append(tmain_list[0]['t_notes'])
        for i in list(t_ulib):
            slib = slib + i + ";"
        t_descr.append(slib)
        l_ret = [j_dict, t_html, t_descr]
        # print(json.dumps(j_dict, indent=4))
        cursor.close()
        conn.close()

        return l_ret


    except Exception as e:
        print("Error1: ", e)

    cursor.close()


def load_data(p_struct, id_templ, schema, sdescr, sdescrl, scover, sprice, d_base='helium_ai'):
    r_msg = ""

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': d_base,
        'user': 'kingmalza',
        'password': '11235813post',
    }

    l_num = settings_gen.objects.values_list('lic_num', flat=True).get(id=1)
    ex_id = l_num + "_" + str(id_templ)
    now = datetime.datetime.now()
    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True
    # First check if original_id already exist (meand that template was already charged)
    # IMPORTANT IN FUTURE IF I WHANT  THAT ANYONE CAN PUBLISH YOUR TEMPLATE LEAVE THIS CHECK
    ck_cursor = conn.cursor()
    ck_cursor.execute("SELECT * FROM public.aida_export as aie WHERE upper(aie.export_id) = '" + ex_id.upper() + "' AND (aie.status = 'A' OR aie.status = 'P') ")
    ck_old = ck_cursor.fetchone()
    if not ck_old and p_struct[1]:
        try:
            b_cursor = conn.cursor()
            b_cursor.execute(
                "insert into aida_export (py_dict,html_test, export_id, descr, notes, u_libs, dt, status, store_descr, store_descr_long, coverage, credits) values ('" + json.dumps(p_struct[0], default=hinted_tuple_hook) + "','" + p_struct[1] + "', '" + ex_id + "', '" + p_struct[2][0] + "', '" +p_struct[2][1] + "', '" + p_struct[2][2] + "', '" + str(
                    now) + "', 'P', '" + sdescr + "', '" + sdescrl + "', '" + scover + "', " + sprice + ");")
            b_cursor.close()
            r_msg = "OK"
        except Exception as e:
            print("Error Insert: ", e)
            r_msg = e
    else:
        r_msg = "BUSY"

    ck_cursor.close()

    return r_msg


@csrf_exempt
def ret_list(request, t_status="A"):
    response = []
    alvar = "N"

    l_num = settings_gen.objects.values_list('lic_num', flat=True).get(id=1)
    try:
        t_status = str(request.POST['t_status'])
    except:
        pass

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': 'helium_ai',
        'user': 'kingmalza',
        'password': '11235813post',
    }

    # First retreive all template already imported by user
    alist = []
    alimp = import_his.objects.all()
    for x in alimp: alist.append(x.imp_template)

    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True
    cursor = conn.cursor()

    #Se chiamata da marketplace deve estrarre tutti i template pubblicati in stato attivo mentre se chiamata per popolare la tabella nella sessione export deve chiamare tutti i template con quella licenza, se in alternativa dalla maschera della lista dei template viene selezionato uno in stato R (rejected) viene chiamata quest funzione passando id del template per estrarre le note di disapprovazione
    if t_status == "A":
        s_exec = "SELECT * FROM public.aida_export WHERE status = 'A' ORDER BY id DESC"
    elif t_status == "E":
        s_exec = "SELECT * FROM public.aida_export WHERE export_id like '"+l_num+"%' ORDER BY id DESC"
    else:
        s_exec = "SELECT * FROM public.aida_export WHERE id =" + t_status

    cursor.execute(s_exec)
    rec_tot = cursor.fetchall()
    for row in rec_tot:
        var_dtend = None
        if row[14]: var_dtend = str("{:%Y-%m-%d %H:%M}".format(row[14]))

        if row[1] in alist: alvar = "Y"
        response.append({'rl_py': row[0],
                         'rl_id': row[1],
                         'rl_html': row[2],
                         'rl_desc': row[3],
                         'rl_notes': row[4],
                         'rl_libs': row[5],
                         'rl_ndown': row[6],
                         'rl_exps': row[8],
                         'rl_view': row[8],
                         'rl_dt': str("{:%Y-%m-%d %H:%M}".format(row[9])),
                         'rl_dt_end': var_dtend,
                         'rl_sdescr': row[11],
                         'rl_sdescrl': row[16],
                         'rl_scover': row[12],
                         'rl_scredits': row[13],
                         'rl_status': row[10],
                         'rl_already': alvar,
                         'rl_staffn': row[15]
                         })
        alvar = "N"

    cursor.close()
    conn.close()

    json = simplejson.dumps(response)

    return HttpResponse(
        json, content_type='application/json'
    )

@csrf_exempt
def stop_templ(request):

    id_t = request.POST['idTemp']
    now = datetime.datetime.now()
    response = []
    vallabel={'res': 'Something went wrong, try reloading the page.',}

    if id_t:
        connection_parameters = {
            'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
            'database': 'helium_ai',
            'user': 'kingmalza',
            'password': '11235813post',
        }

        conn = psycopg2.connect(**connection_parameters)
        conn.autocommit = True
        cursor = conn.cursor()

        if request.POST['atype'] == 'end':
            s_exec = "UPDATE public.aida_export SET status='E', dt_end='"+str(now)+"' WHERE ID="+id_t+""
        else:
            s_exec = "UPDATE public.aida_export SET status='P', store_descr='" + request.POST['tdescr'] + "', coverage='"+request.POST['tcover']+"', credits="+request.POST['tcredit']+" WHERE ID=" + id_t + ""

        try:
            cursor.execute(s_exec)

            cursor.close()
            conn.close()
        except Exception as e:
            vallabel = {'res': e, }

        vallabel = {'res': 'The changes have been made correctly.', }


    response.append(vallabel)
    json = simplejson.dumps(response)

    return HttpResponse(
        json, content_type='application/json'
    )


if __name__ == "__main__":
    start("1")

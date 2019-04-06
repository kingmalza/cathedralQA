
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

#!/usr/bin/python

import psycopg2
import json
import datetime
import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#if launch export manual from idlelib.idle, comment this
from frontend.models import import_his



def start(id_templ, schema='helium', d_base='helium_web', internal = False):

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': d_base,
        'user': 'kingmalza',
        'password': '11235813post',
    }

    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True

    pydict = main(schema, id_templ, conn)

    #If this function was called from view.py temp_clone (internal) return just dict
    if internal:
        conn.close()
        return pydict
    #print(json.dumps(pydict, indent=4))
    load_data(pydict,id_templ, schema)

    conn.close()




def main(schema, id_templ, conn, p_force=False):

    t_html = None
    t_descr = []
    t_ulib = set()
    slib = ""
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    tmain_list = []
    tcase_list= []
    tvar_list = []
    tlib_list = []
    ttk_list = []
    tpk_list = []
    #schema tab
    t_main = schema+'.frontend_temp_main'
    t_case = schema+'.frontend_temp_case'
    t_var = schema + '.frontend_temp_variables'
    t_libs = schema + '.frontend_temp_library'

    # execute our Query
    try:
        cursor.execute("SELECT * FROM "+t_main+" WHERE id= "+id_templ)


        # retrieve the records from the database
        rec_main = cursor.fetchall()
        tmain_list.append({'t_name' : rec_main[0][1],
                            't_type' : rec_main[0][9],
                           't_notes' : rec_main[0][2],
                           't_expected' : rec_main[0][5],
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

        cursor.execute("SELECT key_val, key_group, main_id_id, test_id_id, ftk.descr, ftk.owner_id FROM helium.frontend_temp_test_keywords as ftt, helium.frontend_temp_keywords as ftk WHERE ftt.key_id_id = ftk.id AND ftt.main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in reversed(rec_main):
            ttk_list.append({'tk_kval': row[0],
                            'tk_kgroup': row[1],
                            'tk_descr': row[4],
                            't_owner': row[5]
                            })


        cursor.execute("SELECT t.id, t.pers_id_id, t.standard_id_id, l1.descr AS desc_l1,l2.descr AS desc_l2,t.variable_val, t.owner_id FROM helium.frontend_temp_pers_keywords t LEFT JOIN helium.frontend_temp_keywords l1 ON t.pers_id_id = l1.id LEFT JOIN helium.frontend_temp_keywords l2 ON t.standard_id_id = l2.id WHERE t.main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tpk_list.append({'tp_key1': row[3],
                            'tp_key2': row[4],
                            'tp_kval': row[5],
                            't_owner': row[6]
                            })


        #Now retreive the pid from histoy (for html)
        #cursor.execute("SELECT format('%s',html_test) FROM demo.frontend_t_history as fth WHERE fth.html_test ~* '[^a-z0-9]' AND fth.test_main_id = " + id_templ + " LIMIT 1")
        cursor.execute("SELECT pid FROM helium.frontend_t_history as fth WHERE fth.test_main_id = " + id_templ + "ORDER BY id DESC LIMIT 1")
        rec_main = cursor.fetchall()
        for row in rec_main:
            t_html = str(row[0])

        j_dict = {'t_main':tmain_list, 't_case':tcase_list, 't_vars':tvar_list, 't_libs':tlib_list, 't_ttk':ttk_list, 't_tpk':tpk_list}
        t_descr.append(tmain_list[0]['t_name'])
        t_descr.append(tmain_list[0]['t_notes'])
        for i in list(t_ulib):
            slib = slib+i+";"
        t_descr.append(slib)
        l_ret = [j_dict,t_html,t_descr]
        #print(json.dumps(j_dict, indent=4))
        cursor.close()
        conn.close()

        return l_ret


    except Exception as e:
        print("Error1: ",e)


    cursor.close()



def load_data(p_struct, id_templ, schema, d_base='helium_ai'):

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': d_base,
        'user': 'kingmalza',
        'password': '11235813post',
    }

    ex_id = schema+"_"+str(id_templ)
    now = datetime.datetime.now()
    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True
    #First check if original_id already exist (meand that template was already charged)
    #IMPORTANT IN FUTURE IF I WHANT  THAT ANYONE CAN PUBLISH YOUR TEMPLATE LEAVE THIS CHECK
    ck_cursor = conn.cursor()
    ck_cursor.execute("SELECT * FROM public.aida_export as aie WHERE upper(aie.export_id) = '" + ex_id.upper()+"'")
    ck_old = ck_cursor.fetchone()
    if not ck_old and p_struct[1]:
        try:
            b_cursor = conn.cursor()
            b_cursor.execute("insert into aida_export (py_dict,html_test, export_id, descr, notes, u_libs, dt) values ('" + json.dumps(p_struct[0]) + "','"+p_struct[1]+"', '"+ex_id+"', '"+p_struct[2][0]+"', '"+p_struct[2][1]+"', '"+p_struct[2][2]+"', '"+str(now)+"');")
            b_cursor.close()
        except Exception as e:
            print("Error Insert: ",e)
    else:
        print("TEMPLATE ALREADY UPLOADED OR HTML NOT GENERATED! No data was inserted into table")

    ck_cursor.close()


@csrf_exempt
def ret_list(request):
    response = []
    alvar = "N"

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': 'helium_ai',
        'user': 'kingmalza',
        'password': '11235813post',
    }


    #First retreive all template already imported by user
    alist = []
    alimp = import_his.objects.all()
    for x in alimp: alist.append(x.imp_template)

    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM public.aida_export ORDER BY id DESC")
    rec_tot = cursor.fetchall()
    for row in rec_tot:
        if row[1] in alist: alvar = "Y"
        response.append({'rl_py': row[0],
                         'rl_id': row[1],
                         'rl_html': row[2],
                         'rl_desc': row[3],
                         'rl_notes': row[4],
                         'rl_libs': row[5],
                         'rl_ndown': row[6],
                         'rl_exps': row[8],
                         'rl_view': row[9],
                         'rl_dt': str(row[10]),
                            'rl_already': alvar
                         })
        alvar="N"


    cursor.close()
    conn.close()

    json = simplejson.dumps(response)
    return HttpResponse(
        json, content_type='application/json'
    )


if __name__ == "__main__":
    start("1")

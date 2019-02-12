
"""
Alessandro Malzanini
Methods for export template by id and save in shared DB
"""

#!/usr/bin/python
import sys
import os
import django
import psycopg2
import json
from rsthtml.rst import PrepareRst as pr
from rsthtml.rst import MakeRst as mr

sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

def start(id_templ, d_base='helium_web'):

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': d_base,
        'user': 'kingmalza',
        'password': '11235813post',
    }
  
    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True

    pydict = main('demo', id_templ, conn)
    #print(json.dumps(pydict, indent=4))
    load_data(pydict,id_templ)

    conn.close()


    
       
def main(schema, id_templ, conn, p_force=False):


    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    tmain_list = []
    tcase_list= []
    tvar_list = []
    tlib_list = []
    ttk_list = []
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
                           't_notes' : rec_main[0][2],
                           't_expected' : rec_main[0][5],
                           't_precond': rec_main[0][6],
                           't_steps': rec_main[0][7]})


        cursor.execute("SELECT * FROM " + t_case + " WHERE main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tcase_list.append({'tc_desr': row[1]})


        cursor.execute("SELECT * FROM " + t_var + " WHERE main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tvar_list.append({'tv_key': row[1],
                              'tv_val': row[2],
                               })


        cursor.execute("SELECT * FROM " + t_libs + " WHERE main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            tlib_list.append({'tl_type': row[1],
                            'tl_val': row[2],
                            'tl_group': row[6]
                            })


        cursor.execute("SELECT key_val, key_group, main_id_id, test_id_id, ftk.descr FROM demo.frontend_temp_test_keywords as ftt, demo.frontend_temp_keywords as ftk WHERE ftt.key_id_id = ftk.id AND ftt.main_id_id = " + id_templ)
        rec_main = cursor.fetchall()
        for row in rec_main:
            ttk_list.append({'tk_kval': row[0],
                            'tk_kgroup': row[1],
                            'tk_descr': row[4]
                            })


        j_dict = {'t_main':tmain_list, 't_case':tcase_list, 't_vars':tvar_list, 't_libs':tlib_list, 't_ttk':ttk_list}
        #print(json.dumps(j_dict, indent=4))
        cursor.close()
        conn.close()

        return j_dict

            
    except Exception as e:
        print("Error1: ",e)
    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    #pprint.pprint(records)

    cursor.close()



def load_data(p_struct, id_templ, d_base='helium_ai'):

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': d_base,
        'user': 'kingmalza',
        'password': '11235813post',
    }

    rstcur = load_rst(id_templ)
    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True
    try:
        b_cursor = conn.cursor()
        b_cursor.execute("insert into aida_export (py_dict, rst_tc,rst_tk, rst_ts) values ('" + json.dumps(p_struct) + "','"+rstcur['r_settings']+"', '"+rstcur['r_case']+"', '"+rstcur['r_key']+"', 'bbb');")
        b_cursor.close()
    except Exception as e:
        print("Error Insert: ",e)


def load_rst(mainID):

    # Now i have toretreive html for display in preview div
    # ------------RST AND HTML PREPARATION--------------------------

    # 1 - Table preparation
    table_case = pr(mainID, "TC")
    table_key = pr(mainID, "TK")
    table_setting = pr(mainID, "TS")
    # In this case take the default variables
    # table_var = pr(request.POST['mainID'], "TV")

    # 2 - MakeRst
    mrr1 = mr(table_setting.rst)
    mrr3 = mr(table_case.rst)
    mrr4 = mr(table_key.rst)

    # 3 - Clean string returned for display roperly
    cmr1 = mrr1.rstab.replace("-", "").replace("+", "")
    cmr2 = mrr3.rstab.replace("-", "").replace("+", "")
    cmr3 = mrr4.rstab.replace("-", "").replace("+", "")
    # ------------------------------------------------------------

    valrst = {'r_settings': cmr1, 'r_case': cmr2, 'r_key': cmr3}
    return valrst


if __name__ == "__main__":
    start(1)

"""
Alessandro Malzanini
Methods for export template by id and save in shared DB
"""

#!/usr/bin/python
import psycopg2
import datetime
import json
import boto3
from botocore.exceptions import ClientError
import stripe

glob_riep = {}
glob_amount=0

def start(id_templ):

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': 'helium_web',
        'user': 'kingmalza',
        'password': '11235813post',
    }
  
    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True

    main('demo', id_templ, conn)

    conn.close()

    global glob_amount, glob_riep
    #print(glob_amount, glob_riep)

    
       
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
        print(j_dict)
        cursor.close()
        conn.close()
            
    except Exception as e:
        print("Error1: ",e)
    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    #pprint.pprint(records)

    cursor.close()


if __name__ == "__main__":
    start(1)
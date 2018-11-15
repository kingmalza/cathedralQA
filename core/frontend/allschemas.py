#!/usr/bin/python
import psycopg2
import pprint
import datetime


def main(schema):

    schema = 'demo'
    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': 'helium_web',
        'user': 'kingmalza',
        'password': '11235813post',
    }

    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True


    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    #schema tab
    s_tab = schema+'.frontend_settings_gen'
    t_tab = schema+'.frontend_t_time'
    h_tab = schema + '.frontend_t_history'
    p_tab = schema + '.frontend_bill_his'
    # execute our Query
    try:
        cursor.execute("SELECT * FROM "+s_tab)


        # retrieve the records from the database
        records = cursor.fetchall()
        istrial = records[0][3]
        paidfeed = records[0][4]
        plantype = records[0][5]
        tot_amount = 0
        if not istrial and plantype == 'ondemand':
            print('non è un trial quindi picia')
            #Check las payement data
            p_cursor = conn.cursor()
            t_cursor = conn.cursor()
            try:
                p_cursor.execute("SELECT bill_data FROM " + p_tab+" WHERE  id=(select max(id) from "+p_tab+")")
                pdata = cursor.fetchall()
                t_cursor.execute("SELECT elapsed_t,exec_data FROM " + t_tab+","+h_tab+" WHERE "+t_tab+".history_main_id="+h_tab+".id AND "+h_tab+".exec_data >= "+pdata)
            except Exception:
                t_cursor.execute("SELECT elapsed_t,exec_data FROM " + t_tab+","+h_tab+" WHERE "+t_tab+".history_main_id="+h_tab+".id")

            row = t_cursor.fetchone()
            while row:
                cdata = ""
                #Check data
                if row[1].date() == cdata:
                #Test run append in the same day
                    pass
                else:
                #test append in another day
                    pass

                print(row[1].time().hour)
                row = t_cursor.fetchone()

    except Exception as e:
        print(e)
    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    #pprint.pprint(records)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
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
                t_cursor.execute("SELECT elapsed_t,stop_data FROM " + t_tab +" WHERE "+h_tab+".stop_data >= "+pdata)
            except Exception:
                t_cursor.execute("SELECT elapsed_t,stop_data FROM " + t_tab)

            row = t_cursor.fetchone()
            cdata = ""
            ctime = ""
            while row:
                #Check data
                if row[1].date() == cdata:
                    #Test run append in the same day
                    #i have to check time
                    if row[1].time().hour > ctime:
                        husage = (int(row[0]/3600)+1)*paidfeed
                        tot_amount += husage
                        ctime = row[1].time().hour
                    
                else:
                    #test append in another day
                    #check how mutch hours of usage
                    husage = (int(row[0]/3600)+1)*paidfeed
                    tot_amount += husage
                    cdata = row[1].date()
                    ctime = row[1].time().hour
                    

                row = t_cursor.fetchone()
            #Insert data into bill table
            b_cursor = conn.cursor()
            b_cursor.execute("insert into "+p_tab+"(bill_data,bill_amount, bill_errors) values ('"+str(datetime.datetime.now())+"',"+str(tot_amount)+",'');")
            print("Total to pay is: ",tot_amount)
            
    except Exception as e:
        print(e)
    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    #pprint.pprint(records)

    cursor.close()
    p_cursor.close()
    t_cursor.close()
    b_cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
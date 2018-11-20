
"""
Alessandro Malzanini
TODO:
-Integrate with stripe
"""

#!/usr/bin/python
import psycopg2
import pprint
import datetime
import json
import smtplib
import boto3
from botocore.exceptions import ClientError

glob_riep = {}
glob_amount=0

def start():

    connection_parameters = {
        'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'database': 'helium_web',
        'user': 'kingmalza',
        'password': '11235813post',
    }
  
    conn = psycopg2.connect(**connection_parameters)
    conn.autocommit = True

    #Get list of schemas
    cursor = conn.cursor()
    cursor.execute("select schema_name from information_schema.schemata")
    schemas = cursor.fetchone()
    while schemas:
        exlist = ['pg_catalog','information_schema','public']
        if schemas[0] not in exlist:
            main(schemas[0].strip(),conn)
        schemas = cursor.fetchone()

    cursor.close()
    conn.close()

    global glob_amount, glob_riep
    print(glob_amount, glob_riep)
    
    #login to server and send email to me
    sendemail(glob_amount, json.dumps(glob_riep))
    
       
def main(schema,conn):


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

            p_cursor.execute("SELECT bill_data FROM " + p_tab+" WHERE  id=(select max(id) from "+p_tab+")")
            pdata = p_cursor.fetchall()
            if pdata:
                #Now i have to check if 30 day was passed from last billing
                d0 = datetime.date.today().strftime("%Y-%m-%d")
                d0 = datetime.datetime.strptime(d0, '%Y-%m-%d')
                d1 = datetime.datetime.strptime(str(pdata[0][0].date()), '%Y-%m-%d')
                delta = (d0 - d1)

                if delta.days > 30:
                    t_cursor.execute("SELECT elapsed_t,stop_data FROM " + t_tab + " WHERE stop_data >= '" + str(pdata[0][0]) + "'")
                else:
                    #Not so good, but useful for have a returned blank t_cursor execution
                    t_cursor.execute("SELECT elapsed_t,stop_data FROM " + t_tab + " WHERE stop_data < '2002-11-02 11:00:00'")
            else:
                t_cursor.execute("SELECT elapsed_t,stop_data FROM " + t_tab)

            row = t_cursor.fetchone()
            cdata = ""
            ctime = ""

            while row:
                print(row[1])
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
            print('Numero di linee->',t_cursor.rowcount)
            if t_cursor.rowcount > 0:
                b_cursor = conn.cursor()
                b_cursor.execute("insert into "+p_tab+"(bill_data,bill_amount, bill_errors) values ('"+str(datetime.datetime.now())+"',"+str(tot_amount)+",'');")
                b_cursor.close()
                # HERE THE INTEGRATION WITH STRIPE!!!

            print("Total to pay is: ", tot_amount)

            global glob_amount, glob_riep
            glob_amount += tot_amount
            glob_riep.update({schema: tot_amount})

            p_cursor.close()
            t_cursor.close()
    except Exception as e:
        print(e)
    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    #pprint.pprint(records)

    cursor.close()

    
def sendemail(gam,griep):
    SENDER = "King Malza <kingmalza@comunicame.it>"
    RECIPIENT = "alessandro.malzanini@gmail.com"
    #CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "eu-west-1"
    BODY_HTML = "<html><head></head><body><h1>Aida schemas earn details</h1><p>"+griep+"</p></body></html>"
    BODY_TEXT = griep
    SUBJECT = "Today you earn: "+str(gam)+" euros!"
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
        # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
if __name__ == "__main__":
    start()
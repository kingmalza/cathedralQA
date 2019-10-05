#https://docs.aws.amazon.com/en_us/lambda/latest/dg/vpc-rds.html

import sys
import logging
import pymysql
import datetime
import time
from django.conf import settings
#rds settings
rds_host = getattr(settings, "SENDY_PARAM", None)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host['db_host'], user=rds_host['db_username'], passwd=rds_host['db_password'], db=rds_host['db_name'], connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to Internet....Quit")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event):
    item_count = 0
    l_user = '1'
    l_email = event['email']

    with conn.cursor() as cur:

        list_type = '2'
        #Check if the registration is for a cstomer, then search address in demo lins and disable that
        if event['evtype'] == 'customer_activate':
            list_type = '3'
            try:
                cur.execute("UPDATE subscribers SET list = '3' WHERE email = '" + event['email'] + "'")
            except:
                print('Error in sendy activation')

        else:
            #In customer if there is already an equal address dont do anything and return an error
            cur.execute("select * from subscribers where list = '2' and email = '"+event['email']+"'")
            for row in cur:
                item_count += 1
            if item_count == 0:
                cur.execute("insert into subscribers (userid, name, email, custom_fields, list, timestamp, join_date, gdpr, country) values('" + l_user + "', '" + l_fname + "', '" + l_email + "', '" + l_cus + "', '" + list_type + "', '" + t_stamp + "', +'" + d_now + "', '2', '" + l_country + "')")



        conn.commit()


    conn.commit()

    return str(item_count)

import psycopg2
import socket


def connect_db(cname, cuser, chost, cpassword, null=None):
    try:
        conn = psycopg2.connect("dbname = %s user=%s host=%s password=%s" % (cname, cuser, chost, cpassword))
    except:
        conn = null
<<<<<<< HEAD
        print ("I am unable to connect to the database")
=======
        print "I am unable to connect to the database"
>>>>>>> master

    return conn


def return_ip():
    return socket.gethostbyname(socket.gethostname())

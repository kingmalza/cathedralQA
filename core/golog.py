import sys
from robot import run as run_log

def create_log(fp,od):
    run_log(fp, outputdir=od, level='TRACE')


if __name__ == "__main__":

    create_log(sys.argv[1],sys.argv[2])
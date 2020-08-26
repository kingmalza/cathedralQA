import sys
import os
import functools
import django
import errno
<<<<<<< HEAD
import logging
from functools import reduce
from itertools import chain
from docutils.core import publish_string
from robot import run as run_test
#from robot import run_cli
import threading
from django.db.models import Count
from django.db.models import Q
from backend.models import temp_keywords, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords
=======
from functools import reduce
from itertools import chain
from docutils.core import publish_string
from robot import run as run_test, run_cli
import threading
from django.db.models import Count
from django.db.models import Q
from frontend.models import temp_test_keywords, temp_pers_keywords, temp_library, temp_variables
>>>>>>> master

sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


class PrepareRst:
    def __init__(self, test_id, t_type, log=False):
        self.rst = self.mainprep(test_id, t_type)

    # route to correct prep method locking at t_type
    # TC -> TestCase
    # TK -> Keywords
    # TS -> Setting
    # TV -> Variables

    @staticmethod
    def notNone(s):
        if s == "None":
            return ""
        return str(s)

    def ckDec(func):
        @functools.wraps(func)
        def wrapper(test_id, t_type):
            tab_lib = temp_library.objects.filter(main_id=test_id)
            tslist = [["Settings", ""]]
            if tab_lib.count() == 0:
                tslist.append(["", ""])
            return func(tab_lib, tslist)

        return wrapper

    def mainprep(self, test_id, t_type):
        routedict = {"TC": "self.tc_prep(test_id)", "TK": "self.tk_prep(test_id)", "TS": "self.ts_prep(test_id)",
                     "TV": "self.tv_prep(test_id)"}
        vret = eval(routedict[t_type])
        return vret


    #Clean method for testCase in multiple mode
    @staticmethod
    def tc_clean(t_ext):
        nstring = ''
        noast = ''
        for char in t_ext:
            if char == '-' and noast != 'N':
                char.replace('-', "")
            else:
                noast = 'N'
                nstring = nstring + char

        return nstring


    # TestCase rst prep method
    def tc_prep(self, test_id):
<<<<<<< HEAD
        try:
            maxpar = temp_test_keywords.objects.filter(main_id=test_id).values('key_id','key_group').annotate(total=Count('key_id')).order_by('-total').first()
            maxMax = maxpar['total'] + 1

            # Part1 list creation
            count = 0
            ltouple = ()
            l1 = ["Test Case"]
            while count < maxMax:
                l1.append("")
                count += 1
            ltouple += (l1,)

            # Query for extract keywords, values
            kv = temp_test_keywords.objects.filter(main_id=test_id).order_by('my_order', 'id').select_related()

            vkey = ""
            skey = ""
            vcont = ""
            l = []
            for r in kv.iterator():
                # IMPORTANT: Here use __repr__ instead of __str__ because of the formattation in models for admin panel
                # visualization

                if vkey != repr(r.test_id):
                    if l:
                        # Modified for empty spaces
                        for i in range(maxMax - len(l) + 1):
                            l.append("")
                        ltouple += (l,)
                        l = []
                    l.append(repr(r.test_id))

                    if r.key_group is not None:
                        l.append(str(r.key_group)+str(r.key_id))
                    else:
                        l.append(str(r.key_id))
                    vvar = self.notNone(str(r.key_val))
                    l.append(vvar)

                else:
                    # check if standard_id is the same or diff for create another row"
                    if r.key_group is not None:
                        vcont = str(r.key_group) + str(r.key_id)
                    else:
                        vcont = str(r.key_id)
                    if skey != vcont:
                        if l:
                            # Modified for empty spaces
                            for i in range(maxMax - len(l) + 1):
                                l.append("")
                            ltouple += (l,)
                            l = []
                        l.append("")
                        if r.key_group is not None:
                            l.append(str(r.key_group) + str(r.key_id))
                        else:
                            l.append(str(r.key_id))
                        vvar = self.notNone(str(r.key_val))
                        l.append(vvar)

                    else:
                        vvar = self.notNone(str(r.key_val))
                        l.append(vvar)

                vkey = repr(r.test_id)
                if r.key_group is not None:
                    skey = str(r.key_group) + str(r.key_id)
                else:
                    skey = str(r.key_id)

            # Last check after for cycle finished if l is not null (difference in last loop)
            if l:
                # Modified for empty spaces
                for i in range(maxMax - len(l) + 1):
                    l.append("")
                ltouple += (l,)

                tclist = [x for x in ltouple]
                #Normalize the list
                for i in range(0,len(tclist)):
                    tclist[i][1] = self.tc_clean(tclist[i][1])
        except Exception as e:
            tclist = [['Test Case', '', ''], ['noTest', '', '']]

        return tclist



    # Keywords rst prep method
    def tk_prep(self, test_id):
        try:
            maxpar = temp_pers_keywords.objects.filter(main_id=test_id).values('key_id','key_group').annotate(total=Count('key_id')).order_by('-total').first()
            maxMax = maxpar['total'] + 1

            # Part1 list creation
            count = 0
            ltouple = ()
            l1 = ["Keywords"]
            while count < maxMax:
                l1.append("")
                count += 1
            ltouple += (l1,)

            # Query for extract keywords, values
            kv = temp_pers_keywords.objects.filter(main_id=test_id).order_by('my_order', 'id').select_related()

            vkey = ""
            skey = ""
            vcont = ""
            l = []
            for r in kv.iterator():
                # IMPORTANT: Here use __repr__ instead of __str__ because of the formattation in models for admin panel
                # visualization

                if vkey != repr(r.key_descr):
=======
        maxpar = temp_test_keywords.objects.filter(main_id=test_id).values('key_id').annotate(
            total=Count('key_id')).order_by('-total').first()
        print("internat test_id ", maxpar)
        maxMax = maxpar['total'] + 1

        # Part1 list creation
        count = 0
        ltouple = ()
        l1 = ["Test Case"]
        while count < maxMax:
            l1.append("")
            count += 1
        ltouple += (l1,)

        # Query for extract keywords, values
        kv = temp_test_keywords.objects.filter(main_id=test_id).order_by('id').select_related()

        vkey = ""
        skey = ""
        vcont = ""
        l = []
        for r in kv.iterator():
            # IMPORTANT: Here use __repr__ instead of __str__ because of the formattation in models for admin panel
            # visualization
            if vkey != repr(r.test_id):
                if l:
                    # Modified for empty spaces
                    for i in range(maxMax - len(l) + 1):
                        l.append("")
                    ltouple += (l,)
                    l = []
                l.append(repr(r.test_id))

                if r.key_group is not None:
                    l.append(str(r.key_group)+str(r.key_id))
                else:
                    l.append(str(r.key_id))
                vvar = self.notNone(str(r.key_val))
                l.append(vvar)

            else:
                # check if standard_id is the same or diff for create another row"
                if r.key_group is not None:
                    vcont = str(r.key_group) + str(r.key_id)
                else:
                    vcont = str(r.key_id)
                if skey != vcont:
>>>>>>> master
                    if l:
                        # Modified for empty spaces
                        for i in range(maxMax - len(l) + 1):
                            l.append("")
                        ltouple += (l,)
                        l = []
<<<<<<< HEAD
                    l.append(str(r.key_descr))

                    if r.key_group is not None:
                        l.append(str(r.key_group)+str(r.key_id))
=======
                    l.append("")
                    if r.key_group is not None:
                        l.append(str(r.key_group) + str(r.key_id))
>>>>>>> master
                    else:
                        l.append(str(r.key_id))
                    vvar = self.notNone(str(r.key_val))
                    l.append(vvar)

                else:
<<<<<<< HEAD
                    # check if standard_id is the same or diff for create another row"
                    if r.key_group is not None:
                        vcont = str(r.key_group) + str(r.key_id)
                    else:
                        vcont = str(r.key_id)
                    if skey != vcont:
                        if l:
                            # Modified for empty spaces
                            for i in range(maxMax - len(l) + 1):
                                l.append("")
                            ltouple += (l,)
                            l = []
                        l.append("")
                        if r.key_group is not None:
                            l.append(str(r.key_group) + str(r.key_id))
                        else:
                            l.append(str(r.key_id))
                        vvar = self.notNone(str(r.key_val))
                        l.append(vvar)

                    else:
                        vvar = self.notNone(str(r.key_val))
                        l.append(vvar)

                vkey = repr(r.key_descr)
                if r.key_group is not None:
                    skey = str(r.key_group) + str(r.key_id)
                else:
                    skey = str(r.key_id)

            # Last check after for cycle finished if l is not null (difference in last loop)
            if l:
                # Modified for empty spaces
                for i in range(maxMax - len(l) + 1):
                    l.append("")
                ltouple += (l,)

                tklist = [x for x in ltouple]
                #Normalize the list
                for i in range(0,len(tklist)):
                    tklist[i][1] = self.tc_clean(tklist[i][1])
        except Exception as e:
            logging.exception("Exception occurred")
            tklist = [['Keywords', '', ''], ['', '', '']]

        return tklist

    """
    -->OLD METHOD FOR OLS tmp_pers_keyords MODEL<--
    # Keywords rst prep method
=======
                    print('r_kry->->->', r.key_val,r.key_group)
                    vvar = self.notNone(str(r.key_val))
                    l.append(vvar)

            vkey = repr(r.test_id)
            if r.key_group is not None:
                skey = str(r.key_group) + str(r.key_id)
            else:
                skey = str(r.key_id)

        # Last check after for cycle finished if l is not null (difference in last loop)
        if l:
            # Modified for empty spaces
            for i in range(maxMax - len(l) + 1):
                l.append("")
            ltouple += (l,)

            tclist = [x for x in ltouple]
            #Normalize the list
            for i in range(0,len(tclist)):
                tclist[i][1] = self.tc_clean(tclist[i][1])
                print('TCL1-->',tclist[i][1])
            print('TCLIST-->',tclist)
            return tclist

    # Keywords rst prep method

>>>>>>> master
    def tk_prep(self, test_id):
        # Define max variable for pers and standard keywords
        maxper = temp_pers_keywords.objects.filter(Q(main_id=test_id) & Q(pers_id__isnull=False)).values(
            'pers_id').annotate(total=Count('variable_val')).order_by('-total').first()
        maxstd = temp_pers_keywords.objects.filter(Q(main_id=test_id) & Q(standard_id__isnull=False)).values(
            'standard_id').annotate(total=Count('variable_val')).order_by('-total').first()

        maxP = 0
        maxS = 0
        if maxper: maxP = maxper['total'] + 1
        if maxstd: maxS = maxstd['total'] + 1
        maxMax = maxP
        if maxS > maxP: maxMax = maxS

        count = 0
        ltouple = ()
        l1 = ["Keywords"]
        while count < maxMax:
            l1.append("")
            count += 1
        ltouple += (l1,)

        # Part2
        kt = temp_pers_keywords.objects.filter(main_id=test_id).order_by('id').select_related()

        vkey = ""
        skey = ""
        l = []

        for r in kt.iterator():

            if vkey != str(r.pers_id):
                if l:
                    # Modified for empty spaces
                    for i in range(maxMax - len(l) + 1):
                        l.append("")
                    ltouple += (l,)
                    l = []
                l.append(str(r.pers_id))
                l.append(str(r.standard_id))
                # IMPORTANT: Here use __repr__ instead of __str__ because of the formattation in models for admin
                # panel visualization
                #vvar = self.notNone(repr(r.variable_id))
                #vvar = str(self.notNone(repr(r.variable_val)))
                if r.variable_val:
                    vvar = r.variable_val
                else:
                    vvar = 'noVal'
                l.append(vvar)

            else:
                # check if standard_id is the same or diff for create another row"
                if r.variable_val:
                    vvar = r.variable_val
                else:
                    vvar = 'noVal'
                if skey != str(r.standard_id):
                    if l:
                        # Modified for empty spaces
                        for i in range(maxMax - len(l) + 1):
                            l.append("")
                        ltouple += (l,)
                        l = []
                    l.append("")
                    l.append(str(r.standard_id))
                    #vvar = self.notNone(repr(r.variable_id))
                    #vvar = str(self.notNone(repr(r.variable_val)))

                    l.append(vvar)

                else:
                    #vvar = self.notNone(repr(r.variable_id))
                    #vvar = str(self.notNone(repr(r.variable_val)))
                    l.append(vvar)

            vkey = str(r.pers_id)
            skey = str(r.standard_id)

        # Last check after for cycle finished if l is not null (difference in last loop)
        if l:
            # Modified for empty spaces
            for i in range(maxMax - len(l) + 1):
                l.append("")
            ltouple += (l,)

<<<<<<< HEAD
        tklist = [[x if x != 'None' else '' for x in group] for group in ltouple]
        #If no one insert data into table 6, generate a blank list
        if not l:
            tklist = [['Keywords', '', ''], ['', '', '']]

        return tklist
    """

    # Setting rst prep method
    def ts_prep(self, test_id):
        maxpar = temp_library.objects.filter(l_group__isnull=False).filter(main_id=test_id).values('l_group').annotate(total=Count('l_group')).order_by('-l_group').first()
        count = 0
        maxMax = 1
        g_id = None
        
        if maxpar:
            maxMax = maxpar['total']
            
        ltouple = ()
        l1 = ["Settings"]
        while count < maxMax:
            l1.append("")
            count += 1
        ltouple += (l1,)

        
        tab_lib = temp_library.objects.filter(main_id=test_id).order_by("id")

        #Now extract setup, teardown and documentation in present
        set_test = temp_main.objects.filter(id=test_id).select_related()
        for y in set_test:
            ret_setup = y.t_setup
            ret_teardown = y.t_teardown
            ret_doc = y.t_doc
            ret_vfile = y.t_varfile
            ret_rfile = y.t_resfile


        l=[]
        
        #tslist = [["Settings", ""]]
        
        if tab_lib.count() == 0:
            #tslist.append(["", ""])
            l.append("")
            l.append("")
        else:
            for r in tab_lib.iterator():
                #tslist.append([str(r.l_type), str(r.l_val)])
                if r.l_group:
                    if r.l_group == g_id:
                        #l.append(str(r.l_val))
                        if str(r.l_param) != 'None':l.append(str(r.l_param))
                        g_id = str(r.l_group)
                    else:
                        if l:
                            #Check for l len and add white space if lower than maxMax
                            if len(l) < maxMax+1:
                                len_dif = maxMax-len(l)
                                for x in range(0,len_dif+1): l.append('')
                            ltouple += (l,)
                            l = []
                        l.append('Library')
                        l.append(str(r.l_val))
                        if str(r.l_param) != 'None':l.append(str(r.l_param))
                        g_id = str(r.l_group)
                else:

                    if l:
                        ltouple += (l,)
                        l = []

                    l.append('Library')
                    l.append(str(r.l_val))
                    if str(r.l_param) != 'None': l.append(str(r.l_param))
                    if len(l) < maxMax+1:
                                len_dif = maxMax-len(l)
                                for x in range(0,len_dif+1): l.append('')
                    ltouple += (l,)
                    l = []

        if l:

            if len(l) < maxMax+1:
                len_dif = maxMax-len(l)
                for x in range(0,len_dif+1): l.append('')
            ltouple += (l,)
            l = []
        tslist = [x for x in ltouple]


        if ret_setup:
            tslist.append(['Setup', str(ret_setup)])

        if ret_teardown:
            tslist.append(['Teardown', str(ret_teardown)])

        if ret_doc:
            tslist.append(['Documentation', str(ret_doc)])

        if ret_vfile:
            tslist.append(['Variables', str(ret_vfile)])

        if ret_rfile:
            tslist.append(['Resource', str(ret_rfile)])
=======
        tklist = [x for x in ltouple]
        return tklist

    # Setting rst prep method
    def ts_prep(self, test_id):
        tab_lib = temp_library.objects.filter(main_id=test_id)
        tslist = [["Settings", ""]]
        if tab_lib.count() == 0:
            tslist.append(["", ""])
        for r in tab_lib.iterator():
            tslist.append([str(r.l_type), str(r.l_val)])
>>>>>>> master

        return tslist

    # Variables rst prep method
    def tv_prep(self, test_id):
        ltouple = ()
        tab_var = temp_variables.objects.filter(main_id=test_id)
        l1 = ["Variables", ""]
        ltouple += (l1,)
        l = []
        for r in tab_var.iterator():
            l.append(str(r.v_key))
            l.append(str(r.v_val))
            ltouple += (l,)
            l = []

        tvlist = [x for x in ltouple]
<<<<<<< HEAD

=======
>>>>>>> master
        return tvlist


class MakeRst:
    def __init__(self, table):
        self.rstab = self.make_table(table)

    def make_table(self, grid):
<<<<<<< HEAD
=======
        print(grid)
>>>>>>> master
        try:
            cell_width = 2 + max(reduce(lambda x, y: x + y, [[len(item) for item in row] for row in grid], []))
        except Exception:
            cell_width = 0
        num_cols = len(grid[0])
        rst = self.table_div(num_cols, cell_width, 0)
        header_flag = 1
        for row in grid:
            try:
                rst = rst + '| ' + '| '.join([self.normalize_cell(x, cell_width - 1) for x in row]) + '|\n'
                rst = rst + self.table_div(num_cols, cell_width, header_flag)
                header_flag = 0
            except Exception:
                pass
<<<<<<< HEAD

=======
>>>>>>> master
        return rst

    @staticmethod
    def table_div(num_cols, col_width, header_flag):
        if header_flag == 1:
            return num_cols * ('+' + (col_width) * '=') + '+\n'
        else:
            return num_cols * ('+' + (col_width) * '-') + '+\n'

    @staticmethod
    def normalize_cell(string, length):
        return string + ((length - len(string)) * ' ')



class MakeHtml(threading.Thread):
    def __init__(self, *rstext):
        # super(MakeHtml, self).__init__()
        threading.Thread.__init__(self)
        self.outhtml = [x for x in rstext]
        self.retval = ''
        self._stop_event = threading.Event()
        self._myid = threading.current_thread()
        # self.saverun_html("test")

        # self.save_html('Test')

<<<<<<< HEAD

    ###########################################
    #10/10/2019 LEGACY METHOD FOR SAVE REPORT, NO SAVING ON DISK NEEDED NOW, REPORTS LL OPEN DINAMICALLY FROM DB
    ###########################################
=======
>>>>>>> master
    # Save html file on disk and run it if
    # def saverun_html(self, idTest, runTest=False):
    def run(self):

        ttype = 'TC'

        # Filepath for local save
        filepath = ("frontend/static/out/%s/%s_%s.html" % (id(self), id(self), ttype))
        filedir = ("frontend/static/out/%s/" % (id(self)))

        # Filepath for online env
        # filepath = ("/opt/lyra/static/out/%s/%s_%s.html" % (id(self), id(self), ttype))
        # filedir = ("/opt/lyra/static/out/%s/" % (id(self)))
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filepath, 'wb') as file:
            try:
                for x in self.outhtml:
<<<<<<< HEAD
                    print("SELF---->",self.outhtml)
                    file.write(publish_string(x.rstab.encode('utf-8'), writer_name='html'))
=======
                    file.write(publish_string(x.rstab, writer_name='html'))
>>>>>>> master

                    # run test
                    # rc = run_cli([filepath], exit=False)
                    # print(rc)
                    # run_cli(['--name', 'Example of calling...', filepath], exit=False)
                #run_cli(filepath, outputdir=filedir)
                #run_cli(['--name', 'Example of calling...', filepath], exit=False)

            except:
                raise TypeError("Cannot save html to disk, check if self.outhtml exist on instance!")


            rdict = {'fpath': filepath, 'fdir': filedir, 'pid': id(self)}

        self.retval = rdict
        #run_test(filepath, outputdir=filedir)
        #return rdict


def stop(self):
    self._stop_event.set()


def stopped(self):
    return self._stop_event.is_set()

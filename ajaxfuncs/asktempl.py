import sys
import os
from frontend.getdata import ins_ask
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


import django

sys.path.append('core')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


@csrf_exempt
def askinsert(request):
    if request.is_ajax():


        dict_ins= {'lnum': request.POST['idLic'],
               'ttype': request.POST['tType'],
               'precond': request.POST['tPre'],
               'steps': request.POST['tSteps'],
               'expres': request.POST['tExpect'],
               'scode': request.POST['tCode'],
               'tdescr': request.POST['tDesc']
               }

        try:
            iret = ins_ask(dict_ins)
        except Exception as e:
            print("Ask exception: ",e)

        json = {
            "iresult": str(iret)
        }

        return HttpResponse(
            json["iresult"]
        )

    else:
        pass


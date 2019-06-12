"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.contrib import admin
from django.urls import path
from ajaxfuncs.ajax import mainoptions, tabrefresh, tstopper, tselect, ecount, tlinemgm, filerefresh, jpost, tsingle
from ajaxfuncs.history import histrefresh, retUser, assign_ticket, get_ticket, hfilter, hstartfilter
from ajaxfuncs.template_import import import_templ
from ajaxfuncs.group import mainTgroup, subTgroup
from rsthtml.goTest import startTest
from frontend.views import index, h_list, login_register, user_login, user_logout, temp_main, temp_case, temp_assist, temp_var, \
    temp_lib, temp_group, t_testViewSet, temp_mainViewSet, UserViewSet, temp_caseViewSet, temp_keywordsViewSet, \
    temp_variablesViewSet, \
    temp_pers_keywordsViewSet, temp_test_keywordsViewSet, temp_libraryViewSet, t_scheduleViewSet, t_groupViewSet, \
    t_group_testViewSet, \
    t_historyViewSet, t_threadsViewSet, t_tagsViewSet, t_tags_routeViewSet, f_upload, ext_lib, sys_usage, lic_register, legal_terms, \
    handler500, temp_clone, temp_publish

from frontend.template_export import ret_list

schema_view = get_schema_view(title='Aida API')

router = routers.DefaultRouter()
router.register(r't_testapi', t_testViewSet)
router.register(r'temp_mainapi', temp_mainViewSet)
router.register(r'temp_caseapi', temp_caseViewSet)
router.register(r'temp_keywordsapi', temp_keywordsViewSet)
router.register(r'temp_variablesapi', temp_variablesViewSet)
router.register(r'temp_pers_keywordsapi', temp_pers_keywordsViewSet)
router.register(r'temp_test_keywordsapi', temp_test_keywordsViewSet)
router.register(r'temp_libraryapi', temp_libraryViewSet)
router.register(r't_scheduleapi', t_scheduleViewSet)
router.register(r't_groupapi', t_groupViewSet)
router.register(r't_group_testapi', t_group_testViewSet)
router.register(r't_historyapi', t_historyViewSet)
router.register(r't_threadsapi', t_threadsViewSet)
router.register(r't_tagsapi', t_tagsViewSet)
router.register(r't_tags_routeapi', t_tags_routeViewSet)

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

handler500 = handler500

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', index, name='index'),
                  url(r'^', include(router.urls)),
                  url(r'^login/$', user_login),
                  url(r'^login/(?P<log_err>\w+)/$', user_login),
                  url(r'^logout/$', user_logout),
                    url(r'^history$', h_list),
                  #url(r'^active$', index),
                  url(r'^legal$', legal_terms),
                  url(r'^ajax$', mainoptions),
                  url(r'^trefresh$', tabrefresh),
                  url(r'^files/frefresh$', filerefresh),
                  url(r'^hrefresh$', histrefresh),
                  url(r'^elemcount$', ecount),
                  url(r'^getuser$', retUser),
                  url(r'^addtask$', assign_ticket),
                  url(r'^getass$', get_ticket),
                  url(r'^tline_mgm$', tlinemgm),
                url(r'^filter_data$', hfilter),
                url(r'^startfilter$', hstartfilter),
                  url(r'^thread_stopper$', tstopper),
                  url(r'^test_type$', tselect),
                url(r'^test_single', tsingle),
                  url(r'^start$', startTest),
                  url(r'^tmain$', temp_main),
                  url(r'^tcase$', temp_case),
                url(r'^tassist$', temp_assist),
                url(r'^tpublish$', temp_publish),
                  url(r'^tassist/(?P<templ_id>\w+)/$', temp_assist),
                url(r'^temp_clone/(?P<t_id>\w+)/$', temp_clone),
                  url(r'^register/$', lic_register),
                  url(r'^register/(?P<reg_status>\w+)/$', lic_register),
                  url(r'^tgroup', temp_group),
                url(r'^import_templ/$', import_templ),
                  url(r'^groupmain', mainTgroup),
                url(r'^getassist', ret_list),
                  url(r'^groupsub', subTgroup),
                  url(r'^tvar$', temp_var),
                  url(r'^tlib$', temp_lib),
                  url(r'^jirapost$', jpost),
                  url(r'^libs$', ext_lib),
                  url(r'^usage', sys_usage),
                  url(r'^files', f_upload),
                  url(r'^schema/$', schema_view),
                  path('accounts/', include('django.contrib.auth.urls')),
                  url(r'^users/$', user_list, name='user-list'),
                  url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

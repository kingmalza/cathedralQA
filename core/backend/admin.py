# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from django.forms import Select
from datetime import datetime, timezone
from django.utils import timezone

from frontend.forms import CustomBarModelForm, jra_settingsForm, SettingsForm, TempMainForm, TempCaseForm, TempVarsForm, TempLibsForm, TtkForm, TempKeyForm
from backend.models import temp_keywords, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords, suite_libs



class temp_mainAdmin(admin.ModelAdmin):

    form = TempMainForm

    #list_filter = ('main_id__descr', 'l_type')
    list_filter = ('t_type',)
    list_display = ('descr', 't_type', 'notes', 'dt', 'active')
    #ordering = ('-l_type',)

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        #count = temp_main.objects.all().count()
        #if count > 1:
        #    return True

        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(temp_mainAdmin, self).save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        return {'owner': request.user}

    def changeform_view(self, request, obj_id=None, form_url='', extra_context=None):

        try:
            l_mod = temp_main.objects.latest('id')
        except Exception:
            l_mod = None

        extra_context = {
            'lmod': l_mod,
            'oId': obj_id
        }
        try:
            return super(temp_mainAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)
        except Exception:
            pass


# Here i try an admin model for populate fields with latest values inserted
class temp_caseAdmin(admin.ModelAdmin):
    form = TempCaseForm

    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'descr')
    #ordering = ('-l_type',)

    #Hide link from link list in app but maintain model still manageable with add edit option
    def get_model_perms(self, request):
        return {}

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_caseAdmin, self).get_form(request, obj, **kwargs)
        try:
            # Check if last insertion was made within 1 min otherwise form is blank
            latest_object = temp_case.objects.latest('id')

            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
        except Exception as e:
            print('Error in admin.py->45: ',e)

        return form

    def get_changeform_initial_data(self, request):
        return {'owner': request.user}

    def changeform_view(self, request, obj_id, form_url='', extra_context=None):

        try:
            l_mod = temp_case.objects.latest('id')
        except Exception:
            l_mod = None

        extra_context = {
            'lmod': l_mod,
        }
        return super(temp_caseAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)



class temp_variablesAdmin(admin.ModelAdmin):

    form = TempVarsForm

    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'v_key', 'v_val')
    #ordering = ('-l_type',)

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_variablesAdmin, self).get_form(request, obj, **kwargs)

        try:
            # Check if last insertion was made within 1 min otherwise form is blank
            latest_object = temp_variables.objects.latest('id')
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
        except Exception as e:
            print('Error in admin.py->85: ',e)

        return form


    def get_changeform_initial_data(self, request):
        return {'owner': request.user}

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        try:
            l_mod = temp_variables.objects.latest('id')
        except Exception:
            l_mod = None

        extra_context = {
            'lmod': l_mod,
        }
        return super(temp_variablesAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)



class temp_libraryAdmin(admin.ModelAdmin):

    form = TempLibsForm

    list_filter = ('main_id__descr', 'l_val')
    list_display = ('get_main_id', 'l_val', 'l_param', 'l_group')

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_libraryAdmin, self).get_form(request, obj, **kwargs)

        try:
            # Check if last insertion was made within 1 min otherwise form is blank
            latest_object = temp_library.objects.latest('id')
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
                #form.base_fields['l_type'].initial = latest_object.l_type
        except Exception as e:
            print('Error in admin.py->124: ',e)


        form.base_fields['l_group'].widget = Select(choices=(
            (None, 'No group'),
            ('--', 'Group1'),
            ('---', 'Group2'),
            ('----', 'Group3'),
            ('-----', 'Group4'),
            ('------', 'Group5'),
            ('-------', 'Group6'),
            ('--------', 'Group7'),
            ('---------', 'Group8'),
            ('----------', 'Group9'),
            ('-----------', 'Group10'),
        ))

        return form

    def changelist_view(self, request, extra_context=None):

        s_libs = suite_libs.objects.all()

        extra_context = {
            'sl': s_libs,
        }
        return super(temp_libraryAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_changeform_initial_data(self, request):
        return {'owner': request.user}

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        s_libs = suite_libs.objects.all()
        try:
            l_mod = temp_library.objects.latest('id')
        except Exception:
            l_mod = None

        extra_context = {
            'sl': s_libs,
            'lmod': l_mod,
        }
        return super(temp_libraryAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)

#@admin.register(temp_test_keywords)
class ttkAdmin(SortableAdminMixin, admin.ModelAdmin):

    form = TtkForm

    list_filter = ('main_id__descr', 'test_id__descr')
    list_display = ('get_main_id', 'get_test_id', 'key_id', 'key_val', 'key_group')
    #ordering = ('-l_type',)


    def get_main_id(self, obj):
        return obj.main_id.descr

    def get_test_id(self, obj):
        return obj.test_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    get_test_id.short_description = 'Test Case'
    get_test_id.admin_order_field = 'test_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(ttkAdmin, self).get_form(request, obj, **kwargs)

        try:
            #Check if last insertion was made within 1 min otherwise form is blank
            latest_object = temp_test_keywords.objects.latest('id')
            d1 = datetime.now(timezone.utc)
            #d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1-d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
                form.base_fields['test_id'].initial = latest_object.test_id
                form.base_fields['key_id'].initial = latest_object.key_id
        except Exception as e:
            print('Error in admin.py->164: ',e)

        form.base_fields['key_group'].widget = Select(choices=(
            (None, 'No group'),
            ('--', 'Group1'),
            ('---', 'Group2'),
            ('----', 'Group3'),
            ('-----', 'Group4'),
            ('------', 'Group5'),
            ('-------', 'Group6'),
            ('--------', 'Group7'),
            ('---------', 'Group8'),
            ('----------', 'Group9'),
            ('-----------', 'Group10'),
        ))

        return form


    def get_changeform_initial_data(self, request):
        return {'owner': request.user}

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        try:
            l_mod = temp_test_keywords.objects.latest('id')
        except Exception:
            l_mod = None

        extra_context = {
            'lmod': l_mod,
        }
        return super(ttkAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            'js/admin.js',       # project static folder
        )



# Model page field using custom forms
class tpk(SortableAdminMixin, admin.ModelAdmin):
    form = CustomBarModelForm

    list_filter = ('main_id__descr', 'key_descr')
    list_display = ('get_main_id', 'key_descr', 'key_id', 'key_val', 'key_group')

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(tpk, self).get_form(request, obj, **kwargs)

        try:
            # Check if last insertion was made within 1 min otherwise form is blank
            latest_object = temp_pers_keywords.objects.latest('id')
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
                form.base_fields['key_descr'].initial = latest_object.key_descr
                form.base_fields['key_id'].initial = latest_object.key_id
        except Exception as e:
            print('Error in admin.py->184: ',e)

        form.base_fields['key_group'].widget = Select(choices=(
            (None, 'No group'),
            ('--', 'Group1'),
            ('---', 'Group2'),
            ('----', 'Group3'),
            ('-----', 'Group4'),
            ('------', 'Group5'),
            ('-------', 'Group6'),
            ('--------', 'Group7'),
            ('---------', 'Group8'),
            ('----------', 'Group9'),
            ('-----------', 'Group10'),
        ))

        return form

    def get_changeform_initial_data(self, request):
        return {'owner': request.user}

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        try:
            l_mod = temp_pers_keywords.objects.latest('id')
        except Exception:
            l_mod = None

        extra_context = {
            'lmod': l_mod,
        }
        return super(tpk, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class temp_keywordsAdmin(admin.ModelAdmin):

    form = TempKeyForm

    #list_filter = ('personal',)
    list_display = ('descr', 'human')

    #Hide link from link list in app but maintain model still manageable with add edit option
    def get_model_perms(self, request):
        return {}

    """
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_keywords.objects.all().count()
        if count > 1:
            return True

        return False
    """


class suite_libsAdmin(admin.ModelAdmin):


    #Hide link from link list in app but maintain model still manageable with add edit option
    def get_model_perms(self, request):
        return {}


admin.site.site_title = 'cathedral Backend Admin'
admin.site.site_header = 'Backend admin console'
admin.site.index_title = 'TEST ADMIN ADMINISTRATION'

admin.site.register(temp_main, temp_mainAdmin, )
#admin.site.register(temp_main,)
admin.site.register(temp_case, temp_caseAdmin, )
admin.site.register(temp_keywords, temp_keywordsAdmin)
admin.site.register(temp_variables, temp_variablesAdmin, )
admin.site.register(temp_library, temp_libraryAdmin, )
admin.site.register(temp_pers_keywords, tpk, )
admin.site.register(temp_test_keywords, ttkAdmin, )
admin.site.register(suite_libs, suite_libsAdmin, )
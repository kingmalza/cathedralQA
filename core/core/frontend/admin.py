# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import CustomBarModelForm, jra_settingsForm, SettingsForm, TempMainForm, TempCaseForm, TempVarsForm, TempLibsForm, TtkForm, TempKeyForm
from .models import temp_main, temp_case, temp_keywords, temp_variables, temp_library, temp_pers_keywords, \
    temp_test_keywords, t_group, t_group_test, t_tags_route, t_tags, t_proj, t_proj_route, suite_libs, jra_settings, jra_history, \
    t_time, t_history, settings_gen
from django.forms import Select
from django.conf import settings
from datetime import datetime, timezone
import stripe

#global for check if trial or not


class temp_mainAdmin(admin.ModelAdmin):

    form = TempMainForm

    #list_filter = ('main_id__descr', 'l_type')
    list_filter = ('t_type',)
    list_display = ('descr', 't_type', 'notes', 'dt', 'active')
    #ordering = ('-l_type',)
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_main.objects.all().count()
        if count > 1:
            return True

        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(temp_mainAdmin, self).save_model(request, obj, form, change)

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = temp_main.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
            'oId': obj_id
        }
        return super(temp_mainAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)

# Here i try an admin model for populate fields with latest values inserted
class temp_caseAdmin(admin.ModelAdmin):
    form = TempCaseForm

    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'descr')
    #ordering = ('-l_type',)

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_case.objects.all().count()
        if count > 1:
            return True

        return False

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_caseAdmin, self).get_form(request, obj, **kwargs)
        # Check if last insertion was made within 1 min otherwise form is blank
        latest_object = temp_case.objects.latest('id')
        try:
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
        except Exception as e:
            print('Error in admin.py->45: ',e)

        return form

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = temp_case.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(temp_caseAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class temp_variablesAdmin(admin.ModelAdmin):

    form = TempVarsForm

    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'v_key', 'v_val')
    #ordering = ('-l_type',)
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_variables.objects.all().count()
        if count > 1:
            return True

        return False

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_variablesAdmin, self).get_form(request, obj, **kwargs)

        # Check if last insertion was made within 1 min otherwise form is blank
        latest_object = temp_variables.objects.latest('id')
        try:
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
        except Exception as e:
            print('Error in admin.py->85: ',e)

        return form

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = temp_variables.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(temp_variablesAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class temp_libraryAdmin(admin.ModelAdmin):

    form = TempLibsForm

    list_filter = ('main_id__descr', 'l_type')
    list_display = ('get_main_id', 'l_type', 'l_val', 'l_group')
    #ordering = ('-l_type',)
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_library.objects.all().count()
        if count > 1:
            return True

        return False

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_libraryAdmin, self).get_form(request, obj, **kwargs)

        # Check if last insertion was made within 1 min otherwise form is blank
        latest_object = temp_library.objects.latest('id')
        try:
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
                form.base_fields['l_type'].initial = latest_object.l_type
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

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        s_libs = suite_libs.objects.all()
        l_mod = temp_library.objects.latest('id')

        extra_context = {
            'sl': s_libs,
            'lmod': l_mod,
        }
        return super(temp_libraryAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class ttkAdmin(admin.ModelAdmin):

    form = TtkForm

    list_filter = ('main_id__descr', 'test_id__descr')
    list_display = ('get_main_id', 'get_test_id', 'key_id', 'key_val', 'key_group')
    #ordering = ('-l_type',)
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_test_keywords.objects.all().count()
        if count > 1:
            return True

        return False

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

        #Check if last insertion was made within 1 min otherwise form is blank
        latest_object = temp_test_keywords.objects.latest('id')
        try:
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

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = temp_test_keywords.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(ttkAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


# Model page field using custom forms
class tpk(admin.ModelAdmin):
    form = CustomBarModelForm

    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'standard_id', 'pers_id', 'variable_val')
    #ordering = ('-l_type',)
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_pers_keywords.objects.all().count()
        if count > 1:
            return True

        return False

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(tpk, self).get_form(request, obj, **kwargs)

        # Check if last insertion was made within 1 min otherwise form is blank
        latest_object = temp_pers_keywords.objects.latest('id')
        try:
            d1 = datetime.now(timezone.utc)
            # d2 = datetime.strptime(latest_object.dt, '%Y-%m-%d %H:%M:%S')
            d2 = latest_object.dt
            i_sec = (d1 - d2).total_seconds()
            if i_sec < 60:
                form.base_fields['main_id'].initial = latest_object.main_id
        except Exception as e:
            print('Error in admin.py->164: ',e)

        return form

    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = temp_pers_keywords.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(tpk, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)

class t_tags_routeAdmin(admin.ModelAdmin):

    list_filter = ('main_id__descr', 'tag_id__descr')
    list_display = ('get_main_id', 'get_tag_id', 'route_notes')

    # ordering = ('-l_type',)
    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = t_tags_route.objects.all().count()
        if count > 1:
            return True

        return False

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_tag_id(self, obj):
        return obj.tag_id.descr

    get_tag_id.short_description = 'TAG'
    get_tag_id.admin_order_field = 'tag_id__descr'


    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        l_mod = t_tags_route.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(t_tags_routeAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class temp_keywordsAdmin(admin.ModelAdmin):

    form = TempKeyForm

    list_filter = ('personal',)
    list_display = ('descr', 'human', 'personal')

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = temp_keywords.objects.all().count()
        if count > 1:
            return True

        return False

    # ordering = ('-l_type',)
    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = temp_keywords.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(temp_keywordsAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)



class t_proj_routeAdmin(admin.ModelAdmin):

    list_filter = ('main_id__descr', 'proj_id__descr')
    list_display = ('get_main_id', 'get_proj_id', 'route_notes')

    # ordering = ('-l_type',)

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = t_proj_route.objects.all().count()
        if count > 1:
            return True

        return False

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_proj_id(self, obj):
        return obj.proj_id.descr

    get_proj_id.short_description = 'PROJECT'
    get_proj_id.admin_order_field = 'proj_id__descr'


    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        l_mod = t_proj_route.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(t_proj_routeAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class t_projAdmin(admin.ModelAdmin):

    #list_filter = ('main_id__descr', 'proj_id__descr')
    list_display = ('descr', 'proj_start', 'proj_stop', 'proj_actors', 'proj_notes')

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = t_proj.objects.all().count()
        if count > 1:
            return True

        return False

    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        l_mod = t_proj.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        return super(t_projAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class t_tagsAdmin(admin.ModelAdmin):

    # list_filter = ('main_id__descr', 'proj_id__descr')
    list_display = ('descr',  'tag_notes')

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = t_tags.objects.all().count()
        if count > 1:
            return True

        return False

    def changeform_view(self, request, obj_id, form_url, extra_context=None):
            l_mod = t_tags.objects.latest('id')

            extra_context = {
                'lmod': l_mod,
            }
            return super(t_tagsAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class t_groupAdmin(admin.ModelAdmin):

    list_filter = ('active',)
    list_display = ('descr',  'g_prior', 'g_desc', 'active')

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = t_group.objects.all().count()
        if count > 1:
            return True

        return False

    def changeform_view(self, request, obj_id, form_url, extra_context=None):
            l_mod = t_group.objects.latest('id')

            extra_context = {
                'lmod': l_mod,
            }
            return super(t_groupAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)


class t_group_testAdmin(admin.ModelAdmin):

    list_filter = ('id_grp__descr', 'id_temp__descr')
    list_display = ('id_grp',  'id_temp', 'temp_ord')

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = t_group_test.objects.all().count()
        if count > 1:
            return True

        return False

    def changeform_view(self, request, obj_id, form_url, extra_context=None):
            l_mod = t_group_test.objects.latest('id')

            extra_context = {
                'lmod': l_mod,
            }
            return super(t_group_testAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)



class jra_settingsAdmin(admin.ModelAdmin):

    form = jra_settingsForm
    #list_filter = ('j_address', 'j_user')
    list_display = ('j_address', 'j_user', 'j_notes')

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = jra_settings.objects.all().count()
        if count == 0:
            return True

        return False


    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        print("OBJ_ID--> ", obj_id)
        """
        l_mod = jra_history.objects.latest('id')

        extra_context = {
            'lmod': l_mod,
        }
        """
        return super(jra_settingsAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)

"""
class settings_genAdmin(admin.ModelAdmin):

    form = SettingsForm
    list_display = ('lic_num', 'comp_name', 'tax_id', 'reg_email')
    readonly_fields = ['lic_num', 'stripe_id', 'created_on']

    def has_delete_permission(self, request, obj=None):
        # if there's just an entry don't allow deletion
        count = settings_gen.objects.all().count()
        if count > 1:
            return True

        return False

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = settings_gen.objects.all().count()
        if count == 0:
            return True

        return False


    def save_model(self, request, obj, form, change):
        print('Reg stripe -> ',obj.stripe_id)
        #If exist a stripe connection update data in stripe
        if obj.stripe_id:
            # Retreive stripe API keys
            stripe.api_key = getattr(settings, "STRIPE_KEY", None)
            cu = stripe.Customer.retrieve(obj.stripe_id)
            cu.description = "Customer for "+obj.comp_name
            cu.email = obj.reg_email
            cu.tax_info.tax_id = obj.tax_id
            cu.tax_info.type = 'vat'
            cu.save()


        super(settings_genAdmin, self).save_model(request, obj, form, change)


    def changeform_view(self, request, obj_id, form_url, extra_context=None):

        
        #l_mod = jra_history.objects.latest('id')

        #extra_context = {
        #    'lmod': l_mod,
        #}
        
        return super(settings_genAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)
"""

class APIAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(APIAdmin, self).save_model(request, obj, form, change)

class APIAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(APIAdmin, self).save_model(request, obj, form, change)



admin.site.site_title = 'Aida Admin'
admin.site.site_header = 'Aida admin console'
admin.site.index_title = 'TEST ADMIN ADMINISTRATION'

admin.site.register(temp_main, temp_mainAdmin, )
admin.site.register(temp_case, temp_caseAdmin, )
admin.site.register(temp_keywords, temp_keywordsAdmin)
admin.site.register(temp_variables, temp_variablesAdmin, )
admin.site.register(temp_library, temp_libraryAdmin, )
admin.site.register(temp_pers_keywords, tpk, )
admin.site.register(temp_test_keywords, ttkAdmin, )
admin.site.register(t_group, t_groupAdmin, )
admin.site.register(t_group_test, t_group_testAdmin, )
admin.site.register(t_tags_route, t_tags_routeAdmin)
admin.site.register(t_tags, t_tagsAdmin, )
admin.site.register(t_proj_route, t_proj_routeAdmin )
admin.site.register(t_proj, t_projAdmin, )
#admin.site.register(settings_gen, settings_genAdmin, )
admin.site.register(suite_libs, )
admin.site.register(jra_settings, jra_settingsAdmin)

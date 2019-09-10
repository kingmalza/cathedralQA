# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import CustomBarModelForm, jra_settingsForm, SettingsForm, TempMainForm, TempCaseForm, TempVarsForm, TempLibsForm, TtkForm, TempKeyForm
from frontend.models import t_group, t_group_test, t_tags_route, t_tags, t_proj, t_proj_route, suite_libs, jra_settings, jra_history, \
    t_time, t_history, settings_gen
from django.conf import settings
from datetime import datetime, timezone
import stripe

#global for check if trial or not


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
admin.site.index_title = 'SETTINGS ADMIN ADMINISTRATION'

admin.site.register(t_group, t_groupAdmin, )
admin.site.register(t_group_test, t_group_testAdmin, )
admin.site.register(t_tags_route, t_tags_routeAdmin)
admin.site.register(t_tags, t_tagsAdmin, )
admin.site.register(t_proj_route, t_proj_routeAdmin )
admin.site.register(t_proj, t_projAdmin, )
#admin.site.register(settings_gen, settings_genAdmin, )
admin.site.register(suite_libs, )
admin.site.register(jra_settings, jra_settingsAdmin)

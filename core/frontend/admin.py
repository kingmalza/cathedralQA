# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import CustomBarModelForm
from .models import temp_main, temp_case, temp_keywords, temp_variables, temp_library, temp_pers_keywords, \
    temp_test_keywords, t_group, t_group_test, t_tags_route, t_tags, t_proj, t_proj_route, suite_libs

"""
class temp_mainAdmin(admin.ModelAdmin):
    
    #list_filter = ('main_id__descr', 'l_type')
    list_display = ('descr', 'notes', 'dt')
    #ordering = ('-l_type',)
"""   
# Here i try an admin model for populate fields with latest values inserted
class temp_caseAdmin(admin.ModelAdmin):

    list_filter = ('main_id__descr', 'descr')
    list_display = ('get_main_id', 'descr')
    #ordering = ('-l_type',)

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_caseAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_case.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        return form


class temp_variablesAdmin(admin.ModelAdmin):

    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'v_key', 'v_val')
    #ordering = ('-l_type',)
    
    def get_main_id(self, obj):
        return obj.main_id.descr
    
    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_variablesAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_variables.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        return form


class temp_libraryAdmin(admin.ModelAdmin):
    
    list_filter = ('main_id__descr', 'l_type')
    list_display = ('get_main_id', 'l_type', 'l_val')
    #ordering = ('-l_type',)

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_libraryAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_library.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        form.base_fields['l_type'].initial = latest_object.l_type
        return form
        
    def changelist_view(self, request, extra_context=None):
        
        s_libs = suite_libs.objects.all()
        
        extra_context = {
            'sl': s_libs,
        }
        return super(temp_libraryAdmin, self).changelist_view(request, extra_context=extra_context)
        
    
    def changeform_view(self, request, obj_id=None, form_url='', extra_context=None):
        
        s_libs = suite_libs.objects.all()
        
        extra_context = {
            'sl': s_libs,
        }
        return super(temp_libraryAdmin, self).changeform_view(request, extra_context=extra_context)

        
class ttkAdmin(admin.ModelAdmin):
    
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
        latest_object = temp_test_keywords.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        form.base_fields['test_id'].initial = latest_object.test_id
        form.base_fields['key_id'].initial = latest_object.key_id
        return form
        
    
    def changeform_view(self, request, obj_id=None, form_url='', extra_context=None):
        
        l_mod = temp_test_keywords.objects.latest('id')
        
        extra_context = {
            'lmod': l_mod,
        }
        return super(ttkAdmin, self).changeform_view(request, extra_context=extra_context)


# Model page field using custom forms
class tpk(admin.ModelAdmin):
    form = CustomBarModelForm
        
    list_filter = ('main_id__descr',)
    list_display = ('get_main_id', 'pers_id', 'standard_id', 'variable_val')
    #ordering = ('-l_type',)

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_form(self, request, obj=None, **kwargs):
        form = super(tpk, self).get_form(request, obj, **kwargs)
        latest_object = temp_pers_keywords.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        return form


class t_tags_routeAdmin(admin.ModelAdmin):

    list_filter = ('main_id__descr', 'tag_id__descr')
    list_display = ('get_main_id', 'get_tag_id', 'route_notes')

    # ordering = ('-l_type',)

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_tag_id(self, obj):
        return obj.tag_id.descr

    get_tag_id.short_description = 'TAG'
    get_tag_id.admin_order_field = 'tag_id__descr'


class t_proj_routeAdmin(admin.ModelAdmin):

    list_filter = ('main_id__descr', 'proj_id__descr')
    list_display = ('get_main_id', 'get_proj_id', 'route_notes')

    # ordering = ('-l_type',)

    def get_main_id(self, obj):
        return obj.main_id.descr

    get_main_id.short_description = 'Main Template'
    get_main_id.admin_order_field = 'main_id__descr'

    def get_proj_id(self, obj):
        return obj.proj_id.descr

    get_proj_id.short_description = 'PROJECT'
    get_proj_id.admin_order_field = 'proj_id__descr'


class APIAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(APIAdmin, self).save_model(request, obj, form, change)


        
admin.site.site_title = 'Aida Admin'
admin.site.site_header = 'Aida admin console'
admin.site.index_title = 'TEST ADMIN ADMINISTRATION'

admin.site.register(temp_main, APIAdmin, )
admin.site.register(temp_case, temp_caseAdmin, )
admin.site.register(temp_keywords)
admin.site.register(temp_variables, temp_variablesAdmin, )
admin.site.register(temp_library, temp_libraryAdmin, )
admin.site.register(temp_pers_keywords, tpk, )
admin.site.register(temp_test_keywords, ttkAdmin, )
admin.site.register(t_group, )
admin.site.register(t_group_test, )
admin.site.register(t_tags_route, t_tags_routeAdmin)
admin.site.register(t_tags, )
admin.site.register(t_proj_route, t_proj_routeAdmin )
admin.site.register(t_proj, )
admin.site.register(suite_libs, )

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import CustomBarModelForm
from .models import temp_main, temp_case, temp_keywords, temp_variables, temp_library, temp_pers_keywords, \
    temp_test_keywords, t_group, t_group_test, t_tags_route, t_tags, t_proj, t_proj_route


# Here i try an admin model for populate fields with latest values inserted
class temp_caseAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_caseAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_case.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        return form


class temp_variablesAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_variablesAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_variables.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        return form


class temp_libraryAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(temp_libraryAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_library.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        form.base_fields['l_type'].initial = latest_object.l_type
        return form


class ttkAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ttkAdmin, self).get_form(request, obj, **kwargs)
        latest_object = temp_test_keywords.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        form.base_fields['test_id'].initial = latest_object.test_id
        return form


# Model page field using custom forms
class tpk(admin.ModelAdmin):
    form = CustomBarModelForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(tpk, self).get_form(request, obj, **kwargs)
        latest_object = temp_pers_keywords.objects.latest('id')
        form.base_fields['main_id'].initial = latest_object.main_id
        return form


class APIAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(APIAdmin, self).save_model(request, obj, form, change)


admin.site.site_title = 'Lyra Admin'
admin.site.site_header = 'Lyra admin console'
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
admin.site.register(t_tags_route, )
admin.site.register(t_tags, )
admin.site.register(t_proj_route, )
admin.site.register(t_proj, )

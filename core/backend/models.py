# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def validate_fsize(in_file):
    file_size = in_file.file.size
    limit_kb = 150
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


# temp_keywords
"""
Table for keywords variable
List of selenium, roboframeworks + personalized (flag 1 in personal) keywords and personal human translation
"""


class temp_keywords(models.Model):
    descr = models.CharField(max_length=200, unique=True)
    human = models.CharField(max_length=200, unique=True)
    personal = models.BooleanField(default=True, verbose_name="Personal Keyword")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #personal = models.IntegerField(default=1, verbose_name="Linked variable")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tkey_owner', on_delete=models.CASCADE, verbose_name="API Owner", null=True, blank=True,)

    class Meta:
        verbose_name = 'KEYWORD'
        verbose_name_plural = 'KEYWORDS'
        ordering = ('descr',)

    def __str__(self):
        return self.descr


# temp_main
"""
Main table for teplates
descr -> Template description
dt -> datetime template creation
user_id -> onetoone User
"""


class temp_main(models.Model):

    TYPE_CHOICES = (
        ('Functional', 'Functional'),
        ('Non-Functional', 'Non-Functional')
    )

    descr = models.CharField(max_length=200, verbose_name="Description", unique=True)
    t_type = models.CharField(choices=TYPE_CHOICES, max_length=20, verbose_name="Test Type")
    t_setup = models.ForeignKey(temp_keywords, on_delete=models.CASCADE, related_name='t_set', verbose_name="Test Setup", null=True, blank=True)
    t_teardown = models.ForeignKey(temp_keywords, on_delete=models.CASCADE, related_name='t_ter', verbose_name="Test Teardown", null=True, blank=True)
    t_doc = models.TextField(null=True, blank=True, verbose_name='Documentation')
    precond = models.TextField(null=True, blank=True, verbose_name="Preconditions")
    steps = models.TextField(null=True, blank=True, verbose_name="Steps")
    expected = models.TextField(null=True, blank=True, verbose_name="Expected Result")
    notes = models.TextField(null=True, blank=True, verbose_name="Note")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    active = models.BooleanField(default=True, verbose_name="Active")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tmain_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '1-Main Template'
        verbose_name_plural = '1-Main Templates'

    def __str__(self):
        return self.descr


# temp_case
"""
TestCase table
"""


class temp_case(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, related_name="tm_tc", on_delete=models.CASCADE, verbose_name="Main Template")
    descr = models.CharField(max_length=200, verbose_name="Case description")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tcase_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '2-Test Case'
        verbose_name_plural = '2-Test Cases'
        ordering = ('descr',)

    def __str__(self):
        #return '%s -> %s' % (str(self.main_id), self.descr)
        return str(self.descr)

    def __repr__(self):
        return self.descr



# temp_variables
"""
Table vor variable collection
"""


class temp_variables(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE, related_name="tm_tv", verbose_name="Template")
    v_key = models.CharField(max_length=200, verbose_name="Variable")
    v_val = models.CharField(max_length=200, null=True, blank=True, verbose_name="Default Value")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tvar_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '2-Test Variable'
        verbose_name_plural = '2-Test Variables'
        ordering = ('main_id', 'v_key',)

    def __str__(self):
        return '%s -> %s' % (str(self.main_id), self.v_key)

    def __repr__(self):
        return self.v_key


#----------------------------------------------------
#SUITE LIBRARIES
#----------------------------------------------------

class suite_libs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    descr = models.TextField(null=True, blank=True, verbose_name="Description")
    docs = models.CharField(max_length=255, null=True, blank=True, verbose_name="Doc Link")
    lib_name = models.CharField(max_length=255, verbose_name="Import Name")
    status = models.CharField(max_length=10, default='ACTIVE', editable= False)
    #f_lib = models.FileField(upload_to='libs/', blank=True, validators=[FileExtensionValidator(['py']),validate_fsize], verbose_name="File ( .py Max 150Kb )")
    notes = models.TextField(null=True, blank=True, verbose_name="Notes")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #owner = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'LIBRARY'
        verbose_name_plural = 'LIBRARIES'
        ordering = ('name', 'lib_name', 'status',)


    def __str__(self):
        return '%s' % (str(self.lib_name))



# temp_library
"""
Table for libraries
"""


class temp_library(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE, related_name='tm_tl', verbose_name="Template")
    #l_type = models.CharField(max_length=50, verbose_name='Type')
    #l_val = models.CharField(max_length=254, verbose_name='Value')
    l_val = models.ForeignKey(suite_libs, on_delete=models.CASCADE, related_name='li_val', verbose_name="Library")
    l_group = models.CharField(max_length=200, null=True, blank=True, verbose_name='Group')
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tlib_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '3-Test Library'
        verbose_name_plural = '3-Test Libraries'
        ordering = ('main_id', 'l_val',)

    def __str__(self):
        return '%s -> %s' % (str(self.main_id), self.l_val)


# temp_test_keywords
"""
Table for define keywords for testcases
"""


class temp_test_keywords(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE, related_name='tm_ttk', verbose_name="Template")
    test_id = models.ForeignKey(temp_case, on_delete=models.CASCADE, related_name='tc_ttk', verbose_name="Test Case")
    key_id = models.ForeignKey(temp_keywords, on_delete=models.CASCADE, related_name='tk_ttk', verbose_name="Keyword")
    key_val = models.TextField(null=True, blank=True, verbose_name='Value')
    key_group = models.CharField(max_length=200, null=True, blank=True, verbose_name='Group')
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='ttestkey_owner', on_delete=models.CASCADE, verbose_name="API Owner")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        verbose_name = '4-Test Case Main Chain'
        verbose_name_plural = '4-Test Cases Main Chain'
        #ordering = ('my_order', 'main_id', 'test_id', 'key_id',)
        ordering = ['my_order']

    def __str__(self):
        return '%s (%s -> %s)' % (str(self.test_id), str(self.key_id), str(self.key_val))



# temp_pers_keywords
"""
Table for define actions for personalized keywords
Add standard keywords like actions for personalized key
"""


class temp_pers_keywords(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE, related_name='tm_tpk', verbose_name="Template")
    standard_id = models.ForeignKey(temp_keywords, related_name='tks_tpk', on_delete=models.CASCADE, verbose_name="Keyword")
    pers_id = models.ForeignKey(temp_keywords, related_name='tk_tpk', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Sub Keyword")
    variable_val = models.CharField(max_length=250, null=True, blank=True, verbose_name='Value')
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #variable_id = models.ForeignKey(temp_variables, null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tperskey_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '5-Keyword Link Chain'
        verbose_name_plural = '5-Keywords Link Chain'
        ordering = ('main_id', 'standard_id', 'pers_id',)

    def __str__(self):
        return '%s -> %s -> %s (%s)' % (str(self.main_id), str(self.pers_id), str(self.standard_id), str(self.variable_val))


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tenant_schemas.models import TenantMixin
from django.contrib.auth.models import User
from decimal import Decimal

# 1 create user table
"""
id(PK)
Surname -> The user surname
Name -> The user name
user -> Username
pass -> Password
pic -> User pic file (128x128)
regdata -> Data of first registration
lastlogin -> Last login datetime
note -> Textfield for note
"""
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.website


# 2 Create test table
"""
id(PK)
test_id -> Automatic id generated from python rst.py on new test save
test_data -> cPickle of test rst
text_creation -> Datetime of creation
ip_addr -> Creation ip address
"""


class t_test(models.Model):
    test_id = models.CharField(max_length=30)
    test_data = models.BinaryField()
    test_rst = models.TextField()
    test_html = models.TextField()
    test_creation = models.DateTimeField(auto_now=True)
    ip_addr = models.CharField(max_length=30)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='t_owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.test_id


# -----------------------------------------------------------------------------
# TEMPLATE DATA
# -----------------------------------------------------------------------------

# temp_main
"""
Main table for teplates
descr -> Template description
dt -> datetime template creation
user_id -> onetoone User
"""


class temp_main(models.Model):
    descr = models.CharField(max_length=200, verbose_name="Description")
    notes = models.TextField(null=True, blank=True, verbose_name="Note")
    dt = models.DateTimeField(auto_now=True)
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
    main_id = models.ForeignKey(temp_main, null=True, blank=True, verbose_name="Main Template", on_delete=models.SET_NULL,)
    descr = models.CharField(max_length=200, verbose_name="Case description")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tcase_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '2-Test Case'
        verbose_name_plural = '2-Test Cases'
        ordering = ('descr',)

    def __str__(self):
        return '%s -> %s' % (str(self.main_id), self.descr)

    def __repr__(self):
        return self.descr


# temp_keywords
"""
Table for keywords variable
List of selenium, roboframeworks + personalized (flag 1 in personal) keywords and personal human translation
"""


class temp_keywords(models.Model):
    descr = models.CharField(max_length=200, unique=True)
    human = models.CharField(max_length=200, unique=True)
    personal = models.BooleanField(default=False, verbose_name="Linked variable")
    #personal = models.IntegerField(default=1, verbose_name="Linked variable")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tkey_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = 'KEYWORD'
        verbose_name_plural = 'KEYWORDS'
        ordering = ('descr',)

    def __str__(self):
        return self.descr


# temp_variables
"""
Table vor variable collection
"""


class temp_variables(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    v_key = models.CharField(max_length=200)
    v_val = models.CharField(max_length=200, null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tvar_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '3-Test Variable'
        verbose_name_plural = '3-Test Variables'
        ordering = ('main_id', 'v_key',)

    def __str__(self):
        return '%s -> %s' % (str(self.main_id), self.v_key)

    def __repr__(self):
        return self.v_key


# temp_pers_keywords
"""
Table for define actions for personalized keywords
Add standard keywords like actions for personalized key
"""


class temp_pers_keywords(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    pers_id = models.ForeignKey(temp_keywords, related_name='personal_key', null=True, blank=True, on_delete=models.CASCADE,)
    standard_id = models.ForeignKey(temp_keywords, related_name='standard_key', on_delete=models.CASCADE,)
    variable_val = models.CharField(max_length=250, null=True, blank=True)
    #variable_id = models.ForeignKey(temp_variables, null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tperskey_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '6-Keyword Link Chain'
        verbose_name_plural = '6-Keywords Link Chain'
        ordering = ('main_id', 'standard_id', 'pers_id',)

    def __str__(self):
        return '%s -> %s -> %s (%s)' % (
        str(self.main_id), str(self.pers_id), str(self.standard_id), str(self.variable_val))


# temp_test_keywords
"""
Table for define keywords for testcases
"""


class temp_test_keywords(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    test_id = models.ForeignKey(temp_case, on_delete=models.CASCADE,)
    key_id = models.ForeignKey(temp_keywords, on_delete=models.CASCADE,)
    key_val = models.CharField(max_length=200, null=True, blank=True)
    key_group = models.CharField(max_length=200, null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='ttestkey_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '5-Test Case Main Chain'
        verbose_name_plural = '5-Test Cases Main Chain'
        ordering = ('main_id', 'test_id', 'key_id',)

    def __str__(self):
        return '%s (%s -> %s)' % (str(self.test_id), str(self.key_id), str(self.key_val))


# temp_library
"""
Table for libraries
"""


class temp_library(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    l_type = models.CharField(max_length=50)
    l_val = models.CharField(max_length=100)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tlib_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '4-Test Setting'
        verbose_name_plural = '4-Test Settings'
        ordering = ('main_id', 'l_type',)

    def __str__(self):
        return '%s -> %s (%s)' % (str(self.main_id), self.l_type, self.l_val)


# Create a TestSchedue table
"""
id(PK)
id_test -> Test table Foreign key 
plan_data -> First inserted data
exec_main -> Type of execution (Done, Every)
exec_every -> Repetition indicator (10m, 2h, 3 days)
exec_at -> At repetition (22:30AM)
last_exec -> Last job execution
active -> Is job active (o=no, 1= yes)
"""


class t_schedule(models.Model):
    id_test = models.OneToOneField(t_test, on_delete=models.CASCADE,)
    plan_data = models.DateTimeField(auto_now=True)
    exec_main = models.CharField(max_length=10)
    exec_every = models.CharField(max_length=10, null=True, blank=True)
    exec_at = models.CharField(max_length=10, null=True, blank=True)
    last_exec = models.DateTimeField(auto_now=True)
    active = models.IntegerField(default=1)

    def __str__(self):
        return self.plan_data


# Create a Schedule repetition table
"""
id(PK)
id_test -> Test table Foreign key 
plan_data -> First inserted data
exec_main -> Type of execution (Done, Every)
exec_every -> Repetition indicator (10m, 2h, 3 days)
exec_at -> At repetition (22:30AM)
last_exec -> Last job execution
active -> Is job active (o=no, 1= yes)
"""


class t_schedsettings(models.Model):
    sched_desc = models.CharField(max_length=20)
    sched_command = models.CharField(max_length=20)
    sched_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.sched_desc


# Create a table for registering threads elapsed time
"""
"""


class t_time(models.Model):
    history_main = models.IntegerField(default=0)
    elapsed_t = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal('0.0000'))

    def __str__(self):
        return self.history_main


# -----------------------------------------------------------------------------
# TEST GROUP MANAGE
# -----------------------------------------------------------------------------

# Create main group table
"""
"""


class t_group(models.Model):
    descr = models.CharField(max_length=50)
    g_prior = models.IntegerField(default=1)
    g_desc = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    active = models.IntegerField(default=1)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tgrp_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    def __str__(self):
        return self.g_desc

    def __unicode__(self):
        return unicode(self.g_desc)


# Create grpup/templates table link
"""
"""


class t_group_test(models.Model):
    id_grp = models.ForeignKey(t_group, on_delete=models.CASCADE,)
    id_temp = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    temp_ord = models.IntegerField(default=0)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tgrptest_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    def __str__(self):
        return str(self.id_grp)


# -----------------------------------------------------------------------------
# TEST DATA
# -----------------------------------------------------------------------------

# Createtest_history table
"""
id(PK)
id_test -> Test table Foreign key 
exec_data -> DateTime of execution
exec_user -> Exec user Foreign
exec_status -> Job status (IN PROGRESS/TERMINATE)
exec_result -> cPickle of result xml
quick_res -> 0 = OK 1=FAIL
"""


class t_history(models.Model):
    test_main = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    test_type = models.CharField(max_length=5, blank=True)
    test_group = models.CharField(max_length=50, blank=True)
    exec_data = models.DateTimeField(auto_now=True)
    exec_status = models.CharField(max_length=10)
    xml_result = models.TextField()
    html_test = models.TextField()
    var_test = models.TextField()
    pid = models.CharField(max_length=20, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    group_id = models.ForeignKey(t_group, null=True, blank=True, on_delete=models.CASCADE,)
    pass_num = models.IntegerField(default=0)
    fail_num = models.IntegerField(default=0)
    sched_type = models.CharField(max_length=50, blank=True)
    sched_val = models.CharField(max_length=10, blank=True)
    thread_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.exec_status


# Create a threads managing table
"""
id(PK)
id_test -> Test table Foreign key 
thread_id -> Single test thread id
thread_main -> Main thread of schedule (a sort of daemon)
"""


class t_threads(models.Model):
    id_test = models.ForeignKey(t_history, on_delete=models.CASCADE,)
    thread_id = models.CharField(max_length=50, null=True, blank=True)
    thread_main = models.CharField(max_length=100, null=True, blank=True)
    thread_stag = models.CharField(max_length=100, null=True, blank=True)
    thread_status = models.CharField(max_length=10, null=True, blank=True)
    thread_startd = models.DateTimeField(auto_now=True)
    thread_stopd = models.DateTimeField(auto_now=False, null=True, blank=True)
    thread_ttype = models.CharField(max_length=5, blank=True)
    thread_tgroup = models.CharField(max_length=50, blank=True)
    thread_stype = models.CharField(max_length=50, blank=True)
    thread_sval = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.thread_id


# -----------------------------------------------------------------------------
# TEMPLATE TAGS DATA
# -----------------------------------------------------------------------------

class t_tags(models.Model):
    descr = models.CharField(max_length=50)
    tag_notes = models.TextField(null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='ttags_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = 'TAGS'
        verbose_name_plural = 'TAGS'
        ordering = ('descr',)

    def __str__(self):
        return self.descr


class t_tags_route(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    tag_id = models.ForeignKey(t_tags, on_delete=models.CASCADE,)
    route_notes = models.TextField(null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='ttagsroute_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '7-Tags for Templates'
        verbose_name_plural = '7-Tags for Templates'
        ordering = ('main_id', 'tag_id', 'route_notes',)

    def __str__(self):
        return '%s -> %s' % (
            str(self.main_id), str(self.tag_id))


# -----------------------------------------------------------------------------
# TEMPLATE PROJECT ASSOCIATION
# -----------------------------------------------------------------------------

class t_proj(models.Model):
    descr = models.CharField(max_length=50)
    proj_notes = models.TextField(null=True, blank=True)
    proj_actors = models.TextField(null=True, blank=True)
    proj_start = models.DateTimeField(auto_now=True, null=True, blank=True)
    proj_stop = models.DateTimeField(auto_now=False, null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tproj_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = 'PROJECTS'
        verbose_name_plural = 'PROJECTS'
        ordering = ('descr',)

    def __str__(self):
        return self.descr


class t_proj_route(models.Model):
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    proj_id = models.ForeignKey(t_proj, on_delete=models.CASCADE,)
    route_notes = models.TextField(null=True, blank=True)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tprojroute_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = '8-Projects Templates link'
        verbose_name_plural = '8-Projects Templates link'
        ordering = ('main_id', 'proj_id', 'route_notes',)

    def __str__(self):
        return '%s -> %s' % (
            str(self.main_id), str(self.proj_id))


#----------------------------------------------------
#FILES UPLOAD
#----------------------------------------------------

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/', blank=True)
    dfolder = models.CharField(max_length=255, blank=True)
    dmessage = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.IntegerField(default=0)
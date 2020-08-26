# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
<<<<<<< HEAD
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from tenant_schemas.models import TenantMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage

from django.template.loader import render_to_string

from decimal import Decimal
from django import forms
from django.forms import ModelForm, PasswordInput

from django.dispatch import receiver
from django.db.models.signals import post_save

from backend.models import temp_main


def validate_fsize(in_file):
    file_size = in_file.file.size
    limit_kb = 150
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)
=======
from django.contrib.auth.models import User
from decimal import Decimal
>>>>>>> master

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
<<<<<<< HEAD
class Client(TenantMixin):
    domain_url = models.CharField(max_length=128, blank=True)
    schema_name = models.CharField(max_length=63, blank=True, unique=True)
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)


    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
=======


class UserProfile(models.Model):
    user = models.OneToOneField(User)
>>>>>>> master
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
<<<<<<< HEAD
#Try to send Welcome email after new DEMO user registration
@receiver(post_save,sender=User)
def create_initial_story(sender, update_fields, created, instance, **kwargs):
    print("CREATED--->",update_fields)
    if not update_fields and instance.email:
        user_name = instance.username
        first_name = instance.first_name
        last_name = instance.last_name
        email = instance.email
        password = "AidaDemo1"
        context = {
            'news': 'Your aida demo account',
            'user': instance.username,
            'pass': "AidaDemo1"
        }
        html_content = render_to_string('email_demo.html', context)
        #html_content = "your username:%s <br> first name:%s <br> last name:%s <br> address:%s <br> password:%s"
        #message=EmailMessage(subject='welcome',body=html_content %(user_name,first_name,last_name,email,password),to=[email])
        message=EmailMessage(subject='Myaida Demo Account Registration',body=html_content,to=[email])
        message.content_subtype='html'
        message.send()
=======

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
    main_id = models.ForeignKey(temp_main, null=True, blank=True, verbose_name="Main Template")
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
    main_id = models.ForeignKey(temp_main)
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
    main_id = models.ForeignKey(temp_main)
    pers_id = models.ForeignKey(temp_keywords, related_name='personal_key', null=True, blank=True)
    standard_id = models.ForeignKey(temp_keywords, related_name='standard_key')
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
    main_id = models.ForeignKey(temp_main)
    test_id = models.ForeignKey(temp_case)
    key_id = models.ForeignKey(temp_keywords)
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
    main_id = models.ForeignKey(temp_main)
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
>>>>>>> master


# Create a TestSchedue table
"""
id(PK)
<<<<<<< HEAD
id_test -> Test table Foreign key
=======
id_test -> Test table Foreign key 
>>>>>>> master
plan_data -> First inserted data
exec_main -> Type of execution (Done, Every)
exec_every -> Repetition indicator (10m, 2h, 3 days)
exec_at -> At repetition (22:30AM)
last_exec -> Last job execution
active -> Is job active (o=no, 1= yes)
"""


class t_schedule(models.Model):
<<<<<<< HEAD
    id_test = models.OneToOneField(t_test, on_delete=models.CASCADE,)
=======
    id_test = models.OneToOneField(t_test)
>>>>>>> master
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
<<<<<<< HEAD
id_test -> Test table Foreign key
=======
id_test -> Test table Foreign key 
>>>>>>> master
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


<<<<<<< HEAD
=======
# Create a table for registering threads elapsed time
"""
"""


class t_time(models.Model):
    history_main = models.IntegerField(default=0)
    elapsed_t = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal('0.0000'))

    def __str__(self):
        return self.history_main

>>>>>>> master

# -----------------------------------------------------------------------------
# TEST GROUP MANAGE
# -----------------------------------------------------------------------------

# Create main group table
"""
"""


class t_group(models.Model):
<<<<<<< HEAD
    descr = models.CharField(max_length=50, verbose_name="Group name")
    g_prior = models.IntegerField(default=1, verbose_name="Priority", validators=[MaxValueValidator(3), MinValueValidator(1)])
    g_desc = models.TextField(null=True, blank=True, verbose_name="Notes")
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    active = models.BooleanField(default=True, verbose_name="Active")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tgrp_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = 'TEST GROUP MANAGER'
        verbose_name_plural = 'TEST GROUP MANAGER'
        ordering = ('descr',)

    def __str__(self):
        return self.descr

    def __unicode__(self):
        return unicode(self.g_descr)
=======
    descr = models.CharField(max_length=50)
    g_prior = models.IntegerField(default=1)
    g_desc = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(User)
    active = models.IntegerField(default=1)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tgrp_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    def __str__(self):
        return self.g_desc

    def __unicode__(self):
        return unicode(self.g_desc)
>>>>>>> master


# Create grpup/templates table link
"""
"""


class t_group_test(models.Model):
<<<<<<< HEAD
    id_grp = models.ForeignKey(t_group, on_delete=models.CASCADE, verbose_name="Group")
    id_temp = models.ForeignKey(temp_main, on_delete=models.CASCADE, verbose_name="Template")
    temp_ord = models.IntegerField(default=1, verbose_name="Template order", validators=[MaxValueValidator(100), MinValueValidator(1)])
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tgrptest_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
        verbose_name = 'TEST GROUP ITEMS'
        verbose_name_plural = 'TEST GROUP ITEMS'
        ordering = ('temp_ord',)

    def __str__(self):
        return '%s -> %s (%s)' % (str(self.id_grp), str(self.id_temp), str(self.temp_ord))
=======
    id_grp = models.ForeignKey(t_group)
    id_temp = models.ForeignKey(temp_main)
    temp_ord = models.IntegerField(default=0)
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tgrptest_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    def __str__(self):
        return str(self.id_grp)
>>>>>>> master


# -----------------------------------------------------------------------------
# TEST DATA
# -----------------------------------------------------------------------------

# Createtest_history table
"""
id(PK)
<<<<<<< HEAD
id_test -> Test table Foreign key
=======
id_test -> Test table Foreign key 
>>>>>>> master
exec_data -> DateTime of execution
exec_user -> Exec user Foreign
exec_status -> Job status (IN PROGRESS/TERMINATE)
exec_result -> cPickle of result xml
quick_res -> 0 = OK 1=FAIL
"""


class t_history(models.Model):
<<<<<<< HEAD
    test_main = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
=======
    test_main = models.ForeignKey(temp_main)
>>>>>>> master
    test_type = models.CharField(max_length=5, blank=True)
    test_group = models.CharField(max_length=50, blank=True)
    exec_data = models.DateTimeField(auto_now=True)
    exec_status = models.CharField(max_length=10)
    xml_result = models.TextField()
    html_test = models.TextField()
    var_test = models.TextField()
    pid = models.CharField(max_length=20, null=True, blank=True)
<<<<<<< HEAD
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    group_id = models.ForeignKey(t_group, null=True, blank=True, on_delete=models.CASCADE, db_index=True)
=======
    user_id = models.ForeignKey(User)
    group_id = models.ForeignKey(t_group, null=True, blank=True)
>>>>>>> master
    pass_num = models.IntegerField(default=0)
    fail_num = models.IntegerField(default=0)
    sched_type = models.CharField(max_length=50, blank=True)
    sched_val = models.CharField(max_length=10, blank=True)
    thread_name = models.CharField(max_length=100, blank=True)

<<<<<<< HEAD
    class Meta:
        indexes = [
            models.Index(fields=['group_id']),
        ]

=======
>>>>>>> master
    def __str__(self):
        return self.exec_status


<<<<<<< HEAD

# Create a table for registering threads elapsed time
"""
"""


class t_time(models.Model):
    history_main = models.ForeignKey(t_history, on_delete=models.CASCADE, verbose_name="History")
    elapsed_t = models.DecimalField(max_digits=20, decimal_places=6, default=Decimal('0.0000'))
    stop_data = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = 'RESOURCE USAGE'
        verbose_name_plural = 'RESOURCE USAGE'
        ordering = ('history_main',)

    def __str__(self):
        return '%s -> %s' % (str(self.history_main), str(self.elapsed_t))



# Create a threads managing table
"""
id(PK)
id_test -> Test table Foreign key
=======
# Create a threads managing table
"""
id(PK)
id_test -> Test table Foreign key 
>>>>>>> master
thread_id -> Single test thread id
thread_main -> Main thread of schedule (a sort of daemon)
"""


class t_threads(models.Model):
<<<<<<< HEAD
    id_test = models.ForeignKey(t_history, on_delete=models.CASCADE,)
    thread_id = models.CharField(max_length=50, null=True, blank=True)
    thread_main = models.CharField(max_length=100, null=True, blank=True)
    thread_stag = models.CharField(db_index=True, max_length=100, null=True, blank=True)
    thread_status = models.CharField(db_index=True, max_length=10, null=True, blank=True)
    thread_startd = models.DateTimeField(auto_now=True)
    thread_stopd = models.DateTimeField(auto_now=False, null=True, blank=True)
    id_time = models.ForeignKey(t_time, on_delete=models.CASCADE,)
    thread_ttype = models.CharField(max_length=5, blank=True)
    thread_runtype = models.CharField(max_length=20, blank=True)
=======
    id_test = models.ForeignKey(t_history)
    thread_id = models.CharField(max_length=50, null=True, blank=True)
    thread_main = models.CharField(max_length=100, null=True, blank=True)
    thread_stag = models.CharField(max_length=100, null=True, blank=True)
    thread_status = models.CharField(max_length=10, null=True, blank=True)
    thread_startd = models.DateTimeField(auto_now=True)
    thread_stopd = models.DateTimeField(auto_now=False, null=True, blank=True)
    thread_ttype = models.CharField(max_length=5, blank=True)
>>>>>>> master
    thread_tgroup = models.CharField(max_length=50, blank=True)
    thread_stype = models.CharField(max_length=50, blank=True)
    thread_sval = models.CharField(max_length=10, blank=True)

<<<<<<< HEAD
    class Meta:
        indexes = [
            models.Index(fields=['thread_stag', 'thread_status']),
        ]

=======
>>>>>>> master
    def __str__(self):
        return self.thread_id


<<<<<<< HEAD
#------------------------------------------------------------------------------
#TEMPLATES ASSIGNEMENT TABLE
#------------------------------------------------------------------------------

class t_assign(models.Model):
    t_tag = models.CharField(db_index=True, max_length=100, null=True, blank=True)
    id_userfor = models.ForeignKey('auth.User', related_name='u_for', on_delete=models.CASCADE)
    id_userass = models.ForeignKey('auth.User', related_name='u_ass', on_delete=models.CASCADE)
    dopen = models.DateTimeField(auto_now=True)
    ass_notes = models.TextField(null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['t_tag', 'id_userfor', 'id_userass']),
        ]

    def __str__(self):
        return self.t_tag


=======
>>>>>>> master
# -----------------------------------------------------------------------------
# TEMPLATE TAGS DATA
# -----------------------------------------------------------------------------

class t_tags(models.Model):
    descr = models.CharField(max_length=50)
    tag_notes = models.TextField(null=True, blank=True)
<<<<<<< HEAD
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
=======
>>>>>>> master
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='ttags_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
<<<<<<< HEAD
        verbose_name = 'TAGS MANAGER'
        verbose_name_plural = 'TAGS MANAGER'
        ordering = ('descr',)


=======
        verbose_name = 'TAGS'
        verbose_name_plural = 'TAGS'
        ordering = ('descr',)

>>>>>>> master
    def __str__(self):
        return self.descr


class t_tags_route(models.Model):
<<<<<<< HEAD
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    tag_id = models.ForeignKey(t_tags, on_delete=models.CASCADE,)
    route_notes = models.TextField(null=True, blank=True)
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
=======
    main_id = models.ForeignKey(temp_main)
    tag_id = models.ForeignKey(t_tags)
    route_notes = models.TextField(null=True, blank=True)
>>>>>>> master
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='ttagsroute_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
<<<<<<< HEAD
        verbose_name = 'TAGS TEMPLATES LINK'
        verbose_name_plural = 'TAGS TEMPLATES LINK'
        ordering = ('main_id', 'tag_id', 'route_notes',)


=======
        verbose_name = '7-Tags for Templates'
        verbose_name_plural = '7-Tags for Templates'
        ordering = ('main_id', 'tag_id', 'route_notes',)

>>>>>>> master
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
<<<<<<< HEAD
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
=======
>>>>>>> master
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tproj_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
<<<<<<< HEAD
        verbose_name = 'PROJECTS MANAGER'
        verbose_name_plural = 'PROJECTS MANAGER'
=======
        verbose_name = 'PROJECTS'
        verbose_name_plural = 'PROJECTS'
>>>>>>> master
        ordering = ('descr',)

    def __str__(self):
        return self.descr


class t_proj_route(models.Model):
<<<<<<< HEAD
    id = models.AutoField(primary_key=True)
    main_id = models.ForeignKey(temp_main, on_delete=models.CASCADE,)
    proj_id = models.ForeignKey(t_proj, on_delete=models.CASCADE,)
    route_notes = models.TextField(null=True, blank=True)
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")
=======
    main_id = models.ForeignKey(temp_main)
    proj_id = models.ForeignKey(t_proj)
    route_notes = models.TextField(null=True, blank=True)
>>>>>>> master
    #Fields for API permissions
    owner = models.ForeignKey('auth.User', related_name='tprojroute_owner', on_delete=models.CASCADE, verbose_name="API Owner")

    class Meta:
<<<<<<< HEAD
        verbose_name = 'PROJECT TEMPLATE LINK'
        verbose_name_plural = 'PROJECT TEMPLATE LINK'
        ordering = ('main_id', 'proj_id', 'route_notes',)


=======
        verbose_name = '8-Projects Templates link'
        verbose_name_plural = '8-Projects Templates link'
        ordering = ('main_id', 'proj_id', 'route_notes',)

>>>>>>> master
    def __str__(self):
        return '%s -> %s' % (
            str(self.main_id), str(self.proj_id))


#----------------------------------------------------
#FILES UPLOAD
#----------------------------------------------------

class Document(models.Model):
<<<<<<< HEAD
    id = models.AutoField(primary_key=True)
=======
>>>>>>> master
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/', blank=True)
    dfolder = models.CharField(max_length=255, blank=True)
    dmessage = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    owner = models.IntegerField(default=0)


#----------------------------------------------------
#GENERAL SETTINGS
#----------------------------------------------------

class settings_gen(models.Model):

    PLAN_CHOICES = (
        ('flat', 'FLAT'),
        ('ondemand', 'ON DEMAND')

    )

    id = models.AutoField(primary_key=True)
    tenant_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="System Name")
    lic_num = models.CharField(max_length=255, blank=True, null=True, verbose_name="License Number")
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    on_trial = models.BooleanField(default=True, blank=True, null=True)
    paid_feed = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    #paid_plan = models.CharField(choices=PLAN_CHOICES, max_length=10, null=True, blank=True, default='--------',)
    paid_plan = models.CharField(max_length=10, null=True, blank=True, verbose_name="Plan Selected")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    comp_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Company")
    addr_1 = models.CharField(max_length=200, null=True, blank=True)
    addr_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state_prov = models.CharField(max_length=100, null=True, blank=True)
    postal_zip = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Account ID")
    reg_email = models.CharField(max_length=150, null=True, blank=True, unique=True, verbose_name="Email")


    class Meta:
        verbose_name = 'ACCOUNT SETTINGS'
        verbose_name_plural = 'ACCOUNT SETTINGS'

    def __str__(self):
        return '%s -> %s' % (
            str(self.tenant_name), str(self.comp_name))


#----------------------------------------------------
#TABLE CHECKING ALREADY IMPORTED TEMPLATES
#----------------------------------------------------

class import_his(models.Model):
    id = models.AutoField(primary_key=True)
    imp_data = models.DateTimeField()
    imp_template = models.IntegerField(default=0)
    imp_num = models.IntegerField(default=0)



#----------------------------------------------------
#PAYEMENT DATAS AND AMOUNT FOR ON-DEMAND PLANS
#----------------------------------------------------

class bill_his(models.Model):
    id = models.AutoField(primary_key=True)
    bill_data = models.DateTimeField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_errors = models.CharField(max_length=254, blank=True)



# -----------------------------------------------------------------------------
# JIRA INTERFACE
# -----------------------------------------------------------------------------

class jra_settings(models.Model):
    id = models.AutoField(primary_key=True)
    j_address = models.CharField(max_length=255, verbose_name="Jira server address")
    j_user = models.CharField(max_length=255, blank=True, verbose_name="Username")
    j_pass = models.CharField(max_length=255, blank=True, verbose_name="Password")
    j_notes = models.TextField(null=True, blank=True, verbose_name="Notes")
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")


    class Meta:
        verbose_name = 'JIRA SETTINGS'
        verbose_name_plural = 'JIRA SETTINGS'
        ordering = ('j_address',)

    def __str__(self):
        return '%s -> %s' % (
            str(self.j_address), str(self.j_user))


class jra_history(models.Model):
    id = models.AutoField(primary_key=True)
    j_tid = models.CharField(max_length=1000, blank=True)
    j_issue = models.CharField(max_length=255, blank=True)
    j_comment = models.TextField(null=True, blank=True)
    j_file = models.BooleanField(default=True, verbose_name="Log file")
    j_error = models.TextField(null=True, blank=True)
    dt = models.DateTimeField(auto_now=True, verbose_name="Created")


    class Meta:
        indexes = [
            models.Index(fields=['j_tid', ]),
        ]

    def __str__(self):
        return '%s -> %s' % (
            str(self.j_tid), str(self.j_issue))
=======
    owner = models.IntegerField(default=0)
>>>>>>> master

#Utility for create and setup new tenants, register first data and send registration email

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from frontend.models import Client
from frontend.models import t_schedsettings, settings_gen
from frontend.models import temp_keywords, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords, suite_libs

import datetime


tk = ['Add Cookie','Add Location Strategy','Alert Should Be Present','Alert Should Not Be Present','Assign Id To Element','Capture Page Screenshot','Checkbox Should Be Selected','Checkbox Should Not Be Selected','Choose Cancel On Next Confirmation','Choose File','Choose Ok On Next Confirmation','Clear Element Text','Click Button','Click Element','Click Element At Coordinates','Click Image','Click Link','Close All Browsers','Close Browser','Close Window','Confirm Action','Create Webdriver','Current Frame Contains','Current Frame Should Contain','Current Frame Should Not Contain','Delete All Cookies','Delete Cookie','Dismiss Alert','Double Click Element','Drag And Drop','Drag And Drop By Offset','Element Should Be Disabled','Element Should Be Enabled','Element Should Be Focused','Element Should Be Visible','Element Should Contain','Element Should Not Be Visible','Element Should Not Contain','Element Text Should Be','Execute Async Javascript','Execute Javascript','Focus','Frame Should Contain','Get Alert Message','Get All Links','Get Cookie','Get Cookie Value','Get Cookies','Get Element Attribute','Get Element Count','Get Element Size','Get Horizontal Position','Get List Items','Get Location','Get Locations','Get Matching Xpath Count','Get Selected List Label','Get Selected List Labels','Get Selected List Value','Get Selected List Values','Get Selenium Implicit Wait','Get Selenium Speed','Get Selenium Timeout','Get Source','Get Table Cell','Get Text','Get Title','Get Value','Get Vertical Position','Get WebElement','Get WebElements','Get Window Handles','Get Window Identifiers','Get Window Names','Get Window Position','Get Window Size','Get Window Titles','Go Back','Go To','Handle Alert','Input Password','Input Text','Input Text Into Alert','Input Text Into Prompt','List Selection Should Be','List Should Have No Selections','List Windows','Location Should Be','Location Should Contain','Locator Should Match X Times','Log','Log Location','Log Source','Log Title','Maximize Browser Window','Mouse Down','Mouse Down On Image','Mouse Down On Link','Mouse Out','Mouse Over','Mouse Up','Open Browser','Open Context Menu','Page Should Contain','Page Should Contain Button','Page Should Contain Checkbox','Page Should Contain Element','Page Should Contain Image','Page Should Contain Link','Page Should Contain List','Page Should Contain Radio Button','Page Should Contain Textfield','Page Should Not Contain','Page Should Not Contain Button','Page Should Not Contain Checkbox','Page Should Not Contain Element','Page Should Not Contain Image','Page Should Not Contain Link','Page Should Not Contain List','Page Should Not Contain Radio Button','Page Should Not Contain Textfield','Press Key','Radio Button Should Be Set To','Radio Button Should Not Be Selected','Register Keyword To Run On Failure','Reload Page','Remove Location Strategy','Select All From List','Select Checkbox','Select Frame','Select From List','Select From List By Index','Select From List By Label','Select From List By Value','Select Radio Button','Select Window','Set Browser Implicit Wait','Set Focus To Element','Set Screenshot Directory','Set Selenium Implicit Wait','Set Selenium Speed','Set Selenium Timeout','Set Window Position','Set Window Size','Simulate','Simulate Event','Submit Form','Switch Browser','Table Cell Should Contain','Table Column Should Contain','Table Footer Should Contain','Table Header Should Contain','Table Row Should Contain','Table Should Contain','Textarea Should Contain','Textarea Value Should Be','Textfield Should Contain','Textfield Value Should Be','Title Should Be','Unselect All From List','Unselect Checkbox','Unselect Frame','Unselect From List','Unselect From List By Index','Unselect From List By Label','Unselect From List By Value','Wait For Condition','Wait Until Element Contains','Wait Until Element Does Not Contain','Wait Until Element Is Enabled','Wait Until Element Is Not Visible','Wait Until Element Is Visible','Wait Until Page Contains','Wait Until Page Contains Element','Wait Until Page Does Not Contain','Wait Until Page Does Not Contain Element','Xpath Should Match X Times','[Documentation]','Sleep','Pause Execution',':FOR','\\','Directory Should Exist','Should Be Equal','[Arguments]','...']


def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, to=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
    

def create1(t_tenant,t_name):
    
    #1 Create tenant entry and populate db schema
    tenant = Client(domain_url=t_tenant+'.myaida.io', schema_name=t_tenant,name=t_name)
    tenant.save()

  

def create2(t_tenant,paid=0.49):
  
    print("PRE.Create setting table...")
    #Insert tenant value in settings table
    tenant_insert = settings_gen(tenant_name=t_tenant, paid_feed=paid, on_trial=True)
    tenant_insert.save()
    
    print("1.Create scheduling...")
    #2 Populate schedule table
    sched1 = t_schedsettings(sched_desc='Once', sched_command='once')
    sched2 = t_schedsettings(sched_desc='Every minutes', sched_command='everymin')
    sched3 = t_schedsettings(sched_desc='Every hour', sched_command='everyhour')
    sched4 = t_schedsettings(sched_desc='Every day', sched_command='everyday')

    sched1.save()
    sched2.save()
    sched3.save()
    sched4.save()
    print("Scheduling OK")
    
    #3 Create Keyword tale
    print("2.Create keywords...")
    global tk
    for i in tk:
        addkey = temp_keywords(descr=str(i), human=str(i), personal=False, owner_id=User.objects.get(id=1).id)
        addkey.save()
    
    print("Keywords OK")
    
    #4. Create Library table
    print("3.Create suite Libs...")

    lib1 = suite_libs(name='Buit-In', descr='Robot Framework buitin libraries', lib_name='', status='ACTIVE', docs='http://robotframework.org/robotframework/latest/libraries/BuiltIn.html')
    lib2 = suite_libs(name='Archive library', descr='Library for handling zip- and tar-archives', lib_name='ArchiveLibrary', status='ACTIVE', docs='http://bulkan.github.io/robotframework-archivelibrary/')
    lib3 = suite_libs(name='Django Library', descr='Library for Django, a Python web framework', lib_name='DjangoLibrary', status='ACTIVE', docs='https://kitconcept.github.io/robotframework-djangolibrary/')
    lib4 = suite_libs(name='FTP library', descr='Library for testing and using FTP server', lib_name='FtpLibrary', status='ACTIVE', docs='https://kowalpy.github.io/Robot-Framework-FTP-Library/FtpLibrary.html')
    lib5 = suite_libs(name='RESTinstance', descr='Test library for HTTP JSON APIs', lib_name='REST', status='ACTIVE', docs='https://asyrjasalo.github.io/RESTinstance/')
    lib6 = suite_libs(name='SSHLibrary', descr='Enables executing commands on remote machines over an SSH connection. Also supports transfering files using SFTP', lib_name='SSHLibrary', status='ACTIVE', docs='https://github.com/robotframework/SSHLibrary#usage')
    lib7 = suite_libs(name='Diff Library', descr='Library to diff two files together', lib_name='DiffLibrary', status='ACTIVE', docs='https://bulkan.github.io/robotframework-difflibrary/')
    lib8 = suite_libs(name='robotframework-faker', descr='Library for Faker, a fake test data generator', lib_name='FakerLibrary', status='ACTIVE', docs='https://guykisel.github.io/robotframework-faker/')
    lib9 = suite_libs(name='HTTP library (Requests)', descr='Library for HTTP level testing using Request internally.', lib_name='RequestsLibrary', status='ACTIVE', docs='http://bulkan.github.io/robotframework-requests/')
    lib10 = suite_libs(name='TFTPLibrary', descr='Library for interacting over Trivial File Transfer Portocol.', lib_name='TftpLibrary', status='ACTIVE', docs='https://kowalpy.github.io/Robot-Framework-TFTP-Library/TftpLibrary.html')
    lib11 = suite_libs(name='AppiumLibrary', descr='Library for Android- and iOS-testing.', lib_name='AppiumLibrary', status='ACTIVE',docs='http://serhatbolsu.github.io/robotframework-appiumlibrary/AppiumLibrary.html')

    lib1.save()
    lib2.save()
    lib3.save()
    lib4.save()
    lib5.save()
    lib6.save()
    lib7.save()
    lib8.save()
    lib9.save()
    lib10.save()
    lib11.save()

    print("Suite Libs OK")
    
    #5. Create Helloword test
    print("4.Create helloword...")
    
    dtn = datetime.datetime.now()
    
    hello1 = temp_main(descr='HelloWorld', dt=str(dtn), notes='First Helloworld test', owner_id=User.objects.get(id=1).id)
    hello1.save()
    
    hello2 = temp_case(descr='Test Case Hello', main_id_id=temp_main.objects.get(id=1).id, owner_id=User.objects.get(id=1).id)
    hello2.save()
    
    hello3_1 = temp_variables(v_key='${FORM_URL}', v_val='http://aidaproject.io', main_id_id=temp_main.objects.get(id=1).id, owner_id=User.objects.get(id=1).id)
    hello3_2 = temp_variables(v_key='${TEXT}', v_val='Aida', main_id_id=temp_main.objects.get(id=1).id, owner_id=User.objects.get(id=1).id)
    hello3_1.save()
    hello3_2.save()
    
    hello4_1 = temp_library(l_type='Library', l_val='Selenium2Library', main_id_id=temp_main.objects.get(id=1).id, owner_id=User.objects.get(id=1).id)
    hello4_2 = temp_library(l_type='Test Setup', l_val='Open Browser And Go To Page', main_id_id=temp_main.objects.get(id=1).id, owner_id=User.objects.get(id=1).id)
    hello4_3 = temp_library(l_type='Test Teardown', l_val='Close Browser', main_id_id=temp_main.objects.get(id=1).id, owner_id=User.objects.get(id=1).id)   
    hello4_1.save()
    hello4_2.save()
    hello4_3.save()
    
    hello5_1 = temp_test_keywords(key_id_id=temp_keywords.objects.get(id=178).id, main_id_id=temp_main.objects.get(id=1).id, test_id_id=temp_case.objects.get(id=1).id, key_val='When visit the page it should show the text Aida', owner_id=User.objects.get(id=1).id)
    hello5_2 = temp_test_keywords(key_id_id=temp_keywords.objects.get(id=104).id, main_id_id=temp_main.objects.get(id=1).id, test_id_id=temp_case.objects.get(id=1).id, key_val='${TEXT}', owner_id=User.objects.get(id=1).id)
    hello5_1.save()
    hello5_2.save()
    
    #First add my personal key_id_id
    addkey_pers = temp_keywords(descr='Open Browser And Go To Page', human='Open Browser And Go To Page', personal=True, owner_id=User.objects.get(id=1).id)
    addkey_pers.save()
    
    hello6 = temp_pers_keywords(main_id_id=temp_main.objects.get(id=1).id, pers_id_id=temp_keywords.objects.get(id=187).id, standard_id_id=temp_keywords.objects.get(id=102).id, owner_id=User.objects.get(id=1).id, variable_val='${FORM_URL}')
    hello6.save()
    
    
    print("Helloword OK")
    
    #6. Send email
    print("5.Preparing and sending welcome email...")
    
    """
    email = EmailMessage('Test first registration OK', 'First registration email ok',
                         'kingmalza@comunicame.it',
                         to=['alessandro.malzanini@gmail.com'])
    try:
        email.send()
        print("Email send")
    except Exception as e:
        print(e)

    """
    context = {
        'news': 'We have good news!'
    }
    
    l_sender = []
    l_sender.append(str(User.objects.get(id=1).email))
    
    try:
        send_html_email(l_sender, 'Get started with Aida', 'email.html', context, sender='wepredict@cathedral.ai')
        print("Email send")
    except Exception as e:
        print(e)
    

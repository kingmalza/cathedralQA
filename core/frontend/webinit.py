#Utility for create and setup new tenants, register first data and send registration email

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from frontend.models import Client
from frontend.models import t_schedsettings, settings_gen
from frontend.models import temp_keywords, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords

import datetime


tk = ['Add Cookie','Add Location Strategy','Alert Should Be Present','Alert Should Not Be Present','Assign Id To Element','Capture Page Screenshot','Checkbox Should Be Selected','Checkbox Should Not Be Selected','Choose Cancel On Next Confirmation','Choose File','Choose Ok On Next Confirmation','Clear Element Text','Click Button','Click Element','Click Element At Coordinates','Click Image','Click Link','Close All Browsers','Close Browser','Close Window','Confirm Action','Create Webdriver','Current Frame Contains','Current Frame Should Contain','Current Frame Should Not Contain','Delete All Cookies','Delete Cookie','Dismiss Alert','Double Click Element','Drag And Drop','Drag And Drop By Offset','Element Should Be Disabled','Element Should Be Enabled','Element Should Be Focused','Element Should Be Visible','Element Should Contain','Element Should Not Be Visible','Element Should Not Contain','Element Text Should Be','Execute Async Javascript','Execute Javascript','Focus','Frame Should Contain','Get Alert Message','Get All Links','Get Cookie','Get Cookie Value','Get Cookies','Get Element Attribute','Get Element Count','Get Element Size','Get Horizontal Position','Get List Items','Get Location','Get Locations','Get Matching Xpath Count','Get Selected List Label','Get Selected List Labels','Get Selected List Value','Get Selected List Values','Get Selenium Implicit Wait','Get Selenium Speed','Get Selenium Timeout','Get Source','Get Table Cell','Get Text','Get Title','Get Value','Get Vertical Position','Get WebElement','Get WebElements','Get Window Handles','Get Window Identifiers','Get Window Names','Get Window Position','Get Window Size','Get Window Titles','Go Back','Go To','Handle Alert','Input Password','Input Text','Input Text Into Alert','Input Text Into Prompt','List Selection Should Be','List Should Have No Selections','List Windows','Location Should Be','Location Should Contain','Locator Should Match X Times','Log Location','Log Source','Log Title','Maximize Browser Window','Mouse Down','Mouse Down On Image','Mouse Down On Link','Mouse Out','Mouse Over','Mouse Up','Open Browser','Open Context Menu','Page Should Contain','Page Should Contain Button','Page Should Contain Checkbox','Page Should Contain Element','Page Should Contain Image','Page Should Contain Link','Page Should Contain List','Page Should Contain Radio Button','Page Should Contain Textfield','Page Should Not Contain','Page Should Not Contain Button','Page Should Not Contain Checkbox','Page Should Not Contain Element','Page Should Not Contain Image','Page Should Not Contain Link','Page Should Not Contain List','Page Should Not Contain Radio Button','Page Should Not Contain Textfield','Press Key','Radio Button Should Be Set To','Radio Button Should Not Be Selected','Register Keyword To Run On Failure','Reload Page','Remove Location Strategy','Select All From List','Select Checkbox','Select Frame','Select From List','Select From List By Index','Select From List By Label','Select From List By Value','Select Radio Button','Select Window','Set Browser Implicit Wait','Set Focus To Element','Set Screenshot Directory','Set Selenium Implicit Wait','Set Selenium Speed','Set Selenium Timeout','Set Window Position','Set Window Size','Simulate','Simulate Event','Submit Form','Switch Browser','Table Cell Should Contain','Table Column Should Contain','Table Footer Should Contain','Table Header Should Contain','Table Row Should Contain','Table Should Contain','Textarea Should Contain','Textarea Value Should Be','Textfield Should Contain','Textfield Value Should Be','Title Should Be','Unselect All From List','Unselect Checkbox','Unselect Frame','Unselect From List','Unselect From List By Index','Unselect From List By Label','Unselect From List By Value','Wait For Condition','Wait Until Element Contains','Wait Until Element Does Not Contain','Wait Until Element Is Enabled','Wait Until Element Is Not Visible','Wait Until Element Is Visible','Wait Until Page Contains','Wait Until Page Contains Element','Wait Until Page Does Not Contain','Wait Until Page Does Not Contain Element','Xpath Should Match X Times','[Documentation]','Sleep','Pause Execution',':FOR','\\']


def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, to=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
    

def create1(t_tenant,t_name):
    
    #1 Create tenant entry and populate db schema
    tenant = Client(domain_url=t_tenant+'.myaida.io', schema_name=t_tenant,name=t_name, paid_until='2019-12-05',on_trial=False)
    tenant.save()

    #Insert tenant value in settings table
    tenant_insert = settings_gen(tenant_name=t_tenant)
    tenant_insert.save()
    

def create2():
  
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
    
    #4. Create Helloword test
    print("3.Create helloword...")
    
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
    
    hello5_1 = temp_test_keywords(key_id_id=temp_keywords.objects.get(id=177).id, main_id_id=temp_main.objects.get(id=1).id, test_id_id=temp_case.objects.get(id=1).id, key_val='When visit the page it should show the text Aida', owner_id=User.objects.get(id=1).id)
    hello5_2 = temp_test_keywords(key_id_id=temp_keywords.objects.get(id=103).id, main_id_id=temp_main.objects.get(id=1).id, test_id_id=temp_case.objects.get(id=1).id, key_val='${TEXT}', owner_id=User.objects.get(id=1).id)
    hello5_1.save()
    hello5_2.save()
    
    #First add my personal key_id_id
    addkey_pers = temp_keywords(descr='Open Browser And Go To Page', human='Open Browser And Go To Page', personal=True, owner_id=User.objects.get(id=1).id)
    addkey_pers.save()
    
    hello6 = temp_pers_keywords(main_id_id=temp_main.objects.get(id=1).id, pers_id_id=temp_keywords.objects.get(id=182).id, standard_id_id=temp_keywords.objects.get(id=101).id, owner_id=User.objects.get(id=1).id, variable_val='${FORM_URL}')
    hello6.save()
    
    
    print("Helloword OK")
    
    #5. Send email
    print("4.Preparing and sending welcome email...")
    
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
    

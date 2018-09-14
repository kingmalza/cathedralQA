#Utility for create and setup new tenants

from frontend.models import Client
from frontend.models import t_schedsettings
from frontend.models import temp_keywords

from django.contrib.auth.models import User

tk = ['Add Cookie','Add Location Strategy','Alert Should Be Present','Alert Should Not Be Present','Assign Id To Element','Capture Page Screenshot','Checkbox Should Be Selected','Checkbox Should Not Be Selected','Choose Cancel On Next Confirmation','Choose File','Choose Ok On Next Confirmation','Clear Element Text','Click Button','Click Element','Click Element At Coordinates','Click Image','Click Link','Close All Browsers','Close Browser','Close Window','Confirm Action','Create Webdriver','Current Frame Contains','Current Frame Should Contain','Current Frame Should Not Contain','Delete All Cookies','Delete Cookie','Dismiss Alert','Double Click Element','Drag And Drop','Drag And Drop By Offset','Element Should Be Disabled','Element Should Be Enabled','Element Should Be Focused','Element Should Be Visible','Element Should Contain','Element Should Not Be Visible','Element Should Not Contain','Element Text Should Be','Execute Async Javascript','Execute Javascript','Focus','Frame Should Contain','Get Alert Message','Get All Links','Get Cookie','Get Cookie Value','Get Cookies','Get Element Attribute','Get Element Count','Get Element Size','Get Horizontal Position','Get List Items','Get Location','Get Locations','Get Matching Xpath Count','Get Selected List Label','Get Selected List Labels','Get Selected List Value','Get Selected List Values','Get Selenium Implicit Wait','Get Selenium Speed','Get Selenium Timeout','Get Source','Get Table Cell','Get Text','Get Title','Get Value','Get Vertical Position','Get WebElement','Get WebElements','Get Window Handles','Get Window Identifiers','Get Window Names','Get Window Position','Get Window Size','Get Window Titles','Go Back','Go To','Handle Alert','Input Password','Input Text','Input Text Into Alert','Input Text Into Prompt','List Selection Should Be','List Should Have No Selections','List Windows','Location Should Be','Location Should Contain','Locator Should Match X Times','Log Location','Log Source','Log Title','Maximize Browser Window','Mouse Down','Mouse Down On Image','Mouse Down On Link','Mouse Out','Mouse Over','Mouse Up','Open Browser','Open Context Menu','Page Should Contain','Page Should Contain Button','Page Should Contain Checkbox','Page Should Contain Element','Page Should Contain Image','Page Should Contain Link','Page Should Contain List','Page Should Contain Radio Button','Page Should Contain Textfield','Page Should Not Contain','Page Should Not Contain Button','Page Should Not Contain Checkbox','Page Should Not Contain Element','Page Should Not Contain Image','Page Should Not Contain Link','Page Should Not Contain List','Page Should Not Contain Radio Button','Page Should Not Contain Textfield','Press Key','Radio Button Should Be Set To','Radio Button Should Not Be Selected','Register Keyword To Run On Failure','Reload Page','Remove Location Strategy','Select All From List','Select Checkbox','Select Frame','Select From List','Select From List By Index','Select From List By Label','Select From List By Value','Select Radio Button','Select Window','Set Browser Implicit Wait','Set Focus To Element','Set Screenshot Directory','Set Selenium Implicit Wait','Set Selenium Speed','Set Selenium Timeout','Set Window Position','Set Window Size','Simulate','Simulate Event','Submit Form','Switch Browser','Table Cell Should Contain','Table Column Should Contain','Table Footer Should Contain','Table Header Should Contain','Table Row Should Contain','Table Should Contain','Textarea Should Contain','Textarea Value Should Be','Textfield Should Contain','Textfield Value Should Be','Title Should Be','Unselect All From List','Unselect Checkbox','Unselect Frame','Unselect From List','Unselect From List By Index','Unselect From List By Label','Unselect From List By Value','Wait For Condition','Wait Until Element Contains','Wait Until Element Does Not Contain','Wait Until Element Is Enabled','Wait Until Element Is Not Visible','Wait Until Element Is Visible','Wait Until Page Contains','Wait Until Page Contains Element','Wait Until Page Does Not Contain','Wait Until Page Does Not Contain Element','Xpath Should Match X Times','[Documentation]','Sleep','Pause Execution',':FOR','\\']

def create1(t_tenant,t_name):
    
    #1 Create tenant entry and populate db schema
    tenant = Client(domain_url=t_tenant+'.aidaproject.io', schema_name=t_tenant,name=t_name, paid_until='2019-12-05',on_trial=False)
    tenant.save()
    

def create2():
    
    #2 Populate schedule table
    sched1 = t_schedsettings(sched_desc='Once', sched_command='once')
    sched2 = t_schedsettings(sched_desc='Every minutes', sched_command='everymin')
    sched3 = t_schedsettings(sched_desc='Every hour', sched_command='everyhour')
    sched4 = t_schedsettings(sched_desc='Every day', sched_command='everyday')

    sched1.save()
    sched2.save()
    sched3.save()
    sched4.save()
    
    #3 Create Keyword tale
    global tk
    for i in tk:
        addkey = temp_keywords(descr=str(i), human=str(i), personal=False, owner_id=User.objects.get(id=1).id)
        addkey.save()
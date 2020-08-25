# cathedralQA
Repo for the open source Test Suite Cathedral project

Aida ATM (Automa-on Test Suite) allows you to
independently create, manage, plan and execute any type
of test on any type of soNware / firmware, a fundamental
characterisBc for every company in every industrial sector.
Aida is based on a roboframework and selenium plaTorm, it
uses a fast and intuiBve graphic interface for the creaBon of
its own test models and allows the importaBon of any
custom clilent libraries inside the suite.

# Installation
I use an ubuntu server machine for develop and test cathedral, with a postgresql db (mandatory because of use of different schemas related to tenants options) and nginx as webserver.
For the srver installation follow these details:

## Server setup
-Create your ubuntu server machine

-Install python3
```
sudo apt-get install python3.6
```

-Install python-pip
```
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
#sudo apt-get install python-pip
sudo apt-get -y install python3-pip
```

-Install virtualenv for creating a new dedicate virtual enviroment (not mandatory but strongly suggested)
```
pip3 install virtualenv
```

-Create .venv in home and install all requirements
```
python -m virtualenv .venv --python=python3
```

-Install nginx
```
sudo apt-get update
sudo apt-get install nginx
sudo service nginx restart
```

-Modify /etc/nginx permission, adding 775 and ubuntu group (or for your server user)
```
sudo chmod -R 775 /etc/nginx
sudo chgrp -R ubuntu /etc/nginx
```
Start nginx service
```
sudo service nginx restart
```

-Create folder var/www and copy all web project
```
#change www folder permission
sudo chmod -R 775 /var/www
sudo chgrp -R ubuntu /var/www
```

-Copy all cathedral file in web folder (or use directly git repo)

-Install Firefox
```
sudo apt-get install firefox
```

-Set geckodriver
(https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)

-Install these x component
```
sudo apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
sudo apt-get install xvfb
sudo apt-get install xserver-xorg-core
```

```
#For make path permanent:
sudo nano ~/.profile
#At the end
PATH=$PATH:/usr/local/lib
export PATH

Xvfb :99 &
export DISPLAY=:99
```

-Install Chrome
```
sudo apt-get install unzip
/usr/local/lib$ wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo apt-get install -y chromium-browser
```

-Update to python 3 (if needed)
```
update-alternatives --install /usr/bin/python python /usr/bin/python3 1
sudo apt install python3-pip -y
which pip3
ln -s /usr/bin/pip3 /usr/bin/pip
pip —version
```

-Install postgresql (**important**)

(https://tecadmin.net/install-postgresql-server-on-ubuntu/)

[Click here set defautl password of postgres user to postgres](https://serverfault.com/questions/110154/whats-the-default-superuser-username-password-for-postgres-after-a-new-install)

## Teant and Cathedral enviroment setup
After the corect instalation of your server you need to configure almost a new enviroment (my software allow to use different third leveldomain as separated enviroment for use te test suite in separed ares) for use cathedral

-Create the DNS record on yourserver
For example if you whant use your cathedral installation for two different business area ex. developers and testers yo can create dev.yourserver.com and test.yourserver.com and in your DNS set an A RECORD with the ip of the created server for this domain


-Create schema and populate tables (**important**)
```

python manage.py shell

from frontend.webinit import create1
create1(<schema_name>,<schema_description>)

CTRL+Z

python manage.py createsuperuser --schema=<schemaname>

python manage.py tenant_command shell --schema=<schemaname>

from frontend.webinit import create2
create2(<schema_name>,<pass_prompted>,<email>,<stripe plan(ondemand or flat)>,<stripe id (get it from stripe customer),’0.49’)
```

-Insert data into license database (from PostgreesSql)
```
INSERT INTO public.a_lic(
            lic_num, is_active, activate_date, descr, note, type, tenant)
    VALUES (<unique lic num>, 'True',<today data> , '', '', 'WEB', <tenant name>);
```

-From server terminal rsequencer INDEX FOR DB
```
python manage.py sqlsequencereset frontend
```

- Fill SETTINGS_GEN Ttable with new registration data

-If you whant use stripe for your marketplace income From stripe registration data get details and fill table (seting_gen stripe_id field)


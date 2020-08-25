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
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
#sudo apt-get install python-pip
sudo apt-get -y install python3-pip

pip3 install virtualenv

-Create .venv36 in home and install all requirements

python -m virtualenv .venv36 --python=python3


-Install nginx

sudo apt-get update
sudo apt-get install nginx
sudo service nginx restart

#Modify /etc/nginx permission, adding 775 and ubuntu group
sudo chmod -R 775 /etc/nginx
sudo chgrp -R ubuntu /etc/nginx

#Copy nginx.conf in /etc/nginx
#change user in line5 of nginx.conf with ububtu
sudo service nginx restart


-Create folder var/www and copy all web project
#change www folder permission
sudo chmod -R 775 /var/www
sudo chgrp -R ubuntu /var/www

-Copy web folder (remove p.y file for standalone client)


-Register AWS key

aws configure (file in drve path)


-Install Firefox

sudo apt-get install firefox

--Set geckodriver
https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu


sudo apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
sudo apt-get install xvfb
sudo apt-get install xserver-xorg-core

#For make path permanent:
sudo nano ~/.profile
#At the end
PATH=$PATH:/usr/local/lib
export PATH

Xvfb :99 &
export DISPLAY=:99



-Install Chrome

sudo apt-get install unzip
/usr/local/lib$ wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo apt-get install -y chromium-browser

-Update to python 3

update-alternatives --install /usr/bin/python python /usr/bin/python3 1

sudo apt install python3-pip -y

which pip3
ln -s /usr/bin/pip3 /usr/bin/pip

pip —version


-Install postgresql

https://tecadmin.net/install-postgresql-server-on-ubuntu/

(for set defautl password of postgres user to postgres see: https://serverfault.com/questions/110154/whats-the-default-superuser-username-password-for-postgres-after-a-new-install)


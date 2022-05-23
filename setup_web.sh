#!/bin/bash
set -e

while getopts a:h flag
do
    case "${flag}" in
        a) ANTICARIUM_SERVER_IP=${OPTARG};;
        h) echo "Anticarium WEB first time setup script for Raspberry Pi
  Arguments:
  -a        public ip address of Raspberry Pi's router for WEB server"; 
            exit 0;;
    esac
done

if [ -z "$ANTICARIUM_SERVER_IP" ]
then
    >&2 echo "Error: ANTICARIUM_SERVER_IP environment variable not set! Use -a flag to pass and set it!"
    exit -1
fi

echo -e "Setting up Anticarium WEB...\n\n"

#-----------------------------------------------------------------
echo "Installing apache2..."

sudo apt install -y apache2

EXPORT_COMMAND="export ANTICARIUM_WEB_PATH=$HOME/Anticarium_Web"
echo $EXPORT_COMMAND >> .profile
sudo sh -c "echo $EXPORT_COMMAND >> /etc/apache2/envvars"

EXPORT_COMMAND="export ANTICARIUM_SERVER_IP=$ANTICARIUM_SERVER_IP"
echo $EXPORT_COMMAND >> .profile
sudo sh -c "echo $EXPORT_COMMAND >> /etc/apache2/envvars"

echo -e "apache2 successfully installed\n\n"

#-----------------------------------------------------------------
echo "Installing libapache2-mod-wsgi-py3..."
sudo apt-get install -y libapache2-mod-wsgi-py3
echo -e "libapache2-mod-wsgi-py3 successfully installed\n\n"

#-----------------------------------------------------------------
echo "Installing python3-dev..."
sudo apt-get install -y python3-dev
echo -e "python3-dev successfully installed\n\n"

#-----------------------------------------------------------------
echo "Installing python3-pip..."
sudo apt-get install -y python3-pip
echo -e "python3-pip successfully installed\n\n"

#-----------------------------------------------------------------
echo "Installing flask..."
pip3 install flask
sudo chmod -R 755 $HOME/.local
echo -e "flask successfully installed\n\n"

#-----------------------------------------------------------------
echo "Configuring apache2..."
cd $HOME/Anticarium_Web
set +e
find anticarium.db
DATABASE_FOUND=$?
set -e
if [ $DATABASE_FOUND != 0 ]
then
    ./sqlite.py
fi
mv json_files.example json_files
chmod -R 777 json_files
mv anticarium_web.example anticarium_web.conf
sudo mv ./anticarium_web.conf /etc/apache2/sites-available
sudo mv ./apache2.conf.example /etc/apache2/apache2.conf
cd /etc/apache2/sites-available
sudo a2ensite anticarium_web.conf
sudo service apache2 reload
cd $HOME
echo -e "Configured apache2\n\n"


echo "Anticarium WEB successfully set up"
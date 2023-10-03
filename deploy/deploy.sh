#!/bin/bash
DIRECTORY=$(cd $(dirname $0) && pwd)

cd ..
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

cd deploy

sudo ln -s $DIRECTORY/My_blog.supervisor.conf /etc/supervisor/conf.d/My_blog.supervisor.conf
sudo supervisorctl reread
# sudo supervisorctl reload
sudo supervisorctl restart My_blog
echo "enter any key to continue."
read
sudo ln -s $DIRECTORY/My_blog.nginx.conf /etc/nginx/sites-available/

sudo ln -s $DIRECTORY/My_blog.nginx.conf /etc/nginx/sites-available/My_blog.nginx.conf
sudo ln -s /etc/nginx/sites-available/My_blog.nginx.conf /etc/nginx/sites-enabled/My_blog.nginx.conf
sudo nginx -t
echo "enter any key to continue with restarting nginx"
read
sudo service nginx restart

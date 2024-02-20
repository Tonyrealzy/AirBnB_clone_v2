#!/usr/bin/env bash
# Bash script to set up a web server for deployment of web_static.

# Update package information and install Nginx
apt-get update
apt-get install -y nginx

# Create necessary directories for web deployment
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a simple index.html file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create a symbolic link to the current release
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership and group for the /data directory
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Configure Nginx default site configuration
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
service nginx restart

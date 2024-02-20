# Variables
$nginx_conf = "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
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
}"

# Install Nginx package
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/releases/test', '/data/web_static/shared']:
  ensure  => 'directory',
}

# Create test index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
}

# Create symbolic link to the test release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Set ownership of /data directory
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

# Create web server directories
file { ['/var/www', '/var/www/html']:
  ensure => 'directory',
}

# Create default index.html and 404.html files
file { ['/var/www/html/index.html', '/var/www/html/404.html']:
  ensure  => 'present',
  content => ["Holberton School Nginx\n", "Ceci n'est pas une page\n"],
}

# Configure Nginx default site
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
} ->

# Restart Nginx service
service { 'nginx':
  ensure => 'running',
  enable => true,
}

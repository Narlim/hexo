---
title: nginx配置总结(二)
date: 2020-01-05 14:56:21
tags: nginx
---

ssl, basic_auth, certbot, reverse_proxy, load_balance
<!--more-->

### ssl

```nginx
worker_processes auto;
  
events {
  worker_connections 1024;
}

http {

  include mime.types;


  server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_uri;
  }


  server {

    listen 443 ssl http2;
    server_name localhost;

    root /sites/demo;

    index index.html;

    ssl_certificate /etc/nginx/ssl/self.crt;
    ssl_certificate_key /etc/nginx/ssl/self.key;

    # Disable SSL
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    # Optimise cipher suits
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

    # Enable DH Params
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    # Enable HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;

    # SSL sessions
    ssl_session_cache shared:SSL:40m;
    ssl_session_timeout 4h;
    ssl_session_tickets on;

    location / {
      try_files $uri $uri/ =404;
    }

    location ~\.php$ {
      # Pass php requests to the php-fpm service (fastcgi)
      include fastcgi.conf;
      fastcgi_pass unix:/run/php/php7.1-fpm.sock;
    }
  }
}
```

### basic_auth

```nginx
    location / {
      auth_basic "Secure Area";
      auth_basic_user_file /etc/nginx/.htpasswd;
      try_files $uri $uri/ =404;
    }

### $ apt install htpasswd
### $ htpasswd -c /etc/nginx/.htpasswd
```

### certbot

```nginx
events {
}

http {

  server {
    listen 80;
    server_name youdomain.com;

    location / {
      return 200 'Hello from nginx.'
    }
  }
}


### 1. install certboot
### 2. $ certbot --nginx
### 3. $ ls -l /etc/letsencrypt/live/youdomain.com/
### 4. $ @weekly certbot renew 
```

### reverse_proxy

```nginx
events {
}

http {

  server {
    listen 8888;

    location / {
      return 200 "Hello from nginx.\n";
    }

    location /php {
      proxy_set_header proxied nginx;
      proxy_pass 'http://localhost:9999/';
    }
  }
}

# 1.
### $ curl http://localhost:8888
### Hello from nginx.

### $ php -S http://localhost:9999 resq.txt
### $ curl http://localhost:9999/resp.txt
### Hello from php

### 添加上面的nginx配置

### $ curl http://localhost:8888/php/resq.txt
### Hello from php
### $ curl http://localhost:8888/
### Hello from nginx.

### 在/etc/nginx下面新建一个show_request.php:
### <?php
    echo 'Path: ' . $_SERVER['REQUEST_URI'];
### php -S http://localhost:8888/php

### $ curl http://localhost:8888/php
### Path: /
### $ curl http://localhost:8888/php/some/url
### Path: //some/url
### 如果把praxy_pass 改成：'http://localhost/9999';
### $ curl http://localhost:8888/php
### Path: /php

# 2.
### 设置代理header，nginx到后端服务器之间的。
```

### load_balance

```nginx
events {
}

http {

  upstream php_servers {
    server localhost:10001;
    server localhost:10002;
    server localhost:10003;
  }

  server {
    listen 8888;

    location / {
      ip_hash
      proxy_pass http://php_servers;
    }

  }
}

# 1.
### echo 'PHP server1' > s1
### echo 'PHP server2' > s2
### echo 'PHP server3' > s3
### $ php -S localhost:10001 s1
### $ php -S localhost:10002 s2
### $ php -S localhost:10003 s3
### $ while sleep 0.5; do curl http://localhost:8888; done

# 2. load balancing method
### ip_hash: The method guarantees that requests from the same address get to the same server unless it is not available.
### least_conn: A request is sent to the server with the least number of active connections, again with server weights taken into consideration
```

下面是一个资源：
[https://github.com/fcambus/nginx-resources](https://github.com/fcambus/nginx-resources)

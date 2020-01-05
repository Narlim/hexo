---
title: nginx配置总结(一)
date: 2020-01-04 21:28:29
tags: nginx
---

nginx的一些总结。
<!--more-->

### location匹配规则

```nginx
events {}
  
http {
  include mime.types;

  server {
    listen 80;
    server_name 127.0.0.1;

    root /sites/demo;

## 1
    # Prefix match
#    location /greet {
#      return 200 'Hello from NGINX "/greet" location.';
#    }

## 2
    # Exact match
#    location = /greet {
#      return 200 'Hello from NGINX "/greet" location. - EXACT MATCH';
#    }

## 3
    # REGEX match - case sensitive
#    location ~ /greet[0-9] {
#      return 200 'Hello from NGINX "/greet" location. - REGEX MATCH';
#    }

## 4
    # REGEX match - case insensitive
    location ~* /greet[0-9] {
      return 200 'Hello from NGINX "/greet" location. - REGEX MATCH INSENSITIVE';
    }

## 5
    # Preferential Prefix match
    location ^~ /Greet2 {
      return 200 'Hello from NGINX "/greet" location.';
    }

  }
}

### 一、如果把1的路径改为‘/Greet2’，同时把4打开，发现匹配的是4，即使4的配置在后面。
### 二、如果把4和5打开，会发现先匹配的是5。
### 总结匹配的先后顺序：
### 1. Exact Match               =  uri
### 2. Preferential Prefix Match ^~ uri
### 3. REGEX Match               ~* uri
### 4. Prefix Match                 uri
```

### rewrite and redirect

```nginx
events {}
  
http {
  include mime.types;

  server {
    listen 80;
    server_name 127.0.0.1;

    root /sites/demo;

# 1.
    location /logo {
      return 307 /thumb.png;
    }
    ### 把/logo的uri重定向到/thumb.png

# 2.
#    rewrite ^/user/\w+ /greet;
#    location /greet {
#      return 200 "Hello user";
#    }
    ### 访问http://127.0.0.1/user/john，实际访问http://127.0.0.1/greet，但是浏览器地址栏的地址不变。


# 3.
#    rewrite ^/user/(\w+) /greet/$1;
    location = /greet/john {
      return 200 "Hello john";
    }

    ### 访问http://127.0.0.1/user/john，实际访问http://127.0.0.1/greet/john，会传递后面的正则。

# 4.
    rewrite ^/user/(\w+) /greet/$1 last;
    rewrite ^/greet/john /thumb.png;

    ### 如果后面有一个last，那这个rewrite就是最后一个rewrite规则，虽然后面还有rewrite也不会生效。
  }
}
```

### 变量

```nginx
events {}
  
http {
  include mime.types;

  server {
    listen 80;
    server_name 127.0.0.1;

    root /sites/demo;

    location /inspect {
      return 200 "$host\n$uri\n$args\n$arg_name";
      ### 访问：http://127.0.0.1/inspect?name=marlin
      ### 返回：
      ### 127.0.0.1
      ### /inspect
      ### name=marlin
      ### marlin
    }


    # Check static API key
#    if ( $arg_apikey != 1234 ) {
#      return 401 "Incorrect API Key";
#    }

    # Check if weekend
    set $weekend 'No';
    if ( $date_local ~ 'Saturday|Sunday' ) {
      set $weekend 'Yes';
    }

    location /is_weekend {
      return 200 $weekend;
    }
  }
}
```

### try_files

```nginx
vents {}
  
http {
  include mime.types;

  server {
    listen 80;
    server_name 127.0.0.1;

    root /sites/demo;


# 1. try_files

    try_files $uri /cat.png /greet /friendly_404;

    location /friendly_404 {
      return 404 "Sorry"
    }

    location /greet {
      return 200 "Hello user";
    }

    ### 访问‘http://127.0.0.1/nothing’
    ### try_files 会查找第一个变量，发现在‘/sites/demo’目录下没有nothing这个文件或文件夹，继续下一个
，也没有，以此类推，当所有参数都找不到的时候，最后会进行一个内部重定向。所以实际返回‘404 sorry’。


# 2. named_location

    try_files $uri /cat.png /greet @friendly_404;

    location @friendly_404 {
      return 404 "Sorry"
    }

    ### 把‘/’换成‘@’，命名location可以确保最后一个参数一定会被重定向。

  }
}
```

### 3种指令

```nginx
events {}

######################
# (1) Array Directive
######################
# Can be specified multiple times without overriding a previous setting
# Gets inherited by all child contexts
# Child context can override inheritance by re-declaring directive
access_log /var/log/nginx/access.log;
access_log /var/log/nginx/custom.log.gz custom_format;

http {

  # Include statement - non directive
  include mime.types;

  server {
    listen 80;
    server_name site1.com;

    # Inherits access_log from parent context (1)
  }

  server {
    listen 80;
    server_name site2.com;

    #########################
    # (2) Standard Directive
    #########################
    # Can only be declared once. A second declaration overrides the first
    # Gets inherited by all child contexts
    # Child context can override inheritance by re-declaring directive
    root /sites/site2;

    # Completely overrides inheritance from (1)
    access_log off;

    location /images {

      # Uses root directive inherited from (2)
      try_files $uri /stock.png;
    }

    location /secret {
      #######################
      # (3) Action Directive
      #######################
      # Invokes an action such as a rewrite or redirect
      # Inheritance does not apply as the request is either stopped (redirect/response) or re-evaluated (rewrite)
      return 403 "You do not have permission to view this.";
    }
  }
}
```

### 缓存和超时配置

```nginx
user www-data;

worker_processes auto;

events {
  worker_connections 1024;
}

http {

  include mime.types;

  # Buffer size for POST submissions
  client_body_buffer_size 10K;
  client_max_body_size 8m;

  # Buffer size for Headers
  client_header_buffer_size 1k;

  # Max time to receive client headers/body
  client_body_timeout 12;
  client_header_timeout 12;

  # Max time to keep a connection open for
  keepalive_timeout 15;

  # Max time for the client accept/receive a response
  send_timeout 10;

  # Skip buffering for static files
  sendfile on;

  # Optimise sendfile packets
  tcp_nopush on;

  server {

    listen 80;
    server_name 167.99.93.26;

    root /sites/demo;

    index index.php index.html;

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

### headers and expires

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

    root /sites/demo;

    index index.php index.html;

    location / {
      try_files $uri $uri/ =404;
    }

    location ~\.php$ {
      # Pass php requests to the php-fpm service (fastcgi)
      include fastcgi.conf;
      fastcgi_pass unix:/run/php/php7.1-fpm.sock;
    }

    location = /thumb.png {

      add_header Cache-Control public;
      add_header Pragma public;
      add_header Vary Accept-Encoding;
      expires 60m;
    }

    ### 60分钟的过期时间，文件缓存在客户端。

  }
}
```

# Challenge Linux 2

- Accéder aux labs pratiques : [Linux Challenges](https://learn.kodekloud.com/user/courses/linux-challenges)

## Résolution DNS

```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

## Installation des packages

```bash
yum install -y nginx firewalld
```


## Securité avec firewalld

```bash
systemctl enable firewalld
systemctl start firewalld
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=8081/tcp --permanent
firewall-cmd --zone=public --add-port=22/tcp --permanent
firewall-cmd --reload
```

## Exécution de Go App

```bash
pushd /home/bob/go-app
nohup go run main.go &
popd
```

## Config Nginx en Reverse Proxy

```bash
vi /etc/nginx/nginx.conf
```

```text
    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location = / {
            proxy_pass  http://localhost:8081;
        }

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }
```

```bash
systemctl enable --now nginx
```

## Vérification du fonctionnement GoApp

Cliquer sur le bouton GoApp au-dessus du terminal pour accéder à l’écran de login.

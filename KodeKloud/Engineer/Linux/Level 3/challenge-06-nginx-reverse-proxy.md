# Challenge 06 - Linux Nginx as Reverse Proxy

**Difficulté** : Level 3  
**Domaine** : Nginx, Reverse Proxy, Apache, Multi-Service Configuration  
**Date** : 18 janvier 2026

---

## 📋 Consigne

L'équipe des administrateurs système Nautilus prévoit de déployer une application frontend pour leur utilitaire de backup sur le serveur Nautilus Backup Server, afin de pouvoir gérer les sauvegardes de différents sites web depuis une interface graphique. Ils ont partagé les exigences pour mettre en place cette solution ; veuillez accomplir les tâches selon les détails ci-dessous :

a. Installer Apache Server sur le serveur Nautilus Backup Server et le configurer pour utiliser le port 8086 (ne pas le lier uniquement à 127.0.0.1, garder la configuration par défaut c'est-à-dire laisser Apache écouter sur l'IP du serveur, le hostname, localhost, 127.0.0.1 etc).

b. Installer le serveur web Nginx sur le serveur Nautilus Backup Server et le configurer pour utiliser le port 8095.

c. Configurer Nginx comme serveur reverse proxy pour Apache.

d. Il y a un fichier index d'exemple `/home/thor/index.html` sur le Jump Host, copier ce fichier dans le répertoire racine des documents Apache.

e. S'assurer de démarrer les services Apache et Nginx.

f. Vous pouvez tester les modifications finales en utilisant la commande curl, par exemple `curl http://<IP ou Hostname du serveur backup>:8095`.

---

## 🔧 Réalisation

### Étape 1 : Transfert index.html vers Backup Server

```bash
# Depuis Jump Host
scp /home/thor/index.html clint@stbkp01:/home/clint/
# Password: H@wk3y3 (user clint)
```

### Étape 2 : Connexion Backup Server

```bash
ssh clint@stbkp01
# Password: H@wk3y3
```

### Étape 3 : Installation Apache + Nginx

```bash
sudo yum install httpd nginx -y
```

**Packages installés** :
- `httpd` : Apache HTTP Server
- `nginx` : Nginx web server + reverse proxy
- Dependencies : libs, modules

**Vérification** :
```bash
rpm -qa | grep -E "httpd|nginx"
# httpd-2.4.6-99.el7.centos.x86_64
# nginx-1.20.1-10.el7.x86_64
```

### Étape 4 : Configuration Apache port 8086

```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Rechercher directive Listen** (environ ligne 42) :
```apache
Listen 80
```

**Modifier Listen 80 → Listen *:8086** :
```apache
Listen *:8086
```

**Explication** :
- `Listen *:8086` : Bind ALL interfaces (*, équivalent 0.0.0.0) port 8086
- **NOT** `Listen 127.0.0.1:8086` (localhost only)
- Accessible : localhost, server IP, hostname

**Sauvegarder** : `:wq`

### Étape 5 : Déployer index.html Apache

```bash
sudo mv /home/clint/index.html /var/www/html/
```

**Vérification** :
```bash
ls -l /var/www/html/
# index.html
```

### Étape 6 : Configuration Nginx

#### Supprimer bloc server default

```bash
sudo vi /etc/nginx/nginx.conf
```

**Rechercher bloc server** (dans section `http`) :
```nginx
http {
    # ...
    
    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;
        # ...
    }
}
```

**Supprimer TOUT bloc `server { ... }`** (éviter conflict port).

**Sauvegarder** : `:wq`

#### Créer configuration reverse proxy

```bash
sudo vi /etc/nginx/conf.d/reverse_proxy.conf
```

**Insérer configuration** :
```nginx
upstream backend_app {
    server 127.0.0.1:8086;  # Apache backend
    keepalive 32;
}

server {
    listen 8095;
    server_name _;

    # Security headers (basic)
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header Referrer-Policy strict-origin-when-cross-origin;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts and buffers
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering on;
        proxy_buffers 32 16k;
        proxy_busy_buffers_size 64k;

        proxy_http_version 1.1;
        proxy_pass http://backend_app;
    }
}
```

**Sauvegarder** : `:wq`

**Explication configuration** :

**upstream backend_app** :
- `server 127.0.0.1:8086` : Apache backend localhost port 8086
- `keepalive 32` : Persistent connections pool (performance)

**server block** :
- `listen 8095` : Nginx écoute port 8095 (frontend public)
- `server_name _` : Catch-all (any hostname)

**Security headers** :
- `X-Content-Type-Options: nosniff` : Prevent MIME sniffing
- `X-Frame-Options: SAMEORIGIN` : Clickjacking protection
- `Referrer-Policy: strict-origin-when-cross-origin` : Referrer privacy

**location / block** :
- `proxy_set_header Host $host` : Preserve original Host header
- `proxy_set_header X-Real-IP $remote_addr` : Client real IP
- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for` : Proxy chain IPs
- `proxy_set_header X-Forwarded-Proto $scheme` : HTTP/HTTPS scheme
- `proxy_http_version 1.1` : HTTP/1.1 backend (keepalive support)
- `proxy_pass http://backend_app` : Forward requests to upstream

**Timeouts** :
- `proxy_connect_timeout 5s` : Connect backend timeout (5 seconds)
- `proxy_send_timeout 60s` : Send request timeout
- `proxy_read_timeout 60s` : Read response timeout

**Buffers** :
- `proxy_buffering on` : Enable response buffering (performance)
- `proxy_buffers 32 16k` : 32 buffers × 16KB (512KB total)
- `proxy_busy_buffers_size 64k` : Busy buffers size

### Étape 7 : Validation syntax Nginx

```bash
sudo nginx -t
# Output :
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Étape 8 : Démarrage services

```bash
# Démarrer Apache
sudo systemctl enable --now httpd

# Démarrer Nginx
sudo systemctl enable --now nginx
```

**Vérification status** :
```bash
sudo systemctl status httpd
# Active (running)

sudo systemctl status nginx
# Active (running)
```

### Étape 9 : Validation locale

```bash
# Test Apache direct (backend)
curl localhost:8086
# Output : HTML content index.html ✅

# Test Nginx reverse proxy (frontend)
curl localhost:8095
# Output : HTML content index.html (same) ✅
```

**Vérification ports listening** :
```bash
sudo netstat -tulnp | grep -E ":8086|:8095"
# tcp   0   0 0.0.0.0:8086   0.0.0.0:*   LISTEN   1234/httpd
# tcp   0   0 0.0.0.0:8095   0.0.0.0:*   LISTEN   5678/nginx
```

### Étape 10 : Validation remote (Jump Host)

```bash
# Depuis Jump Host
curl http://stbkp01:8095
# Output : HTML content index.html ✅
```

---

## 🔗 Ressources

**Nginx Documentation** :
- [Nginx Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Upstream Module](http://nginx.org/en/docs/http/ngx_http_upstream_module.html)
- [Proxy Module](http://nginx.org/en/docs/http/ngx_http_proxy_module.html)

**Security Headers** :
- [OWASP Secure Headers](https://owasp.org/www-project-secure-headers/)
- [Security Headers Scanner](https://securityheaders.com/)

**Nginx Optimization** :
- [Nginx Performance Tuning](https://www.nginx.com/blog/tuning-nginx/)
- [Nginx Caching Guide](https://www.nginx.com/blog/nginx-caching-guide/)
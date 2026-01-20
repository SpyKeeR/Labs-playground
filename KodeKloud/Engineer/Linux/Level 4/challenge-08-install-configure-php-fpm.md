# Challenge 08 - Install and Configure PHP-FPM

**Difficulté** : Level 4  
**Domaine** : Nginx, PHP-FPM, TCP Socket  
**Date** : 20 janvier 2026

---

## 📋 Consigne

L'équipe de développement d'applications Nautilus prévoit de lancer une nouvelle application basée sur PHP, qu'elle souhaite déployer sur l'infrastructure Nautilus dans le Stratos DC. L'équipe de développement a eu une réunion avec l'équipe de support production et ils ont partagé certaines exigences concernant l'infrastructure. Ci-dessous les exigences qu'ils ont partagées :

a. Installer nginx sur le serveur d'application 3, le configurer pour utiliser le port 8096 et son document root doit être `/var/www/html`.

b. Installer php-fpm version 8.3 sur le serveur d'application 3, il doit écouter sur le port 9000.

c. Configurer php-fpm et nginx pour qu'ils fonctionnent ensemble.

d. Une fois configuré correctement, vous pouvez tester le site web en utilisant la commande `curl http://stapp03:8096/index.php` depuis jump host. Veuillez noter que si l'URL affiche index.php en texte brut, c'est-à-dire que vous voyez <?php etc dans la sortie, cela indique que soit PHP-FPM n'est pas installé, soit Nginx n'est pas correctement configuré pour fonctionner avec PHP-FPM.

---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 3

```bash
ssh banner@stapp03
# Password: BigGr33n
```

### Étape 2 : Installation Remi Repository

```bash
sudo dnf install https://rpms.remirepo.net/enterprise/remi-release-$(rpm -E %rhel).rpm
sudo dnf install dnf-utils
```

**Explication** : Remi repository pour PHP 8.3 (pas disponible repos officiels)

### Étape 3 : Configuration module PHP

```bash
dnf module list php
sudo dnf module switch-to php:remi-8.3
sudo dnf install php-fpm -y
```

**Explication** : Switch vers module PHP 8.3 depuis Remi

### Étape 4 : Suppression Apache + Installation Nginx

```bash
sudo yum remove httpd -y
sudo yum install nginx -y
```

**Explication** : Éviter conflit port 80 Apache/Nginx

### Étape 5 : Configuration PHP-FPM

```bash
sudo vi /etc/php-fpm.d/www.conf
```

**Modifications** :
```ini
# Listen directive - TCP socket
listen = 9000

# User/Group (Apache → Nginx)
user = nginx
group = nginx

# Listen permissions
listen.owner = nginx
listen.group = nginx
```

**Explication** :
- `listen = 9000` : TCP socket (alternative Unix socket)
- User `nginx` : Même user que Nginx (permissions)

### Étape 6 : Configuration Nginx

```bash
sudo vi /etc/nginx/conf.d/app.conf
```

**Contenu** :
```nginx
server {
    listen       8096;
    server_name  _;

    root   /var/www/html;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
    
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

**Explication** :
- `fastcgi_pass 127.0.0.1:9000` : TCP socket (vs Unix socket)
- `try_files $uri =404` : Sécurité (évite exécution fichier inexistant)

### Étape 7 : Activation services

```bash
sudo systemctl enable --now nginx
sudo systemctl enable --now php-fpm
```

### Étape 8 : Vérification

```bash
curl http://localhost:8096/index.php
# Affiche output PHP (pas code source) ✅
```


## 🔗 Ressources

- [Remi Repository](https://rpms.remirepo.net/)
- [PHP-FPM TCP vs Unix Socket](https://www.php.net/manual/en/install.fpm.configuration.php)
- [Nginx FastCGI](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html)

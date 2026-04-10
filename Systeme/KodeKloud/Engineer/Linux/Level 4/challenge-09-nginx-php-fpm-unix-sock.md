# Challenge 09 - Configure Nginx + PHP-FPM Using UNIX Sock

**Difficulté** : Level 4  
**Domaine** : Nginx, PHP-FPM, Unix Socket  
**Date** : 20 janvier 2026

---

## 📋 Consigne

L'équipe de développement d'applications Nautilus prévoit de lancer une nouvelle application basée sur PHP, qu'elle souhaite déployer sur l'infrastructure Nautilus dans le Stratos DC. L'équipe de développement a eu une réunion avec l'équipe de support production et ils ont partagé certaines exigences concernant l'infrastructure. Ci-dessous les exigences qu'ils ont partagées :

a. Installer nginx sur le serveur d'application 3, le configurer pour utiliser le port 8091 et son document root doit être `/var/www/html`.

b. Installer php-fpm version 8.2 sur le serveur d'application 3, il doit utiliser le socket unix `/var/run/php-fpm/default.sock` (créer les répertoires parents s'ils n'existent pas).

c. Configurer php-fpm et nginx pour qu'ils fonctionnent ensemble.

d. Une fois configuré correctement, vous pouvez tester le site web en utilisant la commande `curl http://stapp03:8091/index.php` depuis jump host.

NOTE : Nous avons copié deux fichiers, index.php et info.php, sous /var/www/html dans le cadre de la configuration de l'application PHP. Veuillez ne pas modifier ces fichiers.

---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 3

```bash
ssh banner@stapp03
# Password: BigGr33n
```

### Étape 2 : Installation EPEL et Remi Repositories

```bash
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
sudo dnf install https://rpms.remirepo.net/enterprise/remi-release-9.rpm
```

**Explication** : EPEL + Remi pour PHP 8.2

### Étape 3 : Activation CodeReady Builder

```bash
sudo crb enable
```

**Explication** : CRB repository (dépendances build PHP)

### Étape 4 : Configuration module PHP

```bash
sudo dnf module reset php
sudo dnf module install php:remi-8.2
```

**Explication** : 
- `reset php` : Réinitialise module (si version précédente)
- `install php:remi-8.2` : Installe PHP 8.2 + php-fpm

### Étape 5 : Installation Nginx

```bash
sudo yum install nginx -y
```

### Étape 6 : Configuration Nginx

```bash
sudo vi /etc/nginx/conf.d/app.conf
```

**Contenu** :
```nginx
server {
    listen       8091;
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
        fastcgi_pass unix:/var/run/php-fpm/default.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

**Explication** :
- `fastcgi_pass unix:/var/run/php-fpm/default.sock` : Socket Unix custom

### Étape 7 : Configuration PHP-FPM

```bash
sudo vi /etc/php-fpm.d/www.conf
```

**Modifications** :
```ini
# Listen directive - Unix socket custom
listen = /var/run/php-fpm/default.sock

# User/Group (Apache → Nginx)
user = nginx
group = nginx

# Listen permissions
listen.owner = nginx
listen.group = nginx
listen.mode = 0660
```

**Explication** : Socket custom (pas `/run/php-fpm/www.sock` par défaut)

### Étape 8 : Création répertoire socket

```bash
sudo mkdir -p /var/run/php-fpm
sudo chown :nginx /var/run/php-fpm/
sudo chmod g+x /var/run/php-fpm
```

**Explication** :
- Répertoire parent n'existe pas par défaut
- Permissions groupe `nginx` (lecture/exécution)

### Étape 9 : Activation services

```bash
sudo systemctl enable --now nginx
sudo systemctl enable --now php-fpm
```

### Étape 10 : Vérification

```bash
curl http://localhost:8091/index.php
# Affiche output PHP ✅

curl http://localhost:8091/info.php
# Affiche phpinfo() ✅
```

**Vérifier socket créé** :
```bash
ls -l /var/run/php-fpm/default.sock
# srw-rw---- 1 nginx nginx 0 Jan 20 10:30 /var/run/php-fpm/default.sock
```

---

## 🔗 Ressources

- [PHP-FPM Unix Socket Configuration](https://www.php.net/manual/en/install.fpm.configuration.php)
- [Nginx FastCGI Unix Socket](https://www.nginx.com/resources/wiki/start/topics/examples/phpfcgi/)
- [RHEL CodeReady Builder](https://access.redhat.com/articles/4348511)

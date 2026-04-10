# Challenge 05 - Configure LAMP Server

**Difficulté** : Level 4  
**Domaine** : LAMP Stack, Apache, PHP-FPM, MariaDB, WordPress  
**Date** : 19 janvier 2026

---

## 📋 Consigne

xFusionCorp Industries prévoit d'héberger un site web WordPress sur leur infrastructure dans le Stratos Datacenter. Ils ont déjà effectué la configuration de l'infrastructure - par exemple, sur le serveur de stockage, ils ont déjà un répertoire partagé `/var/www/html` qui est monté sur chaque hôte d'application sous le répertoire `/var/www/html`. Veuillez effectuer les étapes suivantes pour accomplir la tâche :

a. Installer httpd, php et ses dépendances sur tous les hôtes d'application.

b. Apache doit servir sur le port 5000 dans les applications.

c. Installer/Configurer le serveur MariaDB sur le serveur de base de données.

d. Créer une base de données nommée `kodekloud_db9` et créer un utilisateur de base de données nommé `kodekloud_joy` identifié par le mot de passe `GyQkFRVNr3`. De plus, assurez-vous que cet utilisateur nouvellement créé est capable d'effectuer toutes les opérations sur la base de données que vous avez créée.

e. Enfin, vous devriez pouvoir accéder au site web sur le lien LBR, en cliquant sur le bouton App dans la barre supérieure. Vous devriez voir un message comme `App is able to connect to the database using user kodekloud_joy`

---

## 🔧 Réalisation

### Partie 1 : Configuration App Servers (3 serveurs identiques)

#### App Server 1

```bash
ssh tony@stapp01
# Password: Ir0nM@n
```

**Installation packages** :
```bash
sudo yum install httpd php-fpm php-mysqlnd -y
```

**Explication** :
- `httpd` : Serveur web Apache
- `php-fpm` : FastCGI Process Manager pour PHP
- `php-mysqlnd` : Driver MySQL Native pour PHP (connexion MariaDB)

---

**Configuration port Apache** :
```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Modifier directive Listen** :
```apache
# Avant
Listen 80

# Après
Listen 5000
```

**Explication** : Port custom 5000 au lieu de port standard 80

---

**Configuration VirtualHost** :
```bash
sudo vi /etc/httpd/conf.d/app.conf
```

**Contenu** :
```apache
<VirtualHost *:5000>
  ServerName www.stapp01.stratos.xfusioncorp.com
  ServerAlias stapp01.stratos.xfusioncorp.com
  DocumentRoot /var/www/html
  DirectoryIndex index.php
  
  <IfModule proxy_fcgi_module>
    <FilesMatch ".+\.ph(ar|p|tml)$">
      SetHandler "proxy:unix:/run/php-fpm/www.sock|fcgi://localhost"
    </FilesMatch>
  </IfModule>
</VirtualHost>
```

**Explication directives** :
- `DirectoryIndex index.php` : Fichier index par défaut
- `FilesMatch` : Regex fichiers PHP (.php, .phar, .phtml)
- `SetHandler proxy:unix:...` : Forward requêtes PHP vers socket PHP-FPM
- Socket Unix `/run/php-fpm/www.sock` (pas TCP)

---

**Activation extension mysqli** :
```bash
sudo vi /etc/php.ini
```

**Ajouter ligne** :
```ini
extension=mysqli
```

**Explication** : Extension PHP pour connexions MySQL/MariaDB

---

**Activation services** :
```bash
sudo systemctl enable --now httpd
sudo systemctl enable --now php-fpm
```

---

#### App Server 2 et 3

**Répéter configuration identique sur stapp02 et stapp03** :
```bash
ssh steve@stapp02  # Password: Am3ric@
ssh banner@stapp03 # Password: BigGr33n
```

**Seule différence** : `ServerName` dans VirtualHost
- stapp02 : `www.stapp02.stratos.xfusioncorp.com`
- stapp03 : `www.stapp03.stratos.xfusioncorp.com`

---

### Partie 2 : Configuration Database Server

```bash
ssh peter@stdb01
# Password: Sp!dy
```

**Installation MariaDB** :
```bash
sudo yum install mariadb-server -y
```

---

**Configuration bind address** :
```bash
sudo vi /etc/my.cnf.d/mariadb-server.cnf
```

**Décommenter ligne** :
```ini
[mysqld]
bind-address = 0.0.0.0
```

**Explication** : Autorise connexions externes (pas seulement localhost)

---

**Activation MariaDB** :
```bash
sudo systemctl enable --now mariadb
```

---

**Création database et user** :
```bash
sudo mysql
```

**Dans shell MariaDB** :
```sql
CREATE DATABASE kodekloud_db9;

CREATE USER 'kodekloud_joy'@'%' IDENTIFIED BY 'GyQkFRVNr3';

GRANT ALL PRIVILEGES ON kodekloud_db9.* TO 'kodekloud_joy'@'%';

FLUSH PRIVILEGES;
```

**Explication** :
- `'user'@'%'` : Accès depuis n'importe quel hôte (app servers)
- `GRANT ALL PRIVILEGES ON db.*` : Toutes permissions sur tables database
- `FLUSH PRIVILEGES` : Recharge table permissions

**Quitter** :
```sql
EXIT;
```

---

### Étape 3 : Vérification

**Test local sur chaque app server** :
```bash
curl stapp01:5000
curl stapp02:5000
curl stapp03:5000
# Output : App is able to connect to the database using user kodekloud_joy ✅
```

**Test via Load Balancer (interface Lab)** :
- Cliquer bouton **App** → Message connexion database affiché


## 🔗 Ressources

- [Apache mod_proxy_fcgi](https://httpd.apache.org/docs/2.4/mod/mod_proxy_fcgi.html)
- [MariaDB User Account Management](https://mariadb.com/kb/en/user-account-management/)
- [PHP MySQLi Extension](https://www.php.net/manual/en/book.mysqli.php)

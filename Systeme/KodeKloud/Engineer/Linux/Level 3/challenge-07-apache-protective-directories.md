# Challenge 07 - Configure Apache Protective Directories

**Difficulté** : Level 3  
**Domaine** : Apache, HTTP Basic Authentication, htpasswd  
**Date** : 18 janvier 2026

---

## 📋 Consigne

xFusionCorp Industries héberge plusieurs sites web statiques sur les serveurs d'applications Nautilus dans le Stratos DC. Certains répertoires confidentiels du document root nécessitent une protection par mot de passe. L'équipe de support production a décidé d'utiliser `.htaccess` avec l'authentification basique. Un site web doit être uploadé sur `/var/www/html/data` sur Nautilus App Server 2. Cependant, nous devons configurer l'authentification avant cela.

1. Créer le répertoire `/var/www/html/data` s'il n'existe pas.

2. Ajouter un utilisateur `javed` dans htpasswd et définir son mot de passe à `LQfKeWWxWD`.

3. Un fichier `/tmp/index.html` est présent sur le Jump Server. Copier ce fichier dans le répertoire créé, en s'assurant que le document root par défaut reste `/var/www/html`. Le site web doit fonctionner sur l'URL `http://<app-server-hostname>:8080/data/`

---

## 🔧 Réalisation

### Étape 1 : Transfert fichier depuis Jump Server

```bash
# Depuis Jump Server
scp /tmp/index.html steve@stapp02:/home/steve/
# Password: Am3ric@ (user steve)
```

**Explication** :
- Transfert `index.html` vers home directory de steve (pas les permissions pour écrire directement dans `/var/www/html/`)

### Étape 2 : Connexion App Server 2

```bash
ssh steve@stapp02
# Password: Am3ric@
```

### Étape 3 : Création structure répertoires

```bash
sudo mkdir /var/www/html/data
```

**Vérification** :
```bash
ls -ld /var/www/html/data
# drwxr-xr-x 2 root root 4096 Jan 18 22:15 /var/www/html/data
```

### Étape 4 : Déplacement fichier HTML

```bash
sudo mv /home/steve/index.html /var/www/html/data/
```

**Vérification** :
```bash
ls -l /var/www/html/data/
# -rw-r--r-- 1 root root 287 Jan 18 22:15 index.html
```

### Étape 5 : Configuration Apache pour autoriser .htaccess

```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Ajouter directive `AllowOverride`** :
```apache
<Directory "/var/www/html/data">
    AllowOverride All
</Directory>
```

**Explication** : `AllowOverride All` permet au fichier `.htaccess` de surcharger la configuration principale.

**Sauvegarder** : `:wq`

**Redémarrage Apache** :
```bash
sudo systemctl restart httpd
```

### Étape 6 : Configuration .htaccess

```bash
sudo vi /var/www/html/data/.htaccess
```

**Contenu fichier `.htaccess`** :
```apache
AuthUserFile /var/www/html/data/.htpasswd
AuthType Basic
AuthName "Accès restreint"
require valid-user
```

**Explication directives** :
- `AuthUserFile` : Chemin **absolu** vers fichier de mots de passe
- `AuthType Basic` : Type d'authentification HTTP Basic
- `AuthName` : Message affiché dans popup navigateur
- `require valid-user` : Tout utilisateur authentifié autorisé

**Sauvegarder** : `:wq`

### Étape 7 : Création fichier htpasswd

```bash
sudo htpasswd -c /var/www/html/data/.htpasswd javed
# New password: LQfKeWWxWD
# Re-type new password: LQfKeWWxWD
# Adding password for user javed
```

**Options** :
- `-c` : **Create** nouveau fichier (⚠️ écrase fichier existant si présent)
- `/var/www/html/data/.htpasswd` : Chemin fichier de mots de passe
- `javed` : Nom d'utilisateur

**Vérification fichier créé** :
```bash
sudo cat /var/www/html/data/.htpasswd
# javed:$apr1$A8kLm2Qx$vQJ8KT4zXhB9mD2.xYzL7/
```

Format : `username:$algorithm$salt$hash` (hash MD5 Apache)

### Étape 8 : Activation Apache

```bash
sudo systemctl enable --now httpd
```

**Vérification service** :
```bash
sudo systemctl status httpd
# Active (running)
```

### Étape 9 : Validation authentification

**Test avec credentials corrects** :
```bash
curl -u javed:LQfKeWWxWD localhost:8080/data/
# Output : Page HTML (HTTP 200 OK)
```

**Test sans authentification** :
```bash
curl localhost:8080/data/
# Output : 401 Unauthorized
# <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
# <html><head>
# <title>401 Unauthorized</title>
# ...
```

**Test avec mauvais mot de passe** :
```bash
curl -u javed:wrongpassword localhost:8080/data/
# Output : 401 Unauthorized
```

**Test verbose (headers HTTP)** :
```bash
curl -v -u javed:LQfKeWWxWD localhost:8080/data/
# > Authorization: Basic amF2ZWQ6TFFmS2VXV3hXRA==
# < HTTP/1.1 200 OK
# < Server: Apache/2.4.37 (centos)
# ...
```

**Test depuis Jump Host** :
```bash
curl -u javed:LQfKeWWxWD http://stapp02:8080/data/
# Output : Page HTML ✅
```

---

## 📂 Configuration finale

**Arborescence** :
```
/var/www/html/data/
├── .htaccess      (Configuration Apache HTTP Auth)
├── .htpasswd      (Fichier utilisateurs/mots de passe)
└── index.html     (Contenu protégé)
```

**Permissions** :
```bash
ls -la /var/www/html/data/
# -rw-r--r-- 1 root root  123 .htaccess
# -rw-r--r-- 1 root root   45 .htpasswd
# -rw-r--r-- 1 root root  287 index.html
```

---

## 🔗 Ressources

**Documentation Apache** :
- [Apache Authentication](https://httpd.apache.org/docs/2.4/howto/auth.html)
- [htpasswd Documentation](https://httpd.apache.org/docs/2.4/programs/htpasswd.html)
- [mod_auth_basic](https://httpd.apache.org/docs/2.4/mod/mod_auth_basic.html)

**HTTP Authentication** :
- [RFC 7617 - HTTP Basic Authentication](https://tools.ietf.org/html/rfc7617)
- [MDN - HTTP authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)

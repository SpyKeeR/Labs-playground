# Challenge 09 - Apache PAM Authentication

**Difficulté** : Level 3  
**Domaine** : Apache, PAM, Linux Authentication  
**Date** : 19 janvier 2026

---

## 📋 Consigne

Nous avons besoin de protéger par mot de passe un répertoire dans le document root du serveur web Apache. Nous souhaitons protéger par mot de passe l'URL `http://<website-url>:<apache_port>/protected/` selon les exigences suivantes (vous pouvez utiliser n'importe quelle website-url comme localhost car il n'y a pas d'exigences spécifiques pour le moment). Configurez cela sur App server 3 selon les exigences mentionnées ci-dessous :

a. Nous voulons utiliser l'authentification basique.

b. Nous ne voulons pas utiliser l'authentification basée sur le fichier htpasswd. Au lieu de cela, nous voulons utiliser l'authentification PAM, c'est-à-dire Basic Auth + PAM afin de pouvoir nous authentifier avec un utilisateur Linux.

c. Nous avons déjà un utilisateur `yousuf` avec le mot de passe `B4zNgHA7Ya` auquel vous devez fournir l'accès.

d. Vous pouvez tester cela en utilisant une commande curl depuis le jump host `curl http://<website-url>:<apache_port>/protected/`.

---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 3

```bash
ssh banner@stapp03
# Password: BigGr33n
```

### Étape 2 : Installation modules PAM

```bash
sudo yum install mod_authnz_pam -y
```

**Explication** : `mod_authnz_pam` permet l'authentification Apache via PAM (Pluggable Authentication Modules).

### Étape 3 : Activation module Apache

```bash
sudo vi /etc/httpd/conf.modules.d/55-authnz_pam.conf
```

**Décommenter ligne `LoadModule`** :
```apache
LoadModule authnz_pam_module modules/mod_authnz_pam.so
```

**Sauvegarder** : `:wq`

### Étape 4 : Configuration répertoire protégé

```bash
sudo vi /etc/httpd/conf.d/protected.conf
```

**Contenu fichier** :
```apache
<Directory "/var/www/html/protected">
    AuthType Basic
    AuthName "Restricted Area"
    AuthBasicProvider PAM
    AuthPAMService httpd
    Require valid-user
</Directory>
```

**Explication directives** :
- `AuthBasicProvider PAM` : Utilise PAM au lieu de htpasswd
- `AuthPAMService httpd` : Service PAM utilisé (fichier `/etc/pam.d/httpd`)
- `Require valid-user` : Tout utilisateur Linux authentifié autorisé

**Sauvegarder** : `:wq`

### Étape 5 : Configuration service PAM

```bash
sudo vi /etc/pam.d/httpd
```

**Contenu fichier** :
```
auth include system-auth
account include system-auth
```

**Explication** : Délègue authentification/autorisation aux modules PAM système standard.

**Sauvegarder** : `:wq`

### Étape 6 : Permissions pour Apache

```bash
sudo groupadd -f shadow
sudo usermod -aG shadow apache
sudo chgrp shadow /etc/shadow
sudo chmod g+r /etc/shadow
```

**Explication** : Apache doit lire `/etc/shadow` pour valider mots de passe utilisateurs Linux.

### Étape 7 : Création répertoire protégé

```bash
sudo mkdir -p /var/www/html/protected
echo "Protected content" | sudo tee /var/www/html/protected/index.html
```

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
curl -u yousuf:B4zNgHA7Ya localhost:8080/protected/
# Protected content ✅
```

**Test sans authentification** :
```bash
curl localhost:8080/protected/
# 401 Unauthorized
```

**Test depuis Jump Host** :
```bash
curl -u yousuf:B4zNgHA7Ya http://stapp03:8080/protected/
# Protected content ✅
```

---

## 📂 Configuration finale

**Fichiers créés/modifiés** :
```
/etc/httpd/conf.modules.d/55-authnz_pam.conf  (LoadModule)
/etc/httpd/conf.d/protected.conf              (Directory config)
/etc/pam.d/httpd                              (PAM service)
/var/www/html/protected/index.html            (Contenu protégé)
```

**Permissions `/etc/shadow`** :
```bash
ls -l /etc/shadow
# -rw-r----- 1 root shadow 1234 Jan 19 10:30 /etc/shadow
```

---

## 🔑 Apprentissages clés

**PAM vs htpasswd** :
- **htpasswd** : Fichier de mots de passe séparé, géré manuellement
- **PAM** : Utilise comptes Linux système, gestion centralisée

**Sécurité** :
- Donner accès lecture `/etc/shadow` à Apache = **risque de sécurité**
- Production : préférer utilisateurs dédiés ou autres solutions PAM

**Architecture PAM** :
- Modules empilables pour authentification système
- Réutilisation de `system-auth` (même config que SSH, login, etc.)

---

## 🔗 Ressources

**Apache PAM** :
- [mod_authnz_pam Documentation](https://github.com/adelton/mod_authnz_pam)
- [Apache Authentication](https://httpd.apache.org/docs/2.4/howto/auth.html)

**PAM** :
- [Linux PAM Guide](https://tldp.org/HOWTO/User-Authentication-HOWTO/x115.html)
- [PAM Configuration Files](https://linux.die.net/man/5/pam.d)

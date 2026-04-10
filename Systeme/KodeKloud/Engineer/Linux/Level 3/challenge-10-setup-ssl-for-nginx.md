# Challenge 10 - Setup SSL for Nginx

**Difficulté** : Level 3  
**Domaine** : Nginx, SSL/TLS, HTTPS  
**Date** : 19 janvier 2026

---

## 📋 Consigne

L'équipe des administrateurs système de xFusionCorp Industries doit déployer une nouvelle application sur App Server 2 dans le Stratos Datacenter. Ils ont quelques pré-requis pour préparer ce serveur au déploiement de l'application. Préparez le serveur selon les exigences partagées ci-dessous :

1. Installer et configurer nginx sur App Server 2.

2. Sur App Server 2, il y a un certificat SSL auto-signé et une clé présents à l'emplacement `/tmp/nautilus.crt` et `/tmp/nautilus.key`. Déplacez-les vers un emplacement approprié et déployez-les dans Nginx.

3. Créer un fichier `index.html` avec le contenu `Welcome!` dans le document root de Nginx.

4. Pour le test final, essayez d'accéder au lien App Server 2 (soit le nom d'hôte, soit l'IP) depuis le jump host en utilisant la commande curl. Par exemple `curl -Ik https://<app-server-ip>/`.

---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 2

```bash
ssh steve@stapp02
# Password: Am3ric@
```

### Étape 2 : Installation Nginx

```bash
sudo yum install nginx -y
```

### Étape 3 : Création répertoire SSL

```bash
sudo mkdir -p /etc/nginx/ssl/
```

**Explication** : Répertoire dédié pour stocker certificats et clés privées.

### Étape 4 : Déplacement certificats

```bash
sudo mv /tmp/nautilus.crt /etc/nginx/ssl/
sudo mv /tmp/nautilus.key /etc/nginx/ssl/
```

**Vérification** :
```bash
ls -l /etc/nginx/ssl/
# -rw-r--r-- 1 root root 1234 nautilus.crt
# -rw------- 1 root root 1704 nautilus.key
```

### Étape 5 : Suppression bloc server par défaut

```bash
sudo vi /etc/nginx/nginx.conf
```

**Supprimer bloc `server { ... }`** dans section `http`.

**Explication** : Configuration personnalisée dans fichier dédié `/etc/nginx/conf.d/`.

**Sauvegarder** : `:wq`

### Étape 6 : Configuration HTTPS

```bash
sudo vi /etc/nginx/conf.d/secure.conf
```

**Contenu fichier** :
```nginx
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    
    ssl_certificate /etc/nginx/ssl/nautilus.crt;
    ssl_certificate_key /etc/nginx/ssl/nautilus.key;
    
    server_name stapp02.stratos.xfusioncorp.com;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}

server {
    listen 80;
    listen [::]:80;
    server_name stapp02.stratos.xfusioncorp.com;
    return 302 https://$server_name$request_uri;
}
```

**Explication blocs** :
- **1er bloc** : HTTPS sur port 443 avec certificat SSL
- **2e bloc** : Redirection HTTP → HTTPS (port 80 → 443)

**Sauvegarder** : `:wq`

### Étape 7 : Création document root

```bash
sudo mkdir -p /var/www/html
```

### Étape 8 : Création page index

```bash
echo "Welcome!" | sudo tee /var/www/html/index.html
```

**Vérification** :
```bash
cat /var/www/html/index.html
# Welcome!
```

### Étape 9 : Permissions

```bash
sudo chown -R nginx:nginx /var/www/html/
```

**Explication** : Utilisateur `nginx` doit pouvoir lire fichiers du document root.

### Étape 10 : Activation Nginx

```bash
sudo systemctl enable --now nginx
```

**Vérification service** :
```bash
sudo systemctl status nginx
# Active (running)
```

### Étape 11 : Validation SSL

**Test HTTPS (headers seulement)** :
```bash
curl -Ik https://stapp02:443
# HTTP/2 200
# server: nginx/1.20.1
# content-type: text/html
```

**Test HTTPS avec contenu** :
```bash
curl -k https://stapp02
# Welcome! ✅
```

**Test redirection HTTP → HTTPS** :
```bash
curl -IL http://stapp02
# HTTP/1.1 302 Moved Temporarily
# Location: https://stapp02.stratos.xfusioncorp.com/
# HTTP/2 200
```

**Options curl** :
- `-I` : Headers seulement (HEAD request)
- `-k` : Ignore erreur certificat auto-signé (insecure)
- `-L` : Suit redirections

---

## 📂 Configuration finale

**Arborescence** :
```
/etc/nginx/
├── nginx.conf              (Config principale, server block retiré)
├── conf.d/
│   └── secure.conf         (Config HTTPS + redirection)
└── ssl/
    ├── nautilus.crt        (Certificat SSL)
    └── nautilus.key        (Clé privée)

/var/www/html/
└── index.html              (Page d'accueil)
```

**Ports en écoute** :
```bash
sudo ss -tlnp | grep nginx
# LISTEN :443 (HTTPS)
# LISTEN :80  (HTTP redirect)
```

---

## 🔑 Apprentissages clés

**SSL/TLS avec Nginx** :
- Directives `ssl_certificate` et `ssl_certificate_key` obligatoires
- Port 443 standard pour HTTPS
- Certificat auto-signé = Warning navigateur (production : Let's Encrypt, CA)

**Redirection HTTP → HTTPS** :
- Code 302 (Temporary Redirect) ou 301 (Permanent)
- Variable `$server_name` et `$request_uri` pour URL complète

**Structure configuration Nginx** :
- `nginx.conf` : Configuration globale
- `conf.d/*.conf` : Configurations modulaires (virtual hosts)

**Sécurité** :
- Clé privée permissions 600 (lecture root uniquement)
- Certificats publics permissions 644 (lecture tous)

---

## 🔗 Ressources

**Nginx SSL** :
- [Nginx SSL Module](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)
- [Configuring HTTPS servers](https://nginx.org/en/docs/http/configuring_https_servers.html)

**SSL/TLS** :
- [Let's Encrypt](https://letsencrypt.org/)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

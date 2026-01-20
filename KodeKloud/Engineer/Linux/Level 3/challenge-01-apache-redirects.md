# Challenge 01 - Apache Redirects

**Difficulté** : Level 3  
**Domaine** : Apache, HTTP Redirects, VirtualHost  
**Date** : 17 janvier 2026

---

## 📋 Consigne

L'équipe devops de Nautilus a reçu des exigences concernant des modifications de configuration Apache. Ils doivent mettre en place des redirections pour certaines URLs. Il pourrait y avoir d'autres changements à effectuer. Vous trouverez ci-dessous plus de détails à ce sujet :

1.) httpd est déjà installé sur le serveur app 3. Configurer Apache pour écouter sur le port 6100.

Configurer Apache pour ajouter des redirections comme mentionné ci-dessous :

a.) Rediriger `http://stapp03.stratos.xfusioncorp.com:<Port>/` vers `http://www.stapp03.stratos.xfusioncorp.com:<Port>/` c'est-à-dire non-www vers www. Cela doit être une redirection permanente, soit 301

b.) Rediriger `http://www.stapp03.stratos.xfusioncorp.com:<Port>/blog/` vers `http://www.stapp03.stratos.xfusioncorp.com:<Port>/news/`. Cela doit être une redirection temporaire, soit 302.


---

## 🔧 Réalisation

### Étape 1 : Connexion App Server 3

```bash
ssh banner@stapp03
# Password: BigGr33n (user banner)
```

### Étape 2 : Configuration Apache port 6100

```bash
# Modifier Listen directive
sudo vi /etc/httpd/conf/httpd.conf

# Rechercher ligne "Listen 80"
# Modifier → Listen 6100
```

**Configuration** :
```apache
# /etc/httpd/conf/httpd.conf
Listen 6100
```

### Étape 3 : Configuration VirtualHosts redirections

```bash
# Créer fichier VirtualHost custom
sudo vi /etc/httpd/conf.d/vhost.conf
```

**Configuration `/etc/httpd/conf.d/vhost.conf`** :

```apache
# VirtualHost 1 : Non-www → www (Redirect 301 permanent)
<VirtualHost *:6100>
   ServerName stapp03.stratos.xfusioncorp.com
   ServerAdmin webmaster@stapp03.stratos.xfusioncorp.com
   Redirect 301 / http://www.stapp03.stratos.xfusioncorp.com:6100/
</VirtualHost>

# VirtualHost 2 : www (destination finale + redirect /blog/ → /news/)
<VirtualHost *:6100>
   DocumentRoot /var/www/html/
   ServerName www.stapp03.stratos.xfusioncorp.com
   ServerAdmin webmaster@stapp03.stratos.xfusioncorp.com
   Redirect 302 /blog/ http://www.stapp03.stratos.xfusioncorp.com:6100/news/
</VirtualHost>
```

**Explications configuration** :

**VirtualHost 1 (Non-www)** :
- `ServerName stapp03.stratos.xfusioncorp.com` : Capture requêtes sans www
- `Redirect 301 /` : Redirige TOUTES URLs (`/`) vers version www
- Status `301` : Permanent redirect (moteurs recherche update indexes)

**VirtualHost 2 (www)** :
- `ServerName www.stapp03.stratos.xfusioncorp.com` : Capture requêtes avec www
- `DocumentRoot /var/www/html/` : Racine site web
- `Redirect 302 /blog/` : Redirige uniquement `/blog/*` vers `/news/*`
- Status `302` : Temporary redirect (moteurs conservent ancien URL)

### Étape 4 : Validation syntax Apache

```bash
sudo httpd -t
# Output attendu : Syntax OK
```

**Vérification** :
- Syntax OK → Aucune erreur configuration
- Si erreur → Affiche ligne + message (ex: `AH00526: Syntax error line 15`)

### Étape 5 : Redémarrage Apache

```bash
sudo systemctl restart httpd
sudo systemctl status httpd
# Status : Active (running)
```

### Étape 6 : Validation redirections

**Test redirection 301 (non-www → www)** :
```bash
# Depuis Jump Host
curl -I http://stapp03.stratos.xfusioncorp.com:6100/

# Output attendu :
# HTTP/1.1 301 Moved Permanently
# Location: http://www.stapp03.stratos.xfusioncorp.com:6100/
```

**Test redirection 302 (/blog/ → /news/)** :
```bash
curl -I http://www.stapp03.stratos.xfusioncorp.com:6100/blog/

# Output attendu :
# HTTP/1.1 302 Found
# Location: http://www.stapp03.stratos.xfusioncorp.com:6100/news/
```

**Test URL finale (pas de redirect)** :
```bash
curl http://www.stapp03.stratos.xfusioncorp.com:6100/news/

# Output : Page HTML (pas de redirection)
```

## 🔗 Ressources

**Documentation Apache** :
- [Apache Redirect Guide](https://httpd.apache.org/docs/2.4/mod/mod_alias.html#redirect)
- [VirtualHost Examples](https://httpd.apache.org/docs/2.4/vhosts/examples.html)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

**SEO Canonicalization** :
- [Google Search Central - Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization)
- [301 vs 302 Redirects](https://moz.com/learn/seo/redirection)


# Challenge 20 : Add Response Headers in Apache

**Difficulté** : Niveau 2  
**Domaine** : Apache HTTP Server, Security Headers, Web Server Hardening  
**Date** : 17 janvier 2026

---

## 📋 Présentation

**Objectif** : Renforcer la sécurité du serveur web Apache en ajoutant des en-têtes HTTP de sécurité (response headers) sur App Server 3.

**Contexte** : xFusionCorp Industries travaille sur le durcissement (hardening) des serveurs web Apache. Les en-têtes de sécurité doivent être activés un par un sur chaque serveur applicatif pour tests.

**Requirements** :

1. **Installation Apache** :
   - Installer package `httpd` via yum sur App Server 3
   - Configurer Apache pour écouter sur port `6100` (au lieu de 80 défaut)
   - Démarrer et activer le service

2. **Page index** :
   - Créer fichier `/var/www/html/index.html` (document root Apache)
   - Contenu : `Welcome to the xFusionCorp Industries!`

3. **Security Headers HTTP** :
   - **X-XSS-Protection** : `1; mode=block` (protection XSS)
   - **X-Frame-Options** : `SAMEORIGIN` (protection Clickjacking)
   - **X-Content-Type-Options** : `nosniff` (protection MIME-type sniffing)

4. **Validation** :
   - Tester avec `curl` sur App Server 3 (LBR URL non fonctionnel pour ce challenge)

**Serveurs** :
- **App Server 3** : `stapp03` (user `banner`)

---

## ⚙️ Réalisation

### Étape 1 : Connexion App Server 3

```bash
ssh banner@stapp03
```

### Étape 2 : Installation Apache (httpd)

```bash
sudo yum install httpd -y
```

**Output attendu** :
```
Installed:
  httpd-2.4.x-xx.el8.x86_64
Complete!
```

### Étape 3 : Création page index.html

```bash
sudo vi /var/www/html/index.html
```

**Contenu** :
```html
Welcome to the xFusionCorp Industries!
```

**Sauvegarder** : `:wq`

### Étape 4 : Configuration Apache - Port 6100

```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Modifier directive Listen** :
```apache
# AVANT
Listen 80

# APRÈS
Listen 6100
```

### Étape 5 : Configuration Security Headers

**Dans `/etc/httpd/conf/httpd.conf`**, ajouter bloc (fin de fichier ou section `<VirtualHost>`) :

```apache
<IfModule headers_module>
    Header set X-XSS-Protection "1; mode=block"
    Header always append X-Frame-Options SAMEORIGIN
    Header set X-Content-Type-Options nosniff
</IfModule>
```

**Sauvegarder** : `:wq`

**Explications directives** :
- `Header set` : Définir header (écrase si existe)
- `Header always append` : Ajouter header (même si réponse erreur 4xx/5xx)
- `<IfModule headers_module>` : Conditionnel (si module mod_headers chargé)

### Étape 6 : Validation syntaxe configuration

```bash
sudo httpd -t
```

**Output attendu** :
```
Syntax OK
```

**⚠️ Si erreur** : Vérifier syntaxe bloc headers, quotes, typos.

### Étape 7 : Démarrage Apache

```bash
# Stop si déjà running (éviter conflicts port)
sudo systemctl stop httpd

# Enable boot + start
sudo systemctl enable --now httpd
```

**Vérifier statut** :
```bash
sudo systemctl status httpd
```

**Output attendu** :
```
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2026-01-17 10:00:00 UTC; 5s ago
```

### Étape 8 : Vérification Headers HTTP

```bash
curl -I localhost:6100
```

**Output attendu** :
```http
HTTP/1.1 200 OK
Date: Sat, 17 Jan 2026 10:00:00 GMT
Server: Apache/2.4.x (Red Hat)
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=UTF-8
```

**✅ Validation points** :
- `HTTP/1.1 200 OK` (page accessible)
- `X-XSS-Protection: 1; mode=block` présent
- `X-Frame-Options: SAMEORIGIN` présent
- `X-Content-Type-Options: nosniff` présent

**Vérifier contenu page** :
```bash
curl http://localhost:6100
```

**Output attendu** :
```
Welcome to the xFusionCorp Industries!
```

---

## 🔍 Commandes utiles

### Apache configuration validation

```bash
# Test syntaxe config (AVANT restart)
sudo httpd -t

# Test syntaxe + dump VirtualHosts
sudo httpd -S

# Vérifier modules chargés
httpd -M | grep headers
# headers_module (shared) → mod_headers actif

# Localiser fichiers config
httpd -V | grep SERVER_CONFIG_FILE
# /etc/httpd/conf/httpd.conf
```

### Headers HTTP debugging

```bash
# Headers response complets
curl -I http://localhost:6100

# Headers + contenu
curl -i http://localhost:6100

# Verbose (debug connexion)
curl -v http://localhost:6100

# Tester header spécifique
curl -I http://localhost:6100 | grep X-XSS-Protection

# Depuis jump host (après validation)
curl -I http://stapp03:6100
```

### Apache service management

```bash
# Démarrer
sudo systemctl start httpd

# Arrêter
sudo systemctl stop httpd

# Restart (stop + start)
sudo systemctl restart httpd

# Reload config (0 downtime)
sudo systemctl reload httpd

# Statut
sudo systemctl status httpd

# Logs real-time
sudo journalctl -u httpd -f

# Error logs
sudo tail -50 /var/log/httpd/error_log

# Access logs
sudo tail -50 /var/log/httpd/access_log
```

### Port listening verification

```bash
# Vérifier Apache écoute port 6100
sudo ss -tuln | grep 6100
# tcp   LISTEN 0   128   *:6100   *:*

# Netstat alternative
sudo netstat -tuln | grep 6100

# lsof alternative
sudo lsof -i :6100
```

---

## 📝 Points clés

### Security Headers HTTP

**1. X-XSS-Protection** :
- **But** : Protection Cross-Site Scripting (XSS) attacks
- **Valeur `1; mode=block`** :
  * `1` : Activer XSS filter navigateur
  * `mode=block` : Bloquer page entière (pas juste sanitize)
- **Browsers support** : Chrome, IE, Safari (Firefox retire support - CSP préféré)
- **⚠️ Deprecated** : Modern browsers utilisent Content-Security-Policy (CSP)

**2. X-Frame-Options** :
- **But** : Protection Clickjacking attacks (iframe malicieuses)
- **Valeur `SAMEORIGIN`** : Page peut être iframe SEULEMENT si même origine
- **Autres valeurs** :
  * `DENY` : Interdit tout iframe (max sécurité)
  * `ALLOW-FROM https://example.com` : Whitelist origine (deprecated)
- **Modern alternative** : `Content-Security-Policy: frame-ancestors 'self'`

**3. X-Content-Type-Options** :
- **But** : Empêcher MIME-type sniffing navigateurs
- **Valeur `nosniff`** : Navigateur DOIT respecter Content-Type header serveur
- **Attack scenario** :
  * Attacker upload fichier `.txt` contenant JavaScript
  * Sans nosniff : Browser "sniff" → exécute comme script
  * Avec nosniff : Browser respecte `text/plain` → pas exécution

### Apache mod_headers

**Module** : `mod_headers` (module Apache manipulation headers HTTP)

**Directives** :
```apache
# Set : Définir header (écrase si existe)
Header set X-Custom-Header "value"

# Append : Ajouter header (même nom = multiple)
Header append X-Custom-Header "value2"

# Always : Appliquer MÊME si erreur 4xx/5xx
Header always set X-Frame-Options "DENY"

# Unset : Supprimer header
Header unset X-Powered-By

# Edit : Modifier header existant (regex)
Header edit Set-Cookie ^(.*)$ "$1; HttpOnly; Secure"
```

**Conditions** :
```apache
# Si module chargé
<IfModule headers_module>
    Header set X-Test "value"
</IfModule>

# Si environnement variable
Header set X-Custom "value" env=HTTPS

# Si réponse status code
Header always set X-Robots-Tag "noindex" "expr=%{CONTENT_TYPE} =~ m#^application/pdf#"
```

---

## 🎯 Tags

`Apache`, `httpd`, `Security-Headers`, `X-XSS-Protection`, `X-Frame-Options`, `X-Content-Type-Options`, `mod_headers`, `Web-Server-Hardening`, `HTTP-Response-Headers`, `Port-Configuration`


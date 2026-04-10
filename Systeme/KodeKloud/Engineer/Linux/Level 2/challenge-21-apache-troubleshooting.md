# Challenge 21 : Apache Troubleshooting

**Difficulté** : Niveau 2  
**Domaine** : Apache HTTP Server, Troubleshooting, Configuration Debugging  
**Date** : 17 janvier 2026

---

## 📋 Présentation

**Objectif** : Identifier et résoudre les problèmes Apache sur les serveurs applicatifs Nautilus (Stratos Datacenter).

**Contexte** : xFusionCorp Industries utilise des outils de monitoring pour vérifier le statut de chaque service. Le système de monitoring a identifié que le service Apache ne fonctionne pas sur certains App Servers.

**Requirements** :

1. **Identifier serveurs défaillants** :
   - Trouver quel(s) Nautilus Application Server(s) ont Apache DOWN
   - Corriger le problème sur chaque serveur

2. **Apache doit tourner** :
   - Service `httpd` actif (running) sur TOUS App Servers
   - Ne PAS arrêter firewall (laisser running)

3. **Configuration standard** :
   - **Port** : `3000` (sur tous App Servers)
   - **DocumentRoot** : `/var/www/html` (sur tous App Servers)

4. **Validation** :
   - Tester depuis Jump Host avec `curl` :
     * `curl http://172.16.238.10:3000/` (stapp01)
     * `curl http://172.16.238.11:3000/` (stapp02)
     * `curl http://172.16.238.12:3000/` (stapp03)
   - Chaque serveur doit retourner page statique (HTML)

**Serveurs** :
- **App Server 1** : `stapp01` - 172.16.238.10 (user `tony`)
- **App Server 2** : `stapp02` - 172.16.238.11 (user `steve`)
- **App Server 3** : `stapp03` - 172.16.238.12 (user `banner`)

---

## ⚙️ Réalisation

### Étape 1 : Troubleshooting App Server 1 (stapp01)

```bash
ssh tony@stapp01
```

**Diagnostic** :
```bash
sudo systemctl status httpd
```

**Output** :
```
● httpd.service - The Apache HTTP Server
   Loaded: loaded
   Active: inactive (dead)
```

**Root cause** : Service `httpd` installé mais **pas démarré** (état `inactive`).

**Solution** :
```bash
sudo systemctl enable --now httpd
```

**Validation** :
```bash
sudo systemctl status httpd
```

**Output attendu** :
```
● httpd.service - The Apache HTTP Server
   Active: active (running) since Sat 2026-01-17 10:00:00 UTC
```

**✅ stapp01 résolu** : Service juste pas started (config OK par défaut).

---

### Étape 2 : Troubleshooting App Server 2 (stapp02)

```bash
ssh steve@stapp02
```

**Diagnostic** :
```bash
sudo systemctl status httpd
```

**Output** :
```
● httpd.service - The Apache HTTP Server
   Loaded: loaded
   Active: failed (Result: exit-code)
```

**Analyser erreur** :
```bash
sudo journalctl -u httpd -n 20
```

**Error message** :
```
AH00526: Syntax error on line XX of /etc/httpd/conf/httpd.conf:
Invalid command 'ServerRoot;', perhaps misspelled...
```

**Root cause** : **Syntax error** dans `/etc/httpd/conf/httpd.conf` - **point-virgule (;) à la fin de directive `ServerRoot`**.

**Solution** :
```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Localiser ligne** :
```apache
# AVANT (incorrect)
ServerRoot "/etc/httpd";

# APRÈS (correct)
ServerRoot "/etc/httpd"
```

**⚠️ Important** : Directives Apache **ne prennent PAS** de point-virgule final (contrairement à CSS, JavaScript, etc.).

**Sauvegarder** : `:wq`

**Tester syntaxe** :
```bash
sudo httpd -t
```

**Output attendu** :
```
Syntax OK
```

**Démarrer Apache** :
```bash
sudo systemctl enable --now httpd
```

**Validation** :
```bash
sudo systemctl status httpd
```

**✅ stapp02 résolu** : Point-virgule syntax error corrigé.

---

### Étape 3 : Troubleshooting App Server 3 (stapp03)

```bash
ssh banner@stapp03
```

**Diagnostic** :
```bash
sudo systemctl status httpd
```

**Output** :
```
● httpd.service - The Apache HTTP Server
   Active: failed (Result: exit-code)
```

**Analyser erreur** :
```bash
sudo journalctl -u httpd -n 20
```

**Error message** :
```
AH00526: Syntax error on line XX of /etc/httpd/conf/httpd.conf:
Invalid command '"Listen', perhaps misspelled...
```

**Root cause** : **Directive `Listen` entourée de guillemets** (quotes incorrectes).

**Solution** :
```bash
sudo vi /etc/httpd/conf/httpd.conf
```

**Localiser ligne** :
```apache
# AVANT (incorrect)
"Listen 3000"

# APRÈS (correct)
Listen 3000
```

**⚠️ Erreur additionnelle** : Vérifier aussi directive `DocumentRoot` (point-virgule potentiel).

**Localiser ligne DocumentRoot** :
```apache
# AVANT (incorrect)
DocumentRoot "/var/www/html";

# APRÈS (correct)
DocumentRoot "/var/www/html"
```

**Sauvegarder** : `:wq`

**Tester syntaxe** :
```bash
sudo httpd -t
```

**Output attendu** :
```
Syntax OK
```

**Démarrer Apache** :
```bash
sudo systemctl enable --now httpd
```

**Validation** :
```bash
sudo systemctl status httpd
```

**✅ stapp03 résolu** : Quotes autour `Listen` + point-virgule `DocumentRoot` corrigés.

---

### Étape 4 : Validation finale (depuis Jump Host)

**Retour Jump Host** :
```bash
exit  # Déconnecter du dernier App Server
```

**Test App Server 1** :
```bash
curl http://stapp01:3000
# OU
curl http://172.16.238.10:3000
```

**Output attendu** : Page HTML statique (contenu varie selon default page Apache).

**Test App Server 2** :
```bash
curl http://stapp02:3000
# OU
curl http://172.16.238.11:3000
```

**Test App Server 3** :
```bash
curl http://stapp03:3000
# OU
curl http://172.16.238.12:3000
```

**✅ Validation** : Les 3 serveurs retournent page HTML (HTTP 200 OK).

---

## 🔍 Commandes utiles

### Apache service troubleshooting

```bash
# Statut service
sudo systemctl status httpd

# Logs erreur (systemd journal)
sudo journalctl -u httpd -n 50
sudo journalctl -u httpd -f  # Real-time

# Logs erreur Apache
sudo tail -50 /var/log/httpd/error_log

# Tester syntaxe config
sudo httpd -t

# Tester syntaxe + VirtualHosts
sudo httpd -S

# Démarrer service
sudo systemctl start httpd

# Redémarrer
sudo systemctl restart httpd

# Enable boot
sudo systemctl enable httpd

# Enable + start (combo)
sudo systemctl enable --now httpd
```

### Network debugging

```bash
# Vérifier Apache écoute port 3000
sudo ss -tuln | grep 3000

# Netstat alternative
sudo netstat -tuln | grep 3000

# lsof alternative
sudo lsof -i :3000

# Test connexion local
curl -I http://localhost:3000

# Test connexion remote (depuis jump host)
curl -I http://172.16.238.10:3000
```

---

## 📝 Points clés

### Apache Configuration Syntax Rules

**1. Pas de point-virgule final** :
```apache
# ❌ INCORRECT
ServerRoot "/etc/httpd";
DocumentRoot "/var/www/html";
Listen 80;

# ✅ CORRECT
ServerRoot "/etc/httpd"
DocumentRoot "/var/www/html"
Listen 80
```

**⚠️ Confusion** : Développeurs venant de CSS/JavaScript/PHP ajoutent `;` par habitude.

**2. Pas de quotes autour directives** :
```apache
# ❌ INCORRECT
"Listen 3000"
"ServerName example.com"

# ✅ CORRECT
Listen 3000
ServerName example.com
```

**Note** : Quotes UNIQUEMENT pour valeurs contenant espaces :
```apache
# Valeur sans espace : pas quotes
ServerAdmin admin@example.com

# Valeur avec espace : quotes requises
ErrorDocument 404 "The requested file was not found"
```

**3. Directives sensibles à la casse** :
```apache
# ❌ INCORRECT
listen 80        # Minuscule
SERVERROOT "/etc/httpd"  # Majuscule

# ✅ CORRECT
Listen 80        # CamelCase exact
ServerRoot "/etc/httpd"
```

**4. Indentation non obligatoire mais recommandée** :
```apache
# Fonctionne mais illisible
<Directory "/var/www/html">
Options Indexes
AllowOverride None
</Directory>

# ✅ Recommandé (lisibilité)
<Directory "/var/www/html">
    Options Indexes
    AllowOverride None
</Directory>
```

### httpd -t (Syntax Validation)

**Commande ESSENTIELLE avant restart** :
```bash
sudo httpd -t
```

**Outputs** :
```
Syntax OK                           # ✅ Config valide
AH00526: Syntax error on line 42... # ❌ Erreur ligne 42
```

---

## 📚 Résumé Erreurs Challenge

| Serveur | Problème | Root Cause | Solution |
|---------|----------|------------|----------|
| **stapp01** | Service inactive | `httpd` pas démarré | `systemctl enable --now httpd` |
| **stapp02** | Service failed | `ServerRoot "/etc/httpd";` (`;` final) | Supprimer point-virgule |
| **stapp03** | Service failed | `"Listen 3000"` (quotes) + `DocumentRoot "/var/www/html";` (`;`) | Supprimer quotes + point-virgule |

**Patterns** :
- **Service pas started** : Simple `systemctl` command
- **Syntax errors** : Point-virgule (PHP/CSS habit), quotes incorrectes
- **Validation workflow** : `httpd -t` détecte 100% syntax errors

---

## 🎯 Tags

`Apache`, `httpd`, `Troubleshooting`, `Configuration-Debugging`, `Syntax-Error`, `systemctl`, `journalctl`, `httpd-t`, `ServerRoot`, `Listen`, `DocumentRoot`


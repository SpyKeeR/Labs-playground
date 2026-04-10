# Challenge 17 : Troubleshooting LBR HAProxy

**Date** : 16 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Résoudre problème service HAProxy non fonctionnel sur LBR server (application Nautilus infrastructure ne fonctionne pas).

---

## 📋 Énoncé

xFusionCorp Industries a une application fonctionnant sur l'infrastructure Nautilus dans le Stratos Datacenter. L'outil de monitoring a détecté un problème avec le service haproxy sur le serveur LBR. Cela doit être corrigé pour que l'application fonctionne correctement.

**Exigences** :
- Dépanner et résoudre le problème
- S'assurer que le service haproxy fonctionne sur le serveur Nautilus LBR
- Accéder au site web en utilisant le bouton StaticApp

**Serveur** : `stlb01` (user `loki`)

---

## 🔧 Résolution

### Étape 1 : Connexion serveur LBR

```bash
ssh loki@stlb01
```

### Étape 2 : Tentative démarrage HAProxy

```bash
sudo systemctl start haproxy
```

**Résultat** : Service échoue au démarrage.

### Étape 3 : Diagnostic erreur

```bash
sudo systemctl status haproxy
```

**Output erreur identifiée** :
```
[ALERT] 015/172036 (317) : Proxy 'main': unable to find required default_backend: 'app'
```

**Analyse** :
- Frontend `main` déclare `default_backend app`
- Backend `app` introuvable dans configuration
- HAProxy refuse démarrer (configuration invalide)

### Étape 4 : Vérifier configuration HAProxy

```bash
sudo vi /etc/haproxy/haproxy.cfg
```

**Problème trouvé** :

```haproxy
#---------------------------------------------------------------------
# main frontend which proxys to the backends
#---------------------------------------------------------------------
frontend main
    bind *:80
    default_backend             app    # ← Référence backend "app"

#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
#backend app                           # ← BACKEND COMMENTÉ ❌
#    balance     roundrobin
#    server  stapp01 172.16.238.10:5004 check
#    server  stapp02 172.16.238.11:5004 check
#    server  stapp03 172.16.238.12:5004 check
```

**Root cause** : Ligne `backend app` commentée (caractère `#`) → Backend pas déclaré.

### Étape 5 : Corriger configuration

Décommenter section backend complète :

```haproxy
#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
backend app
    balance     roundrobin
    server  stapp01 172.16.238.10:5004 check
    server  stapp02 172.16.238.11:5004 check
    server  stapp03 172.16.238.12:5004 check
```

**Action** : Supprimer `#` devant `backend app` et toutes lignes intérieures backend.

### Étape 6 : Démarrer + activer HAProxy

```bash
sudo systemctl start haproxy
sudo systemctl enable haproxy
```

### Étape 7 : Validation

Vérifier statut service :
```bash
sudo systemctl status haproxy
```

**Output attendu** : `active (running)` - Pas d'erreurs.

**Test application** : Cliquer bouton **StaticApp** (top bar) → Website s'affiche.

---

## 📌 Commandes utiles

```bash
# Vérifier syntax config AVANT démarrage
haproxy -c -f /etc/haproxy/haproxy.cfg
# Affiche errors si syntax invalide (ex: backend manquant)

# Vérifier logs erreurs HAProxy
sudo journalctl -u haproxy -n 50
sudo tail -50 /var/log/messages | grep haproxy

# Rechercher ligne spécifique config
grep -n "backend" /etc/haproxy/haproxy.cfg
grep -n "default_backend" /etc/haproxy/haproxy.cfg

# Tester config + voir détails
haproxy -f /etc/haproxy/haproxy.cfg -c -V
# -c = check syntax
# -V = verbose errors

# Vérifier service HAProxy
sudo systemctl status haproxy
sudo systemctl is-active haproxy
sudo systemctl is-enabled haproxy

# Redémarrer HAProxy (après modif config)
sudo systemctl restart haproxy

# Reload config (0 downtime)
sudo systemctl reload haproxy
```

---

## 💡 Points clés

**Erreur "unable to find required default_backend"** :
- Frontend déclare `default_backend <nom>`
- Backend `<nom>` doit exister dans config
- Si backend absent/commenté → HAProxy refuse démarrer
- Erreur CRITIQUE (service fail startup)

**Frontend → Backend dependency** :
```haproxy
frontend main
    default_backend app    # ← Référence backend "app"
    
backend app               # ← DOIT exister
    # ...
```

**Config HAProxy validation** :
- **TOUJOURS** vérifier syntax avant start/restart :
  ```bash
  haproxy -c -f /etc/haproxy/haproxy.cfg && systemctl restart haproxy
  ```
- Si syntax invalide → commande échoue (évite casser service)

**Causes communes HAProxy fail** :
1. **Backend manquant** (Challenge 17) : Frontend référence backend inexistant
2. **Port déjà utilisé** : Port 80 occupé (nginx/apache running)
3. **Syntax error** : Bracket manquant, typo directive
4. **Permissions** : User haproxy pas accès `/var/lib/haproxy/`
5. **Certificat SSL invalide** : Cert expiré ou path incorrect

**Debugging workflow HAProxy** :
1. `systemctl status haproxy` → Voir error message
2. `journalctl -u haproxy -n 50` → Logs détaillés
3. `haproxy -c -f /etc/haproxy/haproxy.cfg` → Test syntax
4. Corriger config
5. `systemctl restart haproxy` → Apply changes

---

## ⚠️ Notes production

**Backup config avant modif** :
```bash
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.$(date +%Y%m%d)
```

**Test syntax systématique** :
```bash
# Script safe reload
haproxy -c -f /etc/haproxy/haproxy.cfg && systemctl reload haproxy || echo "Config INVALIDE - reload annulé"
```

**Monitoring HAProxy** :
- Stats page : Activer `listen stats` (voir Module 32 notes)
- Logs centralisés : rsyslog → ELK/Splunk
- Alerting : Nagios/Zabbix check HAProxy up + backends UP

**Documentation changes** :
- Commenter pourquoi backend était commenté (maintenance ?)
- Versionner config (Git) : `git diff haproxy.cfg`
- Changelog : Noter date + raison modif

---

## 🔍 Troubleshooting avancé

**Si backend commenté volontairement (maintenance)** :
```haproxy
# Option 1 : Utiliser backend backup temporaire
frontend main
    default_backend maintenance_page

backend maintenance_page
    server maint 127.0.0.1:8080 check
    # Page maintenance statique nginx port 8080

# Option 2 : Désactiver servers (pas backend)
backend app
    balance roundrobin
    # server stapp01 172.16.238.10:5004 check disabled
    server stapp02 172.16.238.11:5004 check
    server stapp03 172.16.238.12:5004 check
    # stapp01 disabled = pas trafic (maintenance)
```

**Vérifier tous frontends/backends cohérents** :
```bash
# Lister tous frontends
grep "^frontend" /etc/haproxy/haproxy.cfg

# Lister tous backends déclarés
grep "^backend" /etc/haproxy/haproxy.cfg

# Lister backends référencés (default_backend, use_backend)
grep "default_backend\|use_backend" /etc/haproxy/haproxy.cfg

# Comparer : Tous backends référencés doivent exister
```

---

**Tags** : `HAProxy` `troubleshooting` `backend` `config-error` `default_backend` `Level 2`

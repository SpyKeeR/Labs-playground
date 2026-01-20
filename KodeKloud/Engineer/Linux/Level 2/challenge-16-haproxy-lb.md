# Challenge 16 : Install & Configure HAProxy LB

**Date** : 15 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Installer et configurer HAProxy comme Load Balancer pour répartir trafic HTTP entre 3 serveurs applicatifs Apache (Stratos Datacenter).

---

## 📋 Énoncé

Il existe un site web statique qui fonctionne dans le Stratos Datacenter. L'équipe a déjà configuré les serveurs applicatifs et le code y est déjà déployé. Pour que cela fonctionne correctement, ils doivent configurer le serveur LBR. Il existe plusieurs options pour cela, mais l'équipe a décidé d'utiliser HAproxy. Pour information, Apache fonctionne sur le port 5004 sur tous les serveurs applicatifs.

**Exigences** :
- a. Installer et configurer HAproxy sur le serveur LBR en utilisant uniquement yum
- b. Ajouter tous les serveurs applicatifs au load balancer HAproxy
- c. HAproxy doit servir sur le port HTTP par défaut (80)
- d. NE PAS supprimer l'entrée stats socket `/var/lib/haproxy/stats` de la configuration par défaut de HAproxy
- e. Accéder au site web via le bouton StaticApp

**Serveurs** :
- **Load Balancer** : `stlb01` (user `loki`)
- **App Servers** :
  * `stapp01` : 172.16.238.10:5004 (Apache)
  * `stapp02` : 172.16.238.11:5004 (Apache)
  * `stapp03` : 172.16.238.12:5004 (Apache)

---

## 🔧 Résolution

### Étape 1 : Connexion serveur Load Balancer

```bash
ssh loki@stlb01
```

### Étape 2 : Installation HAProxy

```bash
sudo yum install haproxy -y
```

**Explication** :
- Package `haproxy` disponible repos standard RHEL/CentOS
- Installation via `yum` (requis consigne)

### Étape 3 : Configuration HAProxy

Éditer fichier config principal :
```bash
sudo vi /etc/haproxy/haproxy.cfg
```

**Ajouter à la fin du fichier (après section `stats socket`)** :

```haproxy
#---------------------------------------------------------------------
# main frontend which proxys to the backends
#---------------------------------------------------------------------
frontend main
    bind *:80
    default_backend             app
    option                      forwardfor

#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
backend app
    balance     roundrobin
    server  stapp01 172.16.238.10:5004 check
    server  stapp02 172.16.238.11:5004 check
    server  stapp03 172.16.238.12:5004 check
```

**Explications configuration** :

**Section `frontend main`** :
- `bind *:80` : Écoute port 80 (HTTP standard) sur toutes interfaces
- `default_backend app` : Redirige tout trafic vers backend "app"
- `option forwardfor` : Ajoute header `X-Forwarded-For` (IP client original preserved)

**Section `backend app`** :
- `balance roundrobin` : Algorithme round-robin (distribution équitable séquentielle)
- `server stappXX IP:PORT check` : Déclare serveur backend + health checks actifs
  * `check` : HAProxy vérifie disponibilité serveur (ping TCP régulier)
  * Si serveur down → HAProxy retire du pool automatiquement

### Étape 4 : Redémarrer HAProxy

```bash
# Arrêter HAProxy (si running)
sudo systemctl stop haproxy

# Démarrer + activer boot
sudo systemctl enable --now haproxy
```

**Note** : `stop` puis `enable --now` garantit démarrage clean avec nouvelle config.

### Étape 5 : Validation

Tester load balancer localement :
```bash
curl http://127.0.0.1:80
```

**Output attendu** : HTML page statique website (servie par un des 3 app servers).

**Test via UI** : Cliquer bouton **StaticApp** (top bar) → Website s'affiche.

**Test load balancing** (optionnel) :
```bash
# Requêtes multiples → vérifier distribution
curl -s http://127.0.0.1 | grep -i "server"
curl -s http://127.0.0.1 | grep -i "server"
curl -s http://127.0.0.1 | grep -i "server"
# Round-robin → requêtes alternent entre stapp01, stapp02, stapp03
```

---

## 📌 Commandes utiles

```bash
# Installation HAProxy
sudo yum install haproxy -y
sudo apt install haproxy -y    # Debian/Ubuntu

# Gestion service
sudo systemctl start haproxy
sudo systemctl stop haproxy
sudo systemctl restart haproxy
sudo systemctl reload haproxy
sudo systemctl status haproxy
sudo systemctl enable haproxy

# Vérifier config syntax
haproxy -c -f /etc/haproxy/haproxy.cfg

# Voir version HAProxy
haproxy -v

# Logs HAProxy (RHEL/CentOS)
sudo tail -f /var/log/messages | grep haproxy

# Logs HAProxy (Debian/Ubuntu)
sudo tail -f /var/log/haproxy.log

# Logs journald
sudo journalctl -u haproxy -f

# Tester frontend (port 80)
curl http://localhost:80
curl -I http://localhost:80    # Headers only

# Vérifier port écoute
sudo ss -tuln | grep :80
sudo netstat -tuln | grep :80

# Stats socket (CLI admin)
echo "show stat" | sudo socat stdio /var/lib/haproxy/stats
echo "show servers state" | sudo socat stdio /var/lib/haproxy/stats

# Tester health checks backends
curl http://172.16.238.10:5004
curl http://172.16.238.11:5004
curl http://172.16.238.12:5004
```

### Structure /etc/haproxy/haproxy.cfg

```haproxy
# Section GLOBAL (config daemon HAProxy)
global
    log         127.0.0.1 local2
    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon
    stats socket /var/lib/haproxy/stats    # ⚠️ NE PAS SUPPRIMER

# Section DEFAULTS (paramètres par défaut)
defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    timeout connect         10s
    timeout client          1m
    timeout server          1m

# Section FRONTEND (points d'entrée)
frontend main
    bind *:80
    default_backend app

# Section BACKEND (serveurs backend)
backend app
    balance roundrobin
    server stapp01 172.16.238.10:5004 check
    server stapp02 172.16.238.11:5004 check
    server stapp03 172.16.238.12:5004 check
```

---

## 💡 Points clés

**HAProxy rôle** :
- **Load Balancer** : Répartit trafic entre multiples backends (scaling horizontal)
- **Reverse Proxy** : Clients communiquent avec HAProxy, pas directement backends
- **Health Checks** : Détecte backends down automatiquement (option `check`)
- **High Availability** : Si 1 backend fail, HAProxy redirige vers backends actifs

**Algorithmes load balancing** :
- `roundrobin` : Distribution séquentielle équitable (default, simple, efficace)
- `leastconn` : Serveur avec moins connexions actives (pour long-running requests)
- `source` : Hash IP client (sticky sessions - même client → même backend)
- `uri` : Hash URI request (cache optimization)

**Frontend vs Backend** :
- **Frontend** : Point d'entrée (bind port, ACL rules, routing)
- **Backend** : Pool serveurs (balance algorithm, health checks, servers list)

**Option `forwardfor`** :
- Ajoute HTTP header `X-Forwarded-For: <client_ip>`
- Backends voient IP client original (pas IP HAProxy)
- Essentiel pour logs backends (analytics, geo-location)

**Health checks** :
- `check` : TCP health check (connect backend port régulièrement)
- Fréquence défaut : toutes les 2 secondes
- Si fail → backend marqué DOWN (retiré pool)
- Si backend recover → automatically re-added

---

## ⚠️ Notes production

**Stats socket** :
- `/var/lib/haproxy/stats` = socket UNIX admin HAProxy
- Utilisation : `socat` commands (show stat, disable server, set weight, etc.)
- **⚠️ NE JAMAIS SUPPRIMER** (requis admin runtime HAProxy)

**Sécurité** :
- HAProxy exposé internet → utiliser ACL filters (block malicious IPs)
- Enable stats page avec auth : `stats auth admin:password`
- SSL/TLS termination : `bind *:443 ssl crt /path/to/cert.pem`

**Performance** :
- `maxconn` : Connexions simultanées max (tuning selon RAM/CPU)
- `timeout` values : Adapter selon use case (API vs long-polling)
- Mode `http` vs `tcp` : http = layer 7 (header inspection), tcp = layer 4 (faster)

**Logging** :
- HAProxy logs via syslog (rsyslog config requis)
- Format logs : `option httplog` (verbose HTTP requests)
- Production : centraliser logs (ELK, Splunk)

---

## 🔍 Debugging HAProxy

**Problème : Service fails démarrage** :
```bash
# Vérifier syntax config
haproxy -c -f /etc/haproxy/haproxy.cfg
# Output errors si syntax invalide

# Vérifier logs
sudo journalctl -u haproxy -n 50
sudo tail -50 /var/log/messages | grep haproxy

# Causes communes :
# - Syntax error config (missing bracket, typo)
# - Port 80 already in use (nginx, apache running)
# - Permissions /var/lib/haproxy/ incorrectes
```

**Problème : Backends down (health checks fail)** :
```bash
# Vérifier backend accessible depuis LB
curl http://172.16.238.10:5004
# Si timeout/refused → backend down ou firewall

# Vérifier HAProxy stats
echo "show stat" | sudo socat stdio /var/lib/haproxy/stats
# Colonne "status" : UP = OK, DOWN = health check fail

# Vérifier logs health checks
sudo journalctl -u haproxy | grep -i "health"

# Solutions :
# - Démarrer service backend (systemctl start httpd)
# - Ouvrir firewall backend (firewall-cmd --add-port=5004/tcp)
# - Vérifier IP:PORT correct config HAProxy
```

**Problème : Load balancing asymétrique** :
```bash
# Vérifier algorithme balance
grep "balance" /etc/haproxy/haproxy.cfg

# Vérifier poids serveurs (si weight défini)
echo "show servers state" | sudo socat stdio /var/lib/haproxy/stats

# Tester distribution
for i in {1..10}; do curl -s http://localhost | grep server; done
# Doit alterner stapp01, stapp02, stapp03 si roundrobin
```

---

**Tags** : `HAProxy` `Load-Balancer` `roundrobin` `health-checks` `reverse-proxy` `frontend` `backend` `Level 2`

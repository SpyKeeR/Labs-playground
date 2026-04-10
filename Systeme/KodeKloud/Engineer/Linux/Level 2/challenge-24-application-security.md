# Challenge 24 : Application Security

**Difficulté** : Niveau 2  
**Domaine** : iptables, Firewall, Security, Nginx Reverse Proxy  
**Date** : 17 janvier 2026

---

## 📋 Présentation

**Objectif** : Sécuriser application backup management via firewall iptables - autoriser accès Nginx (reverse proxy) et bloquer accès direct Apache (backend).

**Contexte** : Application backup management hébergée sur Nautilus Backup Server (Stratos DC). Architecture : Nginx (reverse proxy port 8094) → Apache (backend port 5000). Firewall iptables doit protéger backend Apache (accès uniquement via Nginx).

**Consigne originale** :

We have a backup management application UI hosted on Nautilus's backup server in Stratos DC. That backup management application code is deployed under Apache on the backup server itself, and Nginx is running as a reverse proxy on the same server. Apache and Nginx ports are 5000 and 8094, respectively. We have iptables firewall installed on this server. Make the appropriate changes to fulfill the requirements mentioned below:

We want to open all incoming connections to Nginx's port and block all incoming connections to Apache's port. Also make sure rules are permanent.

**Requirements** :

1. **Firewall iptables** :
   - **Activer iptables** (remplacer firewalld si actif)
   - **Ouvrir port Nginx 8094** : ACCEPT connexions incoming/outgoing
   - **Bloquer port Apache 5000** : REJECT connexions incoming/outgoing (accès direct interdit)
   - **Rules permanentes** : Sauvegarder configuration (survit reboot)

2. **Nginx configuration** :
   - Configurer reverse proxy vers Apache (localhost:5000)
   - Écouter port 8094

**Architecture** :
```
Internet → Nginx (port 8094) → Apache (port 5000 localhost)
           ✅ Accessible       ❌ Bloqué accès direct
```

**Serveur** :
- **Backup Server** : `stbkp01` (user `clint`)

---

## ⚙️ Réalisation

### Étape 1 : Connexion Backup Server

```bash
ssh clint@stbkp01
```

### Étape 2 : Remplacer firewalld par iptables

```bash
# Désactiver firewalld
sudo systemctl disable --now firewalld
sudo yum remove firewalld -y

# Activer iptables + ip6tables
sudo systemctl enable --now iptables ip6tables
```

### Étape 3 : Configuration iptables (rules firewall)

**Autoriser loopback (localhost)** :
```bash
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
```

**Autoriser Nginx port 8094** :
```bash
# INPUT : Connexions incoming vers port 8094 (clients → Nginx)
sudo iptables -A INPUT -p tcp --dport 8094 -j ACCEPT

# OUTPUT : Réponses Nginx depuis port 8094 (Nginx → clients)
sudo iptables -A OUTPUT -p tcp --sport 8094 -j ACCEPT
```

**Bloquer Apache port 5000** :
```bash
# INPUT : Bloquer connexions incoming vers port 5000 (protection accès direct)
sudo iptables -A INPUT -p tcp --dport 5000 -j REJECT

# OUTPUT : Bloquer réponses depuis port 5000 (sécurité supplémentaire)
sudo iptables -A OUTPUT -p tcp --sport 5000 -j REJECT
```

**⚠️ Note** : Apache port 5000 reste accessible via **localhost** (Nginx reverse proxy), car rules loopback (`-i lo`) autorisent trafic local.

### Étape 4 : Sauvegarder rules iptables (permanentes)

```bash
# Sauvegarder configuration actuelle
sudo service iptables save

# Supprimer config file (éviter conflicts)
sudo rm /etc/sysconfig/iptables-config

# Restart iptables (charger rules sauvegardées)
sudo systemctl restart iptables
```

### Étape 5 : Configuration Nginx reverse proxy

```bash
sudo vi /etc/nginx/nginx.conf
```

**Remplacer bloc `server` par** :

```nginx
upstream app {
    server 127.0.0.1:5000;
}

server {
    listen 8094;
    server_name _;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://app;
    }
}
```

**Explications** :
- `upstream app` : Définit backend Apache (localhost:5000)
- `listen 8094` : Nginx écoute port 8094 (frontend)
- `proxy_pass http://app` : Proxyfie requêtes vers Apache
- `proxy_set_header` : Préserve informations client (IP, host, protocole)

**Sauvegarder** : `:wq`

### Étape 6 : Restart Nginx

```bash
sudo systemctl restart nginx
```

**Vérifier statut** :
```bash
sudo systemctl status nginx
# Active (running)
```

### Étape 7 : Validation finale (depuis Jump Host)

```bash
# Test accès Nginx (doit fonctionner ✅)
curl http://stbkp01:8094

# Output attendu : Page HTML application backup management
```

**Test accès direct Apache (doit échouer ❌)** :
```bash
curl http://stbkp01:5000
# Connection refused (iptables REJECT)
```

---

## 🔍 Commandes utiles

**iptables management** :
```bash
# Lister rules actives
sudo iptables -L -n -v

# Vérifier rules permanentes sauvegardées
cat /etc/sysconfig/iptables

# Tester port écoute
sudo ss -tuln | grep 8094
sudo ss -tuln | grep 5000

# Supprimer toutes rules (⚠️ dangereux)
sudo iptables -F
```

**Nginx debugging** :
```bash
# Test syntaxe config
sudo nginx -t

# Logs erreur
sudo tail -f /var/log/nginx/error.log

# Logs accès
sudo tail -f /var/log/nginx/access.log
```

---

## 📝 Points clés

**iptables chains** :
- **INPUT** : Trafic entrant serveur (incoming)
- **OUTPUT** : Trafic sortant serveur (outgoing)
- **FORWARD** : Trafic routé (forwarding)

**iptables actions** :
- **ACCEPT** : Autoriser paquet
- **REJECT** : Bloquer + envoyer erreur (Connection refused)
- **DROP** : Bloquer silencieux (timeout)

**Ports** :
- `--dport` : Destination port (incoming)
- `--sport` : Source port (outgoing)

**Nginx reverse proxy** :
- Frontend public (port 8094) protège backend (port 5000 localhost)
- Headers `X-Forwarded-*` préservent informations client
- Use case : Load balancing, SSL termination, sécurité

**Challenge 24 security** :
- Apache inaccessible directement (port 5000 bloqué)
- Accès uniquement via Nginx (port 8094 ouvert)
- Trafic localhost autorisé (Nginx ↔ Apache communication interne)

---

## 🎯 Tags

`iptables`, `Firewall`, `Security`, `Nginx`, `Reverse-Proxy`, `Apache`, `Network-Security`, `Port-Blocking`

---

**Complétion** : ✅ Challenge validé (Nginx accessible, Apache bloqué)  
**Prochaine étape** : Level 3 Linux (pas de certificat Level 2)

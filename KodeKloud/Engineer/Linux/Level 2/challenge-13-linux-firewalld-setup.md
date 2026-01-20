# Challenge 13 : Linux Firewalld Setup

**Date** : 10 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Installer et configurer `firewalld` sur les 3 serveurs applicatifs pour sécuriser l'infrastructure Nautilus :
- Autoriser connexions entrantes Nginx (port 80)
- Bloquer connexions entrantes Apache (port 8080)
- Règles permanentes, zone `public`

---

## 📋 Énoncé

Pour sécuriser notre infrastructure Nautilus dans le Datacenter Stratos, nous avons décidé d'installer et de configurer firewalld sur tous les serveurs applicatifs. Nous avons des services Apache et Nginx qui tournent sur ces applications. Nginx fonctionne comme serveur proxy inverse pour Apache. Nous aurons peut-être des paramètres de pare-feu plus robustes à l'avenir, mais pour l'instant nous avons décidé d'appliquer les exigences suivantes :

a. Autoriser toutes les connexions entrantes sur le port Nginx, c'est-à-dire `80`.

b. Bloquer toutes les connexions entrantes sur le port Apache, c'est-à-dire `8080`.

c. Toutes les règles doivent être permanentes.

d. La zone doit être `public`.

e. Si les services Apache ou Nginx ne sont pas déjà en cours d'exécution, veuillez vous assurer de les démarrer.

**Serveurs concernés** :
- `stapp01` (user `tony`)
- `stapp02` (user `steve`)
- `stapp03` (user `banner`)

---

## 🔧 Résolution

### Approche

Pour chaque serveur :
1. Installer `firewalld`
2. Démarrer + activer le service au boot
3. Ajouter règle permanente pour autoriser HTTP (port 80) dans zone `public`
4. Recharger firewall pour appliquer les règles permanentes
5. Port 8080 bloqué par défaut (pas dans zone public)

### Commandes exécutées

**Serveur stapp01** :
```bash
ssh tony@stapp01
sudo yum install firewalld -y
sudo systemctl enable --now firewalld
sudo firewall-cmd --permanent --zone public --add-service http
sudo firewall-cmd --reload
```

**Serveur stapp02** :
```bash
ssh steve@stapp02
sudo yum install firewalld -y
sudo systemctl enable --now firewalld
sudo firewall-cmd --permanent --zone public --add-service http
sudo firewall-cmd --reload
```

**Serveur stapp03** :
```bash
ssh banner@stapp03
sudo yum install firewalld -y
sudo systemctl enable --now firewalld
sudo firewall-cmd --permanent --zone public --add-service http
sudo firewall-cmd --reload
```

### Explications

**Options `firewall-cmd`** :
- `--permanent` : Règle persistante après reboot
- `--zone public` : Applique règle à la zone `public` (zone par défaut)
- `--add-service http` : Autorise service HTTP (port 80/tcp)
- `--reload` : Recharge les règles permanentes en runtime

**Pourquoi pas de règle pour bloquer 8080 ?**
- Zone `public` bloque par défaut tout trafic entrant NON autorisé
- Seul HTTP (80) est autorisé explicitement
- Port 8080 reste bloqué automatiquement

**Runtime vs Permanent** :
- Sans `--permanent` : Règle active immédiatement mais perdue au reboot
- Avec `--permanent` : Règle sauvegardée mais nécessite `--reload` pour activation

---

## ✅ Validation

Depuis le jump server :

```bash
# Tester port 80 (HTTP Nginx) - DOIT FONCTIONNER
curl stapp01
# Output attendu : Page web Nginx

# Tester port 8080 (Apache) - DOIT ÉCHOUER
curl stapp01:8080
# Output attendu : Connection refused / Timeout
```

Vérifier configuration firewall :

```bash
# Lister toutes les règles zone public
sudo firewall-cmd --list-all --zone public
# Output attendu :
# services: dhcpv6-client http ssh

# Vérifier services autorisés
sudo firewall-cmd --list-services --zone public
# Output attendu : dhcpv6-client http ssh
```

---

## 📌 Commandes utiles

```bash
# Installation
sudo yum install firewalld -y
sudo systemctl enable --now firewalld

# Vérifier statut
sudo firewall-cmd --state
sudo systemctl status firewalld

# Lister zones disponibles
sudo firewall-cmd --get-zones

# Vérifier zone par défaut
sudo firewall-cmd --get-default-zone

# Changer zone par défaut
sudo firewall-cmd --set-default-zone=<zone>

# Lister toutes règles zone active
sudo firewall-cmd --list-all

# Lister services autorisés
sudo firewall-cmd --list-services

# Lister ports autorisés
sudo firewall-cmd --list-ports

# Ajouter service (runtime + permanent)
sudo firewall-cmd --permanent --add-service <service>
sudo firewall-cmd --reload

# Ajouter port custom (runtime + permanent)
sudo firewall-cmd --permanent --add-port <port>/<protocol>
sudo firewall-cmd --reload

# Retirer service/port
sudo firewall-cmd --permanent --remove-service <service>
sudo firewall-cmd --permanent --remove-port <port>/<protocol>
sudo firewall-cmd --reload

# Recharger firewall
sudo firewall-cmd --reload

# Recharger complet (coupe connexions)
sudo firewall-cmd --complete-reload
```

### Services prédéfinis courants

```bash
http        # 80/tcp
https       # 443/tcp
ssh         # 22/tcp
ftp         # 21/tcp
smtp        # 25/tcp
dns         # 53/tcp,udp
mysql       # 3306/tcp
postgresql  # 5432/tcp
```

---

**Tags** : `firewalld` `firewall-cmd` `zones` `services` `permanent` `HTTP` `Level 2`

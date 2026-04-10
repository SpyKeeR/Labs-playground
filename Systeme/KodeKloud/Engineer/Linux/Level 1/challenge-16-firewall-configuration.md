# KodeKloud Engineer - Challenge 16 : Firewall Configuration

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Catégorie :** Firewall / Security

---

## 🎯 Objectif

Configurer **firewalld** (pare-feu dynamique RHEL/CentOS) pour autoriser le trafic entrant sur un port TCP spécifique en zone publique, afin de rendre accessible une application web de backup.

---

## 📋 Énoncé

L'équipe d'administration système Nautilus a déployé une interface web pour leur utilitaire de sauvegarde sur le **serveur de backup Nautilus** au sein du datacenter Stratos. Cette application fonctionne sur le **port 8087**, et **firewalld est actif** sur le serveur. Pour répondre aux besoins opérationnels, les exigences suivantes ont été identifiées :

**Exigences :**
- Autoriser toutes les connexions entrantes sur le **port 8087/tcp**
- S'assurer que la zone est définie sur **public**

**Serveur concerné :** `stbkp01` (Nautilus Backup Server)

---

## 🔧 Résolution

### Connexion serveur

```bash
ssh clint@stbkp01
```

**User :** `clint` (admin privileges via sudo)

---

### Vérifier état firewalld

**1. Statut service**

```bash
sudo systemctl status firewalld
```

**Output attendu :**
```
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled)
   Active: active (running) since Mon 2026-01-06 14:30:12 UTC
```

**Analyse :**
- `active (running)` : Firewalld opérationnel
- `enabled` : Démarrage automatique au boot

---

**2. État firewalld (commande firewall-cmd)**

```bash
sudo firewall-cmd --state
```

**Output :**
```
running
```

**Signification :** Firewall actif, règles appliquées.

---

### Vérifier zone par défaut

**Commande :**
```bash
sudo firewall-cmd --get-default-zone
```

**Output :**
```
public
```

**Analyse :** Zone par défaut déjà `public` (requis énoncé ✅).

---

### Ajouter règle port 8087/tcp

**Commande (permanent) :**
```bash
sudo firewall-cmd --permanent --zone=public --add-port=8087/tcp
```

**Flags expliqués :**
- `--permanent` : Règle persistante (survit reboot + reload)
- `--zone=public` : Cible zone publique (Internet-facing, restrictive)
- `--add-port=8087/tcp` : Autoriser port 8087 protocole TCP

**Output :**
```
success
```

---

### Recharger firewalld

**Pourquoi recharger ?**  
Les règles `--permanent` sont écrites dans fichiers XML (`/etc/firewalld/zones/public.xml`) mais **pas appliquées runtime** immédiatement.

**Commande :**
```bash
sudo firewall-cmd --reload
```

**Output :**
```
success
```

**Effet :** Recharge configs permanentes → Runtime (applique règle port 8087 immédiatement).

---

### Vérification configuration

**1. Lister règles zone public (runtime)**

```bash
# Lister règles zone public
sudo firewall-cmd --zone=public --list-all
```

**Output :**
```
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0
  sources: 
  services: ssh dhcpv6-client
  ports: 8087/tcp
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules:
```

**Analyse :**
- `ports: 8087/tcp` ✅ : Règle présente
- `services: ssh dhcpv6-client` : Services autorisés par défaut (SSH accès admin, DHCP client)
- `interfaces: eth0` : Zone public attachée interface réseau principale

---

**2. Tester depuis jumphost**

**Contexte :** Application web écoute `0.0.0.0:8087` sur `stbkp01`.

**Depuis jumphost :**
```bash
curl http://stbkp01:8087
```

**Output attendu :**
```html
<!DOCTYPE html>
<html>
<head><title>Nautilus Backup Web UI</title></head>
<body>
  <h1>Backup Utility Dashboard</h1>
  <p>Status: Running</p>
</body>
</html>
```

**Succès :** HTTP 200 OK → Firewall autorise trafic port 8087 ✅.

---

**3. Tester refus autres ports**

**Test port 8088 (non autorisé) :**
```bash
curl http://stbkp01:8088 --connect-timeout 5
```

**Output :**
```
curl: (7) Failed to connect to stbkp01 port 8088: Connection timed out
```

**Analyse :** Firewall **bloque** port 8088 (comportement attendu, seul 8087 autorisé).

---

### Alternative : Lister zones actives

**Commande :**
```bash
sudo firewall-cmd --list-all-zones
```

**Output (extrait zone public) :**
```
public
  target: default
  icmp-block-inversion: no
  interfaces: eth0
  sources: 
  services: ssh dhcpv6-client
  ports: 8087/tcp
  ...
```

**Utilité :** Voir **toutes zones** (public, trusted, dmz, internal) + règles actives.

---

## 📝 Commandes clés

```bash
# Vérifier état
firewall-cmd --state
firewall-cmd --get-default-zone

# Ajouter port (permanent)
sudo firewall-cmd --permanent --zone=public --add-port=8087/tcp
sudo firewall-cmd --reload

# Lister règles zone
firewall-cmd --zone=public --list-all

# Services (alternative ports)
sudo firewall-cmd --permanent --add-service=http
firewall-cmd --get-services
```
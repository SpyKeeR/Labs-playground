# Challenge 12 : DNS Troubleshooting

**Date** : 10 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Résoudre les problèmes de résolution DNS sur `stapp01` en ajoutant les serveurs DNS publics Google dans `/etc/resolv.conf`.

---

## 📋 Énoncé

L'équipe des administrateurs système de xFusionCorp Industries a remarqué des problèmes intermittents de résolution DNS dans plusieurs applications. Le serveur App Server 1 dans le Datacenter Stratos rencontre des problèmes de résolution DNS, nous voulons donc ajouter des serveurs DNS supplémentaires sur ce serveur.

Comme solution temporaire, nous avons décidé d'utiliser les DNS publics de Google (ipv4). Veuillez effectuer les modifications appropriées sur ce serveur.

**Serveur concerné** :
- `stapp01` (user `tony`)

**DNS publics Google** :
- `8.8.8.8` (Primary)
- `8.8.4.4` (Secondary)

---

## 🔧 Résolution

### Approche

1. Se connecter via SSH sur `stapp01`
2. Éditer le fichier `/etc/resolv.conf`
3. Ajouter les nameservers Google DNS après les DNS locaux existants
4. Tester résolution DNS

### Commandes exécutées

```bash
ssh tony@stapp01
sudo vi /etc/resolv.conf
```

**Contenu ajouté** (après les déclarations DNS locales existantes) :
```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### Explications

**Structure `/etc/resolv.conf`** :
```
# DNS locaux (existants)
nameserver 10.0.0.1
search stratos.xfusioncorp.com

# DNS publics Google (ajoutés)
nameserver 8.8.8.8
nameserver 8.8.8.4
```

**Ordre de résolution** :
- Le système essaie les nameservers dans l'ordre de déclaration
- Si le premier DNS ne répond pas, il passe au suivant
- Maximum 3 nameservers sont utilisés par le système

**Pourquoi Google DNS ?**
- Haute disponibilité (uptime 99.99%)
- Faible latence (réseau mondial)
- Filtrage malware/phishing
- Pas de censure

---

## ✅ Validation

Tester la résolution DNS :

```bash
# Ping domaine externe
sudo ping google.fr
# Output attendu : résolution OK

# Tester résolution avec nslookup
nslookup google.com
# Devrait résoudre vers IP Google

# Tester avec dig
dig google.com
# Affiche détails résolution DNS
```

---

## 📌 Commandes utiles

```bash
# Vérifier contenu resolv.conf
cat /etc/resolv.conf

# Tester résolution DNS
nslookup <domain>
dig <domain>
host <domain>

# Tester connectivité DNS server
ping 8.8.8.8
nc -zv 8.8.8.8 53

# Vérifier ordre résolution
cat /etc/nsswitch.conf
# Ligne "hosts:" définit ordre (files dns)

# Flush cache DNS (si systemd-resolved)
sudo systemd-resolve --flush-caches

# Vérifier stats DNS (si systemd-resolved)
resolvectl status
```

### DNS publics connus

```bash
# Google DNS
8.8.8.8
8.8.4.4

# Cloudflare DNS
1.1.1.1
1.0.0.1

# OpenDNS
208.67.222.222
208.67.220.220

# Quad9 (sécurité)
9.9.9.9
149.112.112.112
```

---

## ⚠️ Notes importantes

- **Persistance** : `/etc/resolv.conf` peut être écrasé par DHCP/NetworkManager
- **systemd-resolved** : Sur distributions modernes, utiliser `/etc/systemd/resolved.conf` au lieu de `/etc/resolv.conf`
- **DNS local priority** : Toujours conserver les DNS locaux en premier pour résolution interne

---

**Tags** : `DNS` `resolv.conf` `nameserver` `troubleshooting` `Google DNS` `Level 2`

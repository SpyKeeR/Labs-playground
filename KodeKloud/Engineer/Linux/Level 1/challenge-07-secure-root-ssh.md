# Challenge 7 : Secure Root SSH Access

**Date :** 5 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Sécurité SSH  
**Difficulté :** Débutant  
**Durée :** ~15 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Désactiver l'accès SSH direct en root sur tous les serveurs d'application pour renforcer la sécurité suite à des audits de conformité.

---

## 📋 Énoncé

Suite aux audits de sécurité, l'équipe sécurité de **xFusionCorp Industries** a déployé de nouveaux protocoles, incluant la restriction de connexion SSH directe en root.

**Tâche :**
Désactiver la connexion SSH directe root sur **tous les serveurs d'application** dans le Stratos Datacenter.

**Serveurs concernés :**
- App Server 1 (stapp01)
- App Server 2 (stapp02)
- App Server 3 (stapp03)

---

## 🔧 Résolution

### Étape 1 : Connexion au premier serveur

```bash
ssh tony@stapp01
```

**Explication :** Connexion avec user non-root (tony), qui deviendra la seule façon de se connecter après modification.

---

### Étape 2 : Éditer configuration SSH

```bash
sudo vi /etc/ssh/sshd_config
```

**Explication :** Fichier configuration serveur SSH (daemon sshd).

**⚠️ Note :** Utiliser `sudo` car fichier système protégé (owner root, permissions 600).

---

### Étape 3 : Modifier directive PermitRootLogin

**Chercher la ligne (dans vi) :**
```bash
# Dans vi : taper /PermitRootLogin puis Entrée
```

**Ligne originale (peut être commentée ou à "yes") :**
```
#PermitRootLogin yes
```
**OU**
```
PermitRootLogin yes
```

**Modifier en :**
```
PermitRootLogin no
```

**Actions vi :**
1. Appuyer `i` (mode insertion)
2. Modifier ligne
3. Appuyer `Esc` (sortir mode insertion)
4. Taper `:wq!` puis `Entrée` (write + quit + force)

---

### Étape 4 : Redémarrer service SSH

```bash
sudo systemctl restart sshd
```

**Explication :** Recharger configuration SSH pour appliquer changements.

**Alternative (certaines distros) :**
```bash
sudo systemctl reload sshd  # Recharge config sans couper connexions actives
sudo service ssh restart    # Syntaxe ancienne (SysVinit)
```

---

### Étape 5 : Répéter sur autres serveurs

```bash
# Depuis machine locale (ou jump server)
ssh steve@stapp02
sudo vi /etc/ssh/sshd_config
# Modifier PermitRootLogin no
sudo systemctl restart sshd
exit

ssh banner@stapp03
sudo vi /etc/ssh/sshd_config
# Modifier PermitRootLogin no
sudo systemctl restart sshd
exit
```

---

### Étape 6 : Validation

```bash
# Tenter connexion root (DOIT échouer)
ssh root@stapp01
# Résultat attendu : Permission denied
```

**OU (si password prompt) :**
```
root@stapp01's password: [peu importe password]
Permission denied, please try again.
```

**Validation réussie :** Connexion root refusée, mais connexion user normal fonctionne.

---

## 🔗 Ressources

**Documentation officielle :**
- `man sshd_config` : toutes directives configuration
- `man sshd` : daemon SSH server

**Fichiers système :**
- `/etc/ssh/sshd_config` : configuration serveur SSH
- `/etc/ssh/ssh_config` : configuration client SSH (différent!)
- `/var/log/auth.log` : logs authentification (Debian/Ubuntu)
- `/var/log/secure` : logs authentification (RedHat/CentOS)

**Guides hardening SSH :**
- [CIS Benchmark SSH](https://www.cisecurity.org/benchmark/debian_linux)
- [NSA SSH Hardening](https://github.com/nsacyber/SSH-Hardening)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)

---

## 🎓 Commandes à Retenir

```bash
# Éditer config SSH
sudo vi /etc/ssh/sshd_config

# Tester config AVANT restart (CRITIQUE!)
sudo sshd -t

# Redémarrer SSH (appliquer changements)
sudo systemctl restart sshd

# Recharger sans couper connexions actives
sudo systemctl reload sshd

# Vérifier statut service SSH
sudo systemctl status sshd

# Logs SSH temps réel
sudo tail -f /var/log/auth.log

# Lister tentatives failed login
sudo grep "Failed password" /var/log/auth.log | tail -20

# Bannir IP après 3 tentatives (fail2ban)
sudo fail2ban-client status sshd
```

---

**Tags :** #Linux #SSH #Security #Hardening #Audit #KodeKloud

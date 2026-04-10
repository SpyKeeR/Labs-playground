# KodeKloud Engineer - Challenge 13 : Task Scheduling Restriction

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Security & Cron Access Control  
**Difficulté :** Medium  
**Durée :** ~25 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Implémenter des restrictions d'accès au système de planification cron pour se conformer aux standards de sécurité.

---

## 📋 Énoncé

**Contexte :** Dans le cadre de la conformité aux standards de sécurité, l'équipe projet Nautilus a décidé d'imposer des restrictions sur l'accès à crontab. Seuls des utilisateurs désignés seront autorisés à créer ou modifier des tâches cron.

**Mission :** Configurer l'accès crontab sur App Server 1 selon les spécifications suivantes :
- **Autoriser** l'accès crontab à l'utilisateur `anita`
- **Refuser** l'accès crontab à l'utilisateur `garrett`

**Serveur cible :** App Server 1

---

## 🔧 Résolution

### Étape 1 : Comprendre mécanisme cron.allow / cron.deny

**Documentation :**
```bash
man 1 crontab
```

**Section "FILES" :**
```
/etc/cron.allow
    If this file exists, only users listed in it are allowed to use crontab.

/etc/cron.deny
    If cron.allow does not exist, users listed in cron.deny are NOT allowed to use crontab.

If neither file exists, only root can use crontab (restrictive).
If both exist, cron.allow takes precedence.
```

**Logique :**
1. Si `/etc/cron.allow` existe → Seuls users listés autorisés (whitelist)
2. Sinon, si `/etc/cron.deny` existe → Tous users autorisés SAUF listés (blacklist)
3. Si aucun → Seul root autorisé (par défaut RHEL/CentOS)

---

### Étape 2 : Créer /etc/cron.deny (bloquer garrett)

```bash
sudo vi /etc/cron.deny
```

**Ajouter :**
```
garrett
```

**⚠️ Format :** Un username par ligne.

---

### Étape 3 : Créer /etc/cron.allow (autoriser anita)

```bash
sudo vi /etc/cron.allow
```

**Ajouter :**
```
anita
```

**⚠️ Important :** 
- `cron.allow` existe → **SEULS** users listés autorisés
- garrett **pas** dans cron.allow → automatiquement bloqué (même si pas dans cron.deny)

---

### Étape 4 : Définir permissions fichiers (critical!)

**Problème découvert :** Par défaut, fichiers créés avec permissions restrictives.

**Vérifier :**
```bash
ls -l /etc/cron.*
```

**Résultat initial (problématique) :**
```
-rw------- 1 root root  7 Jan  6 09:30 /etc/cron.allow
-rw------- 1 root root  8 Jan  6 09:29 /etc/cron.deny
```

**Problème :** Permissions `600` (rw-------) = seul root peut lire.  
→ Cron daemon ne peut pas lire → **tous users bloqués**.

**Solution : Rendre readable par tous :**
```bash
sudo chmod a+r /etc/cron.allow
sudo chmod a+r /etc/cron.deny
```

**Vérification :**
```bash
ls -l /etc/cron.*
```

**Résultat correct :**
```
-rw-r--r-- 1 root root  7 Jan  6 09:30 /etc/cron.allow
-rw-r--r-- 1 root root  8 Jan  6 09:29 /etc/cron.deny
```

**Permissions `644` (rw-r--r--) :**
- Owner (root) : read + write
- Group : read
- Others : read ← **Cron daemon peut lire**

---

### Étape 5 : Redémarrer service cron

```bash
sudo systemctl restart crond.service
```

**⚠️ Note nom service :**
- **RHEL/CentOS** : `crond` (avec 'd')
- **Debian/Ubuntu** : `cron` (sans 'd')

**Vérifier service actif :**
```bash
sudo systemctl status crond.service
```

**Résultat attendu :**
```
● crond.service - Command Scheduler
   Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled)
   Active: active (running) since Tue 2026-01-06 09:32:15 UTC; 5s ago
 Main PID: 12345 (crond)
   CGroup: /system.slice/crond.service
           └─12345 /usr/sbin/crond -n

Jan 06 09:32:15 stapp01 systemd[1]: Started Command Scheduler.
Jan 06 09:32:15 stapp01 crond[12345]: (CRON) INFO (running with inotify support)
```

---

### Étape 6 : Tester restrictions

**Test 1 : User anita (doit être autorisé) :**
```bash
sudo su - anita
crontab -l
```

**Résultat attendu :**
```
no crontab for anita
```

**✅ OK** : Pas d'erreur "access denied" → anita autorisée.

**Créer test cron :**
```bash
crontab -e
# Ajouter :
# * * * * * echo "test" > /tmp/anita_cron_test.txt

crontab -l
# * * * * * echo "test" > /tmp/anita_cron_test.txt
```

**✅ Succès** : anita peut créer crontab.

---

**Test 2 : User garrett (doit être bloqué) :**
```bash
sudo su - garrett
crontab -l
```

**Résultat attendu :**
```
You (garrett) are not allowed to use this program (crontab)
See crontab(1) for more information
```

**✅ OK** : garrett bloqué comme prévu.

---

## 🎓 Commandes à Retenir

```bash
# Créer cron.allow (whitelist)
echo "username" | sudo tee -a /etc/cron.allow

# Créer cron.deny (blacklist)
echo "username" | sudo tee -a /etc/cron.deny

# Permissions correctes (readable)
sudo chmod 644 /etc/cron.allow
sudo chmod 644 /etc/cron.deny

# Redémarrer service cron
sudo systemctl restart crond     # RHEL/CentOS
sudo systemctl restart cron      # Debian/Ubuntu

# Vérifier service actif
sudo systemctl status crond

# Tester accès user
sudo -u username crontab -l

# Lister tous crontabs système
for user in $(cut -d: -f1 /etc/passwd); do
  sudo crontab -u $user -l 2>/dev/null && echo "=== $user ==="
done

# Vérifier configuration actuelle
ls -l /etc/cron.{allow,deny}
cat /etc/cron.allow
cat /etc/cron.deny

# Logs cron
sudo tail -f /var/log/cron               # RHEL
sudo grep CRON /var/log/syslog | tail    # Debian
```

---

**Tags :** #Linux #Cron #Security #AccessControl #SystemAdministration #KodeKloud #Compliance

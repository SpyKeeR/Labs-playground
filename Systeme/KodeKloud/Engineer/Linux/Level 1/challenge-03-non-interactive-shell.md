# Challenge 3 : Non-Interactive Shell User

**Date :** Janvier 2026 (antérieur au 5 janvier)  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Utilisateurs système et sécurité  
**Difficulté :** Débutant  
**Durée :** ~8 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Créer un utilisateur avec shell non-interactif pour un agent de sauvegarde, empêchant toute connexion interactive tout en permettant l'exécution de processus automatisés.

---

## 📋 Énoncé

L'équipe d'administration système de **xFusionCorp Industries** a installé un outil d'agent de sauvegarde sur tous les serveurs App.

Selon les exigences de cet outil, il est nécessaire de créer un utilisateur avec un **shell non-interactif**.

**Tâche à réaliser :**
- Créer un utilisateur nommé `mariyam` avec un shell non-interactif sur **App Server 1**

**Serveur cible :** `stapp01` (tony@172.16.238.10)

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur cible

```bash
ssh tony@172.16.238.10
```

---

### Étape 2 : Créer l'utilisateur avec shell non-interactif

```bash
sudo useradd --shell /bin/false mariyam
```

**Explication détaillée :**
- `useradd` : commande création utilisateur
- `--shell /bin/false` : définir shell à `/bin/false` (équivalent `-s /bin/false`)
- `/bin/false` : binaire qui retourne immédiatement code sortie 1 (échec)
- `mariyam` : nom utilisateur

**Résultat :**
- Utilisateur existe dans système (`/etc/passwd`)
- Processus peuvent tourner sous cet user (via `su -s /bin/bash mariyam -c "command"`)
- **Connexion interactive IMPOSSIBLE** (SSH, login console refusés)

---

### Étape 3 : Validation

```bash
# Vérifier user créé
id mariyam

# Vérifier shell dans /etc/passwd
grep "mariyam:" /etc/passwd
```

**Résultat attendu :**
```
uid=1001(mariyam) gid=1001(mariyam) groups=1001(mariyam)
```

**Ligne /etc/passwd :**
```
mariyam:x:1001:1001::/home/mariyam:/bin/false
                                     └─ Shell non-interactif
```

---

### Étape 4 : Tester impossibilité connexion interactive

```bash
# Depuis serveur local, tenter SSH user mariyam
ssh mariyam@172.16.238.10
# Résultat : Connexion fermée immédiatement (pas de shell)
```

**OU :**
```bash
# Tenter su vers mariyam
sudo su - mariyam
# Résultat : Pas de prompt, retour immédiat
```

---

## 🔗 Ressources

**Documentation :**
- `man useradd` : options création users
- `man passwd` : format /etc/passwd (champ shell)
- `man nologin` : comportement /usr/sbin/nologin

**Fichiers système :**
- `/etc/shells` : liste shells valides
- `/etc/passwd` : user database (champ 7 = shell)
- `/bin/false` : binaire retourne toujours false
- `/usr/sbin/nologin` : binaire affiche message + refuse login

**Guides sécurité :**
- [Linux Service Accounts Best Practices](https://www.redhat.com/sysadmin/linux-service-accounts)
- [Systemd Hardening](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)

---

## 🎓 Commandes à Retenir

```bash
# Créer user avec shell non-interactif
sudo useradd --shell /bin/false username

# Variante avec message explicatif
sudo useradd --shell /usr/sbin/nologin username

# Modifier shell user existant
sudo usermod -s /bin/false username

# Exécuter commande sous user non-interactif
sudo su -s /bin/bash username -c "command"

# Vérifier shell d'un user
grep "^username:" /etc/passwd | cut -d: -f7

# Lister tous users avec shell non-interactif
awk -F: '$7 ~ /(false|nologin)/ {print $1}' /etc/passwd
```

---

**Tags :** #Linux #Security #SystemAccounts #UserManagement #LeastPrivilege #KodeKloud

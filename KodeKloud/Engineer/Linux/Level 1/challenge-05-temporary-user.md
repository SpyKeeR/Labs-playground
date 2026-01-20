# Challenge 5 : Create Temporary Linux User

**Date :** 5 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Gestion utilisateurs  
**Difficulté :** Débutant  
**Durée :** ~10 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Créer un utilisateur temporaire avec date d'expiration pour accès limité dans le temps à un serveur de production.

---

## 📋 Énoncé

Dans le cadre d'une mission temporaire sur le projet Nautilus, un développeur nommé **mark** nécessite un accès pour une durée limitée. Pour assurer une gestion fluide des accès, un compte utilisateur temporaire avec une date d'expiration est requis.

**Tâche :**
- Créer un utilisateur nommé `mark` sur **App Server 2** dans le Stratos Datacenter
- Définir la date d'expiration au **17 février 2024**
- S'assurer que l'utilisateur est créé en minuscules selon le protocole standard

**Serveur cible :** `stapp02` (steve@stapp02)

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur cible

```bash
ssh steve@stapp02
```

**Explication :** Connexion SSH sur App Server 2 avec l'utilisateur steve.

---

### Étape 2 : Vérifier les options useradd

```bash
useradd --help
```

**Explication :** Consultation de l'aide pour trouver l'option d'expiration (`-e, --expiredate`).

**Options clés identifiées :**
- `-m` : créer le répertoire home
- `-e YYYY-MM-DD` : définir date d'expiration du compte

---

### Étape 3 : Créer l'utilisateur avec expiration

```bash
useradd -m -e 2024-02-17 mark
```

**Explication détaillée :**
- `useradd` : commande création utilisateur Linux
- `-m` : créer automatiquement `/home/mark` (répertoire home)
- `-e 2024-02-17` : date expiration compte (format YYYY-MM-DD)
- `mark` : nom utilisateur (minuscules comme requis)

**Note :** Pas besoin de `-s /bin/bash` car c'est le shell par défaut sur la plupart des systèmes.

---

### Étape 4 : Validation

```bash
# Vérifier existence utilisateur et UID/GID
id mark

# Vérifier entrée dans /etc/passwd
cat /etc/passwd | grep mark

# Vérifier date expiration dans /etc/shadow
sudo cat /etc/shadow | grep mark
```

**Résultat attendu :**
- `/etc/passwd` : `mark:x:1002:1002::/home/mark:/bin/bash`
- `/etc/shadow` : `mark:!!:19723:0:99999:7::19770:` (le dernier champ = jours depuis epoch pour 2024-02-17)

---

## 🔗 Ressources

**Documentation officielle :**
- `man useradd` : manual page complète
- `man shadow` : format fichier /etc/shadow
- `man chage` : change user password expiry information

**Fichiers système concernés :**
- `/etc/passwd` : infos utilisateurs (UID, GID, home, shell)
- `/etc/shadow` : passwords hashés + infos expiration
- `/etc/login.defs` : configuration par défaut création users

**Liens utiles :**
- [Linux Users and Groups](https://www.redhat.com/sysadmin/linux-user-group-management)
- [Understanding /etc/shadow](https://www.cyberciti.biz/faq/understanding-etcshadow-file/)

---

## 🎓 Commandes à Retenir

```bash
# Créer user temporaire
useradd -m -e YYYY-MM-DD username

# Vérifier expiration
chage -l username

# Modifier expiration user existant
chage -E YYYY-MM-DD username

# Lister users avec expiration proche
awk -F: '$8 && $8 < '$(date +%s)'/86400+30 {print $1}' /etc/shadow
```

---

**Tags :** #Linux #UserManagement #Security #Expiration #KodeKloud

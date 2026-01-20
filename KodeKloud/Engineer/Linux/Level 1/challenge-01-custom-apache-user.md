# Challenge 1 : Configure Custom Apache User

**Date :** Janvier 2026 (antérieur au 5 janvier)  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Gestion utilisateurs avancée  
**Difficulté :** Débutant  
**Durée :** ~10 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Créer un utilisateur Apache personnalisé avec UID spécifique et répertoire personnel custom pour renforcer la sécurité des applications web.

---

## 📋 Énoncé

Pour des raisons de sécurité, l'équipe de sécurité de **xFusionCorp Industries** a décidé d'utiliser des utilisateurs Apache personnalisés pour chaque application web hébergée, au lieu de l'utilisateur par défaut.

Chaque application web devra donc avoir son propre utilisateur Apache, avec un répertoire personnel spécifique, différent du répertoire par défaut.

**Tâches à réaliser :**
1. Créer un utilisateur nommé `jim` sur **App Server 2** dans le Stratos Datacenter
2. Assigner à cet utilisateur l'UID `1582`
3. Définir son répertoire personnel sur `/var/www/jim`

**Serveur cible :** `stapp02` (steve@172.16.238.11)

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur cible

```bash
ssh steve@172.16.238.11
```

**Explication :** Connexion SSH sur App Server 2 avec l'utilisateur steve.

---

### Étape 2 : Créer l'utilisateur avec paramètres spécifiques

```bash
sudo useradd -u 1582 -d /var/www/jim -m jim
```

**Explication détaillée :**
- `useradd` : commande création utilisateur Linux
- `-u 1582` : définir UID (User ID) spécifique à 1582
- `-d /var/www/jim` : spécifier répertoire personnel custom (au lieu de `/home/jim`)
- `-m` : créer automatiquement le répertoire personnel s'il n'existe pas
- `jim` : nom de l'utilisateur

**Pourquoi ces options ?**
- **UID fixe** : Garantit cohérence entre serveurs (permissions fichiers)
- **Répertoire custom** : Sécurité isolation (Apache users dans `/var/www`, pas `/home`)
- **Création automatique** : `-m` évite erreurs "home directory not found"

---

### Étape 3 : Validation

```bash
# Vérifier UID, GID, groupes
id jim

# Vérifier entrée /etc/passwd
grep "jim:" /etc/passwd

# Vérifier répertoire personnel existe
ls -ld /var/www/jim
```

**Résultat attendu :**
```
uid=1582(jim) gid=1582(jim) groups=1582(jim)
```

**Ligne /etc/passwd :**
```
jim:x:1582:1582::/var/www/jim:/bin/bash
```

**Répertoire créé :**
```
drwxr-xr-x 2 jim jim 4096 Jan 02 10:30 /var/www/jim
```

---

## � Ressources

- `man useradd` : Options création utilisateurs
- `man passwd` : Format /etc/passwd
- `/etc/default/useradd` : Defaults système

---

## 📝 Commandes clés

```bash
# Créer user avec UID + home custom
sudo useradd -u UID -d /custom/path -m username

# Vérifier user créé
id username
grep "username:" /etc/passwd

# Trouver fichiers appartenant à UID
find / -uid 1582 -ls
```

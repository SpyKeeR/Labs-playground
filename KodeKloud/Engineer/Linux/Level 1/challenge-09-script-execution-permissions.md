# Challenge 9 : Script Execution Permissions

**Date :** 5 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Permissions et exécution scripts  
**Difficulté :** Débutant  
**Durée :** ~10 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Donner les permissions d'exécution appropriées à un script bash pour automatisation des backups, en permettant à tous les utilisateurs de l'exécuter.

---

## 📋 Énoncé

Dans le cadre de l'automatisation des processus de backup, l'équipe sysadmin de **xFusionCorp Industries** a développé un nouveau script bash nommé `xfusioncorp.sh`.

Bien que le script ait été distribué sur tous les serveurs nécessaires, il **manque de permissions exécutables** sur **App Server 2** dans le Stratos Datacenter.

**Tâches :**
1. Donner les permissions exécutables au script `/tmp/xfusioncorp.sh` sur App Server 2
2. S'assurer que **tous les utilisateurs** peuvent l'exécuter

**Serveur cible :** `stapp02` (steve@172.16.238.11)

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur cible

```bash
ssh steve@stapp02
```

---

### Étape 2 : Vérifier permissions actuelles

```bash
ls -l /tmp/xfusioncorp.sh
```

**Résultat initial (exemple) :**
```
-rw------- 1 root root 256 Jan 5 10:30 /tmp/xfusioncorp.sh
└─┬─┘
  └─ Permissions : rw------- (600)
     Owner peut lire/écrire, AUCUNE exécution
     Group/Others : aucun accès
```

**Problème identifié :**
- **Aucune permission exécution** (pas de `x`)
- **Aucune permission lecture** pour group/others (besoin pour exécution)

---

### Étape 3 : Donner permissions lecture + exécution à tous

```bash
sudo chmod a+rx /tmp/xfusioncorp.sh
```

**Explication détaillée :**
- `sudo` : Permissions root nécessaires (fichier owner root)
- `chmod` : Change mode (permissions)
- `a` : **All** (user + group + others)
- `+` : **Ajouter** permissions (au lieu de remplacer)
- `r` : **Read** (lecture nécessaire pour exécution script)
- `x` : **eXecute** (exécution)
- `/tmp/xfusioncorp.sh` : Fichier cible

**Résultat :** Permissions `rwxr-xr-x` (755)

---

### Étape 4 : Validation

```bash
# Vérifier nouvelles permissions
ls -l /tmp/xfusioncorp.sh
```

**Résultat attendu :**
```
-rwxr-xr-x 1 root root 256 Jan 5 10:30 /tmp/xfusioncorp.sh
 └─┬─┘└┬┘└┬┘
   │   │  └─ Others : r-x (lecture + exécution)
   │   └─── Group  : r-x (lecture + exécution)
   └─────── Owner  : rwx (lecture + écriture + exécution)
```

**Tester exécution (optionnel) :**
```bash
# En tant que user steve (non-root)
/tmp/xfusioncorp.sh
# Script doit s'exécuter sans erreur "Permission denied"
```

---

## 🔗 Ressources

**Documentation :**
- `man chmod` : Toutes options chmod
- `man 7 inode` : Inodes et permissions
- `info coreutils 'File permissions'` : Guide détaillé

**Guides sécurité :**
- [Linux Permissions Best Practices](https://www.redhat.com/sysadmin/linux-file-permissions-explained)
- [SUID/SGID Security](https://www.linuxjournal.com/article/2932)

**Outils :**
- `stat fichier` : Voir permissions détaillées (octal + symbolique)
- `getfacl fichier` : ACLs avancées (voir challenge 10)
- `namei -l /path/to/file` : Tracer permissions arborescence complète

---

## 🎓 Commandes à Retenir

```bash
# Ajouter exécution owner
chmod u+x script.sh

# Ajouter lecture+exécution tous (scripts)
chmod a+rx script.sh

# Définir permissions exactes (octal)
chmod 755 script.sh    # rwxr-xr-x
chmod 644 file.txt     # rw-r--r--
chmod 600 secret.key   # rw-------

# Permissions récursives
chmod -R 755 /opt/scripts/

# Vérifier permissions
ls -l fichier
stat fichier

# Trouver fichiers permissions spécifiques
find /path -perm 777    # Exactement 777
find /path -perm -755   # Au moins 755
find /path -perm /u+x   # Owner exécution
```

---

**Tags :** #Linux #Permissions #Chmod #ScriptExecution #Security #FileManagement #KodeKloud

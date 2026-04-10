# Challenge 10 : Correcting File ACL Permissions

**Date :** 5 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - ACL (Access Control Lists) avancées  
**Difficulté :** Intermédiaire  
**Durée :** ~15 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Corriger les permissions ACL sur un fichier système critique suite à un audit de sécurité, en appliquant des règles d'accès granulaires par utilisateur.

---

## 📋 Énoncé

Après avoir conduit un audit de sécurité dans le Stratos DC, l'équipe sécurité Nautilus a découvert des permissions mal configurées sur des fichiers critiques.

Pour corriger cela, l'équipe support production prend des mesures correctives. Spécifiquement, le fichier nommé `/etc/hostname` sur **Nautilus App 2** nécessite des ajustements de ses **Access Control Lists (ACLs)** comme suit :

**Exigences :**
1. Le propriétaire (user owner) et le groupe propriétaire (group owner) du fichier doivent être **root**
2. **Others** doivent posséder **read only** permissions sur le fichier
3. L'utilisateur **john** ne doit avoir **aucune permission** sur le fichier
4. L'utilisateur **garrett** doit avoir **read only** permission sur le fichier

**Serveur cible :** `stapp02` (steve@172.16.238.11)

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur cible

```bash
ssh steve@172.16.238.11
```

---

### Étape 2 : Vérifier état actuel fichier

```bash
# Vérifier ownership et permissions standard
ls -l /etc/hostname

# Vérifier ACLs actuelles
getfacl /etc/hostname
```

**Exemple état initial :**
```
-rw-r--r-- 1 root root 10 Jan 5 09:00 /etc/hostname
```

---

### Étape 3 : Définir ACL pour john (aucune permission)

```bash
sudo setfacl -m u:john:0 /etc/hostname
```

**Explication :**
- `sudo` : Modification fichier système (owner root)
- `setfacl` : Set File ACL (définir ACL)
- `-m` : **Modify** (modifier/ajouter ACL entry)
- `u:john:0` : **User john : Permissions 0** (aucune)
  - `u` : User (type entry)
  - `john` : Username
  - `0` : Permissions (aucune = `---`)

---

### Étape 4 : Définir ACL pour garrett (lecture seule)

```bash
sudo setfacl -m u:garrett:r /etc/hostname
```

**Explication :**
- `u:garrett:r` : **User garrett : Permission read**
  - `r` : Read only (équivalent `r--` ou `4`)

**Alternative syntaxe numérique :**
```bash
sudo setfacl -m u:garrett:4 /etc/hostname
# 4 = read, identique à :r
```

---

### Étape 5 : Vérifier ownership (déjà OK normalement)

```bash
# Vérifier owner et group sont root
ls -l /etc/hostname
# -rw-r--r--+ 1 root root 10 Jan 5 09:00 /etc/hostname
#              └─ root:root OK
#          └─ + indique ACLs présentes

# Si besoin corriger (normalement pas nécessaire)
# sudo chown root:root /etc/hostname
```

---

### Étape 6 : Vérifier permissions others (déjà OK)

```bash
# Permissions standard : rw-r--r-- (644)
# Others ont déjà r-- (read only) → Exigence 2 satisfaite
```

---

### Étape 7 : Validation complète

```bash
getfacl /etc/hostname
```

**Résultat attendu :**
```
# file: etc/hostname
# owner: root
# group: root
user::rw-              # Owner root : read+write
user:john:---          # User john : AUCUNE permission
user:garrett:r--       # User garrett : read only
group::r--             # Group root : read only
mask::r--              # Mask limite permissions effectives
other::r--             # Others : read only
```

**Vérifications :**
- ✅ Owner/Group : root/root
- ✅ Others : read only (`r--`)
- ✅ john : aucune permission (`---`)
- ✅ garrett : read only (`r--`)

---

## 🔗 Ressources

**Documentation :**
- `man setfacl` : Définir ACL
- `man getfacl` : Lire ACL
- `man acl` : Aperçu général ACL Linux

**Guides :**
- [Red Hat ACL Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-access_control_lists)
- [Linux ACL Tutorial](https://www.redhat.com/sysadmin/linux-access-control-lists)

**Filesystem support :**
- ext4 : ✅ ACL supportées
- xfs : ✅ ACL supportées
- btrfs : ✅ ACL supportées
- vfat/FAT32 : ❌ Pas d'ACL
- NFS : ✅ ACL supportées (si NFSv4)

---

## 🎓 Commandes à Retenir

```bash
# Définir ACL user
setfacl -m u:username:rwx fichier

# Définir ACL group
setfacl -m g:groupname:rx fichier

# Bloquer user (aucune permission)
setfacl -m u:username:0 fichier

# Supprimer ACL entry
setfacl -x u:username fichier

# Supprimer TOUTES ACL
setfacl -b fichier

# Lire ACL
getfacl fichier

# ACL récursive
setfacl -R -m u:user:rx /directory

# ACL par défaut (héritage)
setfacl -d -m u:user:rw /directory

# Backup ACL
getfacl -R /data > acl-backup.txt

# Restore ACL
setfacl --restore=acl-backup.txt
```

---

**Tags :** #Linux #ACL #Permissions #Security #AccessControl #FileManagement #KodeKloud

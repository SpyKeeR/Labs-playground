# Challenge 03 : Linux Collaborative Directories

**Date** : 8 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Créer un répertoire collaboratif avec permissions SGID pour que les fichiers créés héritent automatiquement du groupe propriétaire.

---

## 📋 Énoncé

L'équipe Nautilus ne veut pas que ses données soient accessibles par d'autres groupes/équipes pour raisons de sécurité. Les données doivent être strictement accessibles par le groupe sysadmin.

**Tâche** : 
- Créer répertoire collaboratif `/sysadmin/data` sur app server 2 (Stratos Datacenter)
- Groupe propriétaire : `sysadmin`
- Fichiers créés dans répertoire doivent appartenir au groupe `sysadmin`
- Permissions : read/write/execute pour user et group owners, aucun accès pour others

**Serveur cible** : `steve@stapp02`

---

## ✅ Résolution

### 1. Se connecter au serveur

```bash
ssh steve@stapp02
```

### 2. Créer la structure de répertoires

```bash
sudo mkdir -p /sysadmin/data
```

**Explication** :
- `mkdir -p` : Crée répertoires parents si nécessaires (`/sysadmin` puis `/sysadmin/data`)

### 3. Changer groupe propriétaire

```bash
sudo chgrp -R sysadmin /sysadmin
```

**Explication** :
- `chgrp` : Change group ownership
- `-R` : Récursif (applique à `/sysadmin` et sous-répertoires)
- `sysadmin` : Nom du groupe propriétaire

### 4. Configurer permissions avec SGID

```bash
sudo chmod -R 2770 /sysadmin
```

**Explication** :
- `2770` décomposé :
  - `2` : SGID bit (Set Group ID)
  - `7` : User permissions (rwx = 4+2+1)
  - `7` : Group permissions (rwx = 4+2+1)
  - `0` : Others permissions (aucun accès)
- `-R` : Récursif
- **SGID** : Force fichiers créés à hériter du groupe du répertoire parent

**Alternative syntaxe symbolique** :
```bash
sudo chmod -R g+rwxs,u+rwx,o-rwx /sysadmin
```

### 5. Validation

Vérifier permissions et groupe :

```bash
sudo ls -ld /sysadmin /sysadmin/data
```

**Sortie attendue** :
```
drwxrws--- 3 root sysadmin 4096 Jan  8 10:30 /sysadmin
drwxrws--- 2 root sysadmin 4096 Jan  8 10:30 /sysadmin/data
```

**Indicateurs** :
- `d` : Répertoire
- `rwxrws---` : User (rwx), Group (rws), Others (---)
- `s` dans groupe : SGID bit actif
- `sysadmin` : Groupe propriétaire

**Test création fichier** :
```bash
sudo touch /sysadmin/data/testfile
sudo ls -l /sysadmin/data/testfile
```

**Résultat attendu** : Fichier appartient au groupe `sysadmin` automatiquement.

---

## 💡 Notes

- **SGID (Set Group ID)** : Bit spécial (`chmod g+s` ou `2xxx`) forçant fichiers créés à hériter groupe du répertoire parent
- **Collaborative Directory** : Répertoire partagé où plusieurs utilisateurs (même groupe) collaborent
- **Permissions 2770** : User+Group full access (rwx), Others aucun accès, SGID actif
- **Use case** : Projets d'équipe, partage documents, répertoires partagés développeurs

---

## 🏷️ Tags

`#Linux` `#Permissions` `#SGID` `#CollaborativeDirectories` `#chgrp` `#chmod` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

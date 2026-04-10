# Challenge 09 : Configure Local Yum Repos

**Date** : 9 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Configurer un repository yum local pour maintenir packages sur serveur sans dépendre de repos externes.

---

## 📋 Énoncé

L'équipe support production Nautilus et équipe sécurité ont eu réunion le mois dernier où ils ont décidé d'utiliser repositories yum locaux pour maintenir packages nécessaires sur leurs serveurs. Pour l'instant, ils ont décidé de configurer repo yum local sur Nautilus Backup Server.

**Tâches** :

**a.** Des packages sont déjà présents dans `/packages/downloaded_rpms/` sur Nautilus Backup Server

**b.** Créer repo yum nommé `epel_local` avec Repository ID `epel_local`. Configurer pour utiliser emplacement packages `/packages/downloaded_rpms/`

**c.** Installer package `wget` depuis ce nouveau repo

**Serveur cible** : `clint@stbkp01`

---

## ✅ Résolution

### 1. Se connecter au serveur

```bash
ssh clint@stbkp01
```

### 2. Créer metadata repository

```bash
sudo createrepo /packages/downloaded_rpms/
```

**Explication** :
- `createrepo` : Génère metadata XML pour répertoire RPM packages
- Crée fichier `repodata/repomd.xml` (index packages)
- Requis pour que yum reconnaisse répertoire comme repo

### 3. Configurer repository yum

```bash
sudo vi /etc/yum.repos.d/epel_local.repo
```

**Contenu fichier** :
```ini
[epel_local]
name=epel_local
baseurl=file:///packages/downloaded_rpms/
gpgcheck=0
enabled=1
```

**Explication champs** :
- `[epel_local]` : Repository ID (bracket)
- `name=epel_local` : Nom descriptif repo
- `baseurl=file:///packages/downloaded_rpms/` : URL repo (file:// = local)
- `gpgcheck=0` : Désactiver vérification signature GPG (packages locaux)
- `enabled=1` : Activer repo (0 = désactivé)

**Note** : `file:///` = 3 slashes (protocole file + absolute path `/packages/...`)

### 4. Reconstruire cache yum

```bash
sudo yum makecache
```

**Explication** : Télécharge metadata tous les repos activés et crée cache local.

### 5. Installer package depuis repo local

```bash
sudo yum install wget
```

**Yum résout automatiquement depuis `epel_local` si package présent.**

### 6. Validation

```bash
wget --help
```

**Sortie attendue** : Usage wget affiché → installation réussie.

**Vérifier provenance package** :
```bash
yum info wget
```

**Sortie attendue** :
```
Name        : wget
...
Repository  : epel_local
```

---

## 💡 Notes

- **createrepo** : Génère metadata repository (requis pour yum)
- **/etc/yum.repos.d/** : Répertoire configuration repositories yum
- **file:/// protocol** : Repository local (3 slashes)
- **gpgcheck=0** : Désactiver vérification GPG (repos locaux trustés)

---

## 🏷️ Tags

`#Linux` `#yum` `#createrepo` `#PackageManagement` `#LocalRepo` `#RHEL` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

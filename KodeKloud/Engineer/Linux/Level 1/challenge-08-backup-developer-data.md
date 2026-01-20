# Challenge 8 : Backup Developer Data

**Date :** 5 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Archivage et compression  
**Difficulté :** Débutant  
**Durée :** ~10 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Créer une archive compressée des données d'un développeur et la déplacer vers un emplacement de sauvegarde spécifique.

---

## 📋 Énoncé

Dans le Stratos DC, le serveur de stockage Nautilus héberge un répertoire nommé `/data`, servant de dépôt pour diverses données non-confidentielles des développeurs.

La développeuse **anita** a demandé une copie de ses données stockées dans `/data/anita`. L'équipe System Admin doit suivre ces étapes :

**Tâches :**
1. Créer une archive compressée nommée `anita.tar.gz` du répertoire `/data/anita`
2. Transférer l'archive vers le répertoire `/home` sur le Storage Server

**Serveur cible :** Storage Server (natasha@ststor01)

---

## 🔧 Résolution

### Étape 1 : Connexion au Storage Server

```bash
ssh natasha@ststor01
```

---

### Étape 2 : Navigation vers répertoire source

```bash
cd /data/
```

**Explication :** Se placer dans le répertoire parent pour faciliter l'archivage avec chemins relatifs.

---

### Étape 3 : Créer archive compressée

```bash
sudo tar cvzf /home/anita.tar.gz ./anita/
```

**Explication détaillée :**
- `sudo` : **Permissions élevées nécessaires** (lecture `/data/anita` + écriture `/home`)
- `tar` : Commande archivage
- `c` : **Create** (créer nouvelle archive)
- `v` : **Verbose** (afficher fichiers archivés - optionnel mais utile)
- `z` : **gZip** (compresser avec gzip → extension `.tar.gz`)
- `f` : **File** (spécifier nom fichier archive)
- `/home/anita.tar.gz` : Chemin destination archive
- `./anita/` : Répertoire source (chemin relatif depuis `/data/`)

**Ordre options important :** `f` doit être **avant** le nom fichier.

---

### Étape 4 : Validation

```bash
# Vérifier archive créée
ls -lh /home/anita.tar.gz

# Lister contenu archive (sans extraire)
tar tvf /home/anita.tar.gz
```

**Options `tar tvf` :**
- `t` : **Test/List** (lister contenu)
- `v` : **Verbose** (détails permissions, dates)
- `f` : **File** (fichier archive à lister)

**Résultat attendu :**
```
-rw-r--r-- 1 root root 2.3M Jan 5 16:30 /home/anita.tar.gz

# Contenu :
drwxr-xr-x anita/anita       0 2026-01-05 10:00 anita/
-rw-r--r-- anita/anita    1234 2026-01-05 09:30 anita/file1.txt
-rw-r--r-- anita/anita    5678 2026-01-05 09:45 anita/file2.log
...
```

---

## 🔗 Ressources

**Documentation :**
- `man tar` : Manuel complet
- `info tar` : Documentation GNU détaillée

**Guides compression :**
- [GNU Tar Manual](https://www.gnu.org/software/tar/manual/)
- [Linux Backup Best Practices](https://www.redhat.com/sysadmin/linux-backup-solutions)

**Outils alternatifs :**
- `zip/unzip` : Compatible Windows (mais moins performant)
- `7z` : Compression excellente (multi-plateforme)
- `rsync` : Synchronisation incrémentale (meilleur que tar pour backups)

---

## 🎓 Commandes à Retenir

```bash
# Créer archive compressée
tar czf archive.tar.gz /path/to/dir

# Créer avec chemins relatifs (SAFE)
cd /parent && tar czf backup.tar.gz ./subdir/

# Extraire archive
tar xzf archive.tar.gz

# Extraire dans répertoire spécifique
tar xzf archive.tar.gz -C /destination/

# Lister contenu sans extraire
tar tzf archive.tar.gz

# Préserver permissions à l'extraction
sudo tar xzpf archive.tar.gz

# Exclure fichiers
tar czf backup.tar.gz --exclude='*.log' --exclude='tmp/*' /data/

# Vérifier intégrité
tar tzf archive.tar.gz > /dev/null && echo "OK" || echo "CORRUPTED"
```

---

**Tags :** #Linux #Backup #Tar #Compression #DataManagement #Archiving #KodeKloud

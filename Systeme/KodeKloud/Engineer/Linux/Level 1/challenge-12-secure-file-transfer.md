# KodeKloud Engineer - Challenge 12 : Secure File Transfer

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - File Transfer & SSH  
**Difficulté :** Easy  
**Durée :** ~10 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Transférer de manière sécurisée un fichier confidentiel entre serveurs en utilisant les protocoles SSH.

---

## 📋 Énoncé

**Contexte :** Un développeur Nautilus a stocké des données confidentielles sur le jump host. Pour assurer sécurité et conformité, ces données doivent être transférées vers un app server. Les développeurs n'ayant pas accès direct aux serveurs, l'équipe système administre le transfert.

**Mission :** Copier le fichier `/tmp/nautilus.txt.gpg` du jump server vers App Server 1, en le plaçant dans le répertoire `/home/web`.

**Contraintes :**
- **Source** : `/tmp/nautilus.txt.gpg` (jump host)
- **Destination** : `tony@stapp01:/home/web/`
- Transfert sécurisé (SSH)

---

## 🔧 Résolution

### Étape 1 : Vérifier fichier source existe

```bash
ls -lh /tmp/nautilus.txt.gpg
```

**Résultat attendu :**
```
-rw-r--r-- 1 user user 1.2K Jan  6 09:15 /tmp/nautilus.txt.gpg
```

**⚠️ Note fichier GPG :** Extension `.gpg` = fichier chiffré (GNU Privacy Guard).

---

### Étape 2 : Transférer avec scp (Secure Copy)

```bash
scp /tmp/nautilus.txt.gpg tony@stapp01:/home/web/
```

**Décomposition commande :**
- `scp` : **S**ecure **C**o**P**y (via SSH)
- `/tmp/nautilus.txt.gpg` : Fichier source (chemin local)
- `tony@stapp01` : User@host destination
- `:/home/web/` : Répertoire destination

**Output attendu :**
```
nautilus.txt.gpg                     100% 1234     1.2MB/s   00:00
```

**⚠️ Si demande password :** Entrer password user `tony`.

---

### Étape 3 : Vérifier transfert réussi

**Connexion serveur destination :**
```bash
ssh tony@stapp01
```

**Vérifier fichier présent :**
```bash
ls -lh /home/web/
```

**Résultat attendu :**
```
total 4.0K
-rw-r--r-- 1 tony tony 1.2K Jan  6 09:16 nautilus.txt.gpg
```

**Vérifier intégrité (optionnel) :**
```bash
# Sur jump host (source)
md5sum /tmp/nautilus.txt.gpg
# 5d41402abc4b2a76b9719d911017c592  /tmp/nautilus.txt.gpg

# Sur stapp01 (destination)
md5sum /home/web/nautilus.txt.gpg
# 5d41402abc4b2a76b9719d911017c592  /home/web/nautilus.txt.gpg
```

**✅ Hashes identiques** = transfert intègre (pas corruption).

---

**Tags :** #Linux #scp #SSH #FileTransfer #Security #KodeKloud

---

## 🎓 Commandes à Retenir

```bash
# Local → Remote (fichier)
scp /local/file.txt user@remote:/path/

# Local → Remote (répertoire)
scp -r /local/dir user@remote:/path/

# Remote → Local
scp user@remote:/remote/file.txt /local/path/

# Préserver timestamps/permissions
scp -p file.txt user@remote:/path/

# Compression (fichiers gros)
scp -C largefile.tar user@remote:/path/

# Port custom
scp -P 2222 file.txt user@remote:/path/

# Clé SSH custom
scp -i ~/.ssh/custom_key file.txt user@remote:/path/

# Vérifier intégrité
md5sum /local/file.txt
ssh user@remote "md5sum /remote/file.txt"

# Rsync (delta transfer, backups)
rsync -avz /local/dir/ user@remote:/remote/dir/

# Rsync avec suppression (mirror exact)
rsync -avz --delete /local/dir/ user@remote:/remote/dir/
```

---

**Tags :** #Linux #scp #SSH #FileTransfer #rsync #Security #KodeKloud #RemoteAccess

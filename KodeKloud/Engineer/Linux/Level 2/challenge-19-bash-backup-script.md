# Challenge 19 : Linux Bash Script

**Date** : 16 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Créer script Bash automatisation backup website statique avec archive ZIP + copie vers serveur backup distant (sans demander password).

---

## 📋 Énoncé

L'équipe de support production de xFusionCorp Industries travaille sur le développement de scripts bash pour automatiser différentes tâches quotidiennes. L'une d'elles consiste à créer un script bash pour effectuer des sauvegardes de sites web. Ils ont un site web statique fonctionnant sur App Server 2 dans le Stratos Datacenter.

**Exigences** : Créer un script `news_backup.sh` (placer dans `/scripts/` sur App Server 2) :

a. Créer une archive zip nommée `xfusioncorp_news.zip` du répertoire `/var/www/html/news`
b. Sauvegarder l'archive dans `/backup/` sur App Server 2 (stockage temporaire)
c. Copier l'archive créée vers Nautilus Backup Server dans l'emplacement `/backup/`
d. Le script ne doit PAS demander de mot de passe lors de la copie du fichier d'archive
e. L'utilisateur serveur (steve pour App Server 2) doit pouvoir exécuter le script
f. Ne PAS utiliser sudo à l'intérieur du script

**Note** : Installer le package `zip` manuellement AVANT d'exécuter le script.

**Serveurs** :
- **App Server 2** : user `steve`
- **Nautilus Backup Server** : `stbkp01`, user `clint`

---

## 🔧 Résolution

### Étape 1 : Connexion App Server 2

```bash
ssh steve@stapp02
```

### Étape 2 : Créer script backup

```bash
vi /scripts/news_backup.sh
```

**Contenu script** :

```bash
#!/bin/bash

# Variables
target='/var/www/html/news'
archivefile='/backup/xfusioncorp_news.zip'

# Créer archive ZIP
zip -r $archivefile $target

# Copier vers serveur backup distant
scp $archivefile clint@stbkp01:/backup/
```

**Explications lignes** :
- `#!/bin/bash` : Shebang (interpreter Bash)
- `target` : Répertoire source à archiver
- `archivefile` : Chemin archive ZIP créée
- `zip -r` : Créer archive récursive (inclut sous-dossiers)
- `scp` : Secure Copy vers serveur distant (SSH)

### Étape 3 : Rendre script exécutable

```bash
chmod +x /scripts/news_backup.sh
```

### Étape 4 : Configurer SSH sans password (App Server 2 → Backup Server)

**Générer clé SSH user steve** :
```bash
ssh-keygen
# Appuyer Enter (pas passphrase, défauts OK)
```

**Output** :
```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/steve/.ssh/id_rsa): [Enter]
Enter passphrase (empty for no passphrase): [Enter]
Enter same passphrase again: [Enter]
Your identification has been saved in /home/steve/.ssh/id_rsa.
Your public key has been saved in /home/steve/.ssh/id_rsa.pub.
```

**Copier clé publique vers serveur backup** :
```bash
ssh-copy-id clint@stbkp01
```

**Prompt** : Demande password user `clint` (1x uniquement).

**Output** :
```
Number of key(s) added: 1

Now try logging into the machine, with: "ssh 'clint@stbkp01'"
and check to make sure that only the key(s) you wanted were added.
```

**Test connexion sans password** :
```bash
ssh clint@stbkp01
# Connexion directe SANS demander password ✅
exit
```

### Étape 5 : Répéter pour autres App Servers (consigne implicite)

**App Server 1 (user tony)** :
```bash
ssh tony@stapp01
ssh-keygen
ssh-copy-id clint@stbkp01
```

**App Server 3 (user banner)** :
```bash
ssh banner@stapp03
ssh-keygen
ssh-copy-id clint@stbkp01
```

**Raison** : Tous app servers doivent pouvoir copier backups vers `stbkp01` sans password.

### Étape 6 : Exécuter script backup

Retourner App Server 2 :
```bash
ssh steve@stapp02
/scripts/news_backup.sh
```

**Output attendu** :
```
  adding: var/www/html/news/ (stored 0%)
  adding: var/www/html/news/index.html (deflated 45%)
  ...
xfusioncorp_news.zip      100%  1234KB   5.2MB/s   00:00
```

### Étape 7 : Validation

Vérifier archive locale :
```bash
ls -lh /backup/xfusioncorp_news.zip
```

Vérifier copie serveur backup :
```bash
ssh clint@stbkp01 "ls -lh /backup/xfusioncorp_news.zip"
```

---

## 📌 Commandes utiles

```bash
# Zip archives
zip archive.zip file1 file2              # Archiver fichiers spécifiques
zip -r archive.zip directory/            # Archiver répertoire récursif
zip -r -9 archive.zip directory/         # Compression max (level 9)
unzip archive.zip                        # Extraire archive
unzip -l archive.zip                     # Lister contenu (pas extraire)

# SSH keys management
ssh-keygen                               # Générer paire clés SSH (RSA défaut)
ssh-keygen -t ed25519                    # Générer clé ED25519 (plus moderne)
ssh-copy-id user@host                    # Copier clé publique vers serveur distant
ssh-add ~/.ssh/id_rsa                    # Ajouter clé à ssh-agent (si passphrase)

# Voir clés SSH
ls -la ~/.ssh/
cat ~/.ssh/id_rsa.pub                    # Clé publique (copier vers serveurs)
cat ~/.ssh/id_rsa                        # Clé privée (GARDER SECRÈTE)

# Tester connexion SSH
ssh -v user@host                         # Verbose (debug connexion)
ssh -i ~/.ssh/custom_key user@host       # Utiliser clé spécifique

# SCP (Secure Copy)
scp file.txt user@host:/path/            # Copier fichier local → distant
scp user@host:/path/file.txt .           # Copier fichier distant → local
scp -r directory/ user@host:/path/       # Copier répertoire récursif
scp -P 2222 file.txt user@host:/path/    # Port SSH custom

# Bash script testing
bash -x script.sh                        # Debug mode (affiche commandes exécutées)
bash -n script.sh                        # Syntax check (pas exécution)
chmod +x script.sh                       # Rendre exécutable
./script.sh                              # Exécuter script (doit être +x)
bash script.sh                           # Exécuter via bash (pas besoin +x)
```

---

## 💡 Points clés

**SSH key authentication (passwordless)** :
- **Clé privée** (`~/.ssh/id_rsa`) : SECRÈTE, reste client (jamais copier)
- **Clé publique** (`~/.ssh/id_rsa.pub`) : Copier vers serveurs distants
- **authorized_keys** : Serveur distant stocke clés publiques autorisées (`~/.ssh/authorized_keys`)
- **Workflow** : Client envoie signature clé privée → Serveur vérifie avec clé publique

**ssh-copy-id workflow** :
```bash
ssh-copy-id user@host
# 1. Demande password user@host (1x uniquement)
# 2. Copie ~/.ssh/id_rsa.pub → /home/user/.ssh/authorized_keys (serveur distant)
# 3. Connexions futures : SSH key auth (pas password)
```

**Zip vs tar** :
| Commande | Compression | Use case | Compatibilité |
|----------|-------------|----------|---------------|
| `zip` | Oui (deflate) | Archives Windows-compatible | ✅ Windows + Linux |
| `tar` | Non (tar seul) | Archives Unix | ✅ Linux (⚠️ Windows nécessite 7-Zip) |
| `tar.gz` | Oui (gzip) | Backups Linux standard | ✅ Linux, ⚠️ Windows tools |

**SCP vs rsync** :
- **scp** : Simple copy (1x, full transfer)
- **rsync** : Sync incremental (delta transfer, faster updates)
  ```bash
  rsync -avz /local/path/ user@host:/remote/path/
  # -a = archive mode, -v = verbose, -z = compression
  ```

**Bash script best practices** :
- Shebang : `#!/bin/bash` (ligne 1)
- `set -e` : Exit si commande échoue (fail-fast)
- Variables UPPERCASE : Convention (lisibilité)
- Quotes `"$var"` : Éviter word splitting
- Functions : Modularité (debugging facile)
- Logging : `echo "[$(date)] message"`
- Error handling : `if [ $? -ne 0 ]; then ... fi`

---

**Tags** : `Bash` `scripting` `backup` `automation` `ssh-keys` `ssh-copy-id` `scp` `zip` `passwordless-ssh` `Level 2`

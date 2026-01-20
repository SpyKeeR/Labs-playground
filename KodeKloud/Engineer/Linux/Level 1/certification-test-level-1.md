# Certification Test - System Administrator I (Niveau 1)

**Date** : 7 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Parcours** : Linux  
**Résultat** : ✅ 100% (10/10 tâches validées)

---

## 🎯 Objectif

Valider les compétences de base en administration système Linux (gestion utilisateurs, transferts fichiers, sécurité SSH, ACL, manipulation fichiers, archives, packages, limites ressources).

---

## 📋 Tâches du test

### Tâche 1/10 : Création utilisateur non-interactif (Weight: 8)

**Énoncé** : Créer un utilisateur `eric` avec un shell non-interactif sur App Server 2.

**Résolution** :

```bash
ssh steve@stapp02
sudo useradd -m -s /sbin/nologin eric
```

**Explication** :
- `-m` : Créer le répertoire home (`/home/eric`)
- `-s /sbin/nologin` : Shell non-interactif (empêche login direct, utile pour services/daemons)

---

### Tâche 2/10 : Transfert fichier sécurisé (Weight: 8)

**Énoncé** : Copier `/tmp/nautilus.txt.gpg` du jump host vers App Server 2 (`/home/appdata`).

**Résolution** :

```bash
scp /tmp/nautilus.txt.gpg steve@stapp02:/home/appdata
```

**Explication** : `scp` (Secure Copy Protocol) utilise SSH pour transférer des fichiers de manière chiffrée entre machines.

---

### Tâche 3/10 : Désactiver login root SSH (Weight: 8)

**Énoncé** : Désactiver le login SSH root direct sur tous les serveurs applicatifs (stapp01, stapp02, stapp03).

**Résolution** :

```bash
# App Server 1
ssh tony@stapp01
sudo vi /etc/ssh/sshd_config
# Remplacer : PermitRootLogin yes → PermitRootLogin no
sudo systemctl restart sshd

# App Server 2
ssh steve@stapp02
sudo vi /etc/ssh/sshd_config
# Remplacer : PermitRootLogin yes → PermitRootLogin no
sudo systemctl restart sshd

# App Server 3
ssh banner@stapp03
sudo vi /etc/ssh/sshd_config
# Remplacer : PermitRootLogin yes → PermitRootLogin no
sudo systemctl restart sshd
```

**Explication** :
- `PermitRootLogin no` : Empêche connexion SSH directe avec compte root (bonnes pratiques sécurité)
- `systemctl restart sshd` : Redémarrage service SSH pour appliquer configuration

---

### Tâche 4/10 : Configuration ACL fichier (Weight: 12)

**Énoncé** : Configurer les ACL (Access Control Lists) sur `/etc/hosts` (App Server 2) :
- User `virat` : Aucun accès
- User `vivek` : Lecture seule
- Group `sysadmin` : Lecture/écriture

**Résolution** :

```bash
ssh steve@stapp02

# Créer utilisateurs et groupe
sudo useradd -s /sbin/nologin virat
sudo useradd -s /sbin/nologin vivek
sudo groupadd sysadmin

# Configurer ACL
sudo setfacl -m u:vivek:r /etc/hosts
sudo setfacl -m u:virat:0 /etc/hosts
sudo setfacl -m g:sysadmin:rw /etc/hosts

# Vérification
getfacl /etc/hosts
```

**Explication** :
- `setfacl -m` : Modifier ACL (`u:` user, `g:` group)
- Permissions : `r` (read), `w` (write), `0` (aucun accès)
- `getfacl` : Afficher ACL configurées sur fichier

---

### Tâche 5/10 : Création fichier HTML (Weight: 8)

**Énoncé** : Créer `/var/www/html/index.html` sur App Server 2 avec le contenu `Welcome to the KKE labs!`.

**Résolution** :

```bash
ssh steve@stapp02
sudo vi /var/www/html/index.html
```

Contenu :
```html
Welcome to the KKE labs!
```

**Explication** : `/var/www/html/` est le répertoire racine par défaut des serveurs web Apache/Nginx sur RHEL/CentOS.

---

### Tâche 6/10 : Création archives tar (Weight: 14)

**Énoncé** : Sur le serveur de stockage, créer deux archives du répertoire `/var/log/` :
- `logs.tar` (archive non compressée)
- `logs.tar.gz` (archive compressée gzip)

**Résolution** :

```bash
ssh natasha@ststor01
cd /var/log
sudo tar cvf /home/natasha/logs.tar .
sudo tar cvzf /home/natasha/logs.tar.gz .
```

**Explication** :
- `tar cvf` : Créer archive (`c`), verbose (`v`), fichier (`f`)
- `tar cvzf` : Idem + compression gzip (`z`)
- `.` : Archiver contenu du répertoire courant

---

### Tâche 7/10 : Manipulation texte avec vim (Weight: 14)

**Énoncé** : Modifier `/home/BSD.txt` sur App Server 2 :
- Supprimer toutes les lignes contenant le mot `following` → sauvegarder dans `/home/BSD_DELETE.txt`
- Remplacer toutes les occurrences du mot `and` (exact match) par `them` → sauvegarder dans `/home/BSD_REPLACE.txt`

**Résolution** :

```bash
ssh steve@stapp02
sudo yum install vim

# Copier fichier source
sudo cp /home/BSD.txt /home/BSD_DELETE.txt
sudo cp /home/BSD.txt /home/BSD_REPLACE.txt

# Suppression lignes
sudo vim /home/BSD_DELETE.txt
:g/\<following\>/d
:wq!

# Remplacement mot
sudo vim /home/BSD_REPLACE.txt
:%s/\<and\>/them/g
:wq!
```

**Explication** :
- `:g/\<following\>/d` : Commande globale (`g`) supprimant lignes contenant mot exact `following` (`\<` `\>` = word boundaries)
- `:%s/\<and\>/them/g` : Substitution globale (`%s`) du mot exact `and` par `them` (flag `g` = toutes occurrences)

---

### Tâche 8/10 : Installation package Samba (Weight: 8)

**Énoncé** : Installer le package `samba` sur tous les serveurs applicatifs.

**Résolution** :

```bash
# App Server 1
ssh tony@stapp01
sudo yum install samba

# App Server 2
ssh steve@stapp02
sudo yum install samba

# App Server 3
ssh banner@stapp03
sudo yum install samba
```

**Explication** : Samba permet le partage de fichiers/imprimantes entre Linux et Windows (protocole SMB/CIFS).

---

### Tâche 9/10 : Limites processus utilisateur (Weight: 12)

**Énoncé** : Sur le serveur de stockage, limiter le nombre de processus de l'utilisateur `nfsuser` :
- Soft limit : 1026
- Hard limit : 2026

**Résolution** :

```bash
ssh natasha@ststor01
sudo vi /etc/security/limits.conf
```

Ajouter :
```
nfsuser soft nproc 1026
nfsuser hard nproc 2026
```

**Explication** :
- **Soft limit** : Limite par défaut (modifiable par user jusqu'à hard)
- **Hard limit** : Limite absolue (seul root peut augmenter)
- Application : Prochaine connexion utilisateur (logout/login requis)

---

### Tâche 10/10 : Installation et activation service Bind (Weight: 6)

**Énoncé** : Installer le package `bind` sur tous les serveurs applicatifs et démarrer/activer son service.

**Résolution** :

```bash
# App Server 1
ssh tony@stapp01
sudo yum install bind -y
sudo systemctl enable --now named

# App Server 2
ssh steve@stapp02
sudo yum install bind -y
sudo systemctl enable --now named

# App Server 3
ssh banner@stapp03
sudo yum install bind -y
sudo systemctl enable --now named
```

**Explication** :
- `bind` : Serveur DNS (Berkeley Internet Name Domain)
- `named` : Nom du service bind
- `enable --now` : Activer au boot + démarrer immédiatement

---

## ✅ Validation

**Résultat final** : ✅ **100%** (10/10 tâches validées)

**Certification obtenue** : System Administrator I - Linux Engineer (Niveau 1)

---

## 📌 Commandes clés à retenir

| Commande | Usage |
|----------|-------|
| `useradd -m -s /sbin/nologin USER` | Créer utilisateur sans shell interactif |
| `scp SOURCE USER@HOST:DEST` | Transfert fichier sécurisé SSH |
| `setfacl -m u:USER:PERMS FILE` | Définir ACL utilisateur sur fichier |
| `setfacl -m g:GROUP:PERMS FILE` | Définir ACL groupe sur fichier |
| `tar cvf archive.tar DIR` | Créer archive tar non compressée |
| `tar cvzf archive.tar.gz DIR` | Créer archive tar compressée gzip |
| `vim :g/PATTERN/d` | Supprimer lignes matchant pattern |
| `vim :%s/WORD/REPLACE/g` | Remplacer mot (exact match) globalement |
| `systemctl enable --now SERVICE` | Activer + démarrer service |

---

## 🏷️ Tags

`#Linux` `#Certification` `#UserManagement` `#SSH` `#ACL` `#tar` `#vim` `#SELinux` `#SystemAdmin` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

# Challenge 4 : Service Account Without Home Directory

**Date :** Janvier 2026 (antérieur au 5 janvier)  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Comptes système et optimisation  
**Difficulté :** Débutant  
**Durée :** ~8 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Créer un compte utilisateur service sans répertoire personnel pour optimiser l'espace disque et renforcer la sécurité des comptes système.

---

## 📋 Énoncé

L'équipe d'administration système de **xFusionCorp Industries** a déployé un nouvel outil sur tous les serveurs App.

Cet outil nécessite la création d'un **compte utilisateur service** dédié.

**Tâche à réaliser :**
- Créer un utilisateur nommé `anita` sur **App Server 2** **sans répertoire personnel**

**Serveur cible :** `stapp02` (steve@172.16.238.11)

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur cible

```bash
ssh steve@172.16.238.11
```

---

### Étape 2 : Créer l'utilisateur sans home directory

```bash
sudo useradd --no-create-home anita
```

**Explication détaillée :**
- `useradd` : commande création utilisateur
- `--no-create-home` : ne PAS créer `/home/anita` (équivalent `-M`)
- `anita` : nom utilisateur

**Résultat :**
- Utilisateur existe dans `/etc/passwd`
- **Pas de répertoire** `/home/anita` créé
- Processus peuvent tourner sous cet user
- Home directory dans `/etc/passwd` existe (par défaut `/home/anita`) mais répertoire physique NON créé

---

### Étape 3 : Validation

```bash
# Vérifier user créé
id anita

# Vérifier entrée /etc/passwd
grep "anita:" /etc/passwd

# Vérifier répertoire personnel N'EXISTE PAS
ls -ld /home/anita
```

**Résultat attendu :**
```
uid=1002(anita) gid=1002(anita) groups=1002(anita)
```

**Ligne /etc/passwd :**
```
anita:x:1002:1002::/home/anita:/bin/bash
                     └─ Chemin défini mais répertoire NON créé
```

**Vérification répertoire :**
```
ls: cannot access '/home/anita': No such file or directory
```

---

### Étape 4 : Vérifier processus peut tourner sous anita

```bash
# Exécuter commande simple sous user anita
sudo su -s /bin/bash anita -c "echo 'Process OK' && whoami"
```

**Résultat attendu :**
```
Process OK
anita
```

**Note :** Processus fonctionne malgré absence home directory.

---

## 🔗 Ressources

**Documentation :**
- `man useradd` : options création utilisateurs
- `man usermod` : modification utilisateurs
- `man userdel` : suppression utilisateurs

**Fichiers système :**
- `/etc/login.defs` : defaults création users (CREATE_HOME, UID ranges, etc.)
- `/etc/default/useradd` : defaults useradd
- `/etc/skel/` : squelette home directory (copié si -m)

**Standards sécurité :**
- [CIS Benchmark Linux](https://www.cisecurity.org/benchmark/debian_linux) - Section 5 (User Accounts)
- [NIST Guidelines](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-123.pdf) - System Accounts

---

## 🎓 Commandes à Retenir

```bash
# Créer user SANS home directory
sudo useradd --no-create-home username
sudo useradd -M username  # Équivalent court

# Créer user système complet
sudo useradd --system -M -s /bin/false servicename

# Vérifier home existe
ls -ld /home/username

# Lister users SANS home existant
awk -F: '{print $1, $6}' /etc/passwd | while read u h; do [ ! -d "$h" ] && echo "$u"; done

# Créer home pour user existant
sudo mkdir /home/username
sudo chown username:username /home/username
sudo cp -r /etc/skel/. /home/username/

# Supprimer user + home (si existe)
sudo userdel --remove username
```

---

**Tags :** #Linux #SystemAccounts #UserManagement #DiskOptimization #Security #KodeKloud

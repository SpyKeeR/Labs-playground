# Challenge 18 : MariaDB Troubleshooting

**Date** : 16 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Résoudre problème service MariaDB down empêchant application Nautilus de se connecter à la base de données (Stratos Datacenter).

---

## 📋 Énoncé
Un problème critique affecte l'application Nautilus dans le Stratos DC. L'équipe de support production a identifié que l'application ne peut pas se connecter à la base de données. Après investigation, l'équipe a découvert que le service mariadb est arrêté sur le serveur de base de données.

**Exigences** :
- Analyser le problème
- Corriger le service mariadb
- S'assurer que le service fonctionne

**Serveur** : Database server (Stratos DC)

---

## 🔧 Résolution

### Étape 1 : Tentative démarrage MariaDB

```bash
sudo systemctl start mariadb
```

**Résultat** : Service échoue au démarrage.

### Étape 2 : Diagnostic erreur

```bash
systemctl status mariadb.service
```

**Output erreur identifiée** :
```
Jan 16 17:31:06 stdb01.stratos.xfusioncorp.com mariadb-prepare-db-dir[2181]: Database MariaDB is not initialized, but the directory /var/lib/mysql is not empty, so initialization cannot be done.
Jan 16 17:31:06 stdb01.stratos.xfusioncorp.com mariadb-prepare-db-dir[2181]: Make sure the /var/lib/mysql is empty before running mariadb-prepare-db-dir.
```

**Analyse** :
- MariaDB cherche datadir `/var/lib/mysql`
- Directory `/var/lib/mysql` NOT EMPTY mais database pas initialisée
- Contradiction bloque initialization

### Étape 3 : Vérifier filesystem datadir

```bash
ls /var/lib
```

**Output** : Présence répertoire `mysqld` au lieu de `mysql`.

**Root cause identifiée** :
- Config MariaDB pointe `/var/lib/mysql` (défaut)
- Data réellement dans `/var/lib/mysqld` (non-standard)
- Mismatch chemins → MariaDB refuse démarrer

### Étape 4 : Vérifier configuration MariaDB

```bash
sudo vi /etc/my.cnf.d/mariadb-server.cnf
```

**Configuration actuelle (INCORRECTE)** :
```ini
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
```

### Étape 5 : Corriger configuration datadir

Modifier chemins pour pointer vers répertoire réel `/var/lib/mysqld` :

```ini
[mysqld]
datadir=/var/lib/mysqld
socket=/var/lib/mysqld/mysql.sock
```

**Explication** :
- `datadir` : Emplacement fichiers database MariaDB (ibdata, databases/, tables)
- `socket` : Socket UNIX connexions locales (clients MySQL CLI)
- Les 2 doivent pointer vers répertoire contenant data réelle

### Étape 6 : Démarrer MariaDB

```bash
sudo systemctl start mariadb
```

### Étape 7 : Validation

Vérifier statut service :
```bash
sudo systemctl status mariadb
```

**Output attendu** : `active (running)` - Pas d'erreurs.

**Test connexion** (optionnel) :
```bash
mysql -u root -p
# Connexion DB réussie
```

---

## 📌 Commandes utiles

```bash
# Vérifier configuration MariaDB active
mysqld --help --verbose | grep datadir
mysqld --help --verbose | grep socket

# Voir config files MariaDB
mysql --help | grep "Default options"
# Ordre lecture : /etc/my.cnf → /etc/my.cnf.d/*.cnf → ~/.my.cnf

# Lister fichiers config MariaDB
ls -la /etc/my.cnf.d/

# Vérifier datadir existe + permissions
ls -ld /var/lib/mysqld
# Doit être owned par mysql:mysql

# Vérifier contenu datadir
ls -la /var/lib/mysqld
# Fichiers : ibdata1, ib_logfile*, mysql/, performance_schema/, etc.

# Logs MariaDB
sudo tail -50 /var/log/mariadb/mariadb.log
sudo journalctl -u mariadb -n 50

# Test connexion MariaDB
mysql -u root -p
mysql -u root -p -e "SELECT VERSION();"

# Vérifier socket UNIX
ls -la /var/lib/mysqld/mysql.sock
sudo ss -xl | grep mysql
```

### Fichiers configuration MariaDB

```bash
# Fichiers config (ordre priorité) :
/etc/my.cnf                    # Config globale (override tout)
/etc/my.cnf.d/mariadb-server.cnf  # Config serveur MariaDB
/etc/my.cnf.d/mysql-clients.cnf   # Config clients MySQL
~/.my.cnf                      # Config user (credentials)

# Sections config :
[mysqld]         # Paramètres daemon MariaDB server
[mysql]          # Paramètres client mysql CLI
[mysqldump]      # Paramètres mysqldump
[client]         # Paramètres tous clients
```

---

## 💡 Points clés

**Datadir MariaDB** :
- **datadir** : Répertoire CRITIQUE contenant toutes databases
- Défaut : `/var/lib/mysql` (standard Linux)
- Peut être changé (custom path, storage séparé)
- **DOIT correspondre** emplacement data réelle

**Erreur "directory not empty"** :
- MariaDB initialization requiert datadir VIDE
- Si datadir existe + non-vide + pas database initialisée → Erreur
- Causes :
  * Datadir pointé mauvais répertoire (Challenge 18)
  * Data corrompue (re-init requise)
  * Migration database incomplète

**Socket UNIX MariaDB** :
- Fichier socket : `/var/lib/mysql/mysql.sock` (défaut)
- Connexions locales clients (pas TCP/IP)
- Plus rapide que TCP (pas network stack)
- **DOIT** être dans même répertoire datadir (ou accessible)

**Config MariaDB troubleshooting** :
1. Vérifier chemins config (`datadir`, `socket`)
2. Vérifier filesystem (datadir existe ?)
3. Vérifier permissions (mysql:mysql ownership)
4. Vérifier logs (`/var/log/mariadb/mariadb.log`)

**Permissions datadir** :
```bash
sudo chown -R mysql:mysql /var/lib/mysqld
sudo chmod 750 /var/lib/mysqld
# Owner mysql (daemon MariaDB), group mysql, others no access
```

---

## ⚠️ Notes production

**Backup datadir avant modif** :
```bash
sudo systemctl stop mariadb
sudo tar -czf /backup/mariadb_datadir_$(date +%Y%m%d).tar.gz /var/lib/mysqld
# Backup COMPLET avant tout changement datadir
```

**Migration datadir (procédure safe)** :
```bash
# 1. Stop MariaDB
sudo systemctl stop mariadb

# 2. Copier data ancien → nouveau datadir
sudo rsync -av /var/lib/mysql/ /new/datadir/

# 3. Permissions
sudo chown -R mysql:mysql /new/datadir
sudo chmod 750 /new/datadir

# 4. Modifier config
sudo vi /etc/my.cnf.d/mariadb-server.cnf
# datadir=/new/datadir
# socket=/new/datadir/mysql.sock

# 5. SELinux context (si activé)
sudo semanage fcontext -a -t mysqld_db_t "/new/datadir(/.*)?"
sudo restorecon -Rv /new/datadir

# 6. Start MariaDB
sudo systemctl start mariadb

# 7. Vérifier
mysql -u root -p -e "SHOW VARIABLES LIKE 'datadir';"
```

**Monitoring MariaDB** :
- Check service up : `systemctl is-active mariadb`
- Check connexions : `mysqladmin -u root -p processlist`
- Check replication (si master-slave) : `SHOW SLAVE STATUS\G;`
- Disk space datadir : `df -h /var/lib/mysqld`

**Sécurité MariaDB** :
```bash
# Initialisation sécurité (1x après install)
sudo mysql_secure_installation
# - Set root password
# - Remove anonymous users
# - Disable root remote login
# - Remove test database
```

---

## 🔍 Debugging avancé

**Si datadir vraiment vide (re-initialization requis)** :
```bash
# ATTENTION : Détruit toutes databases existantes
sudo systemctl stop mariadb
sudo rm -rf /var/lib/mysql/*
sudo mysql_install_db --user=mysql --datadir=/var/lib/mysql
sudo systemctl start mariadb
```

**Vérifier logs détaillés** :
```bash
# Logs daemon
sudo tail -f /var/log/mariadb/mariadb.log

# Logs système
sudo journalctl -u mariadb -f

# Activer logs verbose (debug)
# /etc/my.cnf.d/mariadb-server.cnf
[mysqld]
log_error=/var/log/mariadb/error.log
general_log=1
general_log_file=/var/log/mariadb/general.log
slow_query_log=1
slow_query_log_file=/var/log/mariadb/slow.log
long_query_time=2
```

**Causes communes MariaDB fail** :
1. **Datadir incorrect** (Challenge 18) : Config pointe mauvais répertoire
2. **Permissions** : datadir pas owned mysql:mysql
3. **Disk full** : Espace disque épuisé (ibdata1 trop gros)
4. **Port 3306 utilisé** : Autre MySQL/MariaDB instance running
5. **Corruption data** : Crash serveur → tables corrompues (repair requis)
6. **SELinux** : Context incorrect datadir custom

**Test après résolution** :
```bash
# Connexion
mysql -u root -p

# Lister databases
SHOW DATABASES;

# Vérifier datadir
SHOW VARIABLES LIKE 'datadir';

# Vérifier socket
SHOW VARIABLES LIKE 'socket';

# Vérifier version
SELECT VERSION();
```

---

**Tags** : `MariaDB` `MySQL` `troubleshooting` `datadir` `configuration` `database` `Level 2`

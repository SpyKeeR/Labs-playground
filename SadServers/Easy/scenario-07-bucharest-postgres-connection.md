# Scenario "Bucharest" : Connecting to Postgres

**Date** : 13 janvier 2026  
**Plateforme** : SadServers - Troubleshooting Production Linux  
**Niveau** : Medium  
**Temps imparti** : 10 minutes  
**Statut** : ✅ Résolu

---

## 🎯 Objectif

Résoudre problème de connexion PostgreSQL 13 pour application web. L'application ne peut pas se connecter à la database `app1` avec l'utilisateur `app1user`.

---

## 📋 Contexte

**Environnement** :
- OS : Debian 11
- Database : PostgreSQL 13
- Application : Database `app1`, user `app1user`, password `app1user`
- Connexion attendue : localhost (127.0.0.1)

**Symptôme** : Application web ne peut pas se connecter à PostgreSQL.

---

## ✅ Test de validation

```bash
PGPASSWORD=app1user psql -h 127.0.0.1 -d app1 -U app1user -c '\q'
```

**Output attendu** : Connexion réussie sans erreur (exit code 0).

---

## 🔧 Résolution

### Étape 1 : Diagnostic initial

Test connexion PostgreSQL :
```bash
PGPASSWORD=app1user psql -h 127.0.0.1 -d app1 -U app1user -c '\q'
```

**Erreur observée** : Connexion refusée ou timeout (PostgreSQL n'écoute pas sur 127.0.0.1).

### Étape 2 : Vérifier configuration écoute PostgreSQL

Éditer fichier config principal :
```bash
sudo vim /etc/postgresql/13/main/postgresql.conf
```

**Problème 1 identifié** : Ligne `listen_addresses` commentée.

**Ligne trouvée** :
```
#listen_addresses = 'localhost'
```

**Correction** : Décommenter et modifier pour accepter toutes interfaces :
```
listen_addresses = '*'
```

**Explication** : Par défaut commenté, PostgreSQL n'écoute que sur socket UNIX (`/var/run/postgresql/.s.PGSQL.5432`), pas sur TCP/IP.

### Étape 3 : Vérifier règles authentification client

Éditer fichier Host-Based Authentication :
```bash
sudo vim /etc/postgresql/13/main/pg_hba.conf
```

**Problème 2 identifié** : Règles `reject` bloquent toutes connexions.

**Lignes trouvées** :
```
host all all all reject
host all all all reject
```

**Correction** : Supprimer ou commenter ces 2 lignes :
```bash
# host all all all reject
# host all all all reject
```

**Explication** : Règles `reject` explicites prioritaires sur règles `allow` → bloquent toute connexion TCP.

### Étape 4 : Recharger configuration PostgreSQL

```bash
sudo systemctl reload postgresql
```

**Pourquoi `reload` et pas `restart` ?** :
- `reload` : Recharge config sans couper connexions existantes (0 downtime)
- `restart` : Redémarre service complètement (coupe connexions actives)

### Étape 5 : Validation finale

Test connexion :
```bash
PGPASSWORD=app1user psql -h 127.0.0.1 -d app1 -U app1user -c '\q'
```

**Output** : Connexion réussie (exit code 0), aucune erreur.

---

## 📌 Commandes utiles

```bash
# Vérifier statut PostgreSQL
sudo systemctl status postgresql

# Vérifier port écoute (5432)
sudo ss -tuln | grep 5432
sudo netstat -tuln | grep 5432

# Tester connexion locale (socket UNIX)
sudo -u postgres psql -d app1 -c '\l'

# Tester connexion TCP/IP
PGPASSWORD=password psql -h 127.0.0.1 -d dbname -U username -c '\q'

# Voir logs PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-13-main.log

# Recharger config PostgreSQL
sudo systemctl reload postgresql

# Redémarrer PostgreSQL
sudo systemctl restart postgresql

# Vérifier config active
sudo -u postgres psql -c 'SHOW listen_addresses;'
sudo -u postgres psql -c 'SHOW port;'
```

### Fichiers config PostgreSQL

```bash
# Config principale
/etc/postgresql/13/main/postgresql.conf

# Authentification clients (HBA)
/etc/postgresql/13/main/pg_hba.conf

# Logs
/var/log/postgresql/postgresql-13-main.log

# Socket UNIX
/var/run/postgresql/.s.PGSQL.5432
```

### Syntaxe pg_hba.conf

```
# TYPE  DATABASE  USER  ADDRESS      METHOD
host    all       all   127.0.0.1/32 md5
host    all       all   0.0.0.0/0    reject
local   all       all                peer
```

**Ordre important** : Première règle match = appliquée (pas de cascade).

---

## 💡 Points clés

**Deux problèmes simultanés** :
1. PostgreSQL n'écoutait pas sur TCP/IP (`listen_addresses` commenté)
2. Règles HBA rejetaient explicitement toutes connexions

**Configuration production** :
- `listen_addresses = '*'` : Accepte toutes interfaces (sécuriser avec firewall/pg_hba)
- pg_hba.conf : Règles granulaires (IP, réseaux, users, databases)
- Toujours `reload` après modif config (éviter restart si possible)

**Erreurs évitées** :
- Ne pas restart PostgreSQL inutilement (coupe connexions actives)
- Ordre règles pg_hba.conf critique (reject avant allow = bloque tout)
- Oublier reload après modif config → changements ignorés

---

**Tags** : `PostgreSQL` `pg_hba.conf` `listen_addresses` `troubleshooting` `database` `SadServers`

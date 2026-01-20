# Challenge 03 - Install and Configure PostgreSQL

**Difficulté** : Level 4  
**Domaine** : PostgreSQL, Database Administration  
**Date** : 19 janvier 2026

---

## 📋 Consigne

L'équipe de développement d'applications Nautilus a partagé qu'elle prévoit de déployer une application nouvellement développée sur l'infrastructure Nautilus dans le Stratos DC. L'application utilise une base de données PostgreSQL, donc en tant que pré-requis, nous devons configurer un serveur de base de données PostgreSQL selon les exigences partagées ci-dessous :

Le serveur de base de données PostgreSQL est déjà installé sur le serveur de base de données Nautilus.

a. Créer un utilisateur de base de données `kodekloud_roy` et définir son mot de passe à `ksH85UJjhb`.

b. Créer une base de données `kodekloud_db8` et accorder toutes les permissions à l'utilisateur `kodekloud_roy` sur cette base de données.

Note : Veuillez ne pas essayer de redémarrer le service du serveur PostgreSQL.

---

## 🔧 Réalisation

### Étape 1 : Connexion serveur Database

```bash
ssh peter@stdb01
# Password: Sp!dy
```

### Étape 2 : Création utilisateur PostgreSQL

```bash
sudo -u postgres createuser kodekloud_roy
```

**Explication** :
- `-u postgres` : Exécute commande en tant qu'utilisateur système `postgres`
- `createuser` : Utilitaire PostgreSQL création utilisateur

---

### Étape 3 : Création base de données

```bash
sudo -u postgres createdb kodekloud_db8
```

**Explication** : `createdb` crée nouvelle database PostgreSQL

---

### Étape 4 : Configuration mot de passe et permissions

```bash
sudo -u postgres psql
```

**Dans le shell PostgreSQL** :
```sql
ALTER USER kodekloud_roy WITH ENCRYPTED PASSWORD 'ksH85UJjhb';
```

**Explication** :
- `ALTER USER` : Modifie propriétés utilisateur existant
- `ENCRYPTED PASSWORD` : Hash mot de passe (sécurité)

**Accorder permissions** :
```sql
GRANT ALL PRIVILEGES ON DATABASE kodekloud_db8 TO kodekloud_roy;
```

**Explication** :
- `ALL PRIVILEGES` : Permissions complètes (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, etc.)
- Scope : Database `kodekloud_db8` uniquement

**Quitter psql** :
```sql
\q
```

---

### Étape 5 : Vérification

**Lister utilisateurs** :
```bash
sudo -u postgres psql -c "\du"
                                   List of roles
 Role name     |                         Attributes                         
---------------+------------------------------------------------------------
 kodekloud_roy | 
 postgres      | Superuser, Create role, Create DB, Replication, Bypass RLS
```

**Lister databases** :
```bash
sudo -u postgres psql -c "\l" | grep kodekloud_db8
 kodekloud_db8 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
```

**Vérifier permissions** :
```bash
sudo -u postgres psql -c "\l kodekloud_db8"
# Access privileges : kodekloud_roy=CTc/postgres
```

---

## 🔗 Ressources

- [PostgreSQL User Management](https://www.postgresql.org/docs/current/user-manag.html)
- [PostgreSQL GRANT](https://www.postgresql.org/docs/current/sql-grant.html)
- [psql Meta-Commands](https://www.postgresql.org/docs/current/app-psql.html)

# Challenge 06 - Install and Configure DB Server

**Difficulté** : Level 4  
**Domaine** : MariaDB, Database Administration  
**Date** : 20 janvier 2026

---

## 📋 Consigne

Nous devons configurer un serveur de base de données sur le serveur de base de données Nautilus dans le Stratos Datacenter. Veuillez effectuer les étapes ci-dessous sur le serveur de base de données :

a. Installer/Configurer le serveur MariaDB.

b. Créer une base de données nommée `kodekloud_db1`.

c. Créer un utilisateur appelé `kodekloud_rin` et définir son mot de passe à `LQfKeWWxWD`.

d. Accorder toutes les permissions à l'utilisateur `kodekloud_rin` sur la base de données `kodekloud_db1`.

---

## 🔧 Réalisation

### Étape 1 : Connexion serveur Database

```bash
ssh peter@stdb01
# Password: Sp!dy
```

### Étape 2 : Installation MariaDB

```bash
sudo yum install mariadb-server -y
```

**Explication** : Installation serveur MariaDB (fork MySQL)

### Étape 3 : Activation service

```bash
sudo systemctl enable --now mariadb
```

### Étape 4 : Configuration database et utilisateur

```bash
sudo mysql
```

**Dans shell MariaDB** :
```sql
CREATE DATABASE kodekloud_db1;

CREATE USER 'kodekloud_rin'@'%' IDENTIFIED BY 'LQfKeWWxWD';

GRANT ALL PRIVILEGES ON kodekloud_db1.* TO 'kodekloud_rin'@'%';

FLUSH PRIVILEGES;
```

**Explication** :
- `CREATE DATABASE` : Crée nouvelle base de données
- `CREATE USER '@'%'` : Utilisateur accès depuis n'importe quel hôte
- `GRANT ALL PRIVILEGES ON db.*` : Toutes permissions sur tables database
- `FLUSH PRIVILEGES` : Recharge table permissions

**Quitter** :
```sql
quit
```

### Étape 5 : Vérification

```bash
sudo mysql -e "SHOW DATABASES;" | grep kodekloud_db1
# kodekloud_db1

sudo mysql -e "SELECT user, host FROM mysql.user WHERE user='kodekloud_rin';"
# kodekloud_rin    %
```

---

## 🔑 Apprentissages clés

**Configuration basique MariaDB** :
- Installation package `mariadb-server`
- Service `mariadb` (pas `mysql`)
- Accès root sans password initial (socket authentication)

**Wildcard host '%'** :
- Utilisateur peut se connecter depuis n'importe quelle IP
- Production : Limiter à subnet spécifique (`'@'192.168.1.%'`)

**GRANT ALL PRIVILEGES** :
- Équivaut à : SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, etc.
- Scope database : `db.*` (toutes tables)

---

## 🔗 Ressources

- [MariaDB User Management](https://mariadb.com/kb/en/grant/)
- [MySQL GRANT Documentation](https://dev.mysql.com/doc/refman/8.0/en/grant.html)

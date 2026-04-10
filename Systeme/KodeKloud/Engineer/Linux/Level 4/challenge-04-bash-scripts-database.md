# Challenge 04 - Bash Scripts If/Else Statements

**Difficulté** : Level 4  
**Domaine** : Bash Scripting, MariaDB, Automation  
**Date** : 19 janvier 2026

---

## 📋 Consigne

L'équipe DevOps de Nautilus travaille sur le développement d'un script bash pour automatiser certaines tâches. Selon les exigences partagées avec l'équipe, les tâches liées à la base de données doivent être automatisées. Vous trouverez ci-dessous plus de détails à ce sujet :

Écrire un script bash nommé `/opt/scripts/database.sh` sur le serveur de base de données. Le serveur de base de données MariaDB est déjà installé sur ce serveur.

Ajouter du code dans le script pour effectuer certaines opérations liées à la base de données selon les conditions données ci-dessous :

a. Créer une nouvelle base de données nommée `kodekloud_db01`. Si cette base de données existe déjà sur le serveur, le script doit afficher le message `Database already exists` et si la base de données n'existe pas, créer la même et le script doit afficher `Database kodekloud_db01 has been created`. De plus, créer un utilisateur nommé `kodekloud_roy` et définir son mot de passe à `asdfgdsd`, et donner également un accès complet à cet utilisateur sur la base de données nouvellement créée (n'oubliez pas d'utiliser un hôte générique lors de la création de l'utilisateur).

b. Maintenant, vérifier si la base de données (si elle existait déjà) contient déjà des données (tables). Si oui, le script doit afficher `database is not empty`, sinon importer le dump de base de données `/opt/db_backups/db.sql` et afficher `imported database dump into kodekloud_db01 database`.

c. Prendre un dump MySQL qui doit être nommé `kodekloud_db01.sql` et le sauvegarder dans le répertoire `/opt/db_backups/`.

---

## 🔧 Réalisation

### Étape 1 : Connexion serveur Database

```bash
ssh peter@stdb01
# Password: Sp!dy
```

### Étape 2 : Création script Bash

```bash
sudo vi /opt/scripts/database.sh
```

**Contenu script** :
```bash
#!/bin/bash

# Variables
db='kodekloud_db01'
user='kodekloud_roy'
user_pw='asdfgdsd'
import_db='/opt/db_backups/db.sql'
export_db="/opt/db_backups/${db}.sql"

# Requêtes SQL
db_exist_req="USE $db;"
db_empty_req="SHOW TABLES FROM $db;"
create_db_req="CREATE DATABASE $db;"
create_user_req="CREATE USER '${user}'@'%' IDENTIFIED BY '${user_pw}';"
grant_priv_req="GRANT ALL PRIVILEGES ON ${db}.* TO '${user}'@'%';"
flush_priv_req="FLUSH PRIVILEGES;"

# Vérifier si database existe
if [[ -z $(echo "Sp!dy" | sudo -S mysql -se "${db_exist_req}" 2>&1) ]]
then
    echo "Database already exists"
    
    # Vérifier si database contient des tables
    if [[ -z $(echo "Sp!dy" | sudo -S mysql -se "${db_empty_req}") ]]
    then
        # Database vide -> Import dump
        echo "Sp!dy" | sudo -S sh -c "mysql ${db} < ${import_db}"
        echo "Imported database dump into kodekloud_db01 database"
    else
        # Database contient données
        echo "database is not empty"
    fi
else
    # Database n'existe pas -> Créer
    echo "Sp!dy" | sudo -S mysql -se "${create_db_req}"
    echo "Database $db has been created"
    
    # Créer utilisateur
    echo "Sp!dy" | sudo -S mysql -se "${create_user_req}"
    
    # Accorder permissions
    echo "Sp!dy" | sudo -S mysql -se "${grant_priv_req}"
    echo "Sp!dy" | sudo -S mysql -se "${flush_priv_req}"
    
    # Import dump
    echo "Sp!dy" | sudo -S mysql ${db} < ${import_db}
    echo "imported database dump into ${db} database."
fi

# Export dump
echo "Sp!dy" | sudo -S sh -c "mysqldump ${db} > ${export_db}"
```

**Explication logique** :

**Test existence database** :
```bash
[[ -z $(echo "Sp!dy" | sudo -S mysql -se "${db_exist_req}" 2>&1) ]]
```
- `mysql -se "USE db;"` : Retourne erreur si database inexistante
- `-z` : True si string vide (pas d'erreur = database existe)
- `2>&1` : Redirige stderr vers stdout

**Test database vide** :
```bash
[[ -z $(echo "Sp!dy" | sudo -S mysql -se "${db_empty_req}") ]]
```
- `SHOW TABLES` : Retourne liste tables (vide si aucune)
- `-z` : True si vide (aucune table)

**Import/Export** :
```bash
mysql ${db} < ${import_db}     # Import
mysqldump ${db} > ${export_db}  # Export
```

---

### Étape 3 : Permissions exécution

```bash
sudo chmod +x /opt/scripts/database.sh
```

**Explication** : Rend script exécutable

---

### Étape 4 : Exécution et vérification

**Première exécution (database n'existe pas)** :
```bash
sudo /opt/scripts/database.sh
# Database kodekloud_db01 has been created
# imported database dump into kodekloud_db01 database.
```

**Vérification** :
```bash
sudo mysql -e "SHOW DATABASES;" | grep kodekloud_db01
# kodekloud_db01

sudo mysql -e "SELECT user, host FROM mysql.user;" | grep kodekloud_roy
# kodekloud_roy    %

ls -l /opt/db_backups/kodekloud_db01.sql
# -rw-r--r-- 1 root root 2048 Jan 19 16:30 kodekloud_db01.sql
```

**Deuxième exécution (database existe, non vide)** :
```bash
sudo /opt/scripts/database.sh
# Database already exists
# database is not empty
```

---

## 🔗 Ressources

- [Bash Conditional Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)
- [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)
- [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)

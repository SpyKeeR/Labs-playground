# Instructions

Pour des raisons de sécurité, l’équipe de sécurité de **xFusionCorp Industries** a décidé d’utiliser des utilisateurs Apache personnalisés pour chaque application web hébergée, au lieu de l’utilisateur par défaut.  

Chaque application web devra donc avoir son propre utilisateur Apache, avec un répertoire personnel spécifique, différent du répertoire par défaut.  

**Tâches à réaliser :**  

1. Créer un utilisateur nommé `jim` sur le **App Server 2** dans le datacenter Stratos.  
2. Assigner à cet utilisateur l’UID `1582` et définir son répertoire personnel sur `/var/www/jim`.  

---

# Solution

1. **Se connecter au serveur App 2**  

```bash
ssh steve@172.16.238.11
```

2. **Créer l’utilisateur avec les paramètres requis**  

La commande suivante crée l’utilisateur `jim`, définit son UID à `1582` et crée le répertoire personnel `/var/www/jim` :  

```bash
sudo useradd -u 1582 -d /var/www/jim -m jim
```

- `-u 1582` : définit l’UID de l’utilisateur.  
- `-d /var/www/jim` : spécifie le chemin du répertoire personnel.  
- `-m` : crée automatiquement le répertoire personnel s’il n’existe pas.  

3. **Vérifier que l’utilisateur a été créé correctement**  

Pour vérifier la création de l’utilisateur et ses informations associées :  

```bash
id jim
```

Cette commande affiche :  

- UID (User ID)  
- GID (Group ID)  
- Les groupes auxquels l’utilisateur appartient  

Si l’utilisateur a été créé correctement, vous verrez un résultat similaire à ceci :  

```
uid=1582(jim) gid=1582(jim) groups=1582(jim)
```
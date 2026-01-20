# Challenge 01 : Create Cron Task

**Date** : 7 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Installer et configurer le service cron sur les serveurs applicatifs, puis créer une tâche planifiée pour automatiser l'exécution d'un script.

---

## 📋 Énoncé

L'équipe système de Nautilus a préparé des scripts d'automatisation pour des tâches quotidiennes. Avant le déploiement en production sur tous les app servers, un test doit être effectué avec un cron job simple :

**Tâches** :

a. Installer le package `cronie` sur tous les app servers Nautilus et démarrer le service `crond`

b. Ajouter un cron job pour l'utilisateur root :  
   `*/5 * * * * echo hello > /tmp/cron_text`  
   (Exécuté toutes les 5 minutes, écrit "hello" dans `/tmp/cron_text`)

**Serveurs cibles** : `tony@stapp01`, `steve@stapp02`, `banner@stapp03`

---

## ✅ Résolution

### 1. Connexion au premier serveur

```bash
ssh tony@stapp01
```

### 2. Vérifier l'état du service crond

```bash
sudo systemctl status crond
```

**Explication** : Vérifier si le service cron est déjà installé et actif. Si `cronie` n'est pas installé, le service n'existera pas.

### 3. Installer cronie (si nécessaire)

```bash
sudo yum install cronie -y
```

**Explication** : 
- `cronie` : Package RHEL/CentOS fournissant le daemon cron et les utilitaires (`crontab`, `anacron`)
- Le service se nomme `crond` (cron daemon)

### 4. Démarrer et activer le service crond

```bash
sudo systemctl start crond
sudo systemctl enable crond
```

**Explication** :
- `start` : Démarre le service immédiatement
- `enable` : Active le service au boot (persistant après reboot)

**Alternative combinée** :
```bash
sudo systemctl enable --now crond
```

### 5. Éditer la crontab de root

```bash
sudo crontab -e
```

**Explication** : 
- `crontab -e` : Édite la crontab de l'utilisateur courant
- `sudo crontab -e` : Édite la crontab de root (équivalent à `sudo crontab -e -u root`)

Ajouter la ligne suivante :

```
*/5 * * * * echo hello > /tmp/cron_text
```

**Format cron job** :
```
┌───────────── minute (0-59)
│ ┌─────────── heure (0-23)
│ │ ┌───────── jour du mois (1-31)
│ │ │ ┌─────── mois (1-12)
│ │ │ │ ┌───── jour de la semaine (0-6, 0=dimanche)
│ │ │ │ │
* * * * * commande
```

**Détail de la tâche** :
- `*/5` : Toutes les 5 minutes (diviseur)
- `*` : Toutes les heures, tous les jours, tous les mois, tous les jours de la semaine
- `echo hello > /tmp/cron_text` : Écrit "hello" dans `/tmp/cron_text` (écrase contenu précédent)

Sauvegarder et quitter (vim : `:wq`)

### 6. Validation

Vérifier la crontab de root :

```bash
sudo crontab -l -u root
```

**Sortie attendue** :
```
*/5 * * * * echo hello > /tmp/cron_text
```

**Explication** :
- `crontab -l` : Liste les cron jobs de l'utilisateur courant
- `-u root` : Spécifie l'utilisateur root (redondant avec `sudo crontab -l`)

**Vérification exécution** (attendre 5 minutes) :

```bash
cat /tmp/cron_text
# hello
```

### 7. Répéter pour les autres serveurs

**App Server 2** :

```bash
ssh steve@stapp02
sudo yum install cronie -y
sudo systemctl enable --now crond
sudo crontab -e
# Ajouter : */5 * * * * echo hello > /tmp/cron_text
sudo crontab -l -u root
```

**App Server 3** :

```bash
ssh banner@stapp03
sudo yum install cronie -y
sudo systemctl enable --now crond
sudo crontab -e
# Ajouter : */5 * * * * echo hello > /tmp/cron_text
sudo crontab -l -u root
```

---

## 📌 Commandes clés

| Commande | Usage |
|----------|-------|
| `crontab -e` | Éditer crontab utilisateur courant |
| `crontab -l` | Lister cron jobs utilisateur courant |
| `sudo crontab -e -u USER` | Éditer crontab d'un utilisateur spécifique |
| `sudo crontab -l -u USER` | Lister cron jobs d'un utilisateur |
| `crontab -r` | Supprimer toute la crontab utilisateur (DANGER) |
| `systemctl status crond` | Vérifier statut service cron |
| `journalctl -u crond -f` | Logs en temps réel du service cron |

---

## 🔍 Syntaxe cron (rappels)

**Diviseurs** :
- `*/5` : Toutes les 5 unités
- `*/15` : Toutes les 15 unités

**Listes** :
- `0,30 * * * *` : À 0 et 30 minutes de chaque heure
- `0 9,17 * * *` : À 9h00 et 17h00 chaque jour

**Plages** :
- `0 9-17 * * *` : Toutes les heures de 9h à 17h
- `0 0 * * 1-5` : Minuit du lundi au vendredi

**Combinaisons** :
- `30 2 * * 0` : 2h30 chaque dimanche
- `0 */4 * * *` : Toutes les 4 heures (0h, 4h, 8h, 12h, 16h, 20h)

**Chaînes spéciales** :
- `@reboot` : Au démarrage système
- `@daily` ou `@midnight` : Une fois par jour (0h00)
- `@hourly` : Une fois par heure (minute 0)
- `@weekly` : Une fois par semaine (dimanche 0h00)
- `@monthly` : Une fois par mois (1er jour 0h00)
- `@yearly` ou `@annually` : Une fois par an (1er janvier 0h00)

---

## 🏷️ Tags

`#Linux` `#Cron` `#Automation` `#Scheduling` `#SystemAdmin` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

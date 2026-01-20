# Challenge 11 : Linux Configure sudo

**Date** : 10 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Accorder les privilèges `sudo` à l'utilisateur `yousuf` sur les 3 serveurs applicatifs, sans demander de mot de passe (NOPASSWD).

---

## 📋 Énoncé
Nous avons plusieurs utilisateurs sur tous les serveurs applicatifs du Stratos Datacenter. Certains d'entre eux se sont vu attribuer de nouveaux rôles et responsabilités, par conséquent leurs comptes utilisateurs doivent être mis à niveau avec un accès sudo afin qu'ils puissent effectuer des tâches de niveau administrateur.

**Tâches** :
- Fournir l'accès sudo à l'utilisateur `yousuf` sur tous les serveurs applicatifs
- S'assurer d'avoir configuré sudo sans mot de passe pour cet utilisateur

**Serveurs concernés** :
- `stapp01` (user `tony`)
- `stapp02` (user `steve`)
- `stapp03` (user `banner`)

---

## 🔧 Résolution

### Approche

Pour chaque serveur :
1. Se connecter via SSH
2. Éditer le fichier sudoers avec `visudo` (safe editing)
3. Ajouter la ligne de configuration pour `yousuf` avec `NOPASSWD`

### Commandes exécutées

**Serveur stapp01** :
```bash
ssh tony@stapp01
sudo visudo
```

Insérer en dernière ligne :
```
yousuf     ALL=(ALL)    NOPASSWD:ALL
```

**Serveur stapp02** :
```bash
ssh steve@stapp02
sudo visudo
```

Insérer en dernière ligne :
```
yousuf     ALL=(ALL)    NOPASSWD:ALL
```

**Serveur stapp03** :
```bash
ssh banner@stapp03
sudo visudo
```

Insérer en dernière ligne :
```
yousuf     ALL=(ALL)    NOPASSWD:ALL
```

### Explications

**Syntaxe sudoers** :
```
user    hosts=(runas)    commands
```

- `yousuf` : Utilisateur concerné
- `ALL` (hosts) : Sur tous les hôtes
- `(ALL)` (runas) : Peut exécuter en tant que n'importe quel utilisateur
- `NOPASSWD:ALL` : Toutes les commandes SANS demander mot de passe

**Pourquoi `visudo` ?**
- Verrouille le fichier `/etc/sudoers` pendant édition
- Vérifie la syntaxe avant d'enregistrer
- Évite de casser sudo avec une erreur de syntaxe

---

## ✅ Validation

Se connecter en tant que `yousuf` et tester :

```bash
# Lister privilèges sudo
sudo -l
# Output attendu : (ALL) NOPASSWD: ALL

# Tester commande sudo sans password
sudo whoami
# Output attendu : root (sans demander password)
```

---

## 📌 Commandes utiles

```bash
# Éditer sudoers (safe)
sudo visudo

# Lister privilèges sudo user courant
sudo -l

# Tester privilèges sudo autre user
sudo -l -U <username>

# Vérifier syntaxe sudoers
sudo visudo -c

# Valider timestamp sudo (rafraîchir 15min)
sudo -v

# Tester commande sudo
sudo <command>
```

### Syntaxes sudoers courantes

```bash
# User sudo complet avec password
user    ALL=(ALL)    ALL

# User sudo complet SANS password
user    ALL=(ALL)    NOPASSWD:ALL

# User sudo commandes spécifiques
user    ALL=(ALL)    /bin/systemctl, /usr/bin/yum

# Group sudo (préfixe %)
%admin  ALL=(ALL)    ALL

# Alias commandes
Cmnd_Alias SERVICES = /bin/systemctl, /usr/bin/service
user    ALL=(ALL)    SERVICES
```

---

**Tags** : `sudo` `visudo` `NOPASSWD` `sudoers` `permissions` `Level 2`

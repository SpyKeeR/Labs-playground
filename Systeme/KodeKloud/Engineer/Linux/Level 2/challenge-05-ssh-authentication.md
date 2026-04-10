# Challenge 05 : Linux SSH Authentication

**Date** : 8 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Configurer authentification SSH sans mot de passe depuis jump host vers tous les app servers via clés SSH publiques.

---

## 📋 Énoncé

L'équipe sysadmin de xFusionCorp Industries a configuré scripts sur jump host s'exécutant à intervalles réguliers sur tous les app servers du Stratos Datacenter. Pour fonctionnement correct, l'utilisateur `thor` sur jump host doit avoir accès SSH sans mot de passe vers tous les app servers via leurs utilisateurs sudo respectifs.

**Tâche** : Configurer authentification password-less depuis `thor@jump_host` vers tous app servers via leurs sudo users :
- `tony@stapp01` (App Server 1)
- `steve@stapp02` (App Server 2)
- `banner@stapp03` (App Server 3)

---

## ✅ Résolution

### 1. Générer paire de clés SSH

Depuis jump host (utilisateur `thor`) :

```bash
ssh-keygen -t ed25519
```

**Explication** :
- `ssh-keygen` : Génère paire clés SSH (publique/privée)
- `-t ed25519` : Type algorithme (Ed25519, moderne et sécurisé)
- **Prompts** :
  * Fichier sauvegarde : Défaut `~/.ssh/id_ed25519` (Enter)
  * Passphrase : Vide pour password-less (Enter 2x)

**Résultat** :
- `~/.ssh/id_ed25519` : Clé privée (garder secrète)
- `~/.ssh/id_ed25519.pub` : Clé publique (copier sur serveurs)

### 2. Copier clé publique vers App Server 1

```bash
ssh-copy-id tony@stapp01
```

**Explication** :
- `ssh-copy-id` : Copie clé publique vers `~/.ssh/authorized_keys` serveur distant
- **Prompt** : Mot de passe `tony@stapp01` (dernière fois)
- Ajoute clé publique dans `/home/tony/.ssh/authorized_keys`

### 3. Copier clé publique vers App Server 2

```bash
ssh-copy-id steve@stapp02
```

**Prompt** : Mot de passe `steve@stapp02`

### 4. Copier clé publique vers App Server 3

```bash
ssh-copy-id banner@stapp03
```

**Prompt** : Mot de passe `banner@stapp03`

### 5. Validation

Tester connexion sans mot de passe :

```bash
ssh tony@stapp01
# Connexion directe sans prompt password
exit

ssh steve@stapp02
# Connexion directe sans prompt password
exit

ssh banner@stapp03
# Connexion directe sans prompt password
exit
```

**Résultat attendu** : Connexions SSH réussies sans demande mot de passe.

---

## 💡 Notes

- **Ed25519** : Algorithme moderne (plus rapide/sécurisé que RSA 2048-bit)
- **ssh-copy-id** : Automatise copie clé publique + permissions correctes `~/.ssh/authorized_keys`
- **Password-less** : Clé privée sans passphrase (automation scripts)
- **Security** : Clé privée jamais partagée, protégée permissions `600`

---

## 🏷️ Tags

`#Linux` `#SSH` `#Authentication` `#PublicKey` `#Ed25519` `#ssh-keygen` `#ssh-copy-id` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

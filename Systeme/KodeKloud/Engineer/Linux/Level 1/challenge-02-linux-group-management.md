# Challenge 2 : Linux Group Management

**Date :** Janvier 2026 (antérieur au 5 janvier)  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Gestion groupes et utilisateurs  
**Difficulté :** Débutant  
**Durée :** ~15 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Créer un groupe système sur plusieurs serveurs et y affecter un utilisateur pour implémenter une gestion des accès basée sur les groupes (GBAC - Group-Based Access Control).

---

## 📋 Énoncé

L'équipe d'administration système de **xFusionCorp Industries** a défini des niveaux d'accès spécifiques pour les utilisateurs.

Au lieu d'attribuer des droits individuellement à chaque utilisateur, l'équipe a décidé de créer des groupes correspondant aux différents niveaux d'accès, puis d'ajouter les utilisateurs à ces groupes selon les besoins.

**Tâches à réaliser :**
1. Créer un groupe nommé `nautilus_developers` sur **tous les serveurs App** du Stratos Datacenter
2. Ajouter l'utilisateur `mohammed` au groupe `nautilus_developers` sur tous les serveurs App
3. Créer l'utilisateur `mohammed` si nécessaire

**Serveurs cibles :**
- App Server 1 : `stapp01` (tony@172.16.238.10)
- App Server 2 : `stapp02` (steve@172.16.238.11)
- App Server 3 : `stapp03` (banner@172.16.238.12)

---

## 🔧 Résolution

### Étape 1 : Connexion au premier serveur

```bash
ssh tony@172.16.238.10
```

---

### Étape 2 : Vérifier groupes existants (optionnel)

```bash
cat /etc/group
# OU filtrer
grep "nautilus" /etc/group
```

**Explication :** S'assurer que le groupe n'existe pas déjà.

---

### Étape 3 : Créer le groupe nautilus_developers

```bash
sudo groupadd nautilus_developers
```

**Explication :**
- `groupadd` : commande création groupe Linux
- Nom groupe : `nautilus_developers`
- GID (Group ID) : auto-assigné par système (généralement prochain disponible)

---

### Étape 4 : Vérifier création du groupe

```bash
grep "^nautilus_developers:" /etc/group
```

**Résultat attendu :**
```
nautilus_developers:x:1005:
```

**Format ligne /etc/group :**
```
groupname:password:GID:user1,user2,user3
```

---

### Étape 5 : Vérifier si utilisateur mohammed existe

```bash
id mohammed
```

**Si utilisateur n'existe pas :**
```
id: 'mohammed': no such user
```

**Si existe :**
```
uid=1001(mohammed) gid=1001(mohammed) groups=1001(mohammed)
```

---

### Étape 6 : Créer utilisateur mohammed (si nécessaire)

```bash
sudo useradd mohammed
```

**Explication :**
- Création standard sans options particulières
- Home : `/home/mohammed` (défaut)
- Shell : `/bin/bash` (défaut)
- UID/GID : auto-assignés

---

### Étape 7 : Ajouter mohammed au groupe nautilus_developers

```bash
sudo usermod -aG nautilus_developers mohammed
```

**Explication détaillée :**
- `usermod` : modifier utilisateur existant
- `-a` : **append** (ajouter au groupe SANS supprimer groupes existants)
- `-G nautilus_developers` : groupe secondaire à ajouter
- `mohammed` : utilisateur cible

**⚠️ DANGER sans `-a` :**
```bash
# ❌ ERREUR : Écrase TOUS les groupes secondaires
sudo usermod -G nautilus_developers mohammed
# Résultat : mohammed retiré de tous autres groupes!

# ✅ CORRECT : Ajoute au groupe en préservant les autres
sudo usermod -aG nautilus_developers mohammed
```

---

### Étape 8 : Validation

```bash
# Vérifier groupes de mohammed
id mohammed

# OU vérifier membres du groupe
grep "^nautilus_developers:" /etc/group
```

**Résultat attendu :**
```
uid=1001(mohammed) gid=1001(mohammed) groups=1001(mohammed),1005(nautilus_developers)
```

---

### Étape 9 : Répéter sur autres serveurs

```bash
# Serveur 2
ssh steve@172.16.238.11
sudo groupadd nautilus_developers
sudo useradd mohammed  # Si nécessaire
sudo usermod -aG nautilus_developers mohammed
exit

# Serveur 3
ssh banner@172.16.238.12
sudo groupadd nautilus_developers
sudo useradd mohammed  # Si nécessaire
sudo usermod -aG nautilus_developers mohammed
exit
```

---

## 🔗 Ressources

- `man groupadd` : Création groupes
- `man usermod` : Modification utilisateurs
- `man gpasswd` : Gestion membres groupes
- `/etc/group` : Base groupes système

---

## 📝 Commandes clés

```bash
# Créer groupe
sudo groupadd groupname

# Ajouter user à groupe (append)
sudo usermod -aG groupname username

# Vérifier groupes user
groups username
id username

# Lister membres groupe
getent group groupname

# Retirer user d'un groupe
sudo gpasswd -d username groupname
```

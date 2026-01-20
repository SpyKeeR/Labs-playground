# KodeKloud Engineer - Challenge 14 : Default GUI Access

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Systemd Targets & Runlevels  
**Difficulté :** Medium  
**Durée :** ~15 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Configurer les serveurs pour démarrer en mode graphique (GUI) par défaut en modifiant le target systemd.

---

## 📋 Énoncé

**Contexte :** Avec l'installation de nouveaux outils sur les app servers du Stratos Datacenter, certaines fonctionnalités nécessitent maintenant un accès interface graphique (GUI).

**Mission :** Ajuster le runlevel par défaut sur **tous les App servers** pour activer le démarrage GUI par défaut.

**Contrainte critique :** **NE PAS redémarrer** les serveurs après la modification.

**Serveurs cibles :**
- App Server 1 : `tony@stapp01`
- App Server 2 : `steve@stapp02`
- App Server 3 : `banner@stapp03`

---

## 🔧 Résolution

### App Server 1 (stapp01)

#### Étape 1 : Connexion
```bash
ssh tony@stapp01
```

#### Étape 2 : Vérifier target actuel
```bash
sudo systemctl get-default
```

**Résultat probable :**
```
multi-user.target
```

**⚠️ Note :** `multi-user.target` = mode texte (équivalent runlevel 3).

---

#### Étape 3 : Définir target graphical
```bash
sudo systemctl set-default graphical.target
```

**Output :**
```
Removed /etc/systemd/system/default.target.
Created symlink /etc/systemd/system/default.target → /lib/systemd/system/graphical.target.
```

**Explication :**
- `set-default` : Modifie symlink `/etc/systemd/system/default.target`
- `graphical.target` : Target systemd pour mode GUI (équivalent runlevel 5)

---

#### Étape 4 : Recharger daemon systemd
```bash
sudo systemctl daemon-reload
```

**Explication :**
- `daemon-reload` : Recharge configuration systemd (lit nouveaux symlinks)
- **Requis** après modification targets/units

---

#### Étape 5 : Vérifier changement appliqué
```bash
sudo systemctl get-default
```

**Résultat attendu :**
```
graphical.target
```

**✅ Succès** : Au prochain boot, serveur démarrera en mode GUI.

---

### App Server 2 (stapp02)

```bash
ssh steve@stapp02
sudo systemctl set-default graphical.target
sudo systemctl daemon-reload
sudo systemctl get-default
# graphical.target
```

---

### App Server 3 (stapp03)

```bash
ssh banner@stapp03
sudo systemctl set-default graphical.target
sudo systemctl daemon-reload
sudo systemctl get-default
# graphical.target
```

---

## 🎓 Commandes à Retenir

```bash
# Voir target par défaut
systemctl get-default

# Changer target par défaut (permanent)
sudo systemctl set-default graphical.target
sudo systemctl set-default multi-user.target

# Recharger config systemd (après modif)
sudo systemctl daemon-reload

# Changer target immédiatement (temporaire)
sudo systemctl isolate graphical.target

# Lister targets actifs
systemctl list-units --type=target

# Lister tous targets disponibles
systemctl list-units --type=target --all

# Voir dépendances target
systemctl list-dependencies graphical.target

# Vérifier services target spécifique
systemctl list-dependencies --reverse graphical.target

# Retourner target par défaut (depuis rescue)
systemctl default
```

---

**Tags :** #Linux #systemd #Targets #Runlevels #GUI #SystemAdministration #KodeKloud

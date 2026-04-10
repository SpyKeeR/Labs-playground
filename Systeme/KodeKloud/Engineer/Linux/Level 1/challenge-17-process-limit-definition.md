# Challenge 17 : Process Limit Definition

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Resource Limits & ulimit  
**Difficulté :** Débutant  
**Durée :** ~10 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Limiter le nombre maximum de processus pour un utilisateur système afin de résoudre une dégradation de performances due à une consommation excessive de ressources.

---

## 📋 Énoncé

Dans le Stratos Datacenter, le serveur de stockage rencontre des dégradations de performances dues à un nombre excessif de processus détenus par l'utilisateur `nfsuser`.

Pour atténuer ce problème, nous devons imposer des limitations sur le nombre maximum de processus.

**Tâches :**
- Définir la limite **soft** à **1027** processus
- Définir la limite **hard** à **2025** processus
- Utilisateur cible : `nfsuser`

**Serveur cible :** `natasha@ststor01`

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur de stockage

```bash
ssh natasha@ststor01
```

---

### Étape 2 : Éditer le fichier de configuration des limites

```bash
sudo vi /etc/security/limits.conf
```

**Explication :** Le fichier `/etc/security/limits.conf` permet de définir les limites de ressources (processus, fichiers ouverts, mémoire, etc.) pour les utilisateurs et groupes du système.

---

### Étape 3 : Ajouter les limites pour nfsuser

**Ajouter les lignes suivantes dans le fichier :**

```
nfsuser          soft    nproc           1027
nfsuser          hard    nproc           2025
```

**Explication des colonnes :**
- `nfsuser` : Nom de l'utilisateur cible
- `soft` / `hard` : Type de limite
  - **soft** : Limite par défaut, peut être augmentée par l'utilisateur jusqu'à la limite hard
  - **hard** : Limite maximale absolue, ne peut être dépassée
- `nproc` : Type de ressource (nombre de processus)
- `1027` / `2025` : Valeurs des limites

**Sauvegarder et quitter :** `:wq` dans vi

---

### Étape 4 : Validation

```bash
sudo cat /etc/security/limits.conf | grep nfsuser
```

**Résultat attendu :**
```
nfsuser          soft    nproc           1027
nfsuser          hard    nproc           2025
```

**Vérifier les limites appliquées (si l'utilisateur est connecté) :**
```bash
sudo su - nfsuser -c "ulimit -u"
# 1027  (soft limit)

sudo su - nfsuser -c "ulimit -Hu"
# 2025  (hard limit)
```

**⚠️ Note :** Les nouvelles limites prennent effet à la **prochaine connexion** de l'utilisateur.

---

**Tags :** #Linux #ResourceLimits #ulimit #Performance #ProcessManagement #KodeKloud

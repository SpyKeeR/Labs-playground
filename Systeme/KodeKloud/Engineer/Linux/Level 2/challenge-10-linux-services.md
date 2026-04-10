# Challenge 10 : Linux Services

**Date** : 10 janvier 2026  
**Plateforme** : KodeKloud Engineer - Linux Level 2  
**Difficulté** : ⭐⭐ (Niveau 2)  
**Statut** : ✅ Validé

---

## 🎯 Objectif

Installer le package `squid` sur les 3 serveurs applicatifs et configurer le service pour démarrer automatiquement au boot.

---

## 📋 Énoncé

Selon les détails partagés par l'équipe de développement, la nouvelle version de l'application a des dépendances sur le back-end. Il y a des packages/services qui doivent être installés sur tous les serveurs applicatifs du Stratos Datacenter. Selon les exigences, veuillez effectuer les étapes suivantes :

1. Installer le package `squid` sur tous les serveurs applicatifs.
2. Une fois installé, assurez-vous qu'il est activé pour démarrer au boot.

**Serveurs concernés** :
- `stapp01` (user `tony`)
- `stapp02` (user `steve`)
- `stapp03` (user `banner`)

---

## 🔧 Résolution

### Approche

Pour chaque serveur applicatif :
1. Se connecter via SSH
2. Installer le package `squid` avec `yum`
3. Activer + démarrer le service avec `systemctl enable --now`

### Commandes exécutées

**Serveur stapp01** :
```bash
ssh tony@stapp01
sudo yum install squid -y
sudo systemctl enable --now squid
```

**Serveur stapp02** :
```bash
ssh steve@stapp02
sudo yum install squid -y
sudo systemctl enable --now squid
```

**Serveur stapp03** :
```bash
ssh banner@stapp03
sudo yum install squid -y
sudo systemctl enable --now squid
```

### Explications

- `yum install squid -y` : Installation du package sans demander confirmation
- `systemctl enable --now squid` : Combine 2 actions en 1 commande :
  - `enable` : Active le service au démarrage (boot)
  - `--now` : Démarre le service immédiatement

---

## ✅ Validation

Pour chaque serveur, vérifier :

```bash
# Vérifier statut service
sudo systemctl status squid

# Vérifier activation boot
sudo systemctl is-enabled squid
# Output attendu : "enabled"
```

---

## 📌 Commandes utiles

```bash
# Installer package
sudo yum install <package> -y

# Démarrer service
sudo systemctl start <service>

# Activer service au boot
sudo systemctl enable <service>

# Activer + démarrer (combo)
sudo systemctl enable --now <service>

# Vérifier statut
sudo systemctl status <service>

# Vérifier activation boot
sudo systemctl is-enabled <service>

# Arrêter service
sudo systemctl stop <service>

# Redémarrer service
sudo systemctl restart <service>

# Désactiver service
sudo systemctl disable <service>
```

---

**Tags** : `systemd` `services` `squid` `yum` `systemctl` `enable` `Level 2`

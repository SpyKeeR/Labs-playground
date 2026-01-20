# Challenge 23 : Linux LogRotate

**Difficulté** : Niveau 2  
**Domaine** : LogRotate, Logs Management, HAProxy  
**Date** : 17 janvier 2026

---

## 📋 Présentation

**Objectif** : Configurer rotation automatique des logs HAProxy (compression + suppression anciens logs) pour gestion efficace stockage.

**Contexte** : Nautilus DevOps team prépare déploiement nouvelle application. Trafic important attendu sur HAProxy → génération logs massifs. Stockage doit être optimisé via compression et rotation logs.

**Consigne originale** :

The Nautilus DevOps team is ready to launch a new application, which they will deploy on app servers in Stratos Datacenter. They are expecting significant traffic/usage of haproxy on app servers after that. This will generate massive logs, creating huge log files. To utilise the storage efficiently, they need to compress the log files and need to rotate old logs. Check the requirements shared below:

a. In all app servers install haproxy package.

b. Using logrotate configure haproxy logs rotation to monthly and keep only 3 rotated logs.

(If by default log rotation is set, then please update configuration as needed)

**Requirements** :

1. **Installation HAProxy** : Installer package `haproxy` sur TOUS App Servers (stapp01, stapp02, stapp03)

2. **LogRotate configuration** :
   - **Fréquence rotation** : `monthly` (mensuelle, au lieu de `daily` défaut)
   - **Logs conservés** : `3` rotations max (au lieu de 10 défaut)
   - Fichier config : `/etc/logrotate.d/haproxy`

**Serveurs** :
- **App Server 1** : `stapp01` (user `tony`)
- **App Server 2** : `stapp02` (user `steve`)
- **App Server 3** : `stapp03` (user `banner`)

---

## ⚙️ Réalisation

### Configuration identique sur les 3 App Servers

**App Server 1 (stapp01)** :

```bash
# Connexion
ssh tony@stapp01

# Installation HAProxy + LogRotate
sudo yum install haproxy logrotate -y

# Éditer configuration LogRotate HAProxy
sudo vi /etc/logrotate.d/haproxy
```

**Modifications fichier `/etc/logrotate.d/haproxy`** :

```bash
# AVANT (défaut)
/var/log/haproxy.log {
    daily
    rotate 10
    missingok
    notifempty
    compress
    sharedscripts
    postrotate
        /bin/kill -HUP `cat /var/run/syslog.pid 2> /dev/null` 2> /dev/null || true
    endscript
}

# APRÈS (requirements)
/var/log/haproxy.log {
    monthly        # Changer : daily → monthly
    rotate 3       # Changer : rotate 10 → rotate 3
    missingok
    notifempty
    compress
    sharedscripts
    postrotate
        /bin/kill -HUP `cat /var/run/syslog.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
```

**Sauvegarder** : `:wq`

**Démarrer HAProxy** :
```bash
sudo systemctl enable --now haproxy
```

**Vérifier** :
```bash
sudo systemctl status haproxy
# Active (running)
```

---

**App Server 2 (stapp02)** :

```bash
ssh steve@stapp02
sudo yum install haproxy logrotate -y
sudo vi /etc/logrotate.d/haproxy
# Modifier : daily → monthly, rotate 10 → rotate 3
sudo systemctl enable --now haproxy
```

---

**App Server 3 (stapp03)** :

```bash
ssh banner@stapp03
sudo yum install haproxy logrotate -y
sudo vi /etc/logrotate.d/haproxy
# Modifier : daily → monthly, rotate 10 → rotate 3
sudo systemctl enable --now haproxy
```

---

## 🔍 Validation

**Vérifier configuration LogRotate** :

```bash
# Tester config (dry-run, pas rotation effective)
sudo logrotate -d /etc/logrotate.d/haproxy

# Output attendu :
# rotating pattern: /var/log/haproxy.log  monthly (3 rotations)
```

**Vérifier HAProxy running** :
```bash
sudo systemctl status haproxy
# Active (running) sur les 3 serveurs
```

---

## 📝 Commandes utiles

**LogRotate testing** :
```bash
# Test configuration (verbose, dry-run)
sudo logrotate -d /etc/logrotate.d/haproxy

# Forcer rotation immédiate (test)
sudo logrotate -f /etc/logrotate.d/haproxy

# Vérifier logs rotations passées
ls -lh /var/log/haproxy*
# haproxy.log         (actuel)
# haproxy.log.1.gz    (rotation 1 - compressé)
# haproxy.log.2.gz    (rotation 2)
# haproxy.log.3.gz    (rotation 3 - plus ancien conservé)
```

**HAProxy logs** :
```bash
# Logs temps réel
sudo tail -f /var/log/haproxy.log

# Taille logs
du -sh /var/log/haproxy*
```

---

## 🎯 Points clés

**LogRotate** :
- **Rotation automatique logs** : Évite saturation disque (logs cumulés Gigaoctets)
- **Compression** : `.gz` économise ~90% espace disque
- **Fréquences** : `daily`, `weekly`, `monthly`, `yearly`
- **Rétention** : `rotate N` (nombre rotations conservées)

**Options LogRotate courantes** :
- `missingok` : Pas erreur si log absent
- `notifempty` : Pas rotation si log vide
- `compress` : Compression gzip logs rotated
- `delaycompress` : Compression différée (rotation suivante)
- `sharedscripts` : Script postrotate exécuté 1x (pas par log)
- `postrotate` : Commandes après rotation (reload service, kill -HUP)

**Challenge 23 specifics** :
- HAProxy génère logs volumineux (trafic HTTP)
- Rotation mensuelle adaptée production (balance fréquence/rétention)
- 3 mois historique suffisant troubleshooting

---

## 🎯 Tags

`LogRotate`, `Logs-Management`, `HAProxy`, `Compression`, `Storage-Optimization`, `System-Administration`

---

**Complétion** : ✅ Challenge validé (3 App Servers configurés)  
**Prochaine étape** : Challenge 24 - Application Security

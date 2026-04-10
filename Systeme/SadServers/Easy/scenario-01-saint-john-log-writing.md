# SadServers - Saint John : What is Writing to this Log File?

**Date :** Janvier 2026 (antérieur au 5 janvier)  
**Plateforme :** SadServers.com  
**Scenario :** Saint John  
**Domaine :** Linux - Troubleshooting processus et logs  
**Difficulté :** Easy  
**Durée :** ~15 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Identifier et arrêter le processus qui écrit continuellement dans un fichier log problématique.

---

## 📋 Énoncé Scenario

Un fichier log `/var/log/bad.log` grossit anormalement et consomme de l'espace disque.

**Mission :** Trouver quel processus écrit dans ce fichier et l'arrêter proprement.

**Success criteria :** Le processus responsable est terminé et n'écrit plus dans `/var/log/bad.log`.

---

## 🔧 Résolution

### Étape 1 : Identifier le processus utilisant le fichier

```bash
lsof | grep /var/log/bad.log
```

**Explication :**
- `lsof` : **List Open Files** (lister tous fichiers ouverts système)
- `grep /var/log/bad.log` : Filtrer lignes concernant ce fichier spécifique

**Résultat attendu :**
```
badlog.py   591 admin    1w   REG  259,1     2456  /var/log/bad.log
            └─┬─┘          └┬┘
              │             └─ File descriptor 1 (stdout) en write mode
              └─ PID 591
```

**Informations obtenues :**
- **Processus** : `badlog.py` (script Python)
- **PID** : 591
- **User** : admin
- **Mode** : `1w` (stdout en écriture)

---

### Étape 2 : Vérifier détails du processus

```bash
ps -p 591 -f
```

**Explication :**
- `ps` : Process Status
- `-p 591` : Filtrer processus PID 591
- `-f` : Full format (afficher commande complète)

**Résultat attendu :**
```
UID   PID  PPID  C STIME TTY      TIME CMD
admin 591  590   0 10:00 ?        00:00:05 /usr/bin/python3 /home/admin/badlog.py
                  └─┬─┘
                    └─ Parent PID 590
```

**Informations obtenues :**
- **Commande** : `/usr/bin/python3 /home/admin/badlog.py`
- **PPID** : 590 (processus parent)
- **Chemin script** : `/home/admin/badlog.py`

---

### Étape 3 : Vérifier hiérarchie processus (optionnel)

```bash
pstree -p | grep 591
```

**Explication :**
- `pstree -p` : Afficher arbre processus avec PIDs
- `grep 591` : Trouver PID 591 dans l'arbre

**Résultat attendu :**
```
cron(590)───badlog.py(591)
└─┬─┘
  └─ Processus parent = cron
```

**Découverte :** Script lancé par **cron**, donc risque redémarrage automatique.

---

### Étape 4 : Vérifier tâches cron utilisateur

```bash
crontab -l
```

**Explication :**
- `crontab -l` : Lister tâches cron de l'utilisateur courant (admin)

**Résultat attendu :**
```
@reboot /usr/bin/python3 /home/admin/badlog.py > /var/log/bad.log 2>&1
```

**Analyse :**
- `@reboot` : Exécute au démarrage système
- Script redirige stdout/stderr vers `/var/log/bad.log`
- **Problème** : Tâche cron relancera script au prochain reboot

**⚠️ Note :** Dans ce scenario, objectif = arrêter processus actuel seulement (pas supprimer cron).

---

### Étape 5 : Terminer le processus proprement

```bash
kill -15 591
```

**Explication :**
- `kill` : Envoyer signal à processus
- `-15` : **SIGTERM** (signal termination propre)
- `591` : PID cible

**Vérification :**
```bash
ps -p 591
# PID TTY      TIME CMD
# (vide = processus terminé)

lsof | grep /var/log/bad.log
# (vide = fichier plus ouvert)
```

---

## � Commandes à retenir

```bash
# Vérifier processus qui écrit dans fichier
lsof /path/to/file
sudo lsof | grep filename

# Arrêter processus
sudo kill PID
sudo pkill process_name

# Surveiller fichier en temps réel
tail -f /var/log/file.log
watch -n 1 'ls -lh /path/to/file'
```

```bash
# Identifier processus sur port
lsof -i :80

# Détails processus par PID
ps -p PID -f

# Tuer proprement (SIGTERM)
kill -15 PID

# Tuer force (SIGKILL - dernier recours)
kill -9 PID

# Tuer par nom
pkill processname

# Arbre processus
pstree -p

# Vérifier cron
crontab -l
```

---

**Tags :** #Linux #Troubleshooting #Processes #lsof #kill #Cron #SadServers #Debugging

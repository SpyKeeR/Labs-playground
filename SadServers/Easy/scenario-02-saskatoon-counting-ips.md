# SadServers - Saskatoon : Counting IPs

**Date :** Janvier 2026 (antérieur au 5 janvier)  
**Plateforme :** SadServers.com  
**Scenario :** Saskatoon  
**Domaine :** Linux - Log Analysis & Text Processing  
**Difficulté :** Easy  
**Durée :** ~10 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Analyser un fichier log Apache et identifier l'adresse IP la plus fréquente dans les requêtes.

---

## 📋 Énoncé Scenario

Un fichier log Apache `access.log` contient des milliers de requêtes HTTP.

**Mission :** Trouver l'adresse IP qui a effectué le plus de requêtes et l'écrire dans un fichier `highestip.txt`.

**Success criteria :** Fichier `highestip.txt` contient l'IP la plus fréquente uniquement (format `xxx.xxx.xxx.xxx`).

---

## 🔧 Résolution

### Contexte : Format log Apache

**Structure ligne typique `access.log` :**
```
66.249.73.135 - - [27/Jun/2023:10:45:23 +0000] "GET /index.html HTTP/1.1" 200 1234
└────┬────┘   │ │ └──────────┬─────────┘ └──────────┬─────────┘ └┬┘ └┬┘
     │        │ │             │                      │             │   └─ Taille réponse
     │        │ │             │                      │             └─ Code status HTTP
     │        │ │             │                      └─ Requête HTTP
     │        │ │             └─ Timestamp
     │        │ └─ Identd (unused)
     │        └─ Remote logname (unused)
     └─ IP cliente
```

**Champs séparés par espaces** : IP toujours **1er champ**.

---

### Pipeline de résolution complète

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -1 | awk '{print $2}' > highestip.txt
```

**Décomposition étape par étape :**

---

### Étape 1 : Extraire les adresses IP

```bash
awk '{print $1}' access.log
```

**Explication :**
- `awk` : Langage traitement texte (colonnes/lignes)
- `'{print $1}'` : Afficher 1er champ (séparateur défaut = espace)
- `access.log` : Fichier source

**Résultat (extrait) :**
```
66.249.73.135
192.168.1.10
66.249.73.135
10.0.0.5
192.168.1.10
66.249.73.135
...
```

**Pourquoi awk vs cut ?**
```bash
# awk : gère espaces multiples automatiquement
awk '{print $1}'  # Robuste

# cut : séparateur fixe 1 espace
cut -d' ' -f1     # Échoue si double espace
```

---

### Étape 2 : Trier les IPs

```bash
awk '{print $1}' access.log | sort
```

**Explication :**
- `sort` : Trier lignes alphabétiquement (requis pour `uniq`)

**Résultat (extrait) :**
```
10.0.0.5
66.249.73.135
66.249.73.135
66.249.73.135
192.168.1.10
192.168.1.10
...
```

**⚠️ Pourquoi trier ?**  
`uniq` ne compte que lignes **consécutives** identiques.

**Exemple sans `sort` :**
```bash
echo -e "A\nB\nA" | uniq -c
# 1 A
# 1 B
# 1 A  ← A compté 2 fois (pas consécutif)

echo -e "A\nB\nA" | sort | uniq -c
# 2 A
# 1 B  ← Correct
```

---

### Étape 3 : Compter occurrences

```bash
awk '{print $1}' access.log | sort | uniq -c
```

**Explication :**
- `uniq -c` : Compter lignes **consécutives** identiques
  - `-c` : **Count** (afficher nombre occurrences)

**Résultat (extrait) :**
```
     15 10.0.0.5
    342 66.249.73.135
     89 192.168.1.10
    ...
```

**Format output :**
```
COUNT IP_ADDRESS
└─┬─┘ └────┬────┘
  │        └─ Champ 2 ($2)
  └─ Champ 1 ($1)
```

---

### Étape 4 : Trier par fréquence décroissante

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr
```

**Explication :**
- `sort -nr` :
  - `-n` : **Numeric sort** (compare nombres, pas chaînes)
  - `-r` : **Reverse** (décroissant)

**Résultat (extrait) :**
```
    342 66.249.73.135  ← Plus fréquent
     89 192.168.1.10
     15 10.0.0.5
    ...
```

**Pourquoi `-n` critique ?**
```bash
# Sans -n (tri alphabétique)
echo -e "100\n20\n5" | sort
# 100
# 20
# 5  ← Incorrect ("5" > "20" alphabétiquement)

# Avec -n (tri numérique)
echo -e "100\n20\n5" | sort -n
# 5
# 20
# 100  ← Correct
```

---

### Étape 5 : Extraire 1ère ligne (plus fréquent)

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -1
```

**Explication :**
- `head -1` : Afficher **1ère ligne** uniquement

**Résultat :**
```
    342 66.249.73.135
```

---

### Étape 6 : Extraire IP seule (sans count)

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -1 | awk '{print $2}'
```

**Explication :**
- `awk '{print $2}'` : Afficher **2ème champ** (l'IP)

**Résultat :**
```
66.249.73.135
```

---

### Étape 7 : Écrire dans fichier résultat

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -1 | awk '{print $2}' > highestip.txt
```

**Explication :**
- `> highestip.txt` : Rediriger output vers fichier (écrase contenu existant)

**Vérification :**
```bash
cat highestip.txt
# 66.249.73.135
```

---

## 🎓 Commandes à Retenir

```bash
# Extraire colonne (awk)
awk '{print $1}' file.txt

# Trier lignes
sort file.txt
sort -n file.txt  # Numérique
sort -r file.txt  # Reverse
sort -u file.txt  # Unique

# Compter duplicates
sort file.txt | uniq -c

# Top 10 occurrences
sort file.txt | uniq -c | sort -nr | head -10

# Pipeline analyse log complet
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10

# Afficher 1ère/dernière ligne
head -1 file.txt
tail -1 file.txt

# Suivre log temps réel
tail -f /var/log/syslog
```

---

**Tags :** #Linux #LogAnalysis #awk #sort #uniq #Pipelines #SadServers #TextProcessing #Apache

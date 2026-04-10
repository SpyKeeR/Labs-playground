# KodeKloud Engineer - Challenge 11 : String Replacement

**Date :** 6 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Text Processing & sed  
**Difficulté :** Medium  
**Durée :** ~20 minutes  
**Statut :** ✅ Résolu

---

## 🎯 Objectif

Remplacer toutes les occurrences d'une chaîne de caractères dans un fichier XML en utilisant les outils de manipulation de texte Linux.

---

## 📋 Énoncé

**Contexte :** Le serveur de backup Stratos DC contient des fichiers XML templates critiques pour l'application Nautilus. Ces fichiers nécessitent l'insertion de données valides avant utilisation.

**Mission :** Remplacer **toutes** les occurrences de la chaîne `Random` par `Maritime` dans le fichier XML `/root/nautilus.xml` sur le serveur de backup.

**Contraintes :**
- Fichier situé : `/root/nautilus.xml`
- String source : `Random`
- String cible : `Maritime`
- Toutes occurrences doivent être remplacées

**Serveur cible :** `clint@stbkp01`

---

## 🔧 Résolution

### Étape 1 : Connexion au serveur backup

```bash
ssh clint@stbkp01
```

**Vérification :**
```bash
whoami
# clint

hostname
# stbkp01
```

---

### Étape 2 : Vérifier état initial du fichier

```bash
sudo cat /root/nautilus.xml | head -20
```

**Exemple contenu (extrait) :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <database>
        <host>Random-db-server-01</host>
        <port>3306</port>
        <name>Random_database</name>
    </database>
    <application>
        <name>Random Application</name>
        <version>2.4.Random</version>
    </application>
</configuration>
```

**Comptabiliser occurrences :**
```bash
sudo grep -o "Random" /root/nautilus.xml | wc -l
# 15
```

---

### Étape 3 : Remplacer avec sed (in-place)

```bash
sudo sed -i 's/Random/Maritime/g' /root/nautilus.xml
```

**Décomposition commande :**
- `sed` : **S**tream **Ed**itor (éditeur texte stream)
- `-i` : **In-place** (modifier fichier directement)
- `'s/Random/Maritime/g'` :
  - `s` : **Substitute** (commande substitution)
  - `/Random/` : Pattern à chercher
  - `/Maritime/` : Replacement
  - `/g` : **Global** (toutes occurrences ligne, pas juste 1ère)

---

### Étape 4 : Vérifier remplacement réussi

**Vérifier ancien string absent :**
```bash
sudo grep "Random" /root/nautilus.xml
# (vide = aucune occurrence restante)
```

**Vérifier nouveau string présent :**
```bash
sudo grep "Maritime" /root/nautilus.xml
```

**Résultat attendu :**
```xml
        <host>Maritime-db-server-01</host>
        <name>Maritime_database</name>
        <name>Maritime Application</name>
        <version>2.4.Maritime</version>
```

**Compter nouvelles occurrences :**
```bash
sudo grep -o "Maritime" /root/nautilus.xml | wc -l
# 15  (doit matcher count initial "Random")
```

---

### Étape 5 : Vérifier intégrité XML (optionnel)

```bash
sudo xmllint --noout /root/nautilus.xml
# (vide = XML valide, pas d'erreurs)
```

**Si xmllint absent :**
```bash
sudo yum install -y libxml2  # RHEL/CentOS
# OU
sudo apt install -y libxml2-utils  # Debian/Ubuntu
```

---

## 🎓 Commandes à Retenir

```bash
# Substitution basique (stdout)
sed 's/old/new/g' file.txt

# In-place modification
sed -i 's/old/new/g' file.txt

# In-place avec backup
sed -i.bak 's/old/new/g' file.txt

# Délimiteur alternatif (paths)
sed 's|/old/path|/new/path|g' file.txt

# Case-insensitive
sed 's/error/ERROR/gi' log.txt

# Multiple substitutions
sed -e 's/foo/bar/g' -e 's/old/new/g' file.txt

# Extended regex
sed -E 's/pattern+/replacement/g' file.txt

# Supprimer lignes pattern
sed '/pattern/d' file.txt

# Afficher lignes range
sed -n '10,20p' file.txt

# Vérifier avant modifier (dry-run)
sed 's/old/new/g' file.txt | less
```

---

**Tags :** #Linux #sed #TextProcessing #Automation #Regex #KodeKloud #StreamEditor

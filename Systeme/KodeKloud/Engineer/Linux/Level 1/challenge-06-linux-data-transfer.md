# Challenge 6 : Linux Data Transfer

**Date :** 5 janvier 2026  
**Plateforme :** KodeKloud Engineer  
**Domaine :** Linux - Find, Xargs, Gestion fichiers  
**Difficulté :** Intermédiaire  
**Durée :** ~25 minutes  
**Statut :** ✅ Validé

---

## 🎯 Objectif

Filtrer et copier des fichiers appartenant à un utilisateur spécifique tout en préservant l'arborescence des répertoires, dans un contexte de données mélangées accidentellement.

---

## 📋 Énoncé

Suite à un mélange accidentel de données, les données utilisateurs ont été mélangées involontairement sur **Nautilus App Server 1** à l'emplacement `/home/usersdata` par l'équipe de support production Nautilus dans le Stratos DC. Pour corriger cela, des données utilisateur spécifiques doivent être filtrées et déplacées.

**Tâche :**
- Localiser tous les **fichiers** (en excluant les répertoires) appartenant à l'utilisateur `james` dans `/home/usersdata` sur App Server 1
- Copier ces fichiers **en préservant la structure des répertoires** vers `/media`

**Contrainte importante :** Les répertoires ont des permissions différentes (owner root), mais les fichiers appartiennent à james.

---

## 🔧 Résolution

### Étape 1 : Connexion et exploration

```bash
ssh tony@stapp01

# Se placer dans le répertoire source
cd /home/usersdata

# Explorer la structure (optionnel)
ls -laR | head -50
```

**Explication :** Comprendre l'arborescence avant de copier.

---

### Étape 2 : Trouver les fichiers de james

```bash
# Lister tous les fichiers (pas les dossiers) de james
sudo find . -user james -type f
```

**Explication détaillée :**
- `find .` : rechercher depuis répertoire courant récursivement
- `-user james` : filtrer fichiers appartenant à james
- `-type f` : **uniquement les fichiers** (exclut directories `-type d`)

**Exemple output :**
```
./dir1/file1.txt
./dir1/subdir/file2.log
./dir2/config.conf
```

---

### Étape 3 : Copier avec préservation arborescence

```bash
sudo find . -user james -type f | xargs cp -a --parents --no-clobber -t /media
```

**Explication DÉTAILLÉE (commande complexe) :**

#### **`find . -user james -type f`**
- Génère liste fichiers james

#### **`|` (pipe)**
- Passe la liste à la commande suivante

#### **`xargs`**
- Convertit stdin en arguments pour `cp`
- Évite erreur "Argument list too long" si beaucoup de fichiers
- Exécute : `cp -a --parents --no-clobber -t /media file1 file2 file3 ...`

#### **`cp` options critiques :**

**`-a` (archive mode) :**
- Équivalent `-dR --preserve=all`
- Préserve : permissions, ownership, timestamps, symlinks
- **Essentiel** pour backup/migration données

**`--parents` (CLEF du challenge) :**
- **Crée la structure de répertoires parents dans la destination**
- Exemple : `./dir1/subdir/file.txt` → `/media/dir1/subdir/file.txt`
- **Sans cette option** : tous fichiers copiés directement dans `/media/` (écrasement!)

**`--no-clobber` :**
- Ne pas écraser fichiers existants destination
- Sécurité anti-perte données

**`-t /media` (target directory) :**
- Spécifie répertoire destination
- Permet à xargs de mettre tous fichiers sources APRÈS
- Syntaxe : `cp -t DEST SOURCE1 SOURCE2 ...` (vs classique `cp SOURCE DEST`)

---

### Étape 4 : Validation

```bash
# Vérifier fichiers copiés avec arborescence
ls -lR /media

# Comparer nombre fichiers source vs destination
sudo find /home/usersdata -user james -type f | wc -l
sudo find /media -type f | wc -l
# Les 2 doivent être identiques

# Vérifier ownership préservé
ls -l /media/dir1/file1.txt
# Doit afficher owner:group original (james:james)
```

---

## 🔗 Ressources

**Documentation :**
- `man find` : recherche fichiers avancée
- `man cp` : options copie (--parents, -a, etc.)
- `man xargs` : construction commandes depuis stdin

**Fichiers système :**
- `/etc/passwd` : mapping username → UID
- `/etc/group` : mapping groupname → GID

**Guides utiles :**
- [Find Command Examples](https://www.tecmint.com/35-practical-examples-of-linux-find-command/)
- [Xargs vs Exec](https://www.baeldung.com/linux/find-exec-vs-xargs)

---

## 🎓 Commandes à Retenir

```bash
# Copier fichiers user avec arborescence
find . -user USERNAME -type f | xargs cp -a --parents -t /dest

# Variante sécurisée (espaces dans noms)
find . -user USERNAME -type f -print0 | xargs -0 cp -a --parents -t /dest

# Backup incrémental (ne pas écraser existants)
find . -type f -mtime -7 | xargs cp --parents --no-clobber -t /backup

# Lister taille totale fichiers user
find . -user USERNAME -type f -exec du -ch {} + | tail -1

# Compter fichiers par user
find /home -type f -printf '%u\n' | sort | uniq -c | sort -rn
```

---

**Tags :** #Linux #Find #Xargs #DataMigration #Backup #FileManagement #KodeKloud

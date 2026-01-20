# Challenge 04 : Sed Manipulation

**Date** : 8 janvier 2026  
**Plateforme** : KodeKloud Engineer  
**Niveau** : System Administrator II (Level 2)  

---

## 🎯 Objectif

Manipuler fichier texte avec `sed` : supprimer lignes contenant mot spécifique et remplacer occurrences mot complet.

---

## 📋 Énoncé

Données sur Nautilus App Server 1 (Stratos DC) doivent être modifiées dans plusieurs fichiers.

**Tâche** : Modifier fichier `/home/BSD.txt` selon ces critères :

**a.** Supprimer toutes les lignes contenant le mot `software` (case sensitive) et sauvegarder dans `/home/BSD_DELETE.txt`

**b.** Remplacer toutes les occurrences du mot `from` par `their` et sauvegarder dans `/home/BSD_REPLACE.txt`

**Note importante** : Ne pas altérer mots contenant la chaîne (ex: `upto`, `contributor`)

**Serveur cible** : `tony@stapp01`

---

## ✅ Résolution

### 1. Se connecter au serveur

```bash
ssh tony@stapp01
```

### 2. Créer copies fichier source

```bash
sudo cp /home/BSD.txt /home/BSD_DELETE.txt
sudo cp /home/BSD.txt /home/BSD_REPLACE.txt
```

### 3. Supprimer lignes contenant "software"

```bash
sudo sed -i '/\<software\>/d' /home/BSD_DELETE.txt
```

**Explication** :
- `sed -i` : Edit in-place (modifie fichier directement)
- `/\<software\>/d` : Pattern avec word boundaries + delete
  * `\<` : Début de mot (word boundary)
  * `\>` : Fin de mot (word boundary)
  * `/d` : Delete matching lines
- **Case sensitive** : `software` ≠ `Software`

### 4. Remplacer "from" par "their"

```bash
sudo sed -i 's/\<from\>/their/g' /home/BSD_REPLACE.txt
```

**Explication** :
- `s/pattern/replacement/g` : Substitute command
  * `\<from\>` : Mot complet "from" (pas "fromage", "perform")
  * `their` : Remplacement
  * `g` : Global (toutes occurrences ligne)
- **Word boundaries critiques** : Évite altérer "from" dans "performance"

### 5. Validation

**Vérifier suppression** :
```bash
grep "software" /home/BSD_DELETE.txt
```
**Résultat attendu** : Aucune sortie (toutes lignes supprimées)

**Vérifier remplacement** :
```bash
grep "from" /home/BSD_REPLACE.txt
grep "their" /home/BSD_REPLACE.txt
```
**Résultat attendu** : 
- `grep "from"` : Aucune occurrence mot complet "from"
- `grep "their"` : Occurrences remplacées

---

## 💡 Notes

- **sed** : Stream editor (édition texte ligne par ligne)
- **Word boundaries** : `\<` et `\>` essentiels pour matcher mots complets
- **-i flag** : Edit in-place (modifie fichier directement, sinon sortie stdout)
- **Case sensitivity** : sed respecte casse par défaut (`/i` pour ignorer)

---

## 🏷️ Tags

`#Linux` `#sed` `#TextProcessing` `#Regex` `#WordBoundaries` `#KodeKloud`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

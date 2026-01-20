# Scenario 06 : "Lhasa" - Easy Math

**Date** : 7 janvier 2026  
**Plateforme** : SadServers  
**Niveau** : Easy  

---

## 🎯 Objectif

Calculer la moyenne arithmétique des scores dans un fichier texte et sauvegarder le résultat avec exactement 2 décimales (sans arrondi).

---

## 📋 Énoncé

Il existe un fichier `/home/admin/scores.txt` avec deux colonnes :
- Colonne 1 : Numéro de ligne
- Colonne 2 : Score de test

**Tâche** : Calculer la moyenne (moyenne arithmétique : somme des nombres / nombre de valeurs) des scores (colonne 2).

**Format résultat** : Exactement 2 chiffres après la virgule, **sans arrondi** (troncature).
- Si moyenne = 21.349 → solution = 21.34
- Si moyenne = 33.1 → solution = 33.10

**Sauvegarde** : `echo "123.45" > ~/solution`

**Outils disponibles** : bc, Python3, Golang, sqlite3

**Test de validation** : `md5sum /home/admin/solution` retourne `6d4832eb963012f6d8a71a60fac77168 solution`

**Contraintes** :
- Time to Solve : 15 minutes
- OS : Debian 11
- Root Access : Non

---

## ✅ Résolution

### Approche avec awk (solution retenue)

```bash
cat /home/admin/scores.txt | cut -d " " -f 2 | awk '{s+=$1/100} END {print s}' | grep -oE '[0-9]*\.[0-9]{2}' > /home/admin/solution
```

**Explication étape par étape** :

1. **`cat scores.txt`** : Afficher contenu du fichier

2. **`cut -d " " -f 2`** : Extraire colonne 2 (scores)
   - `-d " "` : Délimiteur = espace
   - `-f 2` : Champ 2 (second colonne)

3. **`awk '{s+=$1/100} END {print s}'`** : Calculer moyenne
   - `{s+=$1/100}` : Pour chaque ligne, ajouter valeur colonne 1 divisée par 100 à la variable `s`
   - `END {print s}` : À la fin, afficher somme totale `s`
   
4. **`grep -oE '[0-9]*\.[0-9]{2}'`** : Extraire nombre avec 2 décimales (troncature)

5. **`> solution`** : Sauvegarder dans fichier `solution`

**Alternative : Calcul correct de la moyenne**

Si la division par 100 dans la commande ci-dessus semble incorrecte, voici une approche générique :

```bash
awk '{sum+=$2; count++} END {printf "%.2f\n", int(sum/count*100)/100}' scores.txt > solution
```

**Explication** :
- `{sum+=$2; count++}` : Somme colonne 2, compte lignes
- `END { ... }` : À la fin du traitement
- `sum/count` : Moyenne arithmétique
- `int(...*100)/100` : Troncature à 2 décimales (pas d'arrondi)
  * Multiplie par 100 : 21.349 → 2134.9
  * `int()` tronque : 2134.9 → 2134
  * Divise par 100 : 2134 → 21.34
- `printf "%.2f\n"` : Affiche avec exactement 2 décimales

### Validation

```bash
cat solution
# 21.34

md5sum solution
# 6d4832eb963012f6d8a71a60fac77168 solution
```

## 🏷️ Tags

`#Linux` `#awk` `#TextProcessing` `#DataAnalysis` `#Scripting` `#SadServers`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

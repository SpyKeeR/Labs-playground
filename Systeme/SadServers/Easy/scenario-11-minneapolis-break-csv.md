# Scenario 11 : "Minneapolis" - Break a CSV file

**Date** : 20 août 2026  
**Plateforme** : SadServers  
**Niveau** : Easy  
**Temps imparti** : 10 minutes  
**Statut** : ✅ Résolu

---

## 🎯 Objectif

Découper le fichier `/home/admin/data.csv` en exactement 10 fichiers de taille équivalente, chacun conservant la ligne d'en-tête du fichier d'origine.

---

## 📋 Énoncé

Découper le fichier CSV `data.csv` situé dans `/home/admin/` en **exactement 10 fichiers** plus petits, de taille à peu près égale, nommés :

```
data-00.csv, data-01.csv, ... , data-09.csv
```

**Règles** :
- Les fichiers sont créés dans le même répertoire (`/home/admin/`)
- Chaque fichier doit commencer par la **même ligne d'en-tête** (noms de colonnes) que `data.csv`
- Aucun fichier ne doit dépasser **32 Ko**
- Pour simplifier : on peut couper à n'importe quel endroit (pas forcément sur un retour à la ligne), les fichiers obtenus n'ont pas besoin d'être des CSV valides

**Test de validation** : Le bouton "Check My Solution" exécute `/home/admin/agent/check.sh` (lisible et exécutable).

**Contraintes** :
- Time to Solve : 10 minutes
- Root Access : Oui
- Tags : `csv` `data processing`

---

## ✅ Résolution

### Solution retenue (oneliner `split`)

```bash
cd /home/admin
split --verbose -d -n 10 --additional-suffix=.csv --filter='([ "$FILE" != "data_00.csv" ] && head -1 "data.csv" ; cat) > "$FILE"' "data.csv" "data-"
```

**Explication des options** :

| Option | Rôle |
|--------|------|
| `--verbose` | Affiche chaque fichier créé (`creating file 'data-00.csv'`...) |
| `-d` | Suffixes numériques (`00`, `01`...) au lieu d'alphabétiques (`aa`, `ab`...) |
| `-n 10` | Découpe en **10 morceaux** de taille égale (en octets) |
| `--additional-suffix=.csv` | Ajoute l'extension `.csv` après le suffixe numérique |
| `--filter='...'` | Au lieu d'écrire directement, envoie chaque morceau sur le stdin d'une commande shell ; `$FILE` contient le nom du fichier de sortie |
| `"data.csv"` | Fichier source |
| `"data-"` | Préfixe des fichiers générés |

**Fonctionnement du filtre** :

```bash
( [ "$FILE" != "data_00.csv" ] && head -1 "data.csv" ; cat ) > "$FILE"
```

1. **`[ "$FILE" != "data_00.csv" ]`** : Test pour ne pas rajouter l'en-tête au premier morceau (qui le contient déjà, puisqu'il commence au début de `data.csv`)
2. **`&& head -1 "data.csv"`** : Si le test est vrai → écrit la ligne d'en-tête
3. **`; cat`** : Dans tous les cas → recopie le morceau reçu sur stdin
4. **`( ... ) > "$FILE"`** : Le sous-shell regroupe les deux sorties dans le fichier final

### Validation

```bash
# 10 fichiers créés, tous < 32 Ko
ls -l data-*.csv

# Même en-tête partout
head -qn 1 data-*.csv | sort | uniq -c
#      10 <ligne d'en-tête>

# Lancer le check
bash /home/admin/agent/check.sh
```

---

## 📌 Commandes utiles

```bash
# Découper en N morceaux de taille égale (octets)
split -n 10 fichier prefix-

# Découper en N morceaux sans casser les lignes
split -n l/10 fichier prefix-

# Découper par nombre de lignes / par taille
split -l 1000 fichier prefix-
split -b 32K fichier prefix-

# Suffixes numériques + extension
split -d --additional-suffix=.csv fichier prefix-

# Taille d'un fichier en octets
stat -c %s data.csv
wc -c data.csv
```

---

## 💡 Points clés

- `split --filter` permet de **transformer chaque morceau** à la volée (ajout d'en-tête, compression `gzip`, etc.) sans boucle shell
- `-n 10` découpe en octets → coupe en plein milieu d'une ligne (autorisé ici) ; `-n l/10` respecterait les fins de ligne
- L'ajout de l'en-tête augmente légèrement la taille de chaque fichier → vérifier qu'on reste sous la limite des 32 Ko

## 🏷️ Tags

`#Linux` `#split` `#CSV` `#TextProcessing` `#DataProcessing` `#SadServers`

---

**Révision** : v1.0  
**Auteur** : Maxime Chenaud

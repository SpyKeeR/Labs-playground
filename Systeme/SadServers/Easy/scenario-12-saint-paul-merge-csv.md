# Scenario 12 : "Saint Paul" - Merge Many CSVs files

**Date** : 21 août 2026  
**Plateforme** : SadServers  
**Niveau** : Easy  
**Temps imparti** : 15 minutes  
**Statut** : 🚧 En cours

---

## 🎯 Objectif

Fusionner les 338 fichiers CSV `polldayregistrations_enregistjourduscrutin?????.csv` en un seul fichier `/home/admin/all.csv`, avec une seule ligne d'en-tête.

---

## 📋 Énoncé

Joindre (fusionner) les **338 fichiers** correspondant au motif :

```
/home/admin/polldayregistrations_enregistjourduscrutin?????.csv
```

dans un fichier unique `/home/admin/all.csv` contenant le contenu de tous les CSV, **dans n'importe quel ordre**.

**Règle** : Il ne doit y avoir **qu'une seule ligne** avec les noms de colonnes (en-tête).

**Test de validation** : Le bouton "Check My Solution" exécute `/home/admin/agent/check.sh` (lisible et exécutable).

**Contraintes** :
- Time to Solve : 15 minutes
- Root Access : Non
- Tags : `csv` `data processing`

---

## 🔧 Résolution (en cours)

### Tentative 1 : `find -exec` avec test conditionnel

```bash
find . -type f -name "polldayregistrations_enregistjourduscrutin?????.csv" -exec [ {} != polldayregistrations_enregistjourduscr ... head -n +2 {} > data.csv || cat {} >> data.csv \;
```

**Idée** :
- Parcourir les fichiers avec `find`
- Pour le premier fichier → écrire l'en-tête dans le fichier de sortie
- Pour les suivants → ajouter le contenu à la suite (`>>`)

**Résultat** : ❌ Fonctionne partiellement, le check ne passe pas.

### Solution finale

*À compléter.*

### Validation

```bash
# Nombre de fichiers source
ls /home/admin/polldayregistrations_enregistjourduscrutin?????.csv | wc -l
# 338

# Lancer le check
bash /home/admin/agent/check.sh
```

---

## 📌 Commandes utiles

```bash
# Lire le script de vérification
cat /home/admin/agent/check.sh

# Afficher l'en-tête d'un fichier
head -1 fichier.csv

# Compter les lignes
wc -l fichier.csv
```

---

## 💡 Points clés

*À compléter une fois le scénario résolu.*

## 🏷️ Tags

`#Linux` `#CSV` `#TextProcessing` `#DataProcessing` `#SadServers`

---

**Révision** : v0.1 (brouillon)  
**Auteur** : Maxime Chenaud

# Saskatoon - Couting IPs

## 1. Extraire les adresses IP

```bash
awk '{ print $1 }' /home/admin/access.log
```

*Récupère le premier champ de chaque ligne, correspondant à l'adresse IP.*

## 2. Trier les adresses IP

```bash
awk '{ print $1 }' /home/admin/access.log | sort
```

*Trie les adresses IP pour regrouper les mêmes valeurs ensemble.*

## 3. Compter les occurrences

```bash
awk '{ print $1 }' /home/admin/access.log | sort | uniq -c
```

*Compte combien de fois chaque adresse IP apparaît.*

## 4. Trier par fréquence décroissante

```bash
awk '{ print $1 }' /home/admin/access.log | sort | uniq -c | sort -nr
```

*Classe les adresses IP par nombre de requêtes, de la plus fréquente à la moins fréquente.*

## 5. Identifier l'IP la plus fréquente

```bash
awk '{ print $1 }' /home/admin/access.log | sort | uniq -c | sort -nr | head -1
```

*Affiche l'adresse IP avec le plus grand nombre de requêtes.*

## 6. Écrire l'IP la plus fréquente dans un fichier

```bash
echo "66.249.73.135" > /home/admin/highestip.txt
```

*Stocke l'IP identifiée dans le fichier `/home/admin/highestip.txt`.*
# Labo - Linux Kernel

- Accéder aux labs pratiques : [Labo](https://kodekloud.com/free-labs/linux/linux-kernel)

---

## Vérifier la version exacte du noyau en cours d’exécution
```
    $ uname -r
```
Exemple : `4.15.0-88-generic`

---

## Quelle est la version du noyau (Kernel Version) dans `4.15.0-88-generic` ?
Regarder le **premier chiffre** avant le premier point.  
Réponse : **4**

---

## Quel est le numéro de version majeure du noyau dans `4.15.0-88-generic` ?
Regarder le **deuxième chiffre** après le premier point.  
Réponse : **15**

---

## Afficher les messages générés par le noyau
```bash
    $ dmesg
```
---

## Lister / compter les périphériques blocs de type « disk »
```bash
    $ lsblk
```
Compter le nombre d’entrées dont le type est **disk**.

---

## Vérifier le nombre total de **cœurs physiques**
```bash
    $ lscpu
```
Calculer : **Core(s) per socket × Socket(s)**.

---

## Vérifier la mémoire totale « online »
```bash
    $ lsmem
```
Chercher la valeur **Online memory**.